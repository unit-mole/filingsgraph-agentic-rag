from __future__ import annotations
import json,time
from filingsgraph.core.config import ROOT
from filingsgraph.graph.builder import TemporalKnowledgeGraph
from filingsgraph.graph.traversal import traverse
from scripts._common import save_json

def main():
    kg=TemporalKnowledgeGraph.load(ROOT/'data/graph/filingsgraph.json');companies=[n for n,a in kg.graph.nodes(data=True) if a.get('node_type')=='Company'];rows=[]
    for hops in [0,1,2]:
        counts=[];times=[]
        for c in companies:
            st=time.perf_counter();r={'nodes':[c],'edges':[]} if hops==0 else traverse(kg.graph,[c],max_hops=hops,max_nodes=30);times.append((time.perf_counter()-st)*1000);counts.append(len(r['nodes']))
        rows.append({'hops':hops,'mean_nodes':sum(counts)/len(counts) if counts else 0,'mean_latency_ms':sum(times)/len(times) if times else 0,'answer_accuracy':None})
    report={'rows':rows,'note':'Answer accuracy remains TBD until graph-relevant frozen gold is human-reviewed.'};save_json('reports/ablations/graph_ablation.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
