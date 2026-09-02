from filingsgraph.agents.nodes import ResearchOrchestrator

class FakeRetriever:
    def search(self, q, **kwargs):
        return [{"score": .9, "method": "hybrid", "payload": {"chunk_id": "c1", "ticker": "NVDA", "company_name": "NVIDIA", "fiscal_year": 2025, "section": "Item 1A", "accession_number": "acc", "source_url": "https://www.sec.gov/x", "text": "Export controls may restrict product shipments and affect revenue."}}]
class FakeReranker:
    def rerank(self, q, r, top_k=8): return r
class FakeLLM:
    def generate(self, messages, **kwargs): return "[SEC-NVDA-2025-Item1A-001] Export controls are disclosed as a risk."

def test_text_orchestrator():
    r = ResearchOrchestrator(FakeRetriever(), FakeReranker(), None, None, FakeLLM()).research("What export control risk is described?", ["NVDA"], [2025])
    assert r["evidence"] and r["query_type"] == "TEXTUAL"
