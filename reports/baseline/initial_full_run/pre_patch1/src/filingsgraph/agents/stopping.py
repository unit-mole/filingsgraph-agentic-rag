def should_stop(state:dict,max_tool_calls:int=15,max_cycles:int=2)->bool:
    if state.get('tool_count',0)>=max_tool_calls: return True
    if state.get('retry_count',0)>=max_cycles: return True
    verification=state.get('verification_status') or {}
    return bool(state.get('final_report')) and all(verification.get(k,False) for k in ['citations','numeric','temporal','entity'])
