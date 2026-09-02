from __future__ import annotations
from pathlib import Path
import os
from filingsgraph.core.config import ROOT, get_settings

class ConnectionAdapter:
    def __init__(self, raw, mode: str):
        self.raw = raw
        self.mode = mode
    def execute(self, sql: str, params=None):
        params = params or []
        if self.mode == "duckdb":
            return self.raw.execute(sql, params)
        # SQLAlchemy Connection + psycopg driver; repository SQL uses ? placeholders.
        return self.raw.exec_driver_sql(sql.replace("?", "%s"), tuple(params))
    def close(self):
        self.raw.close()

class Database:
    def __init__(self, path: str | None = None):
        settings = get_settings()
        self.mode = settings.database_mode.lower()
        self.engine = None
        if self.mode == "postgres":
            try:
                from sqlalchemy import create_engine
            except ModuleNotFoundError as e:
                raise RuntimeError('PostgreSQL mode requires: pip install -e ".[postgres]"') from e
            url = os.getenv("POSTGRES_URL", "postgresql+psycopg://filingsgraph:filingsgraph@localhost:5432/filingsgraph")
            self.path = url
            self.engine = create_engine(url, pool_pre_ping=True)
            self.conn = ConnectionAdapter(self.engine.connect(), "postgres")
        else:
            try:
                import duckdb
            except ModuleNotFoundError as e:
                raise RuntimeError("DuckDB dependency is missing. Install the project dependencies first.") from e
            raw_path = path or settings.database_url
            db_path = Path(raw_path)
            if not db_path.is_absolute():
                db_path = ROOT / db_path
            db_path.parent.mkdir(parents=True, exist_ok=True)
            self.path = str(db_path)
            self.conn = ConnectionAdapter(duckdb.connect(self.path), "duckdb")

    def close(self):
        self.conn.close()
        if self.engine is not None:
            self.engine.dispose()

    def initialize(self) -> None:
        self.conn.execute(
            """
        CREATE TABLE IF NOT EXISTS companies(
          cik VARCHAR PRIMARY KEY, ticker VARCHAR, company_name VARCHAR, sec_entity_name VARCHAR,
          industry VARCHAR, sic VARCHAR, fiscal_year_end VARCHAR
        );
        CREATE TABLE IF NOT EXISTS filings(
          accession_number VARCHAR PRIMARY KEY, cik VARCHAR, ticker VARCHAR, company_name VARCHAR,
          form_type VARCHAR, filing_date VARCHAR, report_date VARCHAR, fiscal_year INTEGER,
          fiscal_period VARCHAR, primary_document VARCHAR, source_url VARCHAR, local_path VARCHAR
        );
        CREATE TABLE IF NOT EXISTS filing_sections(
          section_id VARCHAR PRIMARY KEY, document_id VARCHAR, section VARCHAR, title VARCHAR, text VARCHAR, html_location VARCHAR
        );
        CREATE TABLE IF NOT EXISTS facts(
          fact_id VARCHAR PRIMARY KEY, cik VARCHAR, ticker VARCHAR, concept VARCHAR, label VARCHAR, taxonomy VARCHAR,
          unit VARCHAR, raw_value DOUBLE PRECISION, scale DOUBLE PRECISION, normalized_value DOUBLE PRECISION,
          start_date VARCHAR, end_date VARCHAR, instant_date VARCHAR, fiscal_year INTEGER, fiscal_period VARCHAR,
          form_type VARCHAR, accession_number VARCHAR, filed_date VARCHAR, frame VARCHAR, normalized_metric VARCHAR,
          mapping_method VARCHAR, mapping_confidence DOUBLE PRECISION
        );
        """
        )
