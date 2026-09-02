from __future__ import annotations
import atexit
from functools import lru_cache
from filingsgraph.core.config import ROOT
from filingsgraph.database.session import Database
from filingsgraph.database.repositories import Repository
from filingsgraph.graph.builder import TemporalKnowledgeGraph
from filingsgraph.agents.nodes import ResearchOrchestrator

_ENGINE_REF = None

@lru_cache(maxsize=1)
def lightweight_assets():
    db=Database(); db.initialize(); repo=Repository(db)
    graph_path=ROOT/'data/graph/filingsgraph.json'
    graph=TemporalKnowledgeGraph.load(graph_path).graph if graph_path.exists() else None
    return repo,graph

@lru_cache(maxsize=1)
def full_engine():
    global _ENGINE_REF
    from scripts._runtime import load_retrievers
    from filingsgraph.reranking.reranker import BGEReranker
    from filingsgraph.llm.local_provider import get_local_provider
    repo,graph=lightweight_assets()
    _,_,hybrid=load_retrievers(False,'qdrant')
    _ENGINE_REF=ResearchOrchestrator(hybrid,BGEReranker(),repo,graph,get_local_provider())
    return _ENGINE_REF

@atexit.register
def _close_runtime_handles():
    """Close local Qdrant before Python module teardown to avoid destructor noise."""
    try:
        engine=_ENGINE_REF
        dense=getattr(getattr(engine,"retriever",None),"dense",None) if engine else None
        client=getattr(dense,"client",None)
        if client is not None and hasattr(client,"close"):
            client.close()
    except Exception:
        pass
    try:
        cached=lightweight_assets.cache_info().currsize
        if cached:
            repo,_=lightweight_assets()
            db=getattr(repo,"db",None)
            if db is not None and hasattr(db,"close"):
                db.close()
    except Exception:
        pass
