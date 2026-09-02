from pydantic import BaseModel, Field

class EvidenceItem(BaseModel):
    citation_id: str
    evidence_type: str
    company: str | None = None
    ticker: str | None = None
    fiscal_year: int | None = None
    filing: str | None = None
    section: str | None = None
    source_url: str | None = None
    source_excerpt: str | None = None
    retrieval_method: str | None = None
    score: float | None = None
    payload: dict = Field(default_factory=dict)

class CalculationEvidence(BaseModel):
    calculation_id: str
    function: str
    inputs: dict
    output: float
    unit: str | None = None
    source_fact_ids: list[str] = Field(default_factory=list)
