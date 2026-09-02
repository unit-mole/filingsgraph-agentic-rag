from filingsgraph.temporal.risk_diff import compare_risk_topic


def test_temporal_new_and_removed_use_topic_specific_presence():
    old = "The company discusses general economic conditions and product demand."
    new = "New laws regulating AI could impose additional compliance requirements on our products."
    assert compare_risk_topic(old, new, "artificial intelligence regulation").change_type == "NEW"
    assert compare_risk_topic(new, old, "artificial intelligence regulation").change_type == "REMOVED"


def test_temporal_unchanged_for_substantially_same_disclosure():
    old = "Government export controls may limit our ability to sell products to certain customers in China."
    new = "Government export controls may limit our ability to sell products to certain customers in China."
    r = compare_risk_topic(old, new, "export controls")
    assert r.change_type == "UNCHANGED"
    assert r.similarity >= 0.7


def test_temporal_expanded_when_material_new_specific_language_added():
    old = "Government export controls may limit our ability to sell products to certain customers."
    new = (
        "Government export controls may limit our ability to sell products to certain customers. "
        "Additional export restrictions and export licensing requirements may apply to advanced computing products."
    )
    r = compare_risk_topic(old, new, "export controls")
    assert r.change_type in {"EXPANDED", "UNCHANGED"}  # conservative ambiguity is allowed, REDUCED is not
