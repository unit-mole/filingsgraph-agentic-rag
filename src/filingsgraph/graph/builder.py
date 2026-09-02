from __future__ import annotations
import json
from pathlib import Path
import networkx as nx
from networkx.readwrite import json_graph
from filingsgraph.schemas.graph import GraphNode,GraphEdge

class TemporalKnowledgeGraph:
    def __init__(self): self.graph=nx.MultiDiGraph()
    def add_node(self,node:GraphNode): self.graph.add_node(node.node_id,node_type=node.node_type,label=node.label,**node.attributes)
    def add_edge(self,edge:GraphEdge): self.graph.add_edge(edge.source_node,edge.target_node,key=edge.edge_id,**edge.model_dump(exclude={'source_node','target_node'}))
    def save(self,path:str|Path):
        p=Path(path); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(json_graph.node_link_data(self.graph,edges='edges')),encoding='utf-8')
    @classmethod
    def load(cls,path:str|Path):
        obj=cls(); data=json.loads(Path(path).read_text(encoding='utf-8')); obj.graph=json_graph.node_link_graph(data,edges='edges',directed=True,multigraph=True); return obj
