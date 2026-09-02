def relevant_edge_ratio(edges:list[dict],keywords:list[str])->float:
    if not edges: return 0.0
    keys=[k.lower() for k in keywords]
    rel=sum(1 for e in edges if any(k in (str(e).lower()) for k in keys))
    return rel/len(edges)
