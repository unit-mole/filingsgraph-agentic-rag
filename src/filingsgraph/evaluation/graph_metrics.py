def edge_precision(pred:set[tuple],gold:set[tuple])->float: return len(pred&gold)/len(pred) if pred else 0.0
def graph_added_recall(base:set[str],graph:set[str],gold:set[str])->float:
    before=len(base&gold); after=len((base|graph)&gold); return (after-before)/max(1,len(gold)-before)
def irrelevant_expansion_rate(graph:set[str],gold:set[str])->float: return len(graph-gold)/len(graph) if graph else 0.0
