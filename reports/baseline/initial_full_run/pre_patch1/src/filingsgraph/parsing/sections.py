from __future__ import annotations
import hashlib
import re
from filingsgraph.schemas.documents import FilingSection
from filingsgraph.parsing.html import html_to_blocks

ITEM_PATTERN = re.compile(r"^\s*item\s+(1a|1b|1c|1|2|3|4|5|6|7a|7|8|9a|9b|9c|9|10|11|12|13|14|15|16)\b", re.I)

def normalize_item(text: str) -> str | None:
    m = ITEM_PATTERN.search(text.strip())
    if not m:
        return None
    return f"Item {m.group(1).upper()}"

def extract_sections(html: str, document_id: str, target_items: list[str] | None = None) -> list[FilingSection]:
    blocks = html_to_blocks(html)
    target = {x.lower() for x in target_items} if target_items else None
    candidates: list[tuple[int, str, str]] = []
    for i, b in enumerate(blocks):
        item = normalize_item(b["text"])
        if item and (b["tag"].startswith("h") or len(b["text"]) < 220):
            candidates.append((i, item, b["text"]))

    best: dict[str, tuple[int, str, str, int]] = {}
    for pos, (idx, item, title) in enumerate(candidates):
        nxt = candidates[pos + 1][0] if pos + 1 < len(candidates) else len(blocks)
        span_len = sum(len(x["text"]) for x in blocks[idx + 1 : nxt])
        if item not in best or span_len > best[item][3]:
            best[item] = (idx, item, title, span_len)

    selected = sorted(best.values(), key=lambda x: x[0])
    sections = []
    for pos, (idx, item, title, _) in enumerate(selected):
        if target and item.lower() not in target:
            continue
        next_idx = selected[pos + 1][0] if pos + 1 < len(selected) else len(blocks)
        text = "\n\n".join(b["text"] for b in blocks[idx + 1 : next_idx]).strip()
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
