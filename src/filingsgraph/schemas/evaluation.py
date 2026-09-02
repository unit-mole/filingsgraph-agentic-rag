from pydantic import BaseModel, Field

class EvaluationQuestion(BaseModel):
    id: str
    split: str
    category: str
    question: str
    expected_company: str | None = None
    expected_filing: str | None = None
    expected_section: str | None = None
    relevant_chunk_ids: list[str] = Field(default_factory=list)
    expected_answer: str | None = None
    expected_value: float | None = None
    expected_unit: str | None = None
    expected_periods: list[int] = Field(default_factory=list)
    expected_entities: list[str] = Field(default_factory=list)
    expected_paths: list[list[str]] = Field(default_factory=list)
    metadata: dict = Field(default_factory=dict)
