from filingsgraph.parsing.sections import extract_sections, normalize_item
from filingsgraph.parsing.tables import extract_tables
from filingsgraph.parsing.chunking import section_aware_chunks
from filingsgraph.schemas.documents import FilingSection
from filingsgraph.schemas.filings import FilingMetadata

def fixture_html():
    risk = "Risk disclosure detail. " * 30
    discussion = "Discussion detail. " * 30
    financial = "Financial detail. " * 30
    return f"""<html><body><h2>Item 1A. Risk Factors</h2><p>Supply chain disruption and export controls may materially affect operations. {risk}</p><table><tr><th>Metric</th><th>2025</th></tr><tr><td>Revenue</td><td>100</td></tr></table><h2>Item 7. Management Discussion</h2><p>Management discusses demand and capital expenditure. {discussion}</p><h2>Item 8. Financial Statements</h2><p>Financial statements and notes. {financial}</p></body></html>"""

def test_item_normalization(): assert normalize_item("Item 1A. Risk Factors") == "Item 1A"
def test_section_extraction():
    s = extract_sections(fixture_html(), "doc", ["Item 1A", "Item 7"])
    assert {x.section for x in s} == {"Item 1A", "Item 7"}
def test_table_context():
    t = extract_tables(fixture_html())
    assert t and t[0]["rows"][1][0] == "Revenue"
def test_oversized_chunk_is_bounded():
    sec = FilingSection(section_id="s", document_id="d", section="Item 1A", text="A " * 6000)
    meta = FilingMetadata(cik="0000000001", ticker="T", company_name="Test", form_type="10-K", accession_number="a", filing_date="2025-01-01", primary_document="x.htm", source_url="https://www.sec.gov/x")
    chunks = section_aware_chunks(sec, meta, target_chars=1000, overlap_chars=100)
    assert chunks and max(len(c.text) for c in chunks) <= 1000
