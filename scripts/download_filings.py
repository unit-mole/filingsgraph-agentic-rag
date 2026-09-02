from __future__ import annotations
import argparse
from filingsgraph.schemas.companies import Company
from filingsgraph.sec.filings import list_filings,download_filing
from filingsgraph.sec.client import SECClient
from filingsgraph.core.config import load_yaml
from scripts._common import load_json,save_json

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--force',action='store_true');args=ap.parse_args()
    companies=[Company(**x) for x in (load_json('data/processed/companies.json') or [])]
    if not companies: raise RuntimeError('Run python -m scripts.resolve_companies first')
    cfg=load_yaml('companies.yaml')['filing_scope']; forms=set(cfg.get('forms',['10-K'])); limit=int(cfg.get('annual_filings_per_company',4)); client=SECClient(); out=[]
    for c in companies:
        metas=list_filings(c,forms=forms,limit=limit,client=client)
        for m in metas: out.append(download_filing(m,client=client,force=args.force).model_dump())
        print(f'{c.ticker}: {len(metas)} filings')
    p=save_json('data/processed/filings_metadata.json',out); print(f'Downloaded/cached {len(out)} filings -> {p}')
if __name__=='__main__': main()
