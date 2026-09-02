from __future__ import annotations
from functools import lru_cache
from filingsgraph.core.config import ROOT
from filingsgraph.database.session import Database
from filingsgraph.database.repositories import Repository
from filingsgraph.graph.builder import TemporalKnowledgeGraph
from filingsgraph.agents.nodes import ResearchOrchestrator

@lru_cache(maxsize=1)
def lightweight_assets():
    db=Database(); db.initialize(); repo=Repository(db)
    graph_path=ROOT/'data/graph/filingsgraph.json'
    graph=TemporalKnowledgeGraph.load(graph_path).graph if graph_path.exists() else None
    return repo,graph

@lru_cache(maxsize=1)
def full_engine():
    from scripts._runtime import load_retrievers
    from filingsgraph.reranking.reranker import BGEReranker
    from filingsgraph.llm.local_provider import get_local_provider
    repo,graph=lightweight_assets()
    _,_,hybrid=load_retrievers(False,'qdrant')
    return ResearchOrchestrator(hybrid,BGEReranker(),repo,graph,get_local_provider())
