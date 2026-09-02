def matches_filters(payload: dict, filters: dict | None) -> bool:
    if not filters: return True
    for key,val in filters.items():
        actual=payload.get(key)
        if isinstance(val,(list,tuple,set)):
            if actual not in val: return False
        elif actual != val: return False
    return True
