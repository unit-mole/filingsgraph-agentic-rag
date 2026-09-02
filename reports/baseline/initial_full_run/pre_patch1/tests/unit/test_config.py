from filingsgraph.core.config import load_yaml

def test_company_config_has_five_companies():
    assert len(load_yaml("companies.yaml")["companies"]) == 5

def test_graph_limits():
    g = load_yaml("graph.yaml")
    assert g["max_hops"] == 2 and g["max_nodes"] == 30
