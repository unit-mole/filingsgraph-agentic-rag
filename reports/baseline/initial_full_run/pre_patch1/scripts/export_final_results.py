from __future__ import annotations
import json
from pathlib import Path
from scripts._common import save_json

def read(p):
    x=Path(p);return json.loads(x.read_text(encoding='utf-8')) if x.exists() else None

def main():
    summary={'environment':read('reports/final/environment.json'),'data_quality':read('reports/final/data_quality.json'),'parsing':read('reports/final/parsing_report.json'),'xbrl':read('reports/final/xbrl_normalization_report.json'),'graph':read('reports/graph/graph_evaluation.json'),'financial':read('reports/experiments/test_financial.json'),'temporal':read('reports/temporal/temporal_evaluation.json'),'routing':read('reports/experiments/test_agent_routing.json'),'grounding':read('reports/experiments/grounding_evaluation.json'),'graph_ablation':read('reports/ablations/graph_ablation.json'),'structured_ablation':read('reports/ablations/structured_data_ablation.json'),'metrics_policy':'Only values present in generated reports are actual local-run results; None/TBD remain unmeasured.'};p=save_json('reports/final/summary.json',summary);print(f'Final summary -> {p}')
if __name__=='__main__':main()
