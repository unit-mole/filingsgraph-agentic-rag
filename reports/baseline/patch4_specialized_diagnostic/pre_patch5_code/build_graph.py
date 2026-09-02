from __future__ import annotations
from filingsgraph.core.config import ROOT,load_yaml
from filingsgraph.graph.builder import TemporalKnowledgeGraph
from filingsgraph.graph.nodes import make_node
from filingsgraph.graph.edges import make_edge
from filingsgraph.graph.extraction import extract_risk_edges
from scripts._common import load_jsonl,save_json

def main():
    chunks=load_jsonl('data/processed/chunks.jsonl');topics=load_yaml('graph.yaml')['risk_topics'];kg=TemporalKnowledgeGraph();companies={}; filings={}; risk_edges=0
    for c in chunks:
        ticker=c['ticker']; company=companies.get(ticker) or make_node('Company',c['company_name'],ticker=ticker,cik=c['cik']);companies[ticker]=company;kg.add_node(company)
        fkey=c['accession_number']; filing=filings.get(fkey) or make_node('Filing',fkey,ticker=ticker,fiscal_year=c.get('fiscal_year'),source_url=c.get('source_url'));filings[fkey]=filing;kg.add_node(filing)
        kg.add_edge(make_edge(company.node_id,filing.node_id,'COMPANY_HAS_FILING','deterministic',1.0,valid_from=str(c.get('fiscal_year') or ''),valid_to=str(c.get('fiscal_year') or ''),filing_id=fkey,source_chunk_id=c['chunk_id'],source_text_span=c['text'][:300]))
        if c.get('section')=='Item 1A':
            nodes,edges=extract_risk_edges(company.node_id,c,topics)
            for n in nodes:kg.add_node(n)
            for e in edges:kg.add_edge(e);risk_edges+=1
    # Add temporal same-risk transitions per company/year for provenance-bearing risk evolution.
    by_pair={}
    for u,v,k,a in list(kg.graph.edges(keys=True,data=True)):
        if a.get('relationship')=='COMPANY_EXPOSED_TO_RISK':by_pair.setdefault((u,v),[]).append((a.get('valid_from'),k,a))
    for (company,risk),items in by_pair.items():
        items=sorted(items,key=lambda x:str(x[0]));
        for prev,curr in zip(items,items[1:]):
            src=make_node('RiskObservation',f'{company}|{risk}|{prev[0]}',company=company,risk=risk,fiscal_year=prev[0]);dst=make_node('RiskObservation',f'{company}|{risk}|{curr[0]}',company=company,risk=risk,fiscal_year=curr[0]);kg.add_node(src);kg.add_node(dst)
            kg.add_edge(make_edge(src.node_id,dst.node_id,'RISK_CHANGED_FROM','deterministic_temporal_link',1.0,valid_from=str(curr[0] or ''),valid_to=str(curr[0] or ''),filing_id=curr[2].get('filing_id'),source_chunk_id=curr[2].get('source_chunk_id'),source_text_span=curr[2].get('source_text_span')))
    path=ROOT/'data/graph/filingsgraph.json';kg.save(path);report={'nodes':kg.graph.number_of_nodes(),'edges':kg.graph.number_of_edges(),'risk_edges':risk_edges,'path':str(path)};save_json('reports/final/graph_build_report.json',report);print(report)
if __name__=='__main__': main()
