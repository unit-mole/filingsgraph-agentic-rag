from filingsgraph.schemas.companies import Company
from filingsgraph.schemas.graph import GraphEdge

def test_company_cik_validation():
    c = Company(company_name="X", ticker="X", cik="0000000001")
    assert c.cik == "0000000001"

def test_graph_confidence_bounds():
    e = GraphEdge(edge_id="e", source_node="a", target_node="b", relationship="R", extraction_method="rule", confidence=.7)
    assert e.confidence == .7
