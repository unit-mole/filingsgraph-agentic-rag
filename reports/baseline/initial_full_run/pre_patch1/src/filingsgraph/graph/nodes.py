import hashlib
from filingsgraph.schemas.graph import GraphNode

def node_id(node_type:str,label:str)->str: return f"{node_type.lower()}:{hashlib.sha1(label.lower().encode()).hexdigest()[:14]}"
def make_node(node_type:str,label:str,**attrs)->GraphNode: return GraphNode(node_id=node_id(node_type,label),node_type=node_type,label=label,attributes=attrs)
