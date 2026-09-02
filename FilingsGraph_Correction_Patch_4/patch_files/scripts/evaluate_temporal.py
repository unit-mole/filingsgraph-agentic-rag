from __future__ import annotations

import json

from filingsgraph.core.config import load_yaml
from filingsgraph.temporal.risk_diff import compare_risk_disclosures
from scripts._common import load_jsonl, load_json, save_json


def main():
    chunks = load_jsonl("data/processed/chunks.jsonl")
    topics = load_yaml("graph.yaml")["risk_topics"]
    groups = {}
    for c in chunks:
        if c.get("section") == "Item 1A" and c.get("fiscal_year"):
            groups.setdefault(c["ticker"], {}).setdefault(c["fiscal_year"], []).append(c["text"])
    rows = []
    for t, years in groups.items():
        ys = sorted(years)
        for a, b in zip(ys, ys[1:]):
            changes = compare_risk_disclosures(" ".join(years[a]), " ".join(years[b]), topics)
            rows.append({"ticker": t, "from": a, "to": b, "changes": changes})
    final_gold = load_json("reports/temporal/temporal_gold_metrics_final.json", {}) or {}
    report = {
        "comparisons": len(rows),
        "risk_change_f1": final_gold.get("risk_change_f1"),
        "risk_change_accuracy": final_gold.get("risk_change_accuracy"),
        "gold_reviewed_rows": final_gold.get("reviewed_rows", 0),
        "evaluation_status": final_gold.get("evaluation_status", "AWAITING_FRESH_BLIND_GOLD_AFTER_PATCH4"),
        "note": "Patch-4 final metrics are populated only from the fresh blind review file; the prior 30-row set is retained as diagnostic/development gold.",
        "rows": rows,
    }
    save_json("reports/temporal/temporal_evaluation.json", report)
    print(json.dumps({k: v for k, v in report.items() if k != "rows"}, indent=2))


if __name__ == "__main__":
    main()
