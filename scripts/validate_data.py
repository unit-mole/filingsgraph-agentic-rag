from __future__ import annotations
from pathlib import Path
from filingsgraph.core.config import ROOT,load_yaml
from scripts._common import load_json,save_json

def main():
    companies=load_json('data/processed/companies.json',[]); filings=load_json('data/processed/filings_metadata.json',[]); issues=[]
    expected={c['ticker'] for c in companies}; found={f['ticker'] for f in filings}
    for t in expected-found: issues.append(f'No filing metadata for {t}')
    for f in filings:
        p=ROOT/f['local_path'] if f.get('local_path') else None
        if not p or not p.exists() or p.stat().st_size<1000: issues.append(f"Missing/small filing: {f.get('ticker')} {f.get('accession_number')}")
    for c in companies:
        p=ROOT/'data/raw/xbrl'/f"{c['ticker']}_companyfacts.json"
        if not p.exists() or p.stat().st_size<1000: issues.append(f"Missing Company Facts: {c['ticker']}")
    report={"companies":len(companies),"filings":len(filings),"xbrl_files":sum((ROOT/'data/raw/xbrl'/f"{c['ticker']}_companyfacts.json").exists() for c in companies),"issues":issues,"ok":not issues}
    save_json('reports/final/data_quality.json',report);print(report)
    if issues: raise SystemExit(2)
if __name__=='__main__': main()
