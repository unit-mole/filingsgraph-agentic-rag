from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from filingsgraph.evaluation.retrieval_metrics import recall_at_k, reciprocal_rank, ndcg_at_k
from filingsgraph.reranking.reranker import BGEReranker
from scripts._common import load_jsonl, save_json
from scripts._runtime import load_retrievers


def _metrics(rows: list[dict]) -> dict:
    if not rows:
        return {"r10": None, "mrr": None, "ndcg10": None}
    return {
        "r10": sum(r["r10"] for r in rows) / len(rows),
        "mrr": sum(r["mrr"] for r in rows) / len(rows),
        "ndcg10": sum(r["ndcg10"] for r in rows) / len(rows),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--weights", default="0,0.10,0.20,0.25,0.35,0.50,0.75,1.0")
    args = ap.parse_args()
    weights = [float(x) for x in args.weights.split(",")]

    qs = [q for q in load_jsonl("data/evaluation/dev/questions.jsonl") if q.get("relevant_chunk_ids")]
    _, _, hybrid = load_retrievers(False, "qdrant")
    reranker = BGEReranker()

    cached = []
    start = time.perf_counter()
    for q in qs:
        base = hybrid.search(q["question"], dense_top_k=30, sparse_top_k=30, fusion_top_k=30)
        logits = reranker.score(q["question"], base)
        cached.append((q, base, logits))

    results = []
    for weight in weights:
        rows = []
        for q, base, logits in cached:
            if weight <= 0:
                ranked = base[:10]
            else:
                rerank_order = sorted(range(len(base)), key=lambda i: logits[i], reverse=True)
                rr_rank = {idx: rank for rank, idx in enumerate(rerank_order, 1)}
                base_w = 1.0 - weight
                scored = []
                for base_rank, item in enumerate(base, 1):
                    idx = base_rank - 1
                    score = base_w / (60 + base_rank) + weight / (60 + rr_rank[idx])
                    scored.append((score, item))
                ranked = [x[1] for x in sorted(scored, key=lambda x: x[0], reverse=True)[:10]]
            ids = [r.get("payload", {}).get("chunk_id") or r.get("id") for r in ranked]
            rel = set(q["relevant_chunk_ids"])
            rows.append(
                {
                    "r10": recall_at_k(ids, rel, 10),
                    "mrr": reciprocal_rank(ids, rel),
                    "ndcg10": ndcg_at_k(ids, rel, 10),
                }
            )
        m = _metrics(rows)
        # Primary objective: MRR; Recall@10 and nDCG are tie-breakers.
        objective = (m["mrr"] or 0.0, m["r10"] or 0.0, m["ndcg10"] or 0.0)
        results.append({"reranker_weight": weight, **m, "objective": list(objective)})

    best = max(results, key=lambda r: tuple(r["objective"])) if results else None
    report = {
        "split": "dev",
        "questions": len(qs),
        "weights": results,
        "best_weight": best["reranker_weight"] if best else 0.0,
        "best_metrics": {k: best[k] for k in ("r10", "mrr", "ndcg10")} if best else None,
        "elapsed_seconds": time.perf_counter() - start,
        "note": "Tuned on DEV only. The frozen TEST split must not be used for weight selection.",
    }
    save_json("reports/experiments/reranker_tuning.json", report)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
