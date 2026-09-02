from pydantic import BaseModel

class FilingMetadata(BaseModel):
    cik: str
    ticker: str
    company_name: str
    form_type: str
    accession_number: str
    filing_date: str
    report_date: str | None = None
    fiscal_year: int | None = None
    fiscal_period: str | None = None
    primary_document: str
    source_url: str
    local_path: str | None = None
