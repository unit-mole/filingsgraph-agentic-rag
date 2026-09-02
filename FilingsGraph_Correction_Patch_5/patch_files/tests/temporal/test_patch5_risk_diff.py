from filingsgraph.temporal.risk_diff import compare_risk_topic


def test_export_reduction_keeps_topic_present():
    old = "Export regulations and trade measures may limit our ability to export products to certain customers."
    new = "Government regulations may limit our ability to export products to certain customers."
    assert compare_risk_topic(old, new, "export controls").change_type in {"REDUCED", "UNCHANGED"}


def test_ai_export_control_language_counts_as_ai_regulatory_presence():
    old = "General economic conditions may affect demand."
    new = "The US increased export controls on artificial intelligence and advanced computing products."
    assert compare_risk_topic(old, new, "artificial intelligence regulation").change_type == "NEW"
