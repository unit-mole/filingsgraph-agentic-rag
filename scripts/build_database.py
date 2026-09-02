from __future__ import annotations
from pathlib import Path
from filingsgraph.core.config import ROOT
from filingsgraph.database.session import Database
from filingsgraph.database.repositories import Repository
from filingsgraph.schemas.companies import Company
from filingsgraph.schemas.filings import FilingMetadata
from filingsgraph.schemas.documents import FilingSection
from filingsgraph.xbrl.facts import parse_companyfacts
from scripts._common import load_json,load_jsonl,save_json

def main():
    db=Database();db.initialize();repo=Repository(db); companies=[Company(**x) for x in (load_json('data/processed/companies.json') or [])];filings=[FilingMetadata(**x) for x in (load_json('data/processed/filings_metadata.json') or [])]
    for c in companies:repo.upsert_company(c)
    for f in filings:repo.upsert_filing(f)
    for s in load_jsonl('data/processed/sections.jsonl'):repo.upsert_section(FilingSection(**s))
    fact_count=0; by_ticker={}
    report_date_to_fy={(f.ticker, f.report_date): f.fiscal_year for f in filings if f.report_date and f.fiscal_year}
    for c in companies:
        p=ROOT/'data/raw/xbrl'/f'{c.ticker}_companyfacts.json'
        if not p.exists():continue
        facts=parse_companyfacts(p,c.ticker)
        for fact in facts:
            # Stronger fiscal normalization for the bounded 10-K corpus: exact fact end dates
            # that match downloaded annual report dates inherit that filing's fiscal year.
            if fact.end_date and (c.ticker, fact.end_date) in report_date_to_fy:
                fact.fiscal_year=report_date_to_fy[(c.ticker, fact.end_date)]
                if fact.form_type=='10-K': fact.fiscal_period='FY'
            repo.upsert_fact(fact);fact_count+=1
        by_ticker[c.ticker]=len(facts)
    report={'companies':len(companies),'filings':len(filings),'facts':fact_count,'facts_by_ticker':by_ticker,'database':db.path};save_json('reports/final/xbrl_normalization_report.json',report);print(report);db.close()
if __name__=='__main__': main()
