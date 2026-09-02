from filingsgraph.agents.router import classify_query
from filingsgraph.agents.planner import plan


def test_router_numeric():
    assert classify_query("What was NVDA revenue in FY2025?") == "NUMERIC"


def test_router_temporal():
    assert classify_query("How did risk language change over time?") == "TEMPORAL"


def test_router_graph():
    assert classify_query("Which segments are connected to export risk?") == "GRAPH"


def test_router_mixed():
    assert classify_query("How did revenue change while risk language evolved?") == "MIXED"


def test_router_textual_finance_vocabulary_is_not_automatically_numeric():
    assert classify_query("What concerns did management describe about revenue concentration?") == "TEXTUAL"


def test_plan_tools():
    p = plan("How did revenue change while risk language evolved?", ["NVDA"], [2024, 2025])
    assert p.use_xbrl and p.use_temporal


def test_router_graph_benchmark_template():
    assert classify_query("Which selected companies share exposure to export controls risk in FY2025, and what filing evidence connects them?") == "GRAPH"


def test_router_textual_disclosure_with_financial_word():
    assert classify_query("What did NVDA disclose in FY2025 Item 7 about revenue concentration demand?") == "TEXTUAL"


def test_plan_resolves_explicit_ticker():
    p = plan("What did NVDA disclose in FY2025 Item 1A about export controls?", None, None)
    assert p.entities == ["NVDA"]
    assert p.periods == [2025]


def test_plan_resolves_selected_company_graph_to_cohort():
    p = plan("Which selected companies share exposure to export controls risk in FY2025, and what filing evidence connects them?", None, None)
    assert p.query_type == "GRAPH"
    assert set(p.entities) >= {"NVDA", "AMD", "INTC", "AVGO", "QCOM"}
