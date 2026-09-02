from __future__ import annotations

import hashlib
import re
from collections import defaultdict

from filingsgraph.schemas.documents import FilingSection
from filingsgraph.parsing.html import html_to_blocks

ITEM_PATTERN = re.compile(
    r"^\s*item\s+(1a|1b|1c|1|2|3|4|5|6|7a|7|8|9a|9b|9c|9|10|11|12|13|14|15|16)\b",
    re.I,
)

# Some issuers (notably Intel in recent annual reports) organize the 10-K with
# semantic headings rather than repeating the traditional Item labels in the
# body. These aliases are intentionally conservative and are only considered
# for heading-like/short blocks. Explicit Item headings always receive higher
# priority.
SECTION_ALIASES: dict[str, tuple[re.Pattern[str], ...]] = {
    "Item 1": (
        re.compile(r"^(our\s+)?business(?:\s+overview)?$", re.I),
    ),
    "Item 1A": (
        re.compile(r"^risk\s+factors(?:\s+and\s+other\s+considerations)?$", re.I),
        re.compile(r"^principal\s+risks?$", re.I),
    ),
    "Item 7": (
        re.compile(r"^management(?:'|’)?s\s+discussion\s+and\s+analysis(?:\s+of\s+financial\s+condition\s+and\s+results\s+of\s+operations)?$", re.I),
        re.compile(r"^financial\s+condition\s+and\s+results\s+of\s+operations$", re.I),
        re.compile(r"^consolidated\s+results\s+of\s+operations$", re.I),
        re.compile(r"^results\s+of\s+operations$", re.I),
    ),
    "Item 7A": (
        re.compile(r"^quantitative\s+and\s+qualitative\s+disclosures\s+about\s+market\s+risk$", re.I),
        re.compile(r"^market\s+risk$", re.I),
    ),
    "Item 8": (
        re.compile(r"^financial\s+statements\s+and\s+supplementary\s+data$", re.I),
        re.compile(r"^financial\s+statements\s+and\s+supplemental\s+(?:data|details)$", re.I),
        re.compile(r"^consolidated\s+financial\s+statements(?:\s+and\s+notes)?$", re.I),
        re.compile(r"^financial\s+statements$", re.I),
    ),
}


def _clean_heading(text: str) -> str:
    text = " ".join(text.split()).strip()
    text = re.sub(r"^[\u2022\-–—:;|]+\s*", "", text)
    text = re.sub(r"\s+[.·•\-–—]+\s*\d+\s*$", "", text)
    return text.strip(" :;.-–—")


def normalize_item(text: str) -> str | None:
    m = ITEM_PATTERN.search(_clean_heading(text))
    if not m:
        return None
    return f"Item {m.group(1).upper()}"


def normalize_alias(text: str) -> str | None:
    cleaned = _clean_heading(text)
    for item, patterns in SECTION_ALIASES.items():
        if any(p.fullmatch(cleaned) for p in patterns):
            return item
    return None


def _heading_like(block: dict) -> bool:
    text = block.get("text", "")
    tag = str(block.get("tag", ""))
    if tag.startswith("h"):
        return True
    # SEC filings frequently encode visual headings as divs/p elements.
    return len(text) <= 180


def _candidate_markers(blocks: list[dict]) -> list[tuple[int, str, str, int]]:
    """Return (block_index, canonical_item, title, priority).

    priority=2 is an explicit SEC Item heading, priority=1 is a semantic alias.
    """
    out: list[tuple[int, str, str, int]] = []
    for i, block in enumerate(blocks):
        if not _heading_like(block):
            continue
        text = block.get("text", "")
        explicit = normalize_item(text)
        if explicit:
            out.append((i, explicit, text, 2))
            continue
        alias = normalize_alias(text)
        if alias:
            out.append((i, alias, text, 1))
    return out


def extract_sections(
    html: str,
    document_id: str,
    target_items: list[str] | None = None,
) -> list[FilingSection]:
    blocks = html_to_blocks(html)
    target = {x.lower() for x in target_items} if target_items else None
    candidates = _candidate_markers(blocks)
    if not candidates:
        return []

    # Estimate each candidate's body span using the next recognized section
    # marker. We then pick the best occurrence per canonical item. This avoids
    # table-of-contents hits, whose spans are usually tiny, and prefers an
    # explicit Item heading over an alias whenever both exist.
    scored: dict[str, list[tuple[int, str, str, int, int]]] = defaultdict(list)
    for pos, (idx, item, title, priority) in enumerate(candidates):
        nxt = candidates[pos + 1][0] if pos + 1 < len(candidates) else len(blocks)
        span_len = sum(len(x.get("text", "")) for x in blocks[idx + 1 : nxt])
        scored[item].append((idx, item, title, priority, span_len))

    best: dict[str, tuple[int, str, str, int, int]] = {}
    for item, rows in scored.items():
        # Priority dominates. Within a priority tier, choose the occurrence with
        # the largest substantive body span.
        rows.sort(key=lambda x: (x[3], x[4]), reverse=True)
        best[item] = rows[0]

    selected = sorted(best.values(), key=lambda x: x[0])
    sections: list[FilingSection] = []
    for pos, (idx, item, title, _priority, _span_len) in enumerate(selected):
        if target and item.lower() not in target:
            continue
        next_idx = selected[pos + 1][0] if pos + 1 < len(selected) else len(blocks)
        text = "\n\n".join(b.get("text", "") for b in blocks[idx + 1 : next_idx]).strip()
        if len(text) < 100:
            continue
        sid = hashlib.sha1(f"{document_id}:{item}".encode()).hexdigest()[:16]
        sections.append(
            FilingSection(
                section_id=sid,
                document_id=document_id,
                section=item,
                title=title,
                text=text,
                html_location=f"block:{idx}",
            )
        )
    return sections
