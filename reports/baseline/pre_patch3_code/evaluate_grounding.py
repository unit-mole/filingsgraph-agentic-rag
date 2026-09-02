from __future__ import annotations
import json
from filingsgraph.verification.citations import verify_citations
from scripts._common import save_json

def main():
    # Deterministic verifier self-test. Full generated-answer grounding requires V6 LLM execution.
    evidence=[{'citation_id':'SEC-DEMO-1'},{'citation_id':'SEC-DEMO-2'}];good='Claim [SEC-DEMO-1] and another [SEC-DEMO-2]';bad='Unsupported claim.'
    report={'verifier_good_case':verify_citations(good,evidence),'verifier_bad_case':verify_citations(bad,evidence),'citation_precision':None,'unsupported_claim_rate':None,'note':'Generation-level grounding metrics remain TBD until V6 answers are generated and judged against frozen evidence.'};save_json('reports/experiments/grounding_evaluation.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
