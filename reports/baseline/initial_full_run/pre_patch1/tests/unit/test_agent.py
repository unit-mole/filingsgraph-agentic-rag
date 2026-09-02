from filingsgraph.agents.router import classify_query
from filingsgraph.agents.planner import plan

def test_router_numeric(): assert classify_query("What was revenue growth?") == "NUMERIC"
def test_router_temporal(): assert classify_query("How did risk language change over time?") == "TEMPORAL"
def test_router_graph(): assert classify_query("Which segments are connected to export risk?") == "GRAPH"
def test_router_mixed(): assert classify_query("How did revenue change while risk language evolved?") == "MIXED"
def test_plan_tools():
    p = plan("How did revenue change while risk language evolved?", ["NVDA"], [2024, 2025])
    assert p.use_xbrl and p.use_temporal
