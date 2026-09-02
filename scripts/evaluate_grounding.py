from __future__ import annotations

import argparse
import json

from filingsgraph.verification.citations import verify_citations
from scripts._common import save_json

LIVE_CASES = [
    ("What was NVDA revenue in FY2025?", ["NVDA"], [2025]),
    ("How did NVDA's export controls risk disclosure change from FY2024 to FY2025?", ["NVDA"], [2024, 2025]),
    ("Which selected companies share exposure to export controls risk in FY2025, and what filing evidence connects them?", [], [2025]),
    ("How did NVDA revenue change from FY2024 to FY2025, and how did its export controls risk disclosure change over the same period?", ["NVDA"], [2024, 2025]),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true", help="Run four real V6 generations with the configured local model.")
    args = ap.parse_args()
    evidence = [{"citation_id": "SEC-DEMO-1"}, {"citation_id": "SEC-DEMO-2"}]
    good = "Revenue was reported [SEC-DEMO-1]. Risk language changed [SEC-DEMO-2]."
    bad = "Unsupported claim without a citation."
    report = {
        "verifier_good_case": verify_citations(good, evidence),
        "verifier_bad_case": verify_citations(bad, evidence),
        "citation_precision": None,
        "claim_support_rate": None,
        "unsupported_claim_rate": None,
        "thinking_leak_rate": None,
        "nonempty_answer_rate": None,
        "mean_supported_claims_per_answer": None,
        "live_cases": [],
        "metric_scope": "citation attachment/validity; semantic entailment is not fabricated",
    }
    if args.live:
        from app.runtime import full_engine

        rows = []
        for question, tickers, years in LIVE_CASES:
            r = full_engine().research(question, tickers, years)
            v = r["verification"]["citations"]
            answer = r["answer"]
            rows.append(
                {
                    "question": question,
                    "query_type": r["query_type"],
                    "citation_metrics": v,
                    "answer": answer,
                    "think_tag_present": "<think>" in answer.lower(),
                    "answer_nonempty": bool(answer.strip()) and "Evidence is insufficient" not in answer,
                }
            )
        total_citations = sum(
            len(x["citation_metrics"].get("cited", [])) + len(x["citation_metrics"].get("invalid_citations", []))
            for x in rows
        )
        valid_citations = sum(len(x["citation_metrics"].get("cited", [])) for x in rows)
        total_claims = sum(x["citation_metrics"].get("claims_total", 0) for x in rows)
        supported = sum(x["citation_metrics"].get("claims_supported", 0) for x in rows)
        report["citation_precision"] = valid_citations / total_citations if total_citations else 0.0
        report["claim_support_rate"] = supported / total_claims if total_claims else 1.0
        report["unsupported_claim_rate"] = 1.0 - report["claim_support_rate"]
        report["thinking_leak_rate"] = sum(x["think_tag_present"] for x in rows) / len(rows) if rows else 0.0
        report["nonempty_answer_rate"] = sum(x["answer_nonempty"] for x in rows) / len(rows) if rows else 0.0
        report["mean_supported_claims_per_answer"] = supported / len(rows) if rows else 0.0
        report["live_cases"] = rows
        report["note"] = (
            "Patch-5 evidence-first grounding metrics from four representative query types. "
            "The output guard removes uncited generated factual lines; semantic entailment remains outside this deterministic metric."
        )
    else:
        report["note"] = "Verifier self-test only. Run with --live for actual V6 generation-level metrics."
    save_json("reports/experiments/grounding_evaluation.json", report)
    printable = {k: v for k, v in report.items() if k != "live_cases"}
    printable["live_case_count"] = len(report["live_cases"])
    print(json.dumps(printable, indent=2))


if __name__ == "__main__":
    main()
