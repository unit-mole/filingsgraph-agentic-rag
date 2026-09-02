from __future__ import annotations

def sort_filings_by_period(filings:list[dict])->list[dict]:
    return sorted(filings,key=lambda x:(x.get('fiscal_year') or 0,x.get('filing_date') or ''))

def validate_period_pair(old_year:int,new_year:int)->None:
    if new_year<=old_year: raise ValueError('new_year must be after old_year')
