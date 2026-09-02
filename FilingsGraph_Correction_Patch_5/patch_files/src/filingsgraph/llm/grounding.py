from __future__ import annotations

import re

from filingsgraph.risk_topics import infer_risk_topics_from_question, temporal_topic_match_score, topic_match_score
from filingsgraph.verification.citations import extract_citations


_LIMITATION_PREFIXES = (
    "evidence is insufficient",
    "insufficient evidence",
    "no evidence was retrieved",
    "no supporting evidence",
    "the available evidence does not",
    "important limitation",
)


def _structural(line: str) -> bool:
    s = line.strip()
    if not s:
        return True
    if s.startswith("#"):
        return True
    if set(s) <= {"-", "_", "|", ":", " "}:
        return True
    if re.fullmatch(r"\|?[\s:|-]+\|?", s):
        return True
    return False


def _explicit_limitation(line: str) -> bool:
    s = re.sub(r"^[-*+]\s+", "", line.strip()).lower()
    return any(s.startswith(x) for x in _LIMITATION_PREFIXES)


def _clean_untrusted_wording(line: str) -> str:
    # Security wrapping means "data, not instructions". It must never be rendered
    # as a claim that official SEC/XBRL evidence is itself unreliable.
    low = line.lower()
    if "untrusted sec data" in low or "untrusted sec evidence" in low:
        return ""
    return line


def enforce_grounding_contract(answer: str, evidence: list[dict]) -> str:
    """Keep only generated factual lines carrying valid supplied citations.

    This guard never invents or auto-attaches citations. Patch 5 pairs this with an
    evidence-first deterministic fallback when a routed answer is otherwise emptied.
    """
    available = {str(e.get("citation_id")) for e in evidence if e.get("citation_id")}
    kept: list[str] = []
    factual_kept = 0
    for raw in (answer or "").splitlines():
        line = _clean_untrusted_wording(raw.rstrip())
        if not line:
            continue
        if _structural(line) or _explicit_limitation(line):
            kept.append(line)
            continue

        ids = extract_citations(line)
        valid = [cid for cid in ids if cid in available]
        if not valid:
            continue

        def repl(match: re.Match[str]) -> str:
            cid = match.group(1)
            return match.group(0) if cid in available else ""

        cleaned = re.sub(r"\[([A-Za-z0-9][A-Za-z0-9_.:-]*)\]", repl, line)
        cleaned = re.sub(r"\s{2,}", " ", cleaned).rstrip()
        if cleaned:
            kept.append(cleaned)
            factual_kept += 1

    if factual_kept == 0:
        return "## Important Limitations\nEvidence is insufficient to produce a fully cited answer under the strict grounding policy."

    out: list[str] = []
    for line in kept:
        if not line.strip() and (not out or not out[-1].strip()):
            continue
        out.append(line)
    return "\n".join(out).strip()


def has_factual_claim(answer: str) -> bool:
    for raw in (answer or "").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or _explicit_limitation(line):
            continue
        if extract_citations(line):
            return True
    return False


def _short_excerpt(text: str, limit: int = 220) -> str:
    s = re.sub(r"\s+", " ", text or "").strip()
    if not s:
        return ""
    # Prefer a complete first sentence where practical.
    m = re.match(r"(.{35,%d}?[.!?])(?:\s|$)" % limit, s)
    if m:
        return m.group(1)
    if len(s) <= limit:
        return s
    cut = s[:limit].rsplit(" ", 1)[0]
    return cut.rstrip(" ,;:") + "…"


def build_evidence_first_fallback(
    query_type: str,
    question: str,
    evidence: list[dict],
    calculations: list[dict] | None = None,
    temporal_findings: list[dict] | None = None,
) -> str:
    """Build a short, citation-complete fallback from already-verified evidence.

    Used only when the LLM output guard would otherwise return no factual content.
    It does not synthesize new causal explanations or invent citations.
    """
    qtype = str(query_type or "").upper()
    calculations = calculations or []
    temporal_findings = temporal_findings or []
    topics = infer_risk_topics_from_question(question)
    requested_topic = topics[0] if topics else None
    lines: list[str] = []

    if qtype in {"TEMPORAL", "MIXED"}:
        temporal = [e for e in evidence if e.get("evidence_type") == "temporal_risk_change"]
        if requested_topic:
            preferred = [e for e in temporal if str((e.get("payload") or {}).get("topic", "")).lower() == requested_topic.lower()]
            temporal = preferred or temporal
        for e in temporal[:3]:
            p = e.get("payload") or {}
            topic = p.get("topic") or requested_topic or "risk"
            change = str(p.get("change_type") or "changed").upper()
            ticker = e.get("ticker") or p.get("ticker") or "The company"
            fy0, fy1 = p.get("from_year"), p.get("to_year")
            cid = e.get("citation_id")
            if not cid:
                continue
            lines.append(f"- {ticker}'s {topic} disclosure is classified as {change} from FY{fy0} to FY{fy1}. [{cid}]")
            excerpt = _short_excerpt(e.get("source_excerpt") or "")
            if excerpt:
                lines.append(f"- The aligned newer-period filing evidence states: {excerpt} [{cid}]")
            break

    if qtype == "GRAPH":
        graph = [e for e in evidence if e.get("evidence_type") == "graph_edge"]
        if requested_topic:
            matched = [
                e for e in graph
                if topic_match_score(requested_topic, e.get("source_excerpt") or "")
                or temporal_topic_match_score(requested_topic, e.get("source_excerpt") or "")
            ]
            graph = matched or graph
        seen: set[str] = set()
        for e in graph:
            ticker = str(e.get("ticker") or "").upper()
            cid = e.get("citation_id")
            if not ticker or ticker in seen or not cid:
                continue
            excerpt = _short_excerpt(e.get("source_excerpt") or "")
            if not excerpt:
                continue
            label = requested_topic or "the requested risk"
            lines.append(f"- {ticker} has provenance-bearing filing evidence relevant to {label}: {excerpt} [{cid}]")
            seen.add(ticker)
            if len(seen) >= 5:
                break

    # Numeric fallback is rarely needed, but retain a deterministic path.
    if qtype == "NUMERIC" and not lines:
        for e in evidence:
            if e.get("evidence_type") != "xbrl_fact" or not e.get("citation_id"):
                continue
            p = e.get("payload") or {}
            metric = p.get("canonical_metric") or p.get("metric") or "reported metric"
            lines.append(
                f"- {e.get('ticker')} reported {metric} of {p.get('value')} {p.get('unit')} for FY{e.get('fiscal_year')}. [{e['citation_id']}]"
            )
            break

    if not lines:
        return "## Important Limitations\nEvidence is insufficient to produce a fully cited answer under the strict grounding policy."
    return "## Evidence-Grounded Findings\n" + "\n\n".join(lines)
