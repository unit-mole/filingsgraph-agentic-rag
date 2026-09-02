from __future__ import annotations
import re
from filingsgraph.agents.router import classify_query, extract_tickers
from filingsgraph.core.config import load_yaml
from filingsgraph.schemas.queries import ResearchPlan


def _cohort_tickers() -> list[str]:
    try:
        return [str(x["ticker"]).upper() for x in load_yaml("companies.yaml").get("companies", []) if x.get("ticker")]
    except Exception:
        return []


def plan(question: str, tickers: list[str] | None = None, years: list[int] | None = None) -> ResearchPlan:
    qt = classify_query(question)
    known = _cohort_tickers()
    supplied = [str(t).upper() for t in (tickers or [])]
    entities = supplied or extract_tickers(question, known)

    qlow = question.lower()
    if not entities and qt in {"GRAPH", "MULTI_COMPANY"} and any(
        phrase in qlow for phrase in ("selected companies", "cohort", "which companies", "share exposure")
    ):
        entities = known

    periods = years or [int(y) for y in re.findall(r"FY?(20\d{2})", question.upper())]
    return ResearchPlan(
        query_type=qt,
        entities=entities,
        periods=sorted(set(periods)),
        retrieval_queries=[question],
        use_text=qt != "NUMERIC" or any(x in qlow for x in ["management", "risk", "explain", "narrative"]),
        use_xbrl=qt in {"NUMERIC", "MIXED"},
        use_graph=qt in {"GRAPH", "MIXED"},
        use_temporal=qt in {"TEMPORAL", "MIXED"},
        use_macro=qt == "MACRO",
    )
