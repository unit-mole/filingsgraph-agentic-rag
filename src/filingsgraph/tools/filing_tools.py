from __future__ import annotations

def search_filing_sections(retriever,query:str,ticker:str|None=None,fiscal_year:int|None=None,top_k:int=8)->list[dict]:
    filters={}
    if ticker: filters['ticker']=ticker.upper()
    if fiscal_year: filters['fiscal_year']=fiscal_year
    return retriever.search(query,filters=filters or None,fusion_top_k=top_k)

def get_filing_section(chunks:list[dict],ticker:str,year:int,section:str)->list[dict]:
    return [c for c in chunks if c.get('ticker')==ticker.upper() and c.get('fiscal_year')==year and c.get('section','').lower()==section.lower()]

def compare_filing_sections(chunks:list[dict],ticker:str,years:list[int],section:str)->dict:
    return {y:get_filing_section(chunks,ticker,y,section) for y in years}
