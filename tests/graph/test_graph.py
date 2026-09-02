from filingsgraph.graph.builder import TemporalKnowledgeGraph
from filingsgraph.graph.nodes import make_node
from filingsgraph.graph.edges import make_edge
from filingsgraph.graph.traversal import traverse

def test_provenance_and_temporal_traversal(tmp_path):
    kg = TemporalKnowledgeGraph()
    c = make_node("Company", "TestCo", ticker="T")
    r = make_node("Risk", "Export Controls")
    kg.add_node(c); kg.add_node(r)
    e = make_edge(c.node_id, r.node_id, "COMPANY_EXPOSED_TO_RISK", "rule", .8, valid_from="2025", valid_to="2025", filing_id="acc", source_chunk_id="ch", source_text_span="Export controls may affect sales.")
    kg.add_edge(e)
    assert e.filing_id and e.source_chunk_id and e.source_text_span
    assert len(traverse(kg.graph, [c.node_id], period=2025)["edges"]) == 1
    assert len(traverse(kg.graph, [c.node_id], period=2024)["edges"]) == 0
    p = tmp_path / "g.json"; kg.save(p)
    assert TemporalKnowledgeGraph.load(p).graph.number_of_edges() == 1
