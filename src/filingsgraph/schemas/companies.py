from pydantic import BaseModel, Field

class Company(BaseModel):
    company_name: str
    ticker: str
    cik: str = Field(pattern=r"^\d{10}$")
    sec_entity_name: str | None = None
    industry: str | None = None
    sic: str | None = None
    fiscal_year_end: str | None = None
