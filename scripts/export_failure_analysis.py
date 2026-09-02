from __future__ import annotations
import json
from pathlib import Path
from scripts._common import save_json
TAXONOMY=['wrong_company','wrong_CIK','wrong_filing','wrong_period','wrong_section','retrieval_miss','sparse_miss','dense_miss','reranker_failure','wrong_XBRL_concept','wrong_unit','wrong_calculation','custom_taxonomy_failure','temporal_alignment_failure','risk_change_failure','graph_missing_edge','graph_false_edge','graph_over_expansion','tool_routing_failure','citation_mismatch','unsupported_claim','contradictory_evidence','model_format_failure','agent_loop','latency_failure']
def main():
    report={'taxonomy':TAXONOMY,'failures':[],'note':'Populate automatically/manual-review after local evaluation; empty does not mean zero failures.'};save_json('reports/failure_analysis/failure_analysis.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
