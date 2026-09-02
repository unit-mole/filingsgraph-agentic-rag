from __future__ import annotations
import re
from filingsgraph.agents.router import classify_query
from filingsgraph.schemas.queries import ResearchPlan

def plan(question:str,tickers:list[str]|None=None,years:list[int]|None=None)->ResearchPlan:
    qt=classify_query(question); tickers=tickers or []; years=years or [int(y) for y in re.findall(r'FY?(20\d{2})',question.upper())]
    return ResearchPlan(
        query_type=qt,entities=tickers,periods=sorted(set(years)),retrieval_queries=[question],
        use_text=qt!='NUMERIC' or any(x in question.lower() for x in ['management','risk','explain','narrative']),
        use_xbrl=qt in {'NUMERIC','MIXED'},use_graph=qt in {'GRAPH','MIXED'},use_temporal=qt in {'TEMPORAL','MIXED'},use_macro=qt=='MACRO'
    )
