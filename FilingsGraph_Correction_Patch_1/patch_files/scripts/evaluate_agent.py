from __future__ import annotations

import argparse
import json

from filingsgraph.agents.router import classify_query
from scripts._common import load_jsonl, save_json

MAP = {
    "textual_lookup": "TEXTUAL",
    "exact_financial_fact": "NUMERIC",
    "temporal": "TEMPORAL",
    "graph": "GRAPH",
    "mixed": "MIXED",
}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", choices=["dev", "test"], default="dev")
    args = ap.parse_args()
    qs = load_jsonl(f"data/evaluation/{args.split}/questions.jsonl")
    rows = []
    for q in qs:
        if q.get("category") not in MAP:
            continue
        pred = classify_query(q["question"])
        gold = MAP[q["category"]]
        rows.append({"id": q["id"], "category": q["category"], "gold": gold, "pred": pred, "ok": gold == pred})
    by_category = {}
    for cat in sorted({r["category"] for r in rows}):
        cr = [r for r in rows if r["category"] == cat]
        by_category[cat] = sum(r["ok"] for r in cr) / len(cr) if cr else None
    report = {
        "split": args.split,
        "questions": len(rows),
        "routing_accuracy": sum(r["ok"] for r in rows) / len(rows) if rows else None,
        "by_category": by_category,
        "rows": rows,
    }
    save_json(f"reports/experiments/{args.split}_agent_routing.json", report)
    print(json.dumps({k: v for k, v in report.items() if k != "rows"}, indent=2))


if __name__ == "__main__":
    main()
