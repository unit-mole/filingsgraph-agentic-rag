from pydantic import BaseModel, Field

class FilingSection(BaseModel):
    section_id: str
    document_id: str
    section: str
    title: str | None = None
    text: str
    html_location: str | None = None

class DocumentChunk(BaseModel):
    chunk_id: str
    document_id: str
    cik: str
    ticker: str
    company_name: str
    form_type: str
    accession_number: str
    filing_date: str
    report_date: str | None = None
    fiscal_year: int | None = None
    fiscal_period: str | None = None
    section: str
    subsection: str | None = None
    page_or_html_location: str | None = None
    source_url: str
    content_hash: str
    version: str = "1"
    text: str
    parent_text: str | None = None
    entity_ids: list[str] = Field(default_factory=list)
    risk_ids: list[str] = Field(default_factory=list)
    segment_ids: list[str] = Field(default_factory=list)
    metric_ids: list[str] = Field(default_factory=list)
