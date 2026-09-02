from __future__ import annotations
import math

def recall_at_k(retrieved:list[str],relevant:set[str],k:int)->float:
    return len(set(retrieved[:k])&relevant)/len(relevant) if relevant else 0.0
def precision_at_k(retrieved:list[str],relevant:set[str],k:int)->float:
    return len(set(retrieved[:k])&relevant)/max(1,k)
def hit_rate(retrieved:list[str],relevant:set[str],k:int)->float: return float(bool(set(retrieved[:k])&relevant))
def reciprocal_rank(retrieved:list[str],relevant:set[str])->float:
    for i,x in enumerate(retrieved,1):
        if x in relevant:return 1/i
    return 0.0
def ndcg_at_k(retrieved:list[str],relevant:set[str],k:int)->float:
    dcg=sum((1.0 if x in relevant else 0.0)/math.log2(i+2) for i,x in enumerate(retrieved[:k]))
    ideal=sum(1.0/math.log2(i+2) for i in range(min(k,len(relevant))))
    return dcg/ideal if ideal else 0.0
