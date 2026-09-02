from filingsgraph.core.config import load_yaml
from filingsgraph.sec.companies import resolve_tickers
from scripts._common import save_json

def main():
    cfg=load_yaml('companies.yaml'); tickers=[x['ticker'] for x in cfg['companies']]; companies=resolve_tickers(tickers)
    path=save_json('data/processed/companies.json',[c.model_dump() for c in companies]); print(f'Resolved {len(companies)} companies -> {path}')
if __name__=='__main__': main()
