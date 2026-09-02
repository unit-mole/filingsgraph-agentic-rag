from __future__ import annotations
import hashlib
from filingsgraph.database.session import Database
from filingsgraph.schemas.companies import Company
from filingsgraph.schemas.filings import FilingMetadata
from filingsgraph.schemas.documents import FilingSection
from filingsgraph.schemas.financial_facts import FinancialFact

class Repository:
    def __init__(self, db: Database): self.db=db

    def upsert_company(self, c: Company) -> None:
        self.db.conn.execute("DELETE FROM companies WHERE cik=?", [c.cik])
        self.db.conn.execute("INSERT INTO companies VALUES (?,?,?,?,?,?,?)", [c.cik,c.ticker,c.company_name,c.sec_entity_name,c.industry,c.sic,c.fiscal_year_end])

    def upsert_filing(self, f: FilingMetadata) -> None:
        self.db.conn.execute("DELETE FROM filings WHERE accession_number=?", [f.accession_number])
        self.db.conn.execute("INSERT INTO filings VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", [f.accession_number,f.cik,f.ticker,f.company_name,f.form_type,f.filing_date,f.report_date,f.fiscal_year,f.fiscal_period,f.primary_document,f.source_url,f.local_path])

    def upsert_section(self, s: FilingSection) -> None:
        self.db.conn.execute("DELETE FROM filing_sections WHERE section_id=?", [s.section_id])
        self.db.conn.execute("INSERT INTO filing_sections VALUES (?,?,?,?,?,?)", [s.section_id,s.document_id,s.section,s.title,s.text,s.html_location])

    def upsert_fact(self, f: FinancialFact) -> str:
        fid=hashlib.sha1(f"{f.cik}|{f.concept}|{f.unit}|{f.end_date}|{f.fiscal_year}|{f.accession_number}|{f.normalized_value}".encode()).hexdigest()[:24]
        self.db.conn.execute("DELETE FROM facts WHERE fact_id=?", [fid])
        self.db.conn.execute("INSERT INTO facts VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", [
            fid,f.cik,f.ticker,f.concept,f.label,f.taxonomy,f.unit,f.raw_value,f.scale,f.normalized_value,
            f.start_date,f.end_date,f.instant_date,f.fiscal_year,f.fiscal_period,f.form_type,f.accession_number,
            f.filed_date,f.frame,f.normalized_metric,f.mapping_method,f.mapping_confidence
        ])
        return fid

    def metric_history(self, ticker: str, metric: str) -> list[dict]:
        rows=self.db.conn.execute("""
          SELECT fact_id,ticker,normalized_metric,unit,normalized_value,fiscal_year,fiscal_period,accession_number,filed_date
          FROM (
            SELECT *, ROW_NUMBER() OVER (PARTITION BY fiscal_year ORDER BY mapping_confidence DESC, filed_date DESC, end_date DESC) AS rn
            FROM facts
            WHERE upper(ticker)=upper(?) AND normalized_metric=? AND form_type='10-K' AND fiscal_year IS NOT NULL
          )
          WHERE rn=1
          ORDER BY fiscal_year
        """, [ticker,metric]).fetchall()
        cols=["fact_id","ticker","metric","unit","value","fiscal_year","fiscal_period","accession_number","filed_date"]
        return [dict(zip(cols,r)) for r in rows]

    def companies(self) -> list[dict]:
        rows=self.db.conn.execute("SELECT cik,ticker,company_name FROM companies ORDER BY ticker").fetchall()
        return [{"cik":r[0],"ticker":r[1],"company_name":r[2]} for r in rows]
