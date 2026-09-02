from __future__ import annotations

from filingsgraph.graph.nodes import make_node
from filingsgraph.graph.edges import make_edge
from filingsgraph.risk_topics import best_topic_passage


def extract_risk_edges(company_node_id: str, chunk: dict, risk_topics: list[str]) -> tuple[list, list]:
    """Extract high-precision company -> risk edges from Item 1A evidence.

    Patch 4 intentionally favors precision over recall. A risk edge is created only
    when a topic-specific phrase is present in a substantive evidence unit. Generic
    words such as "regulation", "security", or "manufacturing" are insufficient.
    """
    text = chunk.get("text", "")
    nodes, edges = [], []
    for topic in risk_topics:
        span, score = best_topic_passage(text, topic)
        if not span:
            continue
        n = make_node("Risk", topic)
        nodes.append(n)
        confidence = min(0.98, 0.82 + 0.04 * max(0, score - 1))
        edges.append(
            make_edge(
                company_node_id,
                n.node_id,
                "COMPANY_EXPOSED_TO_RISK",
                "topic_rule_high_precision_v2",
                confidence,
                valid_from=str(chunk.get("fiscal_year") or ""),
                valid_to=str(chunk.get("fiscal_year") or ""),
                filing_id=chunk.get("accession_number"),
                source_chunk_id=chunk.get("chunk_id"),
                source_text_span=span[:1000],
            )
        )
    return nodes, edges
