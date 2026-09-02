from __future__ import annotations
import re
from filingsgraph.graph.nodes import make_node
from filingsgraph.graph.edges import make_edge

def extract_risk_edges(company_node_id:str,chunk:dict,risk_topics:list[str])->tuple[list,list]:
    text=chunk.get('text',''); nodes=[]; edges=[]
    for topic in risk_topics:
        terms=[x for x in re.findall(r'[a-z]+',topic.lower()) if len(x)>3]
        if terms and any(t in text.lower() for t in terms):
            n=make_node('Risk',topic); nodes.append(n)
            span=next((s.strip() for s in re.split(r'(?<=[.!?])\s+',text) if any(t in s.lower() for t in terms)),text[:600])[:1000]
            edges.append(make_edge(company_node_id,n.node_id,'COMPANY_EXPOSED_TO_RISK','rule_assisted',0.7,
                valid_from=str(chunk.get('fiscal_year') or ''),valid_to=str(chunk.get('fiscal_year') or ''),
                filing_id=chunk.get('accession_number'),source_chunk_id=chunk.get('chunk_id'),source_text_span=span))
    return nodes,edges
