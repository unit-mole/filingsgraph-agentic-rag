from __future__ import annotations
import json
from filingsgraph.core.config import ROOT,load_yaml
from filingsgraph.database.session import Database
from filingsgraph.database.repositories import Repository
from filingsgraph.temporal.risk_diff import compare_risk_disclosures
from filingsgraph.graph.builder import TemporalKnowledgeGraph
from filingsgraph.graph.traversal import traverse

def compare_companies(tickers:list[str],metric:str)->dict:
    db=Database(); repo=Repository(db); out={t:repo.metric_history(t,metric) for t in tickers}; db.close(); return out

def risk_evolution(ticker:str)->dict:
    p=ROOT/'data/processed/chunks.jsonl'; chunks=[json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()] if p.exists() else []
    years={}
    for c in chunks:
        if c.get('ticker')==ticker.upper() and c.get('section')=='Item 1A' and c.get('fiscal_year'):
            years.setdefault(c['fiscal_year'],[]).append(c['text'])
    topics=load_yaml('graph.yaml')['risk_topics']; ys=sorted(years)
    return {'ticker':ticker,'comparisons':[{'from':a,'to':b,'changes':compare_risk_disclosures(' '.join(years[a]),' '.join(years[b]),topics)} for a,b in zip(ys,ys[1:])]}

def company_graph(ticker:str,max_hops:int=2)->dict:
    p=ROOT/'data/graph/filingsgraph.json'
    if not p.exists(): return {'nodes':[],'edges':[]}
    kg=TemporalKnowledgeGraph.load(p)
    seeds=[n for n,a in kg.graph.nodes(data=True) if a.get('node_type')=='Company' and str(a.get('ticker','')).upper()==ticker.upper()]
    return traverse(kg.graph,seeds,max_hops=max_hops,max_nodes=30)
