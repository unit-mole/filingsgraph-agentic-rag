from __future__ import annotations

import re
from functools import lru_cache

# Topic rules are deliberately high precision. Generic vocabulary such as
# "regulation", "security", or "manufacturing" alone is not enough to create
# a risk observation. This reduces false-positive temporal/graph matches.
TOPIC_PATTERNS: dict[str, tuple[str, ...]] = {
    "export controls": (
        r"\bexport controls?\b",
        r"\bexport restrictions?\b",
        r"\bexport regulations?\b",
        r"\bexport licensing\b",
        r"\brestrictions? on (?:the )?export\b",
        r"\bexport requirements?\b",
        r"\brestrict(?:ed|ions?) .{0,35}\bexports?\b",
        r"\bsanctions? and export controls?\b",
    ),
    "supply chain": (
        r"\bsupply chain\b",
        r"\bsuppliers?\b",
        r"\bsupply assurance\b",
        r"\breliable supply\b",
        r"\bconsistent and reliable supply\b",
        r"\btimely supply of (?:equipment|materials|components)\b",
        r"\bsupply of (?:equipment|materials|components)\b",
        r"\bfoundr(?:y|ies)\b",
        r"\bwafer(?:s)?\b",
        r"\bcapacity constraints?\b",
        r"\bmaterials? shortages?\b",
        r"\bmanufacturing lead times?\b",
    ),
    "cybersecurity": (
        r"\bcybersecurity\b",
        r"\bcyber[- ]?attacks?\b",
        r"\bcyber threats?\b",
        r"\bcyber risks?\b",
        r"\bsecurity breach(?:es)?\b",
        r"\bdata breach(?:es)?\b",
        r"\bsecurity vulnerabilit(?:y|ies)\b",
        r"\binformation security\b",
    ),
    "artificial intelligence regulation": (
        r"\b(?:AI|artificial intelligence)[ -](?:related )?(?:regulation|regulations|law|laws|legislation|rules?)\b",
        r"\bregulat(?:e|ed|ing|ion of) (?:AI|artificial intelligence)\b",
        r"\blaws? regulating (?:AI|artificial intelligence)\b",
        r"\blegislation regulating (?:AI|artificial intelligence)\b",
        r"\bAI Act\b",
    ),
    "semiconductor manufacturing": (
        r"\bsemiconductor manufacturing\b",
        r"\bmanufacturing (?:process|processes|facilit(?:y|ies)|yield|yields|capacity)\b",
        r"\bfoundr(?:y|ies)\b",
        r"\bwafer(?:s)?\b",
        r"\bfabrication\b",
        r"\bprocess nodes?\b",
        r"\bmanufactur(?:e|ing) semiconductors?\b",
    ),
    "geopolitical tensions": (
        r"\bgeopolitical\b",
        r"\bChina.{0,45}Taiwan\b",
        r"\bTaiwan.{0,45}China\b",
        r"\bRussia.{0,35}Ukraine\b",
        r"\bUkraine.{0,35}Russia\b",
        r"\bIsrael.{0,35}Hamas\b",
        r"\barmed conflict\b",
        r"\btrade tensions?\b",
        r"\bpolitical instability\b",
    ),
    "customer concentration": (
        r"\bcustomer concentration\b",
        r"\bconcentration of (?:sales|revenue|revenues|customers)\b",
        r"\bsignificant customers?\b",
        r"\blimited number of (?:customers|partners|distributors)\b",
        r"\bsmall number of customers\b",
        r"\brevenue.{0,60}\b(?:one|few|limited number of) customers\b",
    ),
    "competition": (
        # Avoid a bare "competition" token because regulatory laundry lists
        # frequently mention competition without describing competitive risk.
        r"\bcompetitors?\b",
        r"\bcompetitive (?:pressure|pressures|market|markets|position|landscape|threat|threats|products?|offerings?|environment)\b",
        r"\bcompetition (?:could|may|can|is|remains|will|has|intensif|from|for)\b",
        r"\bintense competition\b",
        r"\bmarket share\b",
        r"\bpricing pressure\b",
    ),
    "intellectual property": (
        r"\bintellectual property\b",
        r"\bpatents?\b",
        r"\bcopyrights?\b",
        r"\btrade secrets?\b",
        r"\binfring(?:e|ed|ement|ing)\b",
        r"\blicen[sc](?:e|ing).{0,45}\b(?:patent|technology|intellectual property)\b",
    ),
    "data privacy": (
        r"\bdata privacy\b",
        r"\bprivacy (?:law|laws|regulation|regulations|risk|risks)\b",
        r"\bprivacy and data security\b",
        r"\bdata protection\b",
        r"\bGDPR\b",
        r"\bCCPA\b",
        r"\bpersonal (?:data|information)\b",
    ),
}


@lru_cache(maxsize=None)
def _compiled(topic: str) -> tuple[re.Pattern[str], ...]:
    return tuple(re.compile(p, re.I | re.S) for p in TOPIC_PATTERNS.get(topic.lower(), ()))


def split_evidence_units(text: str) -> list[str]:
    """Split filing text into evidence-sized units while retaining bullets."""
    if not text:
        return []
    normalized = re.sub(r"\r\n?", "\n", text)
    parts = re.split(r"(?<=[.!?])\s+|\n{2,}|(?=\s*[•▪◦]\s+)", normalized)
    out: list[str] = []
    for part in parts:
        unit = re.sub(r"\s+", " ", part).strip(" \t\n•▪◦")
        if len(unit) >= 35:
            out.append(unit)
    return out


def topic_match_score(topic: str, text: str) -> int:
    """Return the number of distinct high-precision patterns matched."""
    return sum(1 for p in _compiled(topic.lower()) if p.search(text or ""))


def topic_passages(text: str, topic: str, *, max_passages: int = 8) -> list[str]:
    scored: list[tuple[int, int, str]] = []
    for idx, unit in enumerate(split_evidence_units(text)):
        score = topic_match_score(topic, unit)
        if score:
            scored.append((score, -idx, unit))
    scored.sort(reverse=True)
    # Preserve original filing order among selected high-quality passages.
    chosen = sorted(scored[:max_passages], key=lambda x: -x[1])
    return [unit for _, _, unit in chosen]


def best_topic_passage(text: str, topic: str) -> tuple[str | None, int]:
    best: tuple[int, str] | None = None
    for unit in split_evidence_units(text):
        score = topic_match_score(topic, unit)
        if score and (best is None or score > best[0]):
            best = (score, unit)
    return (best[1], best[0]) if best else (None, 0)
