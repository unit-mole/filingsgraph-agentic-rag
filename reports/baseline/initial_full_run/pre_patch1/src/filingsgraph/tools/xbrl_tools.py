from __future__ import annotations
from filingsgraph.database.repositories import Repository
from filingsgraph.finance.comparisons import compare_period_values

def get_metric_history(repo:Repository,ticker:str,metric:str)->list[dict]: return repo.metric_history(ticker,metric)
def get_company_fact(repo:Repository,ticker:str,metric:str,fiscal_year:int)->dict|None:
    rows=[r for r in repo.metric_history(ticker,metric) if r['fiscal_year']==fiscal_year]
    return rows[-1] if rows else None
def compare_periods(repo:Repository,ticker:str,metric:str,old_year:int,new_year:int)->dict:
    a=get_company_fact(repo,ticker,metric,old_year); b=get_company_fact(repo,ticker,metric,new_year)
    if not a or not b: raise LookupError('Required XBRL facts not found')
    return compare_period_values(a,b)
def get_segment_facts(repo:Repository,ticker:str,metric:str)->list[dict]:
    # SEC Company Facts does not consistently expose dimensional segment contexts; core path returns available facts.
    return repo.metric_history(ticker,metric)
