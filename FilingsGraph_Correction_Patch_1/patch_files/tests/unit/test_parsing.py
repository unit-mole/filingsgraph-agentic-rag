from filingsgraph.parsing.sections import extract_sections, normalize_item, normalize_alias
from filingsgraph.parsing.tables import extract_tables
from filingsgraph.parsing.chunking import section_aware_chunks
from filingsgraph.schemas.documents import FilingSection
from filingsgraph.schemas.filings import FilingMetadata


def fixture_html():
    risk = "Risk disclosure detail. " * 30
    discussion = "Discussion detail. " * 30
    financial = "Financial detail. " * 30
    return f"""<html><body><h2>Item 1A. Risk Factors</h2><p>Supply chain disruption and export controls may materially affect operations. {risk}</p><table><tr><th>Metric</th><th>2025</th></tr><tr><td>Revenue</td><td>100</td></tr></table><h2>Item 7. Management Discussion</h2><p>Management discusses demand and capital expenditure. {discussion}</p><h2>Item 8. Financial Statements</h2><p>Financial statements and notes. {financial}</p></body></html>"""


def intel_style_html():
    business = "Intel business description and operating model. " * 30
    risk = "Export controls and supply chain constraints create risks. " * 35
    results = "Consolidated results include revenue and operating performance. " * 35
    market = "Interest rate and currency market risk discussion. " * 25
    fin = "Consolidated financial statements and supplemental details. " * 35
    return f"""<html><body>
    <div>Table of Contents</div><div>Risk Factors .... 18</div>
    <h1>Business</h1><p>{business}</p>
    <h1>Risk Factors</h1><p>{risk}</p>
    <h1>Consolidated Results of Operations</h1><p>{results}</p>
    <h1>Market Risk</h1><p>{market}</p>
    <h1>Financial Statements and Supplemental Details</h1><p>{fin}</p>
    </body></html>"""


def test_item_normalization():
    assert normalize_item("Item 1A. Risk Factors") == "Item 1A"


def test_alias_normalization():
    assert normalize_alias("Risk Factors") == "Item 1A"
    assert normalize_alias("Consolidated Results of Operations") == "Item 7"
    assert normalize_alias("Financial Statements and Supplemental Details") == "Item 8"


def test_section_extraction():
    s = extract_sections(fixture_html(), "doc", ["Item 1A", "Item 7"])
    assert {x.section for x in s} == {"Item 1A", "Item 7"}


def test_nonstandard_semantic_heading_extraction():
    s = extract_sections(intel_style_html(), "intel-doc", ["Item 1", "Item 1A", "Item 7", "Item 7A", "Item 8"])
    assert {x.section for x in s} == {"Item 1", "Item 1A", "Item 7", "Item 7A", "Item 8"}
    risk = next(x for x in s if x.section == "Item 1A")
    assert "Export controls" in risk.text


def test_table_context():
    t = extract_tables(fixture_html())
    assert t and t[0]["rows"][1][0] == "Revenue"


def test_oversized_chunk_is_bounded():
    sec = FilingSection(section_id="s", document_id="d", section="Item 1A", text="A " * 6000)
    meta = FilingMetadata(cik="0000000001", ticker="T", company_name="Test", form_type="10-K", accession_number="a", filing_date="2025-01-01", primary_document="x.htm", source_url="https://www.sec.gov/x")
    chunks = section_aware_chunks(sec, meta, target_chars=1000, overlap_chars=100)
    assert chunks and max(len(c.text) for c in chunks) <= 1000
