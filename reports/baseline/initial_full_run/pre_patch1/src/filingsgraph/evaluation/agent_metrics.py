def accuracy(gold:list,pred:list)->float: return sum(a==b for a,b in zip(gold,pred))/len(gold) if gold else 0.0
def unnecessary_tool_rate(records:list[dict])->float:
    return sum(bool(r.get('unnecessary')) for r in records)/len(records) if records else 0.0
