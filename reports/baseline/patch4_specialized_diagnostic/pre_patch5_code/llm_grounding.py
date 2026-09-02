from __future__ import annotations

import re

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
    # Markdown table separator.
    if re.fullmatch(r"\|?[\s:|-]+\|?", s):
        return True
    return False


def _explicit_limitation(line: str) -> bool:
    s = re.sub(r"^[-*+]\s+", "", line.strip()).lower()
    return any(s.startswith(x) for x in _LIMITATION_PREFIXES)


def enforce_grounding_contract(answer: str, evidence: list[dict]) -> str:
    """Remove generated factual lines that do not carry a valid supplied citation.

    This guard never invents or auto-attaches a citation. It preserves structural
    Markdown and explicit insufficiency statements, retains factual lines only when
    they already cite a valid evidence ID, and removes invalid citation IDs.
    """
    available = {str(e.get("citation_id")) for e in evidence if e.get("citation_id")}
    kept: list[str] = []
    factual_kept = 0
    for raw in (answer or "").splitlines():
        line = raw.rstrip()
        if _structural(line) or _explicit_limitation(line):
            kept.append(line)
            continue

        ids = extract_citations(line)
        valid = [cid for cid in ids if cid in available]
        if not valid:
            continue

        # Strip hallucinated citation tokens while retaining valid supplied IDs.
        def repl(match: re.Match[str]) -> str:
            cid = match.group(1)
            return match.group(0) if cid in available else ""

        cleaned = re.sub(r"\[([A-Za-z0-9][A-Za-z0-9_.:-]*)\]", repl, line)
        cleaned = re.sub(r"\s{2,}", " ", cleaned).rstrip()
        if cleaned:
            kept.append(cleaned)
            factual_kept += 1

    # Prevent a heading-only answer. This is an epistemic fallback, not a factual claim.
    if factual_kept == 0:
        return "## Important Limitations\nEvidence is insufficient to produce a fully cited answer under the strict grounding policy."

    # Collapse excessive blank lines left after filtering.
    out: list[str] = []
    for line in kept:
        if not line.strip() and (not out or not out[-1].strip()):
            continue
        out.append(line)
    return "\n".join(out).strip()
