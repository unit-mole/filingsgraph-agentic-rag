from pathlib import Path
from filingsgraph.core.config import ROOT
from filingsgraph.embeddings.bge import BGEEmbeddingProvider,HashEmbeddingProvider
from filingsgraph.retrieval.dense import QdrantDenseIndex,LocalDenseIndex
from filingsgraph.retrieval.sparse import BM25Index
from filingsgraph.retrieval.hybrid import HybridRetriever

def load_retrievers(smoke:bool=False,dense_backend:str='qdrant'):
    embed=HashEmbeddingProvider() if smoke else BGEEmbeddingProvider()
    if dense_backend=='numpy': dense=LocalDenseIndex(embed).load(ROOT/'data/index/dense')
    else: dense=QdrantDenseIndex(embed)
    sparse=BM25Index().load(ROOT/'data/index/bm25.pkl');hybrid=HybridRetriever(dense,sparse);return dense,sparse,hybrid
