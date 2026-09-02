from __future__ import annotations

import re

from filingsgraph.graph.nodes import make_node
from filingsgraph.graph.edges import make_edge
from filingsgraph.risk_topics import best_topic_passage, exposure_cue_score, topic_match_score


def graph_evidence_quality(topic: str, span: str) -> float:
    """Score substantive support for Company -> exposed-to -> Risk Topic.

    Topic-specific phrases dominate the score. Exposure/consequence language helps
    rank competing chunks for the same company/topic/year but is not mandatory when
    the risk phrase itself is explicit (e.g. "semiconductor supply chain").
    """
    if not span:
        return 0.0
    tscore = topic_match_score(topic, span)
    if not tscore:
        return 0.0
    low = span.lower()

    # Known generic/legal contexts that should not create manufacturing exposure.
    if topic.lower() == "semiconductor manufacturing":
        if re.search(r"\b(?:litigation|injunction|legal proceedings?|regulatory proceedings?)\b", low):
            if not re.search(r"\b(?:wafer|foundry|fabrication|yield|process node|manufacturing facilit|manufacturing capacity|semiconductor manufacturing)\b", low):
                return 0.0

    # A regulatory laundry list should not establish competition exposure.
    if topic.lower() == "competition":
        if re.search(r"areas including|including, but not limited to", low) and not re.search(
            r"\b(?:competitors?|market share|pricing pressure|intense competition|competitive pressure|competitive disadvantage)\b",
            low,
        ):
            return 0.0

    cues = exposure_cue_score(span)
    length_bonus = min(len(span), 800) / 8000.0
    return round(1.0 + 0.55 * min(tscore, 4) + 0.18 * min(cues, 4) + length_bonus, 6)


def extract_risk_edges(company_node_id: str, chunk: dict, risk_topics: list[str]) -> tuple[list, list]:
    """Extract candidate high-precision company -> risk edges from Item 1A evidence."""
    text = chunk.get("text", "")
    nodes, edges = [], []
    for topic in risk_topics:
        span, _ = best_topic_passage(text, topic)
        if not span:
            continue
        quality = graph_evidence_quality(topic, span)
        if quality <= 0:
            continue
        n = make_node("Risk", topic)
        nodes.append(n)
        confidence = min(0.99, 0.72 + 0.08 * quality)
        edges.append(
            make_edge(
                company_node_id,
                n.node_id,
                "COMPANY_EXPOSED_TO_RISK",
                "topic_rule_high_precision_v3",
                confidence,
                valid_from=str(chunk.get("fiscal_year") or ""),
                valid_to=str(chunk.get("fiscal_year") or ""),
                filing_id=chunk.get("accession_number"),
                source_chunk_id=chunk.get("chunk_id"),
                source_text_span=span[:1000],
            )
        )
    return nodes, edges
