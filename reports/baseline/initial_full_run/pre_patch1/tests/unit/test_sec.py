import pytest
from filingsgraph.sec.companies import normalize_cik, resolve_tickers
from filingsgraph.sec.fair_access import RateLimiter

class FakeClient:
    def get_json(self, url):
        return {"0": {"ticker": "NVDA", "title": "NVIDIA Corporation", "cik_str": 1045810}}

def test_normalize_cik(): assert normalize_cik(1045810) == "0001045810"
def test_resolve_from_authoritative_payload():
    c = resolve_tickers(["NVDA"], FakeClient())[0]
    assert c.ticker == "NVDA" and c.cik == "0001045810"
def test_missing_ticker_raises():
    with pytest.raises(KeyError): resolve_tickers(["NOPE"], FakeClient())
def test_rate_limit_guard():
    with pytest.raises(ValueError): RateLimiter(11)
