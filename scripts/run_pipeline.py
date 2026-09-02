from __future__ import annotations
import argparse,subprocess,sys
STAGES={
 'data':['scripts.resolve_companies','scripts.download_filings','scripts.download_companyfacts','scripts.validate_data','scripts.build_documents','scripts.build_database'],
 'index':['scripts.build_index'], 'graph':['scripts.build_graph'], 'evalset':['scripts.build_eval_set'],
 'versions':[f'scripts.run_v{i}' for i in range(7)], 'eval':['scripts.evaluate_all'], 'export':['scripts.export_final_results']}
ORDER=['data','index','graph','evalset','versions','eval','export']
def run(mod):
    print(f'\n>>> {mod}');r=subprocess.run([sys.executable,'-m',mod]);
    if r.returncode:raise SystemExit(r.returncode)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--stage',choices=['all']+ORDER,default='all');args=ap.parse_args()
    for s in ORDER if args.stage=='all' else [args.stage]:
        for m in STAGES[s]:run(m)
if __name__=='__main__':main()
