from __future__ import annotations

import re

TEXTUAL_DISCLOSURE_PATTERNS = [
    r"\bwhat\s+did\b.*\bdisclos(?:e|ed)\b",
    r"\bwhat\s+(?:concerns?|risks?|discussion|narrative)\b.*\b(?:describe|discuss|disclose|mention)",
]
GRAPH_PATTERNS = [
    r"\bconnected\b",
    r"\bconnects?\s+(?:them|these|the\s+companies)\b",
    r"\brelationship(?:s)?\b",
    r"\bshared\s+risk(?:s)?\b",
    r"\bshare\s+exposure\b",
    r"\bshared\s+exposure\b",
    r"\bwhich\s+selected\s+companies\b",
    r"\bwhich\s+companies\b.*\b(?:share|connected|exposure)\b",
    r"\bwhich\s+segments\b",
    r"\bgraph\b",
    r"\bmulti[- ]hop\b",
    r"\bsubsidiar(?:y|ies)\b",
    r"\bsupplier(?:s)?\b",
    r"\bcompetitor(?:s)?\b",
    r"\bfiling\s+evidence\s+connects\b",
]
TEMPORAL_PATTERNS = [
    r"\bhow\s+(?:has|have|did)\b.*\bchang",
    r"\bchanged\s+(?:from|between|over)\b",
    r"\bevolv(?:e|ed|ution)\b",
    r"\bover\s+time\b",
    r"\bbetween\s+fy\d{4}\s+and\s+fy\d{4}\b",
    r"\blast\s+(?:three|four|five|\d+)\b.*\bfilings?\b",
    r"\byear[- ]over[- ]year\b",
    r"\brisk\s+language\b.*\bchang",
]
NUMERIC_PATTERNS = [
    r"\bwhat\s+was\b.*\b(?:revenue|income|margin|capex|cash|assets|liabilities|equity|profit)\b",
    r"\bhow\s+much\b",
    r"\b(?:revenue|income|margin|capex|cash|assets|liabilities|equity|profit)\s+(?:growth|change|increased|decreased)\b",
    r"\b(?:growth|cagr|margin|percentage|percent)\b",
    r"\bcalculate\b",
    r"\bFY\d{4}\b.*\b(?:revenue|income|margin|capex|cash|assets|liabilities|equity|profit)\b",
]
MULTI_PATTERNS = [
    r"\bacross\s+(?:the\s+)?(?:selected\s+)?companies\b",
    r"\bcompare\s+companies\b",
    r"\bacross\s+these\b",
    r"\bcohort\b",
    r"\bversus\b",
    r"\bvs\.?\b",
]


def _matches(patterns: list[str], text: str) -> bool:
    return any(re.search(p, text, flags=re.I | re.S) for p in patterns)


def classify_query(question: str) -> str:
    q = " ".join(question.split())
    textual_disclosure = _matches(TEXTUAL_DISCLOSURE_PATTERNS, q)
    graph = _matches(GRAPH_PATTERNS, q)
    temporal = _matches(TEMPORAL_PATTERNS, q)
    numeric = _matches(NUMERIC_PATTERNS, q)
    multi = _matches(MULTI_PATTERNS, q)

    # Explicit filing-disclosure lookup is textual even if the passage happens
    # to mention a financial metric. Arithmetic words such as growth/calculate
    # still route to numeric/mixed via the checks below.
    if textual_disclosure and not temporal and not graph and not re.search(r"\b(?:growth|cagr|calculate|percentage|percent)\b", q, re.I):
        return "TEXTUAL"
    if graph and (temporal or numeric):
        return "MIXED"
    if temporal and numeric:
        return "MIXED"
    if graph:
        return "GRAPH"
    if temporal:
        return "TEMPORAL"
    if numeric:
        return "NUMERIC"
    if multi:
        return "MULTI_COMPANY"
    return "TEXTUAL"


def extract_tickers(question: str, known: list[str]) -> list[str]:
    up = question.upper()
    return [t for t in known if re.search(rf"\b{re.escape(t)}\b", up)]
