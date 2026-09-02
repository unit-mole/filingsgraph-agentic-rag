from __future__ import annotations
import json,re,pickle
from pathlib import Path
import numpy as np
from rank_bm25 import BM25Okapi
from filingsgraph.retrieval.filters import matches_filters

def tokenize(text:str)->list[str]: return re.findall(r"[A-Za-z0-9$%.-]+",text.lower())

class BM25Index:
    def __init__(self): self.payloads=[]; self.corpus=[]; self.model=None
    def build(self,texts:list[str],payloads:list[dict]):
        self.corpus=[tokenize(t) for t in texts]; self.payloads=payloads; self.model=BM25Okapi(self.corpus)
    def search(self,query:str,top_k:int=10,filters:dict|None=None)->list[dict]:
        if self.model is None: return []
        scores=np.asarray(self.model.get_scores(tokenize(query))); order=np.argsort(-scores); out=[]
        for idx in order:
            p=self.payloads[int(idx)]
            if matches_filters(p,filters): out.append({"id":p.get("chunk_id",str(idx)),"score":float(scores[idx]),"payload":p,"method":"bm25"})
            if len(out)>=top_k: break
        return out
    def save(self,path:str|Path):
        p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
        with p.open('wb') as f: pickle.dump({"corpus":self.corpus,"payloads":self.payloads},f)
    def load(self,path:str|Path):
        with Path(path).open('rb') as f: d=pickle.load(f)
        self.corpus=d['corpus']; self.payloads=d['payloads']; self.model=BM25Okapi(self.corpus); return self
