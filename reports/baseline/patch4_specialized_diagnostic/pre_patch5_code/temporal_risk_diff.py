from __future__ import annotations

import difflib
import hashlib
import re
from dataclasses import asdict, dataclass

from filingsgraph.risk_topics import topic_passages as _topic_passages


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
    return _topic_passages(text, topic, max_passages=10)


def _tokens(text: str) -> set[str]:
    return {
        t for t in re.findall(r"[a-z0-9]+", (text or "").lower())
        if len(t) > 2 and t not in _STOP
    }


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
    return round(0.45 * seq + 0.35 * jac + 0.20 * containment, 6)


def _classify(old: str, new: str, old_count: int, new_count: int, similarity: float) -> str:
    if not old and new:
        return "NEW"
    if old and not new:
        return "REMOVED"
    if not old and not new:
        return "UNCHANGED"

    old_t, new_t = _tokens(old), _tokens(new)
    shared = old_t & new_t
    old_only = old_t - new_t
    new_only = new_t - old_t
    new_novel = len(new_only) / max(1, len(new_t))
    old_lost = len(old_only) / max(1, len(old_t))
    length_ratio = (len(new) + 1) / (len(old) + 1)

    # Strong semantic/textual continuity should not be mislabeled solely because
    # a filing section became longer/shorter due to neighboring disclosure text.
    if similarity >= 0.72:
        return "UNCHANGED"
    if similarity >= 0.58 and 0.72 <= length_ratio <= 1.38 and abs(new_count - old_count) <= 1:
        return "UNCHANGED"

    # Directional information gain/loss. Require a material margin so formatting
    # and duplicated filing language do not create spurious EXPANDED/REDUCED labels.
    if (new_novel - old_lost) >= 0.12 and (length_ratio >= 1.10 or new_count > old_count):
        return "EXPANDED"
    if (old_lost - new_novel) >= 0.12 and (length_ratio <= 0.90 or new_count < old_count):
        return "REDUCED"

    if length_ratio >= 1.35 or new_count >= old_count + 2:
        return "EXPANDED"
    if length_ratio <= 0.68 or old_count >= new_count + 2:
        return "REDUCED"

    # When both periods retain the same topic-specific disclosure but the
    # direction is ambiguous, UNCHANGED is safer than fabricating expansion/loss.
    return "UNCHANGED"


def compare_risk_topic(old_text: str, new_text: str, topic: str) -> RiskChange:
    old_parts = topic_passages(old_text, topic)
    new_parts = topic_passages(new_text, topic)
    old = " ".join(old_parts)[:5000]
    new = " ".join(new_parts)[:5000]
    sim = _similarity(old, new)
    ct = _classify(old, new, len(old_parts), len(new_parts), sim)
    rid = hashlib.sha1(topic.lower().encode()).hexdigest()[:12]
    evidence = (new or old)[:1200]
    return RiskChange(rid, topic, ct, old[:1200] or None, new[:1200] or None, sim, evidence)


def compare_risk_disclosures(old_text: str, new_text: str, topics: list[str]) -> list[dict]:
    return [asdict(compare_risk_topic(old_text, new_text, t)) for t in topics]
