def verify_citations(answer:str,evidence:list[dict])->dict:
    ids={e.get('citation_id') for e in evidence if e.get('citation_id')}
    cited={cid for cid in ids if cid in answer}
    return {"ok": bool(ids) and cited==ids if len(ids)<=6 else len(cited)>=min(2,len(ids)),"available":sorted(ids),"cited":sorted(cited),"missing":sorted(ids-cited)}
