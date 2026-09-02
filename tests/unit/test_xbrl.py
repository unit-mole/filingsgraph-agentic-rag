import json
from filingsgraph.schemas.financial_facts import FinancialFact
from filingsgraph.xbrl.concepts import normalize_concept
from filingsgraph.xbrl.facts import parse_companyfacts, choose_annual_fact


def test_concept_map():
    assert normalize_concept("NetIncomeLoss")[0] == "net_income"


def test_companyfacts_fixture(tmp_path):
    data = {"cik": 123, "facts": {"us-gaap": {"RevenueFromContractWithCustomerExcludingAssessedTax": {"label": "Revenue", "units": {"USD": [{"val": 100, "start": "2024-01-01", "end": "2024-12-31", "fy": 2024, "fp": "FY", "form": "10-K", "accn": "a", "filed": "2025-01-01"}]}}}}}
    p = tmp_path / "f.json"
    p.write_text(json.dumps(data))
    facts = parse_companyfacts(p, "TEST")
    assert len(facts) == 1 and facts[0].normalized_metric == "revenue" and facts[0].fiscal_year == 2024


def test_choose_annual_fact_prefers_target_accession_and_annual_duration():
    base = dict(
        cik="0000000001", ticker="TEST", concept="Revenues", label="Revenue", taxonomy="us-gaap",
        unit="USD", raw_value=100.0, scale=1.0, normalized_value=100.0, end_date="2024-12-31",
        fiscal_year=2024, fiscal_period="FY", form_type="10-K", filed_date="2025-02-01",
        normalized_metric="revenue", mapping_method="deterministic_map", mapping_confidence=1.0,
    )
    quarterly = FinancialFact(**base, start_date="2024-10-01", accession_number="target")
    annual_wrong_accession = FinancialFact(**base, start_date="2024-01-01", accession_number="later-comparative")
    annual_target = FinancialFact(**base, start_date="2024-01-01", accession_number="target")
    got = choose_annual_fact(
        [quarterly, annual_wrong_accession, annual_target],
        "revenue",
        2024,
        target_accession="target",
        target_report_date="2024-12-31",
    )
    assert got is not None and got.accession_number == "target" and got.start_date == "2024-01-01"
