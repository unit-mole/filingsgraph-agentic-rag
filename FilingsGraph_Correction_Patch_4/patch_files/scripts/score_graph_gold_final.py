from __future__ import annotations

import csv
import json
from pathlib import Path

from filingsgraph.core.config import ROOT
from filingsgraph.graph.builder import TemporalKnowledgeGraph
from filingsgraph.graph.temporal import edge_active
from scripts._common import save_json

BASELINE_QA = Path("reports/baseline/v6_specialized_gold_baseline/graph_qa_review.csv")
FINAL_EDGES = Path("reports/gold/graph_edge_review_final.csv")


def parse_set(v: str) -> set[str]:
    return {x.strip().upper() for x in (v or "").split("|") if x.strip()}


def predicted_companies(kg, topic: str, year: int) -> set[str]:
    risks = [n for n, a in kg.nodes(data=True) if a.get("node_type") == "Risk" and str(a.get("label", "")).lower() == topic.lower()]
    result = set()
    for risk in risks:
        for src, _, _, attrs in kg.in_edges(risk, keys=True, data=True):
            if attrs.get("relationship") != "COMPANY_EXPOSED_TO_RISK" or not edge_active(attrs, year):
                continue
            a = kg.nodes[src]
            if a.get("node_type") == "Company" and a.get("ticker"):
                result.add(str(a["ticker"]).upper())
    return result


def main():
    if not BASELINE_QA.exists():
        raise FileNotFoundError("Missing archived human-reviewed graph QA baseline.")
    if not FINAL_EDGES.exists():
        raise FileNotFoundError("Run python -m scripts.export_graph_gold_final and review the CSV first.")
    kg = TemporalKnowledgeGraph.load(ROOT / "data/graph/filingsgraph.json").graph
    with BASELINE_QA.open(encoding="utf-8-sig", newline="") as f:
        qrows = [r for r in csv.DictReader(f) if (r.get("human_approved_gold") or "").strip()]
    exact = []
    for r in qrows:
        pred = predicted_companies(kg, r.get("topic") or "", int(r.get("year") or 0))
        exact.append(pred == parse_set(r.get("human_approved_gold") or ""))
    with FINAL_EDGES.open(encoding="utf-8-sig", newline="") as f:
        erows = list(csv.DictReader(f))
    reviewed_e = [r for r in erows if (r.get("gold_correct") or "").strip().upper() in {"Y", "N"}]
    if not reviewed_e:
        raise ValueError("No reviewed fresh edge rows. Fill gold_correct first.")
    edge_precision = sum(r["gold_correct"].strip().upper() == "Y" for r in reviewed_e) / len(reviewed_e)
    report = {
        "graph_path_accuracy": sum(exact) / len(exact) if exact else None,
        "graph_qa_reviewed": len(exact),
        "graph_qa_status": "known reviewed benchmark regression after Patch 4; not a new blind QA set",
        "edge_precision": edge_precision,
        "edge_reviewed": len(reviewed_e),
        "edge_evaluation_status": "fresh_blind_after_patch4",
        "gold_source": "archived reviewed graph QA + fresh human-reviewed graph_edge_review_final.csv",
    }
    save_json("reports/graph/graph_gold_metrics_final.json", report)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
