from __future__ import annotations
import re

def fiscal_year_from_frame(frame: str | None, end_date: str | None, fallback_fy: int | None) -> int | None:
    # Company Facts `fy` is useful but comparative facts can be repeated in later filings.
    # build_database.py therefore performs the stronger normalization by matching fact end_date
    # to downloaded 10-K report dates. This function is the ingestion fallback only.
    if fallback_fy is not None:
        return int(fallback_fy)
    if frame:
        m = re.match(r"CY(\d{4})", frame)
        if m:
            return int(m.group(1))
    if end_date and len(end_date) >= 4 and end_date[:4].isdigit():
        return int(end_date[:4])
    return None

def fiscal_period_from_frame(frame: str | None, fp: str | None) -> str | None:
    if fp:
        return fp
    if frame:
        for q in ["Q1", "Q2", "Q3", "Q4"]:
            if q in frame:
                return q
        return "FY"
    return None
