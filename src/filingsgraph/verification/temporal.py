def verify_temporal(evidence:list[dict],allowed_years:list[int])->dict:
    bad=[]; allowed=set(allowed_years)
    if not allowed: return {"ok":True,"bad":[]}
    for e in evidence:
        y=e.get('fiscal_year')
        if y is not None and int(y) not in allowed: bad.append(e.get('citation_id'))
    return {"ok":not bad,"bad":bad}
