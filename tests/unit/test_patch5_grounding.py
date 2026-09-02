from filingsgraph.llm.grounding import build_evidence_first_fallback, enforce_grounding_contract
from filingsgraph.verification.citations import verify_citations


def test_temporal_fallback_is_nonempty_and_cited():
    evidence = [{
        "citation_id": "TEMP-NVDA-X-2024-2025",
        "evidence_type": "temporal_risk_change",
        "ticker": "NVDA",
        "source_excerpt": "Export restrictions may adversely impact our business.",
        "payload": {"topic": "export controls", "change_type": "EXPANDED", "from_year": 2024, "to_year": 2025},
    }]
    out = build_evidence_first_fallback(
        "TEMPORAL",
        "How did export controls change?",
        evidence,
        [],
        [],
    )
    out = enforce_grounding_contract(out, evidence)
    assert "TEMP-NVDA-X-2024-2025" in out
    assert "Evidence is insufficient" not in out
    assert verify_citations(out, evidence)["ok"]


def test_graph_fallback_prefers_question_topic():
    evidence = [
        {"citation_id": "GRAPH-NVDA-001", "evidence_type": "graph_edge", "ticker": "NVDA", "source_excerpt": "Export control rules may adversely impact our business."},
        {"citation_id": "GRAPH-NVDA-002", "evidence_type": "graph_edge", "ticker": "NVDA", "source_excerpt": "Cybersecurity threats could disrupt operations."},
    ]
    out = build_evidence_first_fallback("GRAPH", "Which companies share export controls risk?", evidence)
    assert "GRAPH-NVDA-001" in out
    assert "GRAPH-NVDA-002" not in out
