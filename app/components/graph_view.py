from __future__ import annotations
import networkx as nx

def graph_summary(graph: nx.Graph) -> dict:
    return {"nodes": graph.number_of_nodes(), "edges": graph.number_of_edges(), "node_types": sorted({a.get("node_type") for _, a in graph.nodes(data=True) if a.get("node_type")})}
