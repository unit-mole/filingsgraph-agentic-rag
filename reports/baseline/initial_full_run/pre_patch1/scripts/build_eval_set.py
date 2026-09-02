from __future__ import annotations
import argparse,random,re
from filingsgraph.core.config import ROOT,load_yaml
from filingsgraph.database.session import Database
from scripts._common import load_jsonl,save_jsonl,save_json

def first_query_sentence(text:str)->str:
    s=re.split(r'(?<=[.!?])\s+',text.strip())[0]; return s[:300]

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--force-test",action="store_true");args=ap.parse_args()
    cfg=load_yaml('evaluation.yaml');seed=int(cfg.get('seed',42));random.seed(seed);chunks=load_jsonl('data/processed/chunks.jsonl');questions=[]
    # Text gold: query formed from the chunk's own substantive first sentence.
    for c in chunks:
        if len(c.get('text',''))<100:continue
        questions.append({'id':f"text-{len(questions):04d}",'split':'','category':'textual_lookup','question':first_query_sentence(c['text']),'expected_company':c['ticker'],'expected_filing':c['accession_number'],'expected_section':c['section'],'relevant_chunk_ids':[c['chunk_id']],'expected_periods':[c['fiscal_year']] if c.get('fiscal_year') else []})
        if len(questions)>=120:break
    # Numeric gold directly from normalized DB facts.
    try:
        db=Database();rows=db.conn.execute("SELECT ticker,normalized_metric,unit,normalized_value,fiscal_year,fact_id FROM facts WHERE form_type='10-K' AND normalized_metric IN ('revenue','net_income','operating_income','capex') AND fiscal_year IS NOT NULL ORDER BY ticker,fiscal_year").fetchall();db.close()
        seen=set()
        for t,m,u,v,y,fid in rows:
            key=(t,m,y)
            if key in seen:continue
            seen.add(key);questions.append({'id':f"num-{len(questions):04d}",'split':'','category':'exact_financial_fact','question':f'What was {t} {m.replace("_"," ")} in FY{y}?','expected_company':t,'expected_value':v,'expected_unit':u,'expected_periods':[y],'metadata':{'metric':m,'fact_id':fid}})
            if sum(q['category']=='exact_financial_fact' for q in questions)>=50:break
    except Exception: pass
    # Router/temporal/graph benchmark templates, grounded to project-supported classes; no answer metric is fabricated.
    templates=[
      ('temporal','How did {t} supply-chain risk language change across the selected annual filings?'),
      ('graph','Which business risks are connected to {t} in the temporal knowledge graph?'),
      ('mixed','{t} revenue changed over the period; how did management risk language evolve at the same time?'),
      ('no_answer','What acquisition price did {t} pay for a fictional company that is not present in the selected filings?')]
    tickers=sorted({c['ticker'] for c in chunks})
    for t in tickers:
        for cat,tmp in templates:questions.append({'id':f"{cat}-{len(questions):04d}",'split':'','category':cat,'question':tmp.format(t=t),'expected_company':t})
    random.shuffle(questions);dev_n=min(int(cfg.get('dev_questions',120)),len(questions));test_n=min(int(cfg.get('test_questions',80)),max(0,len(questions)-dev_n));dev=questions[:dev_n];test=questions[dev_n:dev_n+test_n]
    for q in dev:q['split']='dev'
    for q in test:q['split']='test'
    save_jsonl('data/evaluation/dev/questions.jsonl',dev)
    test_path=ROOT/'data/evaluation/test/questions.jsonl'
    if test_path.exists() and not args.force_test:
        existing=load_jsonl('data/evaluation/test/questions.jsonl')
        if existing:
            test=existing
        else:
            save_jsonl('data/evaluation/test/questions.jsonl',test)
    else:
        save_jsonl('data/evaluation/test/questions.jsonl',test)
    report={'total':len(dev)+len(test),'dev':len(dev),'test':len(test),'categories':{c:sum(q['category']==c for q in dev+test) for c in sorted({q['category'] for q in dev+test})},'note':'Frozen test file is generated once from ingested evidence. Do not tune against it.'};save_json('reports/final/eval_dataset_report.json',report);print(report)
if __name__=='__main__': main()
