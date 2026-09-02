from __future__ import annotations
import argparse,json,time
from scripts._common import load_jsonl,save_json
from scripts._runtime import load_retrievers

def main():
    ap=argparse.ArgumentParser();ap.add_argument('version',choices=['v0','v1','v2','v3','v4','v5','v6']);ap.add_argument('--smoke',action='store_true');ap.add_argument('--dense-backend',choices=['qdrant','numpy'],default='qdrant');args=ap.parse_args();v=args.version;caps={'v0':['dense'],'v1':['dense','section-aware','metadata filters','parent context'],'v2':['dense','bm25','rrf hybrid'],'v3':['hybrid','reranker'],'v4':['hybrid','reranker','xbrl','deterministic calculations'],'v5':['hybrid','reranker','xbrl','temporal','networkx graph'],'v6':['router','tools','verification','observability','security','fastapi','gradio']}
    start=time.perf_counter();status={'version':v,'capabilities':caps[v],'status':'READY_FOR_LOCAL_EVALUATION','metrics':'TBD until evaluation scripts execute'}
    # Check prerequisite artifacts rather than inventing metrics.
    required=['data/processed/chunks.jsonl','data/index/bm25.pkl'];
    if v in {'v4','v5','v6'}:required.append('data/processed/filingsgraph.duckdb')
    if v in {'v5','v6'}:required.append('data/graph/filingsgraph.json')
    from pathlib import Path
    missing=[p for p in required if not Path(p).exists()];status['missing_artifacts']=missing;status['ready']=not missing;status['latency_ms']=round((time.perf_counter()-start)*1000,3);save_json(f'reports/baseline/{v}_status.json',status);print(json.dumps(status,indent=2))
    if missing:raise SystemExit(2)
if __name__=='__main__':main()
