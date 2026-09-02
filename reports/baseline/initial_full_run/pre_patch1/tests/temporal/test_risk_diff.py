import pytest
from filingsgraph.temporal.risk_diff import compare_risk_topic
from filingsgraph.temporal.alignment import validate_period_pair

def test_new_risk():
    c = compare_risk_topic("", "Export controls may limit shipments to certain regions and materially affect revenue.", "export controls")
    assert c.change_type == "NEW"
def test_removed_risk():
    c = compare_risk_topic("Supply chain disruption may affect production materially.", "", "supply chain")
    assert c.change_type == "REMOVED"
def test_period_order():
    with pytest.raises(ValueError): validate_period_pair(2025, 2024)
