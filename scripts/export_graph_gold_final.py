from __future__ import annotations

import argparse
import csv
import json
import random
from pathlib import Path

from filingsgraph.core.config import ROOT
from filingsgraph.graph.builder import TemporalKnowledgeGraph

BASELINE_EDGE_REVIEW = Path("reports/baseline/v6_specialized_gold_baseline/graph_edge_review.csv")


def prior_edge_ids() -> set[str]:
    if not BASELINE_EDGE_REVIEW.exists():
        return set()
    with BASELINE_EDGE_REVIEW.open(encoding="utf-8-sig", newline="") as f:
        return {str(r.get("edge_id") or "") for r in csv.DictReader(f) if r.get("edge_id")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--edge-sample-size", type=int, default=30)
    ap.add_argument("--seed", type=int, default=20260902)
    args = ap.parse_args()
    kg = TemporalKnowledgeGraph.load(ROOT / "data/graph/filingsgraph.json").graph
    excluded = prior_edge_ids()
    edges = []
    for u, v, k, a in kg.edges(keys=True, data=True):
        if a.get("relationship") != "COMPANY_EXPOSED_TO_RISK" or k in excluded:
            continue
        ua, va = kg.nodes[u], kg.nodes[v]
        edges.append({
            "edge_id": k,
            "ticker": ua.get("ticker"),
            "risk_topic": va.get("label"),
            "year": a.get("valid_from"),
            "source_text_span": (a.get("source_text_span") or "")[:1000],
            "extraction_method": a.get("extraction_method"),
            "confidence": a.get("confidence"),
            "gold_correct": "",
            "review_note": "",
        })
    rng = random.Random(args.seed)
    rng.shuffle(edges)
    chosen, seen = [], set()
    for r in edges:
        bucket = (r["ticker"], r["risk_topic"])
        if bucket not in seen:
            chosen.append(r)
            seen.add(bucket)
        if len(chosen) >= args.edge_sample_size:
            break
    for r in edges:
        if len(chosen) >= args.edge_sample_size:
            break
        if r not in chosen:
            chosen.append(r)
    p = Path("reports/gold/graph_edge_review_final.csv")
    p.parent.mkdir(parents=True, exist_ok=True)
    fields = list(chosen[0]) if chosen else [
        "edge_id", "ticker", "risk_topic", "year", "source_text_span", "extraction_method", "confidence", "gold_correct", "review_note"
    ]
    with p.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(chosen)
    print(json.dumps({
        "edge_rows": len(chosen),
        "excluded_previously_reviewed_edges": len(excluded),
        "path": str(p),
        "instruction": "Fresh blind edge sample. Set gold_correct=Y or N, save CSV, then run scripts.score_graph_gold_final.",
    }, indent=2))


if __name__ == "__main__":
    main()
