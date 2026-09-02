def restore_parent_context(results:list[dict],max_chars:int=5000)->list[dict]:
    out=[]
    for r in results:
        item={**r}; p=dict(item.get("payload",{})); parent=p.get("parent_text")
        if parent: p["context_text"]=parent[:max_chars]
        else: p["context_text"]=p.get("text","")[:max_chars]
        item["payload"]=p; out.append(item)
    return out
