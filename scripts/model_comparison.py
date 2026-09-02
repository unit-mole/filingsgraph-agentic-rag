from __future__ import annotations
import argparse,json,time
from filingsgraph.llm.local_provider import LocalTransformersProvider
from scripts._common import save_json

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--models',nargs='+',default=['Qwen/Qwen3-8B','Qwen/Qwen3-14B']);args=ap.parse_args();prompt=[{'role':'system','content':'Return JSON only.'},{'role':'user','content':'Classify this financial research query as TEXTUAL, NUMERIC, TEMPORAL, GRAPH, MULTI_COMPANY, MACRO, or MIXED: How did revenue change while export-control risk language evolved?'}];rows=[]
    for m in args.models:
        st=time.perf_counter();p=LocalTransformersProvider(m);out=p.generate(prompt,max_new_tokens=80,temperature=0);rows.append({'model':m,'output':out,'latency_s':time.perf_counter()-st})
    save_json('reports/experiments/model_comparison.json',{'rows':rows,'quality_metrics':'TBD until benchmark judging'});print(json.dumps(rows,indent=2))
if __name__=='__main__':main()
