from pydantic import BaseModel

class FinancialFact(BaseModel):
    cik: str
    ticker: str | None = None
    concept: str
    label: str | None = None
    taxonomy: str = "us-gaap"
    unit: str
    raw_value: float
    scale: float = 1.0
    normalized_value: float
    start_date: str | None = None
    end_date: str | None = None
    instant_date: str | None = None
    fiscal_year: int | None = None
    fiscal_period: str | None = None
    form_type: str | None = None
    accession_number: str | None = None
    filed_date: str | None = None
    frame: str | None = None
    segment_context: dict | None = None
    normalized_metric: str | None = None
    mapping_method: str = "raw"
    mapping_confidence: float = 1.0
