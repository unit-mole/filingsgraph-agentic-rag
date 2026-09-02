def build_risk_timeline(observations:list[dict])->dict:
    timeline={}
    for o in sorted(observations,key=lambda x:x.get('fiscal_year') or 0):
        timeline.setdefault(o['topic'],[]).append({k:o.get(k) for k in ['fiscal_year','change_type','citation_id','excerpt']})
    return timeline
