from __future__ import annotations

import re
from functools import lru_cache

# Graph-edge rules are intentionally conservative. A graph edge should represent a
# substantive risk exposure, not a keyword mention in a regulatory laundry list.
TOPIC_PATTERNS: dict[str, tuple[str, ...]] = {
    "export controls": (
        r"\bexport controls?\b",
        r"\bexport restrictions?\b",
        r"\bexport regulations?\b",
        r"\bexport licen[cs](?:e|es|ing)\b",
        r"\brestrictions? on (?:the )?export\b",
        r"\bexport requirements?\b",
        r"\brestrict(?:ed|ions?) .{0,35}\bexports?\b",
        r"\bsanctions? and export controls?\b",
    ),
    "supply chain": (
        r"\bsupply chain\b",
        r"\bsupply assurance\b",
        r"\breliable supply\b",
        r"\bconsistent and reliable supply\b",
        r"\btimely supply of (?:equipment|materials|components)\b",
        r"\bsupply of (?:equipment|materials|components)\b",
        r"\bsuppliers? .{0,45}(?:shortage|constraint|delay|disrupt|depend|rely)\b",
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
        r"\b(?:export controls?|government restrictions?|regulations?|rules?|laws?)\b.{0,140}\b(?:AI|artificial intelligence|advanced computing)\b",
        r"\b(?:AI|artificial intelligence|advanced computing)\b.{0,140}\b(?:export controls?|government restrictions?|regulations?|rules?|laws?)\b",
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
        r"\bcompetitors?\b",
        r"\bcompetitive (?:pressure|pressures|market|markets|position|landscape|threat|threats|products?|offerings?|environment|disadvantage)\b",
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

# Temporal alignment can use a broader presence detector than the graph. The
# direction classifier still compares topic-local passages, but it should not mark
# a disclosure absent merely because the filer used a synonymous phrase.
TEMPORAL_EXTRA_PATTERNS: dict[str, tuple[str, ...]] = {
    "export controls": (
        r"\bexports?\b.{0,80}\b(?:restrictions?|licen[cs](?:e|es|ing)|regulations?|controls?)\b",
        r"\b(?:restrictions?|licen[cs](?:e|es|ing)|regulations?|controls?)\b.{0,80}\bexports?\b",
        r"\bExport Administration Regulations\b",
        r"\bDepartment of Commerce\b.{0,120}\bexport\b",
    ),
    "supply chain": (
        r"\bsuppliers?\b",
        r"\bsupply\b.{0,70}\b(?:constraint|shortage|delay|capacity|availability|depend|risk)\b",
        r"\bfoundr(?:y|ies)\b",
        r"\bwafer(?:s)?\b",
    ),
    "cybersecurity": (
        r"\bcyber\b",
        r"\bsecurity incident\b",
        r"\bconfidential data\b",
        r"\bsensitive information\b.{0,80}\b(?:breach|attack|security|loss|theft)\b",
    ),
    "artificial intelligence regulation": (
        r"\b(?:AI|artificial intelligence|advanced computing)\b.{0,180}\b(?:regulat|law|legislation|rule|restriction|export control|government action)\w*\b",
        r"\b(?:regulat|law|legislation|rule|restriction|export control|government action)\w*\b.{0,180}\b(?:AI|artificial intelligence|advanced computing)\b",
    ),
    "semiconductor manufacturing": (
        r"\bmanufactur(?:e|ing)\b.{0,100}\b(?:wafer|foundry|semiconductor|yield|capacity|facility|process)\b",
        r"\b(?:wafer|foundry|semiconductor|yield|capacity|facility|process node)\b.{0,100}\bmanufactur(?:e|ing)\b",
    ),
    "geopolitical tensions": (
        r"\bpolitical unrest\b",
        r"\bmilitary conflict\b",
        r"\btrade conflict\b",
        r"\bgeopolitical turmoil\b",
    ),
    "customer concentration": (
        r"\b(?:customer|customers)\b.{0,100}\b(?:concentration|significant|limited number|majority|substantial portion)\b",
        r"\b(?:revenue|sales)\b.{0,100}\b(?:customer|customers)\b",
    ),
    "competition": (
        r"\bcompetition\b",
        r"\bcompetitive\b",
        r"\bcompetitor\w*\b",
    ),
    "intellectual property": (
        r"\bIP\b",
        r"\blicen[sc](?:e|es|ing)\b.{0,80}\b(?:technology|software|patent|IP)\b",
    ),
    "data privacy": (
        r"\bprivacy\b",
        r"\bdata security\b",
        r"\bconfidential data\b",
        r"\bsensitive information\b",
    ),
}

# Cues used only to score the strength of a graph edge. They do not create a
# topic match by themselves.
EXPOSURE_CUES = (
    r"\brisk\b", r"\brisks\b", r"\badvers(?:e|ely)\b", r"\bharm\b", r"\bimpact\b",
    r"\bdisrupt\w*\b", r"\blimit\w*\b", r"\brestrict\w*\b", r"\bdepend\w*\b", r"\brely\w*\b",
    r"\bsubject to\b", r"\bexpos(?:e|ed|ure)\b", r"\bthreat\w*\b", r"\buncertain\w*\b",
    r"\bshortage\w*\b", r"\bconstraint\w*\b", r"\bfailure\b", r"\bcould\b", r"\bmay\b",
)


@lru_cache(maxsize=None)
def _compiled(topic: str) -> tuple[re.Pattern[str], ...]:
    return tuple(re.compile(p, re.I | re.S) for p in TOPIC_PATTERNS.get(topic.lower(), ()))


@lru_cache(maxsize=None)
def _compiled_temporal(topic: str) -> tuple[re.Pattern[str], ...]:
    pats = TOPIC_PATTERNS.get(topic.lower(), ()) + TEMPORAL_EXTRA_PATTERNS.get(topic.lower(), ())
    return tuple(re.compile(p, re.I | re.S) for p in pats)


@lru_cache(maxsize=1)
def _compiled_exposure() -> tuple[re.Pattern[str], ...]:
    return tuple(re.compile(p, re.I | re.S) for p in EXPOSURE_CUES)


def split_evidence_units(text: str) -> list[str]:
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
    return sum(1 for p in _compiled(topic.lower()) if p.search(text or ""))


def temporal_topic_match_score(topic: str, text: str) -> int:
    return sum(1 for p in _compiled_temporal(topic.lower()) if p.search(text or ""))


def exposure_cue_score(text: str) -> int:
    return sum(1 for p in _compiled_exposure() if p.search(text or ""))


def topic_passages(text: str, topic: str, *, max_passages: int = 8) -> list[str]:
    scored: list[tuple[int, int, str]] = []
    for idx, unit in enumerate(split_evidence_units(text)):
        score = topic_match_score(topic, unit)
        if score:
            scored.append((score, -idx, unit))
    scored.sort(reverse=True)
    chosen = sorted(scored[:max_passages], key=lambda x: -x[1])
    return [unit for _, _, unit in chosen]


def temporal_topic_passages(text: str, topic: str, *, max_passages: int = 10) -> list[str]:
    units = split_evidence_units(text)
    scored: list[tuple[int, int, str]] = []
    for idx, unit in enumerate(units):
        score = temporal_topic_match_score(topic, unit)
        if not score:
            continue
        # Keep the temporal comparison topic-local. Neighboring risk text from a
        # different topic (for example cybersecurity after an export sentence)
        # must not change EXPANDED/REDUCED direction.
        context = unit
        if idx + 1 < len(units) and len(context) < 900:
            nxt = units[idx + 1]
            if temporal_topic_match_score(topic, nxt):
                context = f"{context} {nxt}"
        scored.append((score, -idx, context))
    scored.sort(reverse=True)
    chosen = sorted(scored[:max_passages], key=lambda x: -x[1])
    # Stable de-duplication.
    out: list[str] = []
    seen: set[str] = set()
    for _, _, unit in chosen:
        key = re.sub(r"\W+", " ", unit.lower()).strip()[:300]
        if key and key not in seen:
            seen.add(key)
            out.append(unit)
    return out


def best_topic_passage(text: str, topic: str) -> tuple[str | None, int]:
    best: tuple[tuple[int, int, int], str] | None = None
    for unit in split_evidence_units(text):
        topic_score = topic_match_score(topic, unit)
        if not topic_score:
            continue
        cue_score = exposure_cue_score(unit)
        # Longer context is useful only as a final tie-breaker.
        score = (topic_score, cue_score, min(len(unit), 1000))
        if best is None or score > best[0]:
            best = (score, unit)
    return (best[1], best[0][0] + min(best[0][1], 3)) if best else (None, 0)


def infer_risk_topics_from_question(question: str, topics: list[str] | None = None) -> list[str]:
    q = question or ""
    candidates = topics or list(TOPIC_PATTERNS)
    scored: list[tuple[int, str]] = []
    for topic in candidates:
        score = temporal_topic_match_score(topic, q)
        # Exact canonical name is a strong signal.
        if topic.lower() in q.lower():
            score += 3
        if score:
            scored.append((score, topic))
    scored.sort(reverse=True)
    return [topic for _, topic in scored]
