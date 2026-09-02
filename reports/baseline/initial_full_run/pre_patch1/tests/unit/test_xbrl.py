import json
from filingsgraph.xbrl.concepts import normalize_concept
from filingsgraph.xbrl.facts import parse_companyfacts

def test_concept_map():
    assert normalize_concept("NetIncomeLoss")[0] == "net_income"

def test_companyfacts_fixture(tmp_path):
    data = {"cik": 123, "facts": {"us-gaap": {"RevenueFromContractWithCustomerExcludingAssessedTax": {"label": "Revenue", "units": {"USD": [{"val": 100, "start": "2024-01-01", "end": "2024-12-31", "fy": 2024, "fp": "FY", "form": "10-K", "accn": "a", "filed": "2025-01-01"}]}}}}}
    p = tmp_path / "f.json"
    p.write_text(json.dumps(data))
    facts = parse_companyfacts(p, "TEST")
    assert len(facts) == 1 and facts[0].normalized_metric == "revenue" and facts[0].fiscal_year == 2024
