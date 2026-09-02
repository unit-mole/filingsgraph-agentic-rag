"""Logical table definitions used by the DuckDB/PostgreSQL storage layer."""
TABLES = {
    "companies": ["cik", "ticker", "company_name", "sec_entity_name", "industry", "sic", "fiscal_year_end"],
    "filings": ["accession_number", "cik", "ticker", "company_name", "form_type", "filing_date", "report_date", "fiscal_year", "fiscal_period", "primary_document", "source_url", "local_path"],
    "filing_sections": ["section_id", "document_id", "section", "title", "text", "html_location"],
    "facts": ["fact_id", "cik", "ticker", "concept", "label", "taxonomy", "unit", "raw_value", "scale", "normalized_value", "start_date", "end_date", "instant_date", "fiscal_year", "fiscal_period", "form_type", "accession_number", "filed_date", "frame", "normalized_metric", "mapping_method", "mapping_confidence"],
}
