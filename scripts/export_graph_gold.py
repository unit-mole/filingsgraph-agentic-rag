from __future__ import annotations

import argparse,csv,json,random,re
from pathlib import Path
from filingsgraph.core.config import ROOT
from filingsgraph.graph.builder import TemporalKnowledgeGraph
from filingsgraph.graph.temporal import edge_active
from scripts._common import load_jsonl


def predicted_companies(kg,topic:str,year:int)->list[str]:
    risk_nodes=[n for n,a in kg.nodes(data=True) if a.get("node_type")=="Risk" and str(a.get("label","")).lower()==topic.lower()]
    result=set()
    for risk in risk_nodes:
        for src,_,_,attrs in kg.in_edges(risk,keys=True,data=True):
            if attrs.get("relationship")!="COMPANY_EXPOSED_TO_RISK" or not edge_active(attrs,year): continue
            a=kg.nodes[src]
            if a.get("node_type")=="Company" and a.get("ticker"): result.add(str(a["ticker"]).upper())
    return sorted(result)


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--edge-sample-size",type=int,default=30); args=ap.parse_args()
    kg=TemporalKnowledgeGraph.load(ROOT/"data/graph/filingsgraph.json").graph
    questions=[]
    for split in ("dev","test"):
        for q in load_jsonl(f"data/evaluation/{split}/questions.jsonl"):
            if q.get("category")=="graph":
                topic=(q.get("metadata") or {}).get("risk_topic",""); year=int((q.get("expected_periods") or [0])[0] or 0)
                gold=sorted({str(x).upper() for x in q.get("expected_companies",[])})
                pred=predicted_companies(kg,topic,year)
                questions.append({"id":q.get("id"),"split":split,"question":q.get("question"),"topic":topic,"year":year,"benchmark_gold_companies":"|".join(gold),"predicted_companies":"|".join(pred),"human_approved_gold":"","review_note":""})
    qp=Path("reports/gold/graph_qa_review.csv"); qp.parent.mkdir(parents=True,exist_ok=True)
    with qp.open("w",newline="",encoding="utf-8-sig") as f:
        w=csv.DictWriter(f,fieldnames=list(questions[0]) if questions else ["id","split","question","topic","year","benchmark_gold_companies","predicted_companies","human_approved_gold","review_note"]); w.writeheader(); w.writerows(questions)

    edges=[]
    for u,v,k,a in kg.edges(keys=True,data=True):
        if a.get("relationship")!="COMPANY_EXPOSED_TO_RISK": continue
        ua=kg.nodes[u]; va=kg.nodes[v]
        edges.append({"edge_id":k,"ticker":ua.get("ticker"),"risk_topic":va.get("label"),"year":a.get("valid_from"),"source_text_span":(a.get("source_text_span") or "")[:900],"gold_correct":"","review_note":""})
    rng=random.Random(42); rng.shuffle(edges); edges=edges[:args.edge_sample_size]
    ep=Path("reports/gold/graph_edge_review.csv")
    with ep.open("w",newline="",encoding="utf-8-sig") as f:
        w=csv.DictWriter(f,fieldnames=list(edges[0]) if edges else ["edge_id","ticker","risk_topic","year","source_text_span","gold_correct","review_note"]); w.writeheader(); w.writerows(edges)
    print(json.dumps({"graph_qa_rows":len(questions),"graph_qa_path":str(qp),"edge_rows":len(edges),"edge_path":str(ep),"instruction":"For QA rows copy benchmark_gold_companies into human_approved_gold if correct, or correct the ticker set. For edge rows set gold_correct=Y or N."},indent=2))

if __name__=="__main__": main()
