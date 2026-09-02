from __future__ import annotations
from filingsgraph.sec.client import SECClient
from filingsgraph.schemas.companies import Company

TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"

def normalize_cik(cik: int | str) -> str:
    return str(cik).zfill(10)

def resolve_tickers(tickers: list[str], client: SECClient | None = None) -> list[Company]:
    client = client or SECClient()
    data = client.get_json(TICKERS_URL)
    lookup = {str(v["ticker"]).upper(): v for v in data.values()}
    companies = []
    missing = []
    for ticker in tickers:
        t = ticker.upper()
        row = lookup.get(t)
        if not row:
            missing.append(t)
            continue
        companies.append(Company(company_name=row["title"], ticker=t, cik=normalize_cik(row["cik_str"]), sec_entity_name=row["title"]))
    if missing:
        raise KeyError(f"Tickers not found in SEC mapping: {missing}")
    return companies
