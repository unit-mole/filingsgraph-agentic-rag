def summarize_changes(changes:list[dict])->dict:
    counts={k:0 for k in ['NEW','EXPANDED','REDUCED','UNCHANGED','REMOVED']}
    for c in changes: counts[c.get('change_type','UNCHANGED')]=counts.get(c.get('change_type','UNCHANGED'),0)+1
    return counts
