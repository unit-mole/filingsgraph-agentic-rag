from __future__ import annotations
import hashlib
from filingsgraph.schemas.documents import DocumentChunk, FilingSection
from filingsgraph.schemas.filings import FilingMetadata
from filingsgraph.parsing.normalization import normalize_text

def _window_long(text: str, target: int, overlap: int) -> list[str]:
    if len(text) <= target:
        return [text]
    step = max(1, target - overlap)
    return [text[i : i + target] for i in range(0, len(text), step) if text[i : i + target].strip()]

def section_aware_chunks(
    section: FilingSection,
    meta: FilingMetadata,
    target_chars: int = 3500,
    overlap_chars: int = 500,
) -> list[DocumentChunk]:
    paragraphs = [normalize_text(p) for p in section.text.split("\n\n") if normalize_text(p)]
    units = []
    for p in paragraphs:
        units.extend(_window_long(p, target_chars, overlap_chars) if len(p) > target_chars else [p])

    groups = []
    current = ""
    for unit in units:
        if current and len(current) + 2 + len(unit) > target_chars:
            groups.append(current)
            tail = current[-overlap_chars:] if overlap_chars else ""
            current = (tail + "\n\n" + unit).strip()
            if len(current) > target_chars:
                current = current[-target_chars:]
        else:
            current = (current + "\n\n" + unit).strip()
    if current:
        groups.append(current)

    out = []
    for i, text in enumerate(groups):
        content_hash = hashlib.sha256(text.encode()).hexdigest()
        chunk_id = hashlib.sha1(
            f"{meta.accession_number}:{section.section}:{i}:{content_hash}".encode()
        ).hexdigest()[:20]
        out.append(
            DocumentChunk(
                chunk_id=chunk_id,
                document_id=section.document_id,
                cik=meta.cik,
                ticker=meta.ticker,
                company_name=meta.company_name,
                form_type=meta.form_type,
                accession_number=meta.accession_number,
                filing_date=meta.filing_date,
                report_date=meta.report_date,
                fiscal_year=meta.fiscal_year,
                fiscal_period=meta.fiscal_period,
                section=section.section,
                page_or_html_location=section.html_location,
                source_url=meta.source_url,
                content_hash=content_hash,
                text=text,
                parent_text=section.text[:5000],
            )
        )
    return out
