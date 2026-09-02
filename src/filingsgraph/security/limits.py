MAX_QUERY_CHARS=5000
MAX_EVIDENCE_ITEMS=30
MAX_GRAPH_NODES=30
MAX_GRAPH_HOPS=2
MAX_TOOL_CALLS=15

def validate_query_limits(question:str)->None:
    if len(question)>MAX_QUERY_CHARS: raise ValueError('Query exceeds maximum length')
