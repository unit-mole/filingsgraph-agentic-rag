def verify_entities(evidence:list[dict],tickers:list[str])->dict:
    allowed={t.upper() for t in tickers}
    if not allowed: return {"ok":True,"bad":[]}
    bad=[e.get('citation_id') for e in evidence if e.get('ticker') and e.get('ticker').upper() not in allowed]
    return {"ok":not bad,"bad":bad}

def detect_contradictions(evidence:list[dict])->list[str]:
    # Conservative deterministic detector for facts with same metric/period but materially different normalized values.
    seen={}; out=[]
    for e in evidence:
        p=e.get('payload') or {}; key=(e.get('ticker'),p.get('metric'),e.get('fiscal_year'),p.get('unit'))
        if not key[1] or 'value' not in p: continue
        val=float(p['value'])
        if key in seen and seen[key]!=val: out.append(f"Conflicting values for {key}: {seen[key]} vs {val}")
        seen[key]=val
    return out
