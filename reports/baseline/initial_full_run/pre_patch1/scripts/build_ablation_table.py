from __future__ import annotations
import csv
import json
from pathlib import Path
from scripts._common import save_json


def read(path):
    p = Path(path)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def metric(path, key):
    d = read(path)
    return (d or {}).get("summary", {}).get(key)


def main():
    financial = read("reports/experiments/test_financial.json") or {}
    temporal = read("reports/temporal/temporal_evaluation.json") or {}
    graph = read("reports/graph/graph_evaluation.json") or {}
    grounding = read("reports/experiments/grounding_evaluation.json") or {}
    rows = []
    architectures = [
        ("Dense only", "dense"),
        ("BM25 only", "bm25"),
        ("Hybrid", "hybrid"),
        ("Hybrid + reranker", "hybrid_reranked"),
    ]
    for label, key in architectures:
        rows.append({
            "Architecture": label,
            "R@10": metric(f"reports/experiments/test_{key}_retrieval.json", "r10"),
            "MRR": metric(f"reports/experiments/test_{key}_retrieval.json", "mrr"),
            "Numeric Acc.": None,
            "Temporal F1": None,
            "Graph QA": None,
            "Citation Precision": None,
            "Latency ms": metric(f"reports/experiments/test_{key}_retrieval.json", "latency_ms"),
        })
    rows.extend([
        {"Architecture": "+ structured XBRL tools", "R@10": rows[-1]["R@10"], "MRR": rows[-1]["MRR"], "Numeric Acc.": financial.get("fact_selection_accuracy"), "Temporal F1": None, "Graph QA": None, "Citation Precision": None, "Latency ms": None},
        {"Architecture": "+ temporal retrieval", "R@10": rows[-1]["R@10"], "MRR": rows[-1]["MRR"], "Numeric Acc.": financial.get("fact_selection_accuracy"), "Temporal F1": temporal.get("risk_change_f1"), "Graph QA": None, "Citation Precision": None, "Latency ms": None},
        {"Architecture": "+ graph retrieval", "R@10": rows[-1]["R@10"], "MRR": rows[-1]["MRR"], "Numeric Acc.": financial.get("fact_selection_accuracy"), "Temporal F1": temporal.get("risk_change_f1"), "Graph QA": graph.get("graph_path_accuracy"), "Citation Precision": None, "Latency ms": None},
        {"Architecture": "Full routed system", "R@10": rows[-1]["R@10"], "MRR": rows[-1]["MRR"], "Numeric Acc.": financial.get("fact_selection_accuracy"), "Temporal F1": temporal.get("risk_change_f1"), "Graph QA": graph.get("graph_path_accuracy"), "Citation Precision": grounding.get("citation_precision"), "Latency ms": None},
    ])
    save_json("reports/ablations/full_ablation_table.json", {"rows": rows, "note": "None values are intentionally unmeasured, not zero."})
    p = Path("reports/ablations/full_ablation_table.csv"); p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()
