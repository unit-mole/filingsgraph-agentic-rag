from __future__ import annotations

import argparse
import csv
import random
from pathlib import Path

from scripts._common import load_json

ALLOWED = "NEW|REMOVED|UNCHANGED|EXPANDED|REDUCED"
BASELINE_REVIEW = Path("reports/baseline/v6_specialized_gold_baseline/temporal_review.csv")


def key(row: dict) -> tuple[str, str, str, str]:
    return (
        str(row.get("ticker") or "").upper(),
        str(row.get("from_year") or ""),
        str(row.get("to_year") or ""),
        str(row.get("topic") or "").lower(),
    )


def reviewed_keys() -> set[tuple[str, str, str, str]]:
    if not BASELINE_REVIEW.exists():
        return set()
    with BASELINE_REVIEW.open(encoding="utf-8-sig", newline="") as f:
        return {key(r) for r in csv.DictReader(f)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample-size", type=int, default=30)
    ap.add_argument("--seed", type=int, default=20260902)
    args = ap.parse_args()
    data = load_json("reports/temporal/temporal_evaluation.json", {}) or {}
    excluded = reviewed_keys()
    rows = []
    for block in data.get("rows", []):
        for c in block.get("changes", []):
            r = {
                "ticker": block.get("ticker"),
                "from_year": block.get("from"),
                "to_year": block.get("to"),
                "topic": c.get("topic"),
                "predicted_change_type": c.get("change_type"),
                "similarity": c.get("similarity"),
                "old_excerpt": (c.get("old_excerpt") or "")[:1000],
                "new_excerpt": (c.get("new_excerpt") or "")[:1000],
                "gold_change_type": "",
                "review_note": "",
            }
            if key(r) not in excluded:
                rows.append(r)
    rng = random.Random(args.seed)
    rng.shuffle(rows)
    chosen, seen = [], set()
    # Broad issuer/topic coverage first.
    for r in rows:
        bucket = (r["ticker"], r["topic"])
        if bucket not in seen:
            chosen.append(r)
            seen.add(bucket)
        if len(chosen) >= args.sample_size:
            break
    for r in rows:
        if len(chosen) >= args.sample_size:
            break
        if r not in chosen:
            chosen.append(r)
    p = Path("reports/gold/temporal_review_final.csv")
    p.parent.mkdir(parents=True, exist_ok=True)
    fields = list(chosen[0]) if chosen else [
        "ticker", "from_year", "to_year", "topic", "predicted_change_type", "similarity",
        "old_excerpt", "new_excerpt", "gold_change_type", "review_note",
    ]
    with p.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(chosen)
    print({
        "rows": len(chosen),
        "excluded_previously_reviewed": len(excluded),
        "path": str(p),
        "instruction": f"Fresh blind set. Fill gold_change_type with one of {ALLOWED}, save CSV, then run scripts.score_temporal_gold_final.",
    })


if __name__ == "__main__":
    main()
