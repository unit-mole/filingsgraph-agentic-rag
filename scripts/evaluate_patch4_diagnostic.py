from __future__ import annotations

import csv
import json
from pathlib import Path

from filingsgraph.core.config import ROOT
from filingsgraph.graph.builder import TemporalKnowledgeGraph
from scripts._common import load_json, save_json

TEMP_BASE = Path("reports/baseline/v6_specialized_gold_baseline/temporal_review.csv")
EDGE_BASE = Path("reports/baseline/v6_specialized_gold_baseline/graph_edge_review.csv")


def macro_f1(gold: list[str], pred: list[str]) -> float:
    labels = sorted({*gold, *pred})
    scores = []
    for label in labels:
        tp = sum(g == label and p == label for g, p in zip(gold, pred))
        fp = sum(g != label and p == label for g, p in zip(gold, pred))
        fn = sum(g == label and p != label for g, p in zip(gold, pred))
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        scores.append(2 * precision * recall / (precision + recall) if precision + recall else 0.0)
    return sum(scores) / len(scores) if scores else 0.0


def temporal_diagnostic() -> dict:
    if not TEMP_BASE.exists():
        return {"available": False, "reason": f"missing {TEMP_BASE}"}
    evaluation = load_json("reports/temporal/temporal_evaluation.json", {}) or {}
    current = {}
    for block in evaluation.get("rows", []):
        for c in block.get("changes", []):
            k = (str(block.get("ticker", "")).upper(), str(block.get("from")), str(block.get("to")), str(c.get("topic", "")).lower())
            current[k] = str(c.get("change_type", "")).upper()
    with TEMP_BASE.open(encoding="utf-8-sig", newline="") as f:
        reviewed = [r for r in csv.DictReader(f) if (r.get("gold_change_type") or "").strip()]
    gold, pred, missing = [], [], []
    for r in reviewed:
        k = (str(r.get("ticker", "")).upper(), str(r.get("from_year")), str(r.get("to_year")), str(r.get("topic", "")).lower())
        if k not in current:
            missing.append(k)
            continue
        gold.append(r["gold_change_type"].strip().upper())
        pred.append(current[k])
    return {
        "available": True,
        "status": "DEVELOPMENT_DIAGNOSTIC_ONLY_PREVIOUSLY_REVIEWED",
        "rows_scored": len(gold),
        "missing_rows": len(missing),
        "macro_f1": macro_f1(gold, pred),
        "accuracy": sum(g == p for g, p in zip(gold, pred)) / len(gold) if gold else None,
    }


def graph_diagnostic() -> dict:
    if not EDGE_BASE.exists():
        return {"available": False, "reason": f"missing {EDGE_BASE}"}
    kg = TemporalKnowledgeGraph.load(ROOT / "data/graph/filingsgraph.json").graph
    live_ids = {k for _, _, k, a in kg.edges(keys=True, data=True) if a.get("relationship") == "COMPANY_EXPOSED_TO_RISK"}
    with EDGE_BASE.open(encoding="utf-8-sig", newline="") as f:
        reviewed = [r for r in csv.DictReader(f) if (r.get("gold_correct") or "").strip().upper() in {"Y", "N"}]
    true_rows = [r for r in reviewed if r["gold_correct"].strip().upper() == "Y"]
    false_rows = [r for r in reviewed if r["gold_correct"].strip().upper() == "N"]
    retained_true = sum(r["edge_id"] in live_ids for r in true_rows)
    retained_false = sum(r["edge_id"] in live_ids for r in false_rows)
    retained_total = retained_true + retained_false
    return {
        "available": True,
        "status": "DEVELOPMENT_DIAGNOSTIC_ONLY_PREVIOUSLY_REVIEWED",
        "reviewed_edges": len(reviewed),
        "known_true_edges": len(true_rows),
        "known_false_edges": len(false_rows),
        "true_edge_retention": retained_true / len(true_rows) if true_rows else None,
        "false_edge_removal": (len(false_rows) - retained_false) / len(false_rows) if false_rows else None,
        "retained_edge_precision": retained_true / retained_total if retained_total else 1.0,
        "retained_true": retained_true,
        "retained_false": retained_false,
    }


def main():
    report = {
        "temporal": temporal_diagnostic(),
        "graph": graph_diagnostic(),
        "note": "These scores use previously reviewed diagnostic labels and are for Patch-4 development checks only. Do not report them as final/blind metrics.",
    }
    save_json("reports/experiments/patch4_diagnostic.json", report)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
