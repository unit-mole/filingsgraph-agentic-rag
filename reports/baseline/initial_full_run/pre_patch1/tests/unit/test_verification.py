from filingsgraph.verification.citations import verify_citations
from filingsgraph.verification.temporal import verify_temporal
from filingsgraph.verification.claims import verify_entities, detect_contradictions

def test_citation_check(): assert verify_citations("[A] x", [{"citation_id": "A"}])["ok"]
def test_temporal_check(): assert not verify_temporal([{"citation_id": "x", "fiscal_year": 2023}], [2025])["ok"]
def test_entity_check(): assert verify_entities([{"ticker": "NVDA"}], ["NVDA"])["ok"]
def test_contradiction_detection():
    ev = [{"ticker": "T", "fiscal_year": 2025, "payload": {"metric": "revenue", "unit": "USD", "value": 1}}, {"ticker": "T", "fiscal_year": 2025, "payload": {"metric": "revenue", "unit": "USD", "value": 2}}]
    assert detect_contradictions(ev)
