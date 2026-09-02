from __future__ import annotations
from bs4 import BeautifulSoup

BLOCK_TAGS = ["p", "div", "li", "h1", "h2", "h3", "h4", "h5", "h6"]

def parse_html(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")

def html_to_blocks(html: str) -> list[dict]:
    soup = parse_html(html)
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    blocks = []
    seen = set()
    for i, tag in enumerate(soup.find_all(BLOCK_TAGS)):
        text = " ".join(tag.stripped_strings)
        text = " ".join(text.split())
        if len(text) < 2 or text in seen:
            continue
        seen.add(text)
        blocks.append({"index": i, "tag": tag.name, "text": text, "id": tag.get("id")})
    return blocks

def html_to_text(html: str) -> str:
    return "\n\n".join(b["text"] for b in html_to_blocks(html))
