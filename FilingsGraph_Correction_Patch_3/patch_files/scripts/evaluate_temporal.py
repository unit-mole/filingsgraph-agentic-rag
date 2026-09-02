from __future__ import annotations
import json
from filingsgraph.core.config import load_yaml
from filingsgraph.temporal.risk_diff import compare_risk_disclosures
from scripts._common import load_jsonl,load_json,save_json

def main():
    chunks=load_jsonl('data/processed/chunks.jsonl');topics=load_yaml('graph.yaml')['risk_topics'];groups={}
    for c in chunks:
        if c.get('section')=='Item 1A' and c.get('fiscal_year'):groups.setdefault(c['ticker'],{}).setdefault(c['fiscal_year'],[]).append(c['text'])
    rows=[]
    for t,years in groups.items():
        ys=sorted(years)
        for a,b in zip(ys,ys[1:]):
            changes=compare_risk_disclosures(' '.join(years[a]),' '.join(years[b]),topics);rows.append({'ticker':t,'from':a,'to':b,'changes':changes})
    gold=load_json('reports/temporal/temporal_gold_metrics.json',{}) or {}
    report={'comparisons':len(rows),'risk_change_f1':gold.get('risk_change_f1'),'risk_change_accuracy':gold.get('risk_change_accuracy'),'gold_reviewed_rows':gold.get('reviewed_rows',0),'note':'Gold metrics are populated only from human-reviewed labels; otherwise they remain null.','rows':rows};save_json('reports/temporal/temporal_evaluation.json',report);print(json.dumps({k:v for k,v in report.items() if k!='rows'},indent=2))
if __name__=='__main__':main()
