from __future__ import annotations

from collections import Counter

from filingsgraph.core.config import ROOT, load_yaml
from filingsgraph.schemas.filings import FilingMetadata
from filingsgraph.parsing.sections import extract_sections
from filingsgraph.parsing.chunking import section_aware_chunks
from filingsgraph.parsing.tables import extract_tables
from scripts._common import load_json, save_jsonl, save_json


def main():
    metas = [FilingMetadata(**x) for x in (load_json("data/processed/filings_metadata.json") or [])]
    if not metas:
        raise RuntimeError("No filing metadata. Run download_filings first.")
    targets = load_yaml("companies.yaml").get("sections")
    chunks = []
    sections = []
    tables_all = []
    table_manifest = []
    failures = []
    coverage = []

    for m in metas:
        try:
            html = (ROOT / m.local_path).read_text(encoding="utf-8", errors="replace")
            docid = m.accession_number
            secs = extract_sections(html, docid, targets)
            found = sorted({s.section for s in secs})
            coverage.append(
                {
                    "ticker": m.ticker,
                    "accession": docid,
                    "fiscal_year": m.fiscal_year,
                    "sections_found": found,
                    "section_count": len(found),
                }
            )
            if not secs:
                failures.append({"ticker": m.ticker, "accession": docid, "reason": "no target sections extracted"})
            sections.extend([{**s.model_dump(), "_ticker": m.ticker} for s in secs])
            for s in secs:
                chunks.extend([c.model_dump() for c in section_aware_chunks(s, m)])
            tables = extract_tables(html)
            for t in tables:
                t.update(
                    {
                        "accession_number": docid,
                        "ticker": m.ticker,
                        "fiscal_year": m.fiscal_year,
                        "source_url": m.source_url,
                    }
                )
                tables_all.append(t)
            table_manifest.append({"accession": docid, "ticker": m.ticker, "table_count": len(tables)})
        except Exception as e:
            failures.append({"ticker": m.ticker, "accession": m.accession_number, "reason": str(e)})

    # Strip reporting-only helper before serializing the schema-compatible file.
    clean_sections = []
    for s in sections:
        x = dict(s)
        x.pop("_ticker", None)
        clean_sections.append(x)

    save_jsonl("data/processed/sections.jsonl", clean_sections)
    save_jsonl("data/processed/chunks.jsonl", chunks)
    save_jsonl("data/processed/tables.jsonl", tables_all)
    save_json("data/processed/table_manifest.json", table_manifest)

    chunks_by_ticker = dict(Counter(c.get("ticker") for c in chunks))
    filings_with_sections = sum(1 for x in coverage if x["section_count"] > 0)
    report = {
        "filings": len(metas),
        "filings_with_target_sections": filings_with_sections,
        "filing_coverage_rate": filings_with_sections / len(metas) if metas else None,
        "sections": len(clean_sections),
        "chunks": len(chunks),
        "chunks_by_ticker": chunks_by_ticker,
        "tables": len(tables_all),
        "coverage": coverage,
        "failures": failures,
    }
    save_json("reports/final/parsing_report.json", report)
    print({k: v for k, v in report.items() if k != "coverage"})
    if not chunks:
        raise SystemExit("No chunks were built; inspect parsing_report.json")


if __name__ == "__main__":
    main()
