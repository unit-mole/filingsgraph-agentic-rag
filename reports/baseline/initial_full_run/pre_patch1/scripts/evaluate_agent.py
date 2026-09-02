from __future__ import annotations
import json
from filingsgraph.agents.router import classify_query
from scripts._common import load_jsonl,save_json
MAP={'textual_lookup':'TEXTUAL','exact_financial_fact':'NUMERIC','temporal':'TEMPORAL','graph':'GRAPH','mixed':'MIXED'}
def main():
    qs=load_jsonl('data/evaluation/test/questions.jsonl');rows=[]
    for q in qs:
        if q['category'] not in MAP:continue
        pred=classify_query(q['question']);gold=MAP[q['category']];rows.append({'id':q['id'],'gold':gold,'pred':pred,'ok':gold==pred})
    report={'questions':len(rows),'routing_accuracy':sum(r['ok'] for r in rows)/len(rows) if rows else None,'rows':rows};save_json('reports/experiments/test_agent_routing.json',report);print(json.dumps({k:v for k,v in report.items() if k!='rows'},indent=2))
if __name__=='__main__':main()
