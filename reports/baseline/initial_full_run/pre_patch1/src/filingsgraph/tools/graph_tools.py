from filingsgraph.graph.traversal import traverse

def find_related_entities(graph,start_nodes:list[str],max_hops:int=2,max_nodes:int=30,period=None): return traverse(graph,start_nodes,max_hops,max_nodes,period)
def find_shared_risks(graph,company_nodes:list[str])->dict:
    risks={}
    for c in company_nodes:
        if c not in graph: continue
        for _,t,attrs in graph.out_edges(c,data=True):
            if attrs.get('relationship')=='COMPANY_EXPOSED_TO_RISK': risks.setdefault(t,[]).append(c)
    return {r:cs for r,cs in risks.items() if len(set(cs))>1}
def get_company_risk_graph(graph,company_node:str,max_hops:int=2): return traverse(graph,[company_node],max_hops=max_hops)
def get_segment_risks(graph,segment_node:str): return traverse(graph,[segment_node],max_hops=1)
def traverse_relationship(graph,start_nodes:list[str],**kwargs): return traverse(graph,start_nodes,**kwargs)
