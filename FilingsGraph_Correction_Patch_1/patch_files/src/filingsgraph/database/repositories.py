from __future__ import annotations

import hashlib
from collections import defaultdict

from filingsgraph.database.session import Database
from filingsgraph.schemas.companies import Company
from filingsgraph.schemas.filings import FilingMetadata
from filingsgraph.schemas.documents import FilingSection
from filingsgraph.schemas.financial_facts import FinancialFact
from filingsgraph.xbrl.facts import choose_annual_fact


class Repository:
    def __init__(self, db: Database):
        self.db = db

    def upsert_company(self, c: Company) -> None:
        self.db.conn.execute("DELETE FROM companies WHERE cik=?", [c.cik])
        self.db.conn.execute(
            "INSERT INTO companies VALUES (?,?,?,?,?,?,?)",
            [c.cik, c.ticker, c.company_name, c.sec_entity_name, c.industry, c.sic, c.fiscal_year_end],
        )

    def upsert_filing(self, f: FilingMetadata) -> None:
        self.db.conn.execute("DELETE FROM filings WHERE accession_number=?", [f.accession_number])
        self.db.conn.execute(
            "INSERT INTO filings VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            [
                f.accession_number,
                f.cik,
                f.ticker,
                f.company_name,
                f.form_type,
                f.filing_date,
                f.report_date,
                f.fiscal_year,
                f.fiscal_period,
                f.primary_document,
                f.source_url,
                f.local_path,
            ],
        )

    def upsert_section(self, s: FilingSection) -> None:
        self.db.conn.execute("DELETE FROM filing_sections WHERE section_id=?", [s.section_id])
        self.db.conn.execute(
            "INSERT INTO filing_sections VALUES (?,?,?,?,?,?)",
            [s.section_id, s.document_id, s.section, s.title, s.text, s.html_location],
        )

    def upsert_fact(self, f: FinancialFact) -> str:
        fid = hashlib.sha1(
            f"{f.cik}|{f.concept}|{f.unit}|{f.end_date}|{f.fiscal_year}|{f.accession_number}|{f.normalized_value}".encode()
        ).hexdigest()[:24]
        self.db.conn.execute("DELETE FROM facts WHERE fact_id=?", [fid])
        self.db.conn.execute(
            "INSERT INTO facts VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            [
                fid,
                f.cik,
                f.ticker,
                f.concept,
                f.label,
                f.taxonomy,
                f.unit,
                f.raw_value,
                f.scale,
                f.normalized_value,
                f.start_date,
                f.end_date,
                f.instant_date,
                f.fiscal_year,
                f.fiscal_period,
                f.form_type,
                f.accession_number,
                f.filed_date,
                f.frame,
                f.normalized_metric,
                f.mapping_method,
                f.mapping_confidence,
            ],
        )
        return fid

    def _candidate_annual_facts(self, ticker: str, metric: str) -> list[tuple[FinancialFact, dict]]:
        rows = self.db.conn.execute(
            """
            SELECT
              f.cik,f.ticker,f.concept,f.label,f.taxonomy,f.unit,f.raw_value,f.scale,f.normalized_value,
              f.start_date,f.end_date,f.instant_date,f.fiscal_year,f.fiscal_period,f.form_type,
              f.accession_number,f.filed_date,f.frame,f.normalized_metric,f.mapping_method,f.mapping_confidence,
              fl.accession_number AS target_accession, fl.report_date AS target_report_date,
              fl.fiscal_year AS target_fiscal_year
            FROM facts f
            JOIN filings fl
              ON upper(f.ticker)=upper(fl.ticker)
             AND fl.form_type='10-K'
             AND f.form_type='10-K'
             AND f.end_date=fl.report_date
            WHERE upper(f.ticker)=upper(?)
              AND f.normalized_metric=?
              AND fl.fiscal_year IS NOT NULL
            ORDER BY fl.fiscal_year
            """,
            [ticker, metric],
        ).fetchall()
        out: list[tuple[FinancialFact, dict]] = []
        for r in rows:
            fact = FinancialFact(
                cik=r[0], ticker=r[1], concept=r[2], label=r[3], taxonomy=r[4], unit=r[5],
                raw_value=r[6], scale=r[7], normalized_value=r[8], start_date=r[9], end_date=r[10],
                instant_date=r[11], fiscal_year=r[12], fiscal_period=r[13], form_type=r[14],
                accession_number=r[15], filed_date=r[16], frame=r[17], normalized_metric=r[18],
                mapping_method=r[19], mapping_confidence=r[20],
            )
            out.append(
                (
                    fact,
                    {
                        "target_accession": r[21],
                        "target_report_date": r[22],
                        "target_fiscal_year": r[23],
                    },
                )
            )
        return out

    def metric_history(self, ticker: str, metric: str) -> list[dict]:
        grouped: dict[int, list[tuple[FinancialFact, dict]]] = defaultdict(list)
        for fact, meta in self._candidate_annual_facts(ticker, metric):
            grouped[int(meta["target_fiscal_year"])].append((fact, meta))

        rows: list[dict] = []
        for fiscal_year in sorted(grouped):
            group = grouped[fiscal_year]
            # Normalize candidates to the filing's fiscal year before applying
            # the provenance-aware selector.
            normalized: list[FinancialFact] = []
            meta_by_key: dict[int, dict] = {}
            for i, (fact, meta) in enumerate(group):
                fact = fact.model_copy(update={"fiscal_year": fiscal_year, "fiscal_period": "FY"})
                normalized.append(fact)
                meta_by_key[i] = meta

            # All candidates in a group share the same target filing metadata.
            target = group[0][1]
            selected = choose_annual_fact(
                normalized,
                metric,
                fiscal_year,
                target_accession=target["target_accession"],
                target_report_date=target["target_report_date"],
            )
            if selected is None:
                continue
            fid_row = self.db.conn.execute(
                """
                SELECT fact_id FROM facts
                WHERE upper(ticker)=upper(?) AND normalized_metric=? AND concept=? AND unit=?
                  AND end_date=? AND accession_number=? AND normalized_value=?
                LIMIT 1
                """,
                [
                    ticker,
                    metric,
                    selected.concept,
                    selected.unit,
                    selected.end_date,
                    selected.accession_number,
                    selected.normalized_value,
                ],
            ).fetchone()
            rows.append(
                {
                    "fact_id": fid_row[0] if fid_row else None,
                    "ticker": ticker,
                    "metric": metric,
                    "unit": selected.unit,
                    "value": selected.normalized_value,
                    "fiscal_year": fiscal_year,
                    "fiscal_period": "FY",
                    "accession_number": selected.accession_number,
                    "filed_date": selected.filed_date,
                    "end_date": selected.end_date,
                    "concept": selected.concept,
                    "target_accession": target["target_accession"],
                }
            )
        return rows

    def companies(self) -> list[dict]:
        rows = self.db.conn.execute("SELECT cik,ticker,company_name FROM companies ORDER BY ticker").fetchall()
        return [{"cik": r[0], "ticker": r[1], "company_name": r[2]} for r in rows]
