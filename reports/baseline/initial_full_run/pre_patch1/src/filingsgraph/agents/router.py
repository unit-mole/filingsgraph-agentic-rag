from __future__ import annotations
import re
NUMERIC_TERMS={'revenue','margin','growth','income','capex','cash','assets','liabilities','percentage','percent','cagr'}
TEMPORAL_TERMS={'changed','change','evolved','evolution','over time','between','last three','year over year','risk language'}
GRAPH_TERMS={'connected','relationship','shared risk','which segments','graph','multi-hop','subsidiar','supplier','competitor'}
MULTI_TERMS={'companies','compare companies','across these','cohort','versus',' vs '}

def classify_query(question:str)->str:
    q=question.lower(); numeric=any(t in q for t in NUMERIC_TERMS); temporal=any(t in q for t in TEMPORAL_TERMS); graph=any(t in q for t in GRAPH_TERMS); multi=any(t in q for t in MULTI_TERMS)
    flags=sum([numeric,temporal,graph,multi])
    if flags>=2: return 'MIXED'
    if graph: return 'GRAPH'
    if temporal: return 'TEMPORAL'
    if numeric: return 'NUMERIC'
    if multi: return 'MULTI_COMPANY'
    return 'TEXTUAL'

def extract_tickers(question:str,known:list[str])->list[str]:
    up=question.upper(); return [t for t in known if re.search(rf'\b{re.escape(t)}\b',up)]
