from __future__ import annotations
import json,shutil
from filingsgraph.core.config import ROOT
from scripts._common import load_jsonl

def main():
    dest=ROOT/'deploy/huggingface/demo_data'; dest.mkdir(parents=True,exist_ok=True)
    chunks=load_jsonl('data/processed/chunks.jsonl'); tickers=['NVDA','AMD','INTC']
    years=sorted({c.get('fiscal_year') for c in chunks if c.get('fiscal_year')},reverse=True)[:3]
    subset=[c for c in chunks if c.get('ticker') in tickers and c.get('fiscal_year') in years]
    (dest/'chunks.jsonl').write_text(''.join(json.dumps(c)+'\n' for c in subset),encoding='utf-8')
    for src,name in [(ROOT/'data/processed/filingsgraph.duckdb','filingsgraph.duckdb'),(ROOT/'data/graph/filingsgraph.json','filingsgraph.json'),(ROOT/'reports/final/summary.json','summary.json')]:
        if src.exists(): shutil.copy2(src,dest/name)
    print({'chunks':len(subset),'tickers':tickers,'years':years,'destination':str(dest)})
if __name__=='__main__': main()
