import hashlib
from filingsgraph.schemas.graph import GraphEdge

def make_edge(source:str,target:str,relationship:str,extraction_method:str,confidence:float,**kwargs)->GraphEdge:
    raw=f"{source}|{relationship}|{target}|{kwargs.get('filing_id')}|{kwargs.get('valid_from')}"
    return GraphEdge(edge_id=hashlib.sha1(raw.encode()).hexdigest()[:20],source_node=source,target_node=target,relationship=relationship,extraction_method=extraction_method,confidence=confidence,**kwargs)
