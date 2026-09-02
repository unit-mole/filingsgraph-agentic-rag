from filingsgraph.llm.grounding import enforce_grounding_contract
from filingsgraph.verification.citations import verify_citations


def test_grounding_guard_drops_uncited_claims_and_invalid_ids():
    evidence = [{"citation_id": "SEC-A-1"}, {"citation_id": "XBRL-NVDA-2025"}]
    answer = """# Summary
Revenue was 10. [XBRL-NVDA-2025]
This unsupported explanation should disappear.
Another claim [FAKE-1].
## Important Limitations
Evidence is insufficient for the missing driver analysis.
"""
    out = enforce_grounding_contract(answer, evidence)
    assert "Revenue was 10." in out
    assert "unsupported explanation" not in out
    assert "FAKE-1" not in out
    v = verify_citations(out, evidence)
    assert v["citation_precision"] == 1.0
    assert v["claim_support_rate"] == 1.0
    assert v["unsupported_claim_rate"] == 0.0


def test_grounding_guard_never_auto_attaches_a_citation():
    evidence = [{"citation_id": "SEC-A-1"}]
    out = enforce_grounding_contract("A factual line without evidence attachment.", evidence)
    assert "SEC-A-1" not in out
    assert "Evidence is insufficient" in out
