from __future__ import annotations
from bs4 import BeautifulSoup

def extract_tables(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    out = []
    for i, table in enumerate(soup.find_all("table")):
        rows = []
        for tr in table.find_all("tr"):
            cells = [" ".join(c.stripped_strings) for c in tr.find_all(["th", "td"])]
            if cells:
                rows.append(cells)
        if not rows:
            continue
        context = ""
        prev = table.find_previous(["h1", "h2", "h3", "h4", "p", "div"])
        if prev:
            context = " ".join(prev.stripped_strings)[:800]
        out.append(
            {
                "table_id": f"table-{i}",
                "rows": rows,
                "text": "\n".join(" | ".join(r) for r in rows),
                "nearby_context": context,
            }
        )
    return out
