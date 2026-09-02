from __future__ import annotations
import json
from filingsgraph.core.config import load_yaml
from filingsgraph.temporal.risk_diff import compare_risk_disclosures
from scripts._common import load_jsonl,save_json

def main():
    chunks=load_jsonl('data/processed/chunks.jsonl');topics=load_yaml('graph.yaml')['risk_topics'];groups={}
    for c in chunks:
        if c.get('section')=='Item 1A' and c.get('fiscal_year'):groups.setdefault(c['ticker'],{}).setdefault(c['fiscal_year'],[]).append(c['text'])
    rows=[]
    for t,years in groups.items():
        ys=sorted(years)
        for a,b in zip(ys,ys[1:]):
            changes=compare_risk_disclosures(' '.join(years[a]),' '.join(years[b]),topics);rows.append({'ticker':t,'from':a,'to':b,'changes':changes})
    report={'comparisons':len(rows),'risk_change_f1':None,'note':'Automated extraction outputs are produced here; F1 remains TBD until the generated labels are human-reviewed/frozen.','rows':rows};save_json('reports/temporal/temporal_evaluation.json',report);print(json.dumps({k:v for k,v in report.items() if k!='rows'},indent=2))
if __name__=='__main__':main()
