def edge_active(attrs:dict,period:str|int|None)->bool:
    if period is None: return True
    p=str(period); start=attrs.get('valid_from'); end=attrs.get('valid_to')
    return (not start or str(start)<=p) and (not end or p<=str(end))
