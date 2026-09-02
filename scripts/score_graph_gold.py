from __future__ import annotations

import csv,json
from pathlib import Path
from scripts._common import save_json


def parse_set(v:str)->set[str]: return {x.strip().upper() for x in (v or "").split("|") if x.strip()}

def main():
    qp=Path("reports/gold/graph_qa_review.csv"); ep=Path("reports/gold/graph_edge_review.csv")
    if not qp.exists() or not ep.exists(): raise FileNotFoundError("Run python -m scripts.export_graph_gold first.")
    with qp.open(encoding="utf-8-sig",newline="") as f: qrows=list(csv.DictReader(f))
    reviewed_q=[r for r in qrows if (r.get("human_approved_gold") or "").strip()]
    if not reviewed_q: raise ValueError("No reviewed graph QA rows. Fill human_approved_gold first.")
    exact=[parse_set(r["predicted_companies"])==parse_set(r["human_approved_gold"]) for r in reviewed_q]
    with ep.open(encoding="utf-8-sig",newline="") as f: erows=list(csv.DictReader(f))
    reviewed_e=[r for r in erows if (r.get("gold_correct") or "").strip().upper() in {"Y","N"}]
    edge_precision=sum((r["gold_correct"].strip().upper()=="Y") for r in reviewed_e)/len(reviewed_e) if reviewed_e else None
    report={"graph_path_accuracy":sum(exact)/len(exact),"graph_qa_reviewed":len(reviewed_q),"edge_precision":edge_precision,"edge_reviewed":len(reviewed_e),"gold_source":"human-reviewed reports/gold/graph_qa_review.csv and graph_edge_review.csv"}
    save_json("reports/graph/graph_gold_metrics.json",report); print(json.dumps(report,indent=2))

if __name__=="__main__": main()
