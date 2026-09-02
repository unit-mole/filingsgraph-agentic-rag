from __future__ import annotations
import json,time
from pathlib import Path
from collections import defaultdict
from filingsgraph.evaluation.retrieval_metrics import recall_at_k,precision_at_k,hit_rate,reciprocal_rank,ndcg_at_k

METRIC_KEYS=['r5','r10','p5','hit10','mrr','ndcg10','latency_ms']

def _summary(rows:list[dict])->dict:
    return {k:(sum(r[k] for r in rows)/len(rows) if rows else None) for k in METRIC_KEYS}

def evaluate_retriever(questions:list[dict],search_fn,out_path:str|Path)->dict:
    rows=[]
    for q in questions:
        if not q.get('relevant_chunk_ids'): continue
        start=time.perf_counter(); res=search_fn(q['question']); lat=(time.perf_counter()-start)*1000
        ids=[r.get('payload',{}).get('chunk_id') or r.get('id') for r in res]; rel=set(q['relevant_chunk_ids'])
        rows.append({"id":q['id'],"category":q['category'],"r5":recall_at_k(ids,rel,5),"r10":recall_at_k(ids,rel,10),"p5":precision_at_k(ids,rel,5),"hit10":hit_rate(ids,rel,10),"mrr":reciprocal_rank(ids,rel),"ndcg10":ndcg_at_k(ids,rel,10),"latency_ms":lat})
    by=defaultdict(list)
    for r in rows: by[r['category']].append(r)
    payload={"summary":_summary(rows),"by_category":{k:_summary(v) for k,v in sorted(by.items())},"rows":rows}
    p=Path(out_path);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(payload,indent=2),encoding='utf-8');return payload
