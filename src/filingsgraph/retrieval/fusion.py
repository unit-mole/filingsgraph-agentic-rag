def reciprocal_rank_fusion(result_lists:list[list[dict]],k:int=60,top_k:int=30)->list[dict]:
    merged={}
    for results in result_lists:
        for rank,item in enumerate(results,1):
            key=item.get("payload",{}).get("chunk_id") or item.get("id")
            if key not in merged: merged[key]={**item,"score":0.0,"component_scores":{}}
            merged[key]["score"] += 1.0/(k+rank)
            merged[key]["component_scores"][item.get("method","unknown")]=item.get("score")
    return sorted(merged.values(),key=lambda x:x["score"],reverse=True)[:top_k]
