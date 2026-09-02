from __future__ import annotations

import json

from filingsgraph.core.config import ROOT
from filingsgraph.graph.builder import TemporalKnowledgeGraph
from scripts._common import load_json, save_json


def main():
    g = TemporalKnowledgeGraph.load(ROOT / "data/graph/filingsgraph.json").graph
    edges = list(g.edges(data=True))
    provenance = [bool(a.get("source_chunk_id") and a.get("source_text_span")) for _, _, a in edges]
    gold = load_json("reports/graph/graph_gold_metrics_final.json", {}) or {}
    report = {
        "nodes": g.number_of_nodes(),
        "edges": g.number_of_edges(),
        "provenance_complete_rate": sum(provenance) / len(provenance) if provenance else 1.0,
        "edge_precision": gold.get("edge_precision"),
        "graph_path_accuracy": gold.get("graph_path_accuracy"),
        "graph_qa_reviewed": gold.get("graph_qa_reviewed", 0),
        "edge_reviewed": gold.get("edge_reviewed", 0),
        "edge_evaluation_status": gold.get("edge_evaluation_status", "AWAITING_FRESH_BLIND_EDGE_GOLD_AFTER_PATCH4"),
        "graph_qa_status": gold.get("graph_qa_status", "known benchmark regression pending final score"),
        "note": "Patch-4 edge precision is populated only from a fresh edge sample excluding the previously reviewed diagnostic edges.",
    }
    save_json("reports/graph/graph_evaluation.json", report)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
