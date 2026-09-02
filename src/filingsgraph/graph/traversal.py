from __future__ import annotations
from collections import deque
from filingsgraph.graph.temporal import edge_active

def traverse(graph,start_nodes:list[str],max_hops:int=2,max_nodes:int=30,period:str|int|None=None)->dict:
    visited=set(start_nodes); q=deque((n,0) for n in start_nodes); edges=[]
    while q and len(visited)<max_nodes:
        node,depth=q.popleft()
        if depth>=max_hops: continue
        if node not in graph: continue
        for _,target,key,attrs in graph.out_edges(node,keys=True,data=True):
            if not edge_active(attrs,period): continue
            edges.append({"source":node,"target":target,"edge_id":key,**attrs})
            if target not in visited and len(visited)<max_nodes:
                visited.add(target); q.append((target,depth+1))
    return {"nodes":list(visited),"edges":edges}
