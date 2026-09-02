from __future__ import annotations
import json
from filingsgraph.core.config import ROOT
from filingsgraph.graph.builder import TemporalKnowledgeGraph
from scripts._common import load_json,save_json

def main():
    kg=TemporalKnowledgeGraph.load(ROOT/'data/graph/filingsgraph.json');prov=[]
    for u,v,k,a in kg.graph.edges(keys=True,data=True):
        if a.get('relationship') in {'COMPANY_EXPOSED_TO_RISK','RISK_CHANGED_FROM'}:
            prov.append(bool(a.get('filing_id') and a.get('source_chunk_id') and a.get('source_text_span')))
    gold=load_json('reports/graph/graph_gold_metrics.json',{}) or {}
    report={'nodes':kg.graph.number_of_nodes(),'edges':kg.graph.number_of_edges(),'provenance_complete_rate':sum(prov)/len(prov) if prov else None,'edge_precision':gold.get('edge_precision'),'graph_path_accuracy':gold.get('graph_path_accuracy'),'graph_qa_reviewed':gold.get('graph_qa_reviewed',0),'edge_reviewed':gold.get('edge_reviewed',0),'note':'Gold metrics are populated only from human-reviewed review sheets; otherwise they remain null.'};save_json('reports/graph/graph_evaluation.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
