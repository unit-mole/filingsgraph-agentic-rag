from __future__ import annotations

import difflib
import hashlib
import re
from dataclasses import asdict, dataclass

from filingsgraph.risk_topics import temporal_topic_passages


@dataclass
class RiskChange:
    risk_id: str
    topic: str
    change_type: str
    old_excerpt: str | None
    new_excerpt: str | None
    similarity: float
    evidence_span: str


_STOP = {
    "the","and","or","of","to","a","an","in","for","our","we","is","are","be","been","being","with","on","as","by",
    "that","this","these","those","may","could","can","will","from","at","if","it","its","their","such","also","including",
}


def topic_passages(text: str, topic: str) -> list[str]:
    return temporal_topic_passages(text, topic, max_passages=10)


def _tokens(text: str) -> set[str]:
    return {
        t for t in re.findall(r"[a-z0-9]+", (text or "").lower())
        if len(t) > 2 and t not in _STOP
    }


def _ngrams(text: str, n: int = 3) -> set[tuple[str, ...]]:
    toks = [
        t for t in re.findall(r"[a-z0-9]+", (text or "").lower())
        if len(t) > 2 and t not in _STOP
    ]
    return {tuple(toks[i:i+n]) for i in range(max(0, len(toks)-n+1))}


def _similarity(old: str, new: str) -> float:
    if not old or not new:
        return 0.0
    seq = difflib.SequenceMatcher(None, old.lower(), new.lower()).ratio()
    a, b = _tokens(old), _tokens(new)
    jac = len(a & b) / len(a | b) if (a | b) else 1.0
    containment = min(
        len(a & b) / len(a) if a else 1.0,
        len(a & b) / len(b) if b else 1.0,
    )
    ga, gb = _ngrams(old), _ngrams(new)
    gj = len(ga & gb) / len(ga | gb) if (ga | gb) else 1.0
    return round(0.30 * seq + 0.30 * jac + 0.20 * containment + 0.20 * gj, 6)


def _info_stats(old: str, new: str) -> tuple[float, float, float]:
    old_t, new_t = _tokens(old), _tokens(new)
    old_only = old_t - new_t
    new_only = new_t - old_t
    new_novel = len(new_only) / max(1, len(new_t))
    old_lost = len(old_only) / max(1, len(old_t))
    length_ratio = (len(new) + 1) / (len(old) + 1)
    return new_novel, old_lost, length_ratio


def _classify(old: str, new: str, old_count: int, new_count: int, similarity: float) -> str:
    if not old and new:
        return "NEW"
    if old and not new:
        return "REMOVED"
    if not old and not new:
        return "UNCHANGED"

    new_novel, old_lost, length_ratio = _info_stats(old, new)

    # Very strong continuity is unchanged even when neighboring filing text differs.
    if similarity >= 0.70:
        return "UNCHANGED"

    # Strong containment also indicates the same core disclosure with additions/removals.
    old_t, new_t = _tokens(old), _tokens(new)
    overlap_old = len(old_t & new_t) / max(1, len(old_t))
    overlap_new = len(old_t & new_t) / max(1, len(new_t))

    # Expansion: prior disclosure remains materially present and the newer period adds
    # substantive topic-local detail. This is more robust than raw section length.
    if overlap_old >= 0.42 and (
        (new_novel >= old_lost + 0.08 and length_ratio >= 1.08)
        or new_count >= old_count + 2
        or (length_ratio >= 1.28 and new_novel >= 0.24)
    ):
        return "EXPANDED"

    # Reduction: newer disclosure is largely contained in the older one and material
    # topic-local content disappeared.
    if overlap_new >= 0.42 and (
        (old_lost >= new_novel + 0.08 and length_ratio <= 0.92)
        or old_count >= new_count + 2
        or (length_ratio <= 0.76 and old_lost >= 0.24)
    ):
        return "REDUCED"

    # Moderate continuity with similar amount of topic-local evidence is unchanged.
    if similarity >= 0.42 and 0.70 <= length_ratio <= 1.45 and abs(new_count - old_count) <= 1:
        return "UNCHANGED"

    # Directional fallback when the textual signal is clear but containment is noisy.
    if new_novel - old_lost >= 0.16 and length_ratio >= 1.12:
        return "EXPANDED"
    if old_lost - new_novel >= 0.16 and length_ratio <= 0.88:
        return "REDUCED"

    return "UNCHANGED"


def compare_risk_topic(old_text: str, new_text: str, topic: str) -> RiskChange:
    old_parts = topic_passages(old_text, topic)
    new_parts = topic_passages(new_text, topic)
    old = " ".join(old_parts)[:6000]
    new = " ".join(new_parts)[:6000]
    sim = _similarity(old, new)
    ct = _classify(old, new, len(old_parts), len(new_parts), sim)
    rid = hashlib.sha1(topic.lower().encode()).hexdigest()[:12]
    evidence = (new or old)[:1200]
    return RiskChange(rid, topic, ct, old[:1200] or None, new[:1200] or None, sim, evidence)


def compare_risk_disclosures(old_text: str, new_text: str, topics: list[str]) -> list[dict]:
    return [asdict(compare_risk_topic(old_text, new_text, t)) for t in topics]
