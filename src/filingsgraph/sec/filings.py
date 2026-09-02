from __future__ import annotations
from pathlib import Path
import json
from filingsgraph.core.config import ROOT
from filingsgraph.schemas.companies import Company
from filingsgraph.schemas.filings import FilingMetadata
from filingsgraph.sec.client import SECClient
from filingsgraph.sec.submissions import get_submissions


def accession_compact(accession: str) -> str:
    return accession.replace("-", "")

def filing_document_url(cik: str, accession: str, primary_document: str) -> str:
    return f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession_compact(accession)}/{primary_document}"

def list_filings(company: Company, forms: set[str] | None = None, limit: int = 4, client: SECClient | None = None) -> list[FilingMetadata]:
    forms = forms or {"10-K"}
    data = get_submissions(company.cik, client=client)
    recent = data.get("filings", {}).get("recent", {})
    keys = ["accessionNumber", "filingDate", "reportDate", "form", "primaryDocument"]
    rows = [dict(zip(keys, vals)) for vals in zip(*(recent.get(k, []) for k in keys))]
    out = []
    for row in rows:
        form = row["form"]
        if form not in forms:
            continue
        report = row.get("reportDate") or None
        fy = int(report[:4]) if report and len(report) >= 4 and report[:4].isdigit() else None
        url = filing_document_url(company.cik, row["accessionNumber"], row["primaryDocument"])
        out.append(FilingMetadata(
            cik=company.cik, ticker=company.ticker, company_name=company.company_name,
            form_type=form, accession_number=row["accessionNumber"], filing_date=row["filingDate"],
            report_date=report, fiscal_year=fy, fiscal_period="FY" if form == "10-K" else None,
            primary_document=row["primaryDocument"], source_url=url,
        ))
        if len(out) >= limit:
            break
    return out

def download_filing(meta: FilingMetadata, client: SECClient | None = None, force: bool = False) -> FilingMetadata:
    client = client or SECClient()
    dest = ROOT / "data" / "raw" / "filings" / meta.ticker / meta.accession_number
    dest.mkdir(parents=True, exist_ok=True)
    html_path = dest / meta.primary_document
    if force or not html_path.exists():
        html_path.write_bytes(client.get_bytes(meta.source_url, force=force))
    meta.local_path = str(html_path.relative_to(ROOT))
    (dest / "metadata.json").write_text(meta.model_dump_json(indent=2), encoding="utf-8")
    return meta
