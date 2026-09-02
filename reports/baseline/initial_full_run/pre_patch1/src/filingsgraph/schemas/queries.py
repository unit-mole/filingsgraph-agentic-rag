from pydantic import BaseModel, Field

class ResearchRequest(BaseModel):
    question: str = Field(min_length=3, max_length=5000)
    tickers: list[str] = Field(default_factory=list, max_length=8)
    fiscal_years: list[int] = Field(default_factory=list, max_length=8)
    mode: str | None = None

class ResearchPlan(BaseModel):
    query_type: str
    entities: list[str] = Field(default_factory=list)
    periods: list[int] = Field(default_factory=list)
    retrieval_queries: list[str] = Field(default_factory=list)
    use_text: bool = True
    use_xbrl: bool = False
    use_graph: bool = False
    use_temporal: bool = False
    use_macro: bool = False

class ResearchResponse(BaseModel):
    query_id: str
    question: str
    query_type: str
    plan: ResearchPlan
    answer: str
    evidence: list[dict] = Field(default_factory=list)
    calculations: list[dict] = Field(default_factory=list)
    contradictions: list[str] = Field(default_factory=list)
    verification: dict = Field(default_factory=dict)
    limitations: list[str] = Field(default_factory=list)
