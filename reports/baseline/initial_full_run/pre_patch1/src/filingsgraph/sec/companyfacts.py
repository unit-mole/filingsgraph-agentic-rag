from __future__ import annotations
from pathlib import Path
from filingsgraph.core.config import ROOT
from filingsgraph.sec.client import SECClient

def companyfacts_url(cik: str) -> str:
    return f"https://data.sec.gov/api/xbrl/companyfacts/CIK{str(cik).zfill(10)}.json"

def download_companyfacts(cik: str, ticker: str, client: SECClient | None = None, force: bool = False) -> Path:
    client = client or SECClient()
    data = client.get_bytes(companyfacts_url(cik), force=force)
    dest = ROOT / "data" / "raw" / "xbrl" / f"{ticker.upper()}_companyfacts.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return dest
