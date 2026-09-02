from filingsgraph.retrieval.fusion import reciprocal_rank_fusion
from filingsgraph.embeddings.bge import HashEmbeddingProvider
from filingsgraph.retrieval.dense import LocalDenseIndex

def test_rrf_merges_duplicate():
    a = [{"id": "1", "score": 1, "payload": {"chunk_id": "x"}, "method": "dense"}]
    b = [{"id": "2", "score": 2, "payload": {"chunk_id": "x"}, "method": "bm25"}]
    r = reciprocal_rank_fusion([a, b])
    assert len(r) == 1 and set(r[0]["component_scores"]) == {"dense", "bm25"}
def test_hash_dense_retrieval():
    idx = LocalDenseIndex(HashEmbeddingProvider(64))
    payloads = [{"chunk_id": "a", "text": "export control semiconductor risk"}, {"chunk_id": "b", "text": "lease accounting office building"}]
    idx.build([p["text"] for p in payloads], payloads)
    assert idx.search("semiconductor export risk", 1)[0]["payload"]["chunk_id"] == "a"
