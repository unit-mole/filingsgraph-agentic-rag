from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts._common import load_jsonl
from scripts._runtime import load_retrievers
from filingsgraph.evaluation.runner import evaluate_retriever
from filingsgraph.core.config import ROOT


def _best_reranker_weight(default: float = 0.25) -> float:
    p = ROOT / "reports/experiments/reranker_tuning.json"
    if not p.exists():
        return default
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
        return float(d.get("best_weight", default))
    except Exception:
        return default


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", choices=["dev", "test"], default="dev")
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--dense-backend", choices=["qdrant", "numpy"], default="qdrant")
    ap.add_argument("--skip-reranker", action="store_true")
    ap.add_argument("--reranker-weight", type=float, default=None)
    args = ap.parse_args()

    qs = load_jsonl(f"data/evaluation/{args.split}/questions.jsonl")
    dense, sparse, hybrid = load_retrievers(args.smoke, args.dense_backend)
    text = [q for q in qs if q.get("relevant_chunk_ids")]

    systems = [
        ("dense", lambda q: dense.search(q, top_k=10)),
        ("bm25", lambda q: sparse.search(q, top_k=10)),
        ("hybrid", lambda q: hybrid.search(q, dense_top_k=30, sparse_top_k=30, fusion_top_k=10)),
    ]
    if not args.skip_reranker and not args.smoke:
        from filingsgraph.reranking.reranker import BGEReranker

        reranker = BGEReranker()
        weight = args.reranker_weight if args.reranker_weight is not None else _best_reranker_weight()
        print(f"Using blended reranker weight={weight:.3f} (DEV-tuned if tuning report exists)")
        systems.append(
            (
                "hybrid_reranked",
                lambda q: reranker.blended_rerank(
                    q,
                    hybrid.search(q, dense_top_k=30, sparse_top_k=30, fusion_top_k=30),
                    top_k=10,
                    reranker_weight=weight,
                ),
            )
        )

    for name, fn in systems:
        r = evaluate_retriever(text, fn, f"reports/experiments/{args.split}_{name}_retrieval.json")
        print(name, r["summary"])


if __name__ == "__main__":
    main()
