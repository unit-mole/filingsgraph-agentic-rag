from __future__ import annotations
import torch
from filingsgraph.core.config import get_settings

class BGEReranker:
    def __init__(self,model_name:str|None=None,device:str|None=None):
        from transformers import AutoTokenizer,AutoModelForSequenceClassification
        s=get_settings(); self.model_name=model_name or s.reranker_model; self.device=device or s.device
        self.tokenizer=AutoTokenizer.from_pretrained(self.model_name)
        dtype=torch.bfloat16 if self.device.startswith("cuda") and torch.cuda.is_available() else torch.float32
        self.model=AutoModelForSequenceClassification.from_pretrained(self.model_name,torch_dtype=dtype).to(self.device).eval()
    @torch.inference_mode()
    def rerank(self,query:str,results:list[dict],top_k:int=8)->list[dict]:
        if not results: return []
        pairs=[[query,r.get("payload",{}).get("text","")] for r in results]
        batch=self.tokenizer(pairs,padding=True,truncation=True,max_length=1024,return_tensors='pt').to(self.device)
        logits=self.model(**batch).logits.view(-1).float().cpu().tolist()
        out=[]
        for r,s in zip(results,logits): out.append({**r,"rerank_score":float(s),"method":"hybrid+reranker"})
        return sorted(out,key=lambda x:x["rerank_score"],reverse=True)[:top_k]

class LexicalReranker:
    def rerank(self,query:str,results:list[dict],top_k:int=8)->list[dict]:
        q=set(query.lower().split()); out=[]
        for r in results:
            t=set(r.get('payload',{}).get('text','').lower().split()); score=len(q&t)/(len(q) or 1)
            out.append({**r,'rerank_score':score})
        return sorted(out,key=lambda x:x['rerank_score'],reverse=True)[:top_k]
