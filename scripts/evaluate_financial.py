from __future__ import annotations

import argparse
import json

from filingsgraph.database.session import Database
from filingsgraph.database.repositories import Repository
from scripts._common import load_jsonl, save_json


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", choices=["dev", "test"], default="dev")
    args = ap.parse_args()

    qs = [
        q for q in load_jsonl(f"data/evaluation/{args.split}/questions.jsonl")
        if q.get("category") == "exact_financial_fact"
    ]
    db = Database()
    repo = Repository(db)
    rows = []
    for q in qs:
        metric = q.get("metadata", {}).get("metric")
        ticker = q.get("expected_company")
        year = q.get("expected_periods", [None])[0]
        candidates = [r for r in repo.metric_history(ticker, metric) if r.get("fiscal_year") == year]
        got = candidates[0] if candidates else None
        expected_fact_id = q.get("metadata", {}).get("fact_id")
        value_ok = bool(got) and abs(float(got["value"]) - float(q["expected_value"])) <= max(1e-9, abs(float(q["expected_value"])) * 1e-12)
        unit_ok = bool(got) and got["unit"] == q["expected_unit"]
        fact_id_ok = bool(got) and (not expected_fact_id or got.get("fact_id") == expected_fact_id)
        rows.append(
            {
                "id": q["id"],
                "ok": bool(value_ok and unit_ok and fact_id_ok),
                "predicted": got["value"] if got else None,
                "expected": q["expected_value"],
                "unit_ok": unit_ok,
                "fact_id_ok": fact_id_ok,
                "predicted_fact_id": got.get("fact_id") if got else None,
                "expected_fact_id": expected_fact_id,
            }
        )
    db.close()
    report = {
        "split": args.split,
        "questions": len(rows),
        "fact_selection_accuracy": sum(r["ok"] for r in rows) / len(rows) if rows else None,
        "unit_accuracy": sum(r["unit_ok"] for r in rows) / len(rows) if rows else None,
        "fact_id_accuracy": sum(r["fact_id_ok"] for r in rows) / len(rows) if rows else None,
        "calculation_exact_match": "evaluated separately by deterministic unit tests",
        "rows": rows,
    }
    save_json(f"reports/experiments/{args.split}_financial.json", report)
    print(json.dumps({k: v for k, v in report.items() if k != "rows"}, indent=2))


if __name__ == "__main__":
    main()
