from filingsgraph.retrieval.fusion import reciprocal_rank_fusion

class HybridRetriever:
    def __init__(self,dense,sparse,rrf_k:int=60): self.dense=dense; self.sparse=sparse; self.rrf_k=rrf_k
    def search(self,query:str,dense_top_k:int=30,sparse_top_k:int=30,fusion_top_k:int=30,filters:dict|None=None):
        d=self.dense.search(query,dense_top_k,filters); s=self.sparse.search(query,sparse_top_k,filters)
        return reciprocal_rank_fusion([d,s],self.rrf_k,fusion_top_k)
