from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

from filingsgraph.graph.extraction import graph_evidence_quality
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
            k = (
                str(block.get("ticker", "")).upper(),
                str(block.get("from")),
                str(block.get("to")),
                str(c.get("topic", "")).lower(),
            )
            current[k] = str(c.get("change_type", "")).upper()

    with TEMP_BASE.open(encoding="utf-8-sig", newline="") as f:
        reviewed = [r for r in csv.DictReader(f) if (r.get("gold_change_type") or "").strip()]

    gold, pred, missing = [], [], []
    confusion = Counter()
    for r in reviewed:
        k = (
            str(r.get("ticker", "")).upper(),
            str(r.get("from_year")),
            str(r.get("to_year")),
            str(r.get("topic", "")).lower(),
        )
        if k not in current:
            missing.append(k)
            continue
        g = r["gold_change_type"].strip().upper()
        p = current[k]
        gold.append(g)
        pred.append(p)
        confusion[(g, p)] += 1

    labels = sorted({*gold, *pred})
    by_class = {}
    for label in labels:
        tp = sum(g == label and p == label for g, p in zip(gold, pred))
        fp = sum(g != label and p == label for g, p in zip(gold, pred))
        fn = sum(g == label and p != label for g, p in zip(gold, pred))
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        by_class[label] = {"precision": precision, "recall": recall, "f1": f1, "support": sum(g == label for g in gold)}

    return {
        "available": True,
        "status": "DEVELOPMENT_DIAGNOSTIC_ONLY_PREVIOUSLY_REVIEWED",
        "rows_scored": len(gold),
        "missing_rows": len(missing),
        "macro_f1": macro_f1(gold, pred),
        "accuracy": sum(g == p for g, p in zip(gold, pred)) / len(gold) if gold else None,
        "by_class": by_class,
        "confusion": {f"{g}->{p}": n for (g, p), n in sorted(confusion.items())},
    }


def graph_rule_diagnostic() -> dict:
    if not EDGE_BASE.exists():
        return {"available": False, "reason": f"missing {EDGE_BASE}"}
    with EDGE_BASE.open(encoding="utf-8-sig", newline="") as f:
        reviewed = [r for r in csv.DictReader(f) if (r.get("gold_correct") or "").strip().upper() in {"Y", "N"}]

    tp = fp = tn = fn = 0
    for r in reviewed:
        pred = graph_evidence_quality(r.get("risk_topic", ""), r.get("source_text_span", "")) > 0
        gold = r["gold_correct"].strip().upper() == "Y"
        if pred and gold:
            tp += 1
        elif pred and not gold:
            fp += 1
        elif not pred and not gold:
            tn += 1
        else:
            fn += 1
    retained = tp + fp
    return {
        "available": True,
        "status": "DEVELOPMENT_RULE_DIAGNOSTIC_ONLY_PREVIOUSLY_REVIEWED_SPANS",
        "reviewed_edges": len(reviewed),
        "known_true_edges": tp + fn,
        "known_false_edges": tn + fp,
        "true_edge_retention": tp / (tp + fn) if tp + fn else None,
        "false_edge_removal": tn / (tn + fp) if tn + fp else None,
        "retained_edge_precision": tp / retained if retained else 1.0,
        "tp": tp,
        "fp": fp,
        "tn": tn,
        "fn": fn,
        "note": "Patch 5 scores the reviewed evidence spans through the current edge-quality rule. This avoids edge-ID collisions when a better provenance span replaces an older span for the same company/risk/year relation.",
    }


def main():
    report = {
        "temporal": temporal_diagnostic(),
        "graph": graph_rule_diagnostic(),
        "note": "Development-only diagnostic on previously reviewed labels. Fresh blind Temporal/Graph files remain untouched until this gate is accepted.",
    }
    save_json("reports/experiments/patch5_diagnostic.json", report)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
