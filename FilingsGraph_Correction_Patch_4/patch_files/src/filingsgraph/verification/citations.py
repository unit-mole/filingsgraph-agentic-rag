from __future__ import annotations

import re

_CITATION = re.compile(r"\[([A-Za-z0-9][A-Za-z0-9_.:-]*)\]")
_LIMITATION = re.compile(
    r"^(?:evidence is insufficient|insufficient evidence|no evidence was retrieved|"
    r"no supporting evidence|the available evidence does not|important limitation)",
    re.I,
)


def extract_citations(text: str) -> list[str]:
    return _CITATION.findall(text or "")


def _claims(answer: str) -> list[str]:
    """Return material factual claim lines for citation-attachment scoring."""
    out: list[str] = []
    for raw in (answer or "").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or set(line) <= {"-", "|", ":", " "}:
            continue
        line = re.sub(r"^[-*+]\s+", "", line)
        line = re.sub(r"^\d+[.)]\s+", "", line)
        if _LIMITATION.match(line):
            continue
        if len(re.sub(r"\[[^\]]+\]", "", line).strip()) < 20:
            continue
        out.append(line)
    return out


def verify_citations(answer: str, evidence: list[dict]) -> dict:
    available = {e.get("citation_id") for e in evidence if e.get("citation_id")}
    emitted = extract_citations(answer)
    emitted_set = set(emitted)
    valid = [cid for cid in emitted if cid in available]
    invalid = [cid for cid in emitted if cid not in available]

    claims = _claims(answer)
    supported_claims, unsupported_claims = [], []
    for claim in claims:
        ids = extract_citations(claim)
        if any(cid in available for cid in ids):
            supported_claims.append(claim)
        else:
            unsupported_claims.append(claim)

    citation_precision = len(valid) / len(emitted) if emitted else 0.0
    claim_support_rate = len(supported_claims) / len(claims) if claims else 1.0
    unsupported_claim_rate = len(unsupported_claims) / len(claims) if claims else 0.0

    return {
        "ok": bool(available) and citation_precision == 1.0 and unsupported_claim_rate == 0.0,
        "available": sorted(available),
        "cited": sorted(emitted_set & available),
        "invalid_citations": sorted(set(invalid)),
        "uncited_evidence": sorted(available - emitted_set),
        "citation_precision": citation_precision,
        "claim_support_rate": claim_support_rate,
        "unsupported_claim_rate": unsupported_claim_rate,
        "citation_completeness": claim_support_rate,
        "claims_total": len(claims),
        "claims_supported": len(supported_claims),
        "claims_unsupported": len(unsupported_claims),
        "unsupported_claim_examples": unsupported_claims[:5],
        "metric_scope": "citation attachment/validity; semantic entailment is not fabricated",
    }
