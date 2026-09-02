from __future__ import annotations
import json
from pathlib import Path
from scripts._common import save_json


def read(path: str):
    p = Path(path)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def main():
    systems = {}
    for name in ["dense", "bm25", "hybrid", "hybrid_reranked"]:
        data = read(f"reports/experiments/test_{name}_retrieval.json")
        if data:
            systems[name] = data.get("summary", {})
    env = read("reports/final/environment.json") or {}
    model_cmp = read("reports/experiments/model_comparison.json")
    report = {
        "retrieval_systems": systems,
        "environment": {
            "gpu": env.get("gpu"),
            "vram_gb": env.get("vram_gb"),
            "cuda_available": env.get("cuda_available"),
        },
        "model_comparison": model_cmp,
        "paid_llm_api_cost_usd": 0,
        "note": "P50/P95 for full V6 generation require generated query traces; component retrieval latency is measured in retrieval reports.",
    }
    save_json("reports/experiments/system_metrics.json", report)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
