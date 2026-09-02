from __future__ import annotations

import math
import torch

from filingsgraph.core.config import get_settings


class BGEReranker:
    def __init__(self, model_name: str | None = None, device: str | None = None):
        from transformers import AutoTokenizer, AutoModelForSequenceClassification

        s = get_settings()
        self.model_name = model_name or s.reranker_model
        self.device = device or s.device
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        dtype = torch.bfloat16 if self.device.startswith("cuda") and torch.cuda.is_available() else torch.float32
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name, dtype=dtype).to(self.device).eval()

    @torch.inference_mode()
    def score(self, query: str, results: list[dict], max_length: int = 512) -> list[float]:
        if not results:
            return []
        pairs = [[query, r.get("payload", {}).get("text", "")] for r in results]
        # This matches BAAI's documented Transformers usage for bge-reranker-v2-m3.
        batch = self.tokenizer(
            pairs,
            padding=True,
            truncation=True,
            max_length=max_length,
            return_tensors="pt",
        ).to(self.device)
        logits = self.model(**batch, return_dict=True).logits.view(-1).float().cpu().tolist()
        return [float(x) for x in logits]

    def rerank(self, query: str, results: list[dict], top_k: int = 8) -> list[dict]:
        logits = self.score(query, results)
        out = [
            {**r, "rerank_score": s, "method": "hybrid+reranker"}
            for r, s in zip(results, logits)
        ]
        return sorted(out, key=lambda x: x["rerank_score"], reverse=True)[:top_k]

    def blended_rerank(
        self,
        query: str,
        results: list[dict],
        top_k: int = 10,
        reranker_weight: float = 0.25,
        rrf_k: int = 60,
    ) -> list[dict]:
        """Fuse original hybrid rank with reranker rank.

        A learned reranker should not be allowed to catastrophically destroy a
        strong lexical/hybrid baseline. Rank fusion keeps the original ranking
        as an anchor while still allowing semantic promotions. The weight is
        tuned on DEV only by scripts/tune_reranker.py.
        """
        if not results:
            return []
        reranker_weight = min(1.0, max(0.0, float(reranker_weight)))
        base_weight = 1.0 - reranker_weight
        logits = self.score(query, results)
        reranked_order = sorted(range(len(results)), key=lambda i: logits[i], reverse=True)
        rr_rank = {idx: rank for rank, idx in enumerate(reranked_order, start=1)}
        out: list[dict] = []
        for base_rank, (item, logit) in enumerate(zip(results, logits), start=1):
            score = base_weight / (rrf_k + base_rank) + reranker_weight / (rrf_k + rr_rank[base_rank - 1])
            out.append(
                {
                    **item,
                    "rerank_score": float(logit),
                    "blended_rank_score": float(score),
                    "method": "hybrid+blended-reranker",
                }
            )
        return sorted(out, key=lambda x: x["blended_rank_score"], reverse=True)[:top_k]


class LexicalReranker:
    def rerank(self, query: str, results: list[dict], top_k: int = 8) -> list[dict]:
        q = set(query.lower().split())
        out = []
        for r in results:
            t = set(r.get("payload", {}).get("text", "").lower().split())
            score = len(q & t) / (len(q) or 1)
            out.append({**r, "rerank_score": score})
        return sorted(out, key=lambda x: x["rerank_score"], reverse=True)[:top_k]
