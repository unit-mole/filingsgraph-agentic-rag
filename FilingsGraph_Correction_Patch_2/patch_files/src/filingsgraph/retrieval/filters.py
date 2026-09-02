from __future__ import annotations

import re


def matches_filters(payload: dict, filters: dict | None) -> bool:
    if not filters:
        return True
    for key, val in filters.items():
        actual = payload.get(key)
        if isinstance(val, (list, tuple, set)):
            if actual not in val:
                return False
        elif actual != val:
            return False
    return True


def infer_query_filters(question: str, known_tickers: list[str] | None = None) -> dict:
    """Infer only explicit metadata constraints present in the user question.

    This intentionally does not use benchmark gold fields. It extracts ticker,
    fiscal year and SEC Item references that a production query parser can
    observe directly from the question text.
    """
    q = " ".join(question.split())
    out: dict = {}
    known = [str(t).upper() for t in (known_tickers or [])]
    found = [t for t in known if re.search(rf"\b{re.escape(t)}\b", q, flags=re.I)]
    if len(found) == 1:
        out["ticker"] = found[0]

    years = sorted({int(y) for y in re.findall(r"\bFY\s*(20\d{2})\b", q, flags=re.I)})
    if len(years) == 1:
        out["fiscal_year"] = years[0]
    elif len(years) > 1:
        out["fiscal_year"] = years

    m = re.search(r"\bItem\s+(1A|7A|1|7|8)\b", q, flags=re.I)
    if m:
        out["section"] = f"Item {m.group(1).upper()}"
    return out
