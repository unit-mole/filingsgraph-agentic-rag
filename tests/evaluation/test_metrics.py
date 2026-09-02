from filingsgraph.evaluation.retrieval_metrics import recall_at_k, precision_at_k, reciprocal_rank, ndcg_at_k
from filingsgraph.evaluation.graph_metrics import edge_precision, irrelevant_expansion_rate

def test_retrieval_metrics():
    r = ["a", "b", "c"]; g = {"b"}
    assert recall_at_k(r, g, 2) == 1 and precision_at_k(r, g, 2) == .5 and reciprocal_rank(r, g) == .5 and 0 < ndcg_at_k(r, g, 3) <= 1
def test_graph_metrics(): assert edge_precision({("a", "b")}, {("a", "b")}) == 1 and irrelevant_expansion_rate({"a", "x"}, {"a"}) == .5
