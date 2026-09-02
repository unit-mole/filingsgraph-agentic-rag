from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

from scripts._common import save_json

ALLOWED = {"NEW", "REMOVED", "UNCHANGED", "EXPANDED", "REDUCED"}


def macro_f1(gold: list[str], pred: list[str]) -> float:
    scores = []
    for label in sorted(ALLOWED):
        tp = sum(g == label and p == label for g, p in zip(gold, pred))
        fp = sum(g != label and p == label for g, p in zip(gold, pred))
        fn = sum(g == label and p != label for g, p in zip(gold, pred))
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        scores.append(2 * precision * recall / (precision + recall) if precision + recall else 0.0)
    return sum(scores) / len(scores)


def main():
    p = Path("reports/gold/temporal_review_final.csv")
    if not p.exists():
        raise FileNotFoundError("Run python -m scripts.export_temporal_gold_final first.")
    with p.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    reviewed = [r for r in rows if (r.get("gold_change_type") or "").strip().upper() in ALLOWED]
    if not reviewed:
        raise ValueError("No reviewed rows. Fill gold_change_type in temporal_review_final.csv first.")
    gold = [r["gold_change_type"].strip().upper() for r in reviewed]
    pred = [r["predicted_change_type"].strip().upper() for r in reviewed]
    acc = sum(g == p for g, p in zip(gold, pred)) / len(gold)
    report = {
        "reviewed_rows": len(reviewed),
        "total_review_rows": len(rows),
        "risk_change_f1": macro_f1(gold, pred),
        "risk_change_accuracy": acc,
        "labels": sorted(ALLOWED),
        "gold_source": "fresh human-reviewed reports/gold/temporal_review_final.csv",
        "evaluation_status": "fresh_blind_after_patch4",
    }
    save_json("reports/temporal/temporal_gold_metrics_final.json", report)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
