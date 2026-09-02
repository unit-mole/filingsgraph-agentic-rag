from __future__ import annotations
import json
from filingsgraph.core.config import ROOT
from filingsgraph.graph.builder import TemporalKnowledgeGraph
from scripts._common import save_json

def main():
    kg=TemporalKnowledgeGraph.load(ROOT/'data/graph/filingsgraph.json');prov=[]
    for u,v,k,a in kg.graph.edges(keys=True,data=True):
        if a.get('relationship') in {'COMPANY_EXPOSED_TO_RISK','RISK_CHANGED_FROM'}:
            prov.append(bool(a.get('filing_id') and a.get('source_chunk_id') and a.get('source_text_span')))
    report={'nodes':kg.graph.number_of_nodes(),'edges':kg.graph.number_of_edges(),'provenance_complete_rate':sum(prov)/len(prov) if prov else None,'edge_precision':None,'graph_path_accuracy':None,'note':'Precision/path accuracy require human-reviewed frozen graph gold; no metric is fabricated.'};save_json('reports/graph/graph_evaluation.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
