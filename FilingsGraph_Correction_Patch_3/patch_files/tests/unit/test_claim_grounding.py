from filingsgraph.verification.citations import verify_citations

def test_claim_level_citation_metrics():
    evidence=[{"citation_id":"SEC-A-1"},{"citation_id":"SEC-A-2"}]
    answer="Revenue increased materially [SEC-A-1].\nRisk language expanded [SEC-A-2]."
    r=verify_citations(answer,evidence)
    assert r["citation_precision"] == 1.0
    assert r["claim_support_rate"] == 1.0
    assert r["unsupported_claim_rate"] == 0.0
    assert r["ok"] is True

def test_unused_evidence_is_not_a_failure():
    evidence=[{"citation_id":"SEC-A-1"},{"citation_id":"SEC-A-2"}]
    answer="Revenue increased materially [SEC-A-1]."
    r=verify_citations(answer,evidence)
    assert r["citation_precision"] == 1.0
    assert "SEC-A-2" in r["uncited_evidence"]
    assert r["ok"] is True

def test_invalid_citation_is_detected():
    evidence=[{"citation_id":"SEC-A-1"}]
    r=verify_citations("Revenue increased [SEC-BOGUS-9].",evidence)
    assert r["citation_precision"] == 0.0
    assert r["ok"] is False
