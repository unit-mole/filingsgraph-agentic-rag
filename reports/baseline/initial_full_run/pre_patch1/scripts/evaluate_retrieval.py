from __future__ import annotations
import argparse
from scripts._common import load_jsonl
from scripts._runtime import load_retrievers
from filingsgraph.evaluation.runner import evaluate_retriever


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", choices=["dev", "test"], default="dev")
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--dense-backend", choices=["qdrant", "numpy"], default="qdrant")
    ap.add_argument("--skip-reranker", action="store_true")
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
        systems.append(
            (
                "hybrid_reranked",
                lambda q: reranker.rerank(
                    q,
                    hybrid.search(q, dense_top_k=30, sparse_top_k=30, fusion_top_k=30),
                    top_k=10,
                ),
            )
        )

    for name, fn in systems:
        r = evaluate_retriever(text, fn, f"reports/experiments/{args.split}_{name}_retrieval.json")
        print(name, r["summary"])


if __name__ == "__main__":
    main()
