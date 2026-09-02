from __future__ import annotations
import json
from filingsgraph.database.session import Database
from scripts._common import load_jsonl,save_json

def main():
    qs=[q for q in load_jsonl('data/evaluation/test/questions.jsonl') if q['category']=='exact_financial_fact'];db=Database();rows=[]
    for q in qs:
        m=q.get('metadata',{}).get('metric');t=q.get('expected_company');y=q.get('expected_periods',[None])[0]
        got=db.conn.execute("SELECT normalized_value,unit FROM facts WHERE upper(ticker)=upper(?) AND normalized_metric=? AND fiscal_year=? AND form_type='10-K' ORDER BY filed_date DESC LIMIT 1",[t,m,y]).fetchone();ok=bool(got) and float(got[0])==float(q['expected_value']) and got[1]==q['expected_unit'];rows.append({'id':q['id'],'ok':ok,'predicted':got[0] if got else None,'expected':q['expected_value'],'unit_ok':bool(got) and got[1]==q['expected_unit']})
    db.close();report={'questions':len(rows),'fact_selection_accuracy':sum(r['ok'] for r in rows)/len(rows) if rows else None,'unit_accuracy':sum(r['unit_ok'] for r in rows)/len(rows) if rows else None,'calculation_exact_match':'evaluated separately by deterministic unit tests','rows':rows};save_json('reports/experiments/test_financial.json',report);print(json.dumps({k:v for k,v in report.items() if k!='rows'},indent=2))
if __name__=='__main__':main()
