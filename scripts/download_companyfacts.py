from __future__ import annotations
import argparse
from filingsgraph.schemas.companies import Company
from filingsgraph.sec.companyfacts import download_companyfacts
from filingsgraph.sec.client import SECClient
from scripts._common import load_json

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--force',action='store_true');args=ap.parse_args(); companies=[Company(**x) for x in (load_json('data/processed/companies.json') or [])]
    if not companies: raise RuntimeError('Run resolve_companies first')
    client=SECClient()
    for c in companies:
        p=download_companyfacts(c.cik,c.ticker,client,args.force);print(f'{c.ticker} -> {p}')
if __name__=='__main__': main()
