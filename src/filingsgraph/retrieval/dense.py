from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from filingsgraph.core.config import ROOT, get_settings
from filingsgraph.retrieval.filters import matches_filters

class LocalDenseIndex:
    def __init__(self, embeddings=None):
        self.embedder=embeddings; self.vectors=np.empty((0,0),dtype=np.float32); self.payloads=[]
    def build(self,texts:list[str],payloads:list[dict]):
        self.vectors=np.asarray(self.embedder.encode(texts),dtype=np.float32); self.payloads=payloads
    def search(self,query:str,top_k:int=10,filters:dict|None=None)->list[dict]:
        q=np.asarray(self.embedder.encode([query])[0],dtype=np.float32)
        scores=self.vectors@q
        order=np.argsort(-scores)
        out=[]
        for idx in order:
            p=self.payloads[int(idx)]
            if matches_filters(p,filters):
                out.append({"id":p.get("chunk_id",str(idx)),"score":float(scores[idx]),"payload":p,"method":"dense"})
            if len(out)>=top_k: break
        return out
    def save(self,path:str|Path):
        p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
        np.save(p.with_suffix('.npy'),self.vectors)
        p.with_suffix('.json').write_text(json.dumps(self.payloads),encoding='utf-8')
    def load(self,path:str|Path):
        p=Path(path); self.vectors=np.load(p.with_suffix('.npy')); self.payloads=json.loads(p.with_suffix('.json').read_text(encoding='utf-8')); return self

class QdrantDenseIndex:
    def __init__(self, embeddings, collection: str="filing_chunks"):
        from qdrant_client import QdrantClient
        s=get_settings(); self.embedder=embeddings; self.collection=collection
        if s.qdrant_mode=="server" and s.qdrant_url:
            self.client=QdrantClient(url=s.qdrant_url)
        else:
            path=ROOT/s.qdrant_path; path.mkdir(parents=True,exist_ok=True); self.client=QdrantClient(path=str(path))
    def build(self,texts:list[str],payloads:list[dict]):
        from qdrant_client.models import Distance,VectorParams,PointStruct
        vecs=self.embedder.encode(texts)
        try: self.client.delete_collection(self.collection)
        except Exception: pass
        self.client.create_collection(self.collection,vectors_config=VectorParams(size=int(vecs.shape[1]),distance=Distance.COSINE))
        pts=[PointStruct(id=i,vector=v.tolist(),payload=p) for i,(v,p) in enumerate(zip(vecs,payloads))]
        for i in range(0,len(pts),128): self.client.upsert(self.collection,pts[i:i+128])
    def search(self,query:str,top_k:int=10,filters:dict|None=None)->list[dict]:
        from qdrant_client.models import Filter,FieldCondition,MatchValue,MatchAny
        q=self.embedder.encode([query])[0].tolist(); qfilter=None
        if filters:
            
            cond=[]
            for k,v in filters.items():
                if isinstance(v,(list,tuple,set)):
                    cond.append(FieldCondition(key=k, match=MatchAny(any=list(v))))
                else:
                    cond.append(FieldCondition(key=k, match=MatchValue(value=v)))
            qfilter=Filter(must=cond) if cond else None
        # qdrant-client API changed across releases; query_points is current, search is fallback.
        try:
            res=self.client.query_points(self.collection,query=q,query_filter=qfilter,limit=top_k).points
        except AttributeError:
            res=self.client.search(self.collection,query_vector=q,query_filter=qfilter,limit=top_k)
        return [{"id":str(r.id),"score":float(r.score),"payload":r.payload or {},"method":"dense"} for r in res]
