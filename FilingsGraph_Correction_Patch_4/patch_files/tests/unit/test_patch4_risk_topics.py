from filingsgraph.risk_topics import best_topic_passage, topic_match_score


def test_export_controls_requires_specific_export_language():
    weak = "We are subject to complex laws and regulations in many jurisdictions."
    strong = "The USG may change export control rules and impose additional export restrictions on our products."
    assert topic_match_score("export controls", weak) == 0
    assert topic_match_score("export controls", strong) >= 1


def test_ai_regulation_does_not_match_generic_ai_or_generic_regulation():
    assert topic_match_score("artificial intelligence regulation", "Demand for artificial intelligence products is growing.") == 0
    assert topic_match_score("artificial intelligence regulation", "We are subject to changing environmental regulations.") == 0
    assert topic_match_score("artificial intelligence regulation", "New laws regulating AI could increase compliance costs.") >= 1


def test_competition_does_not_match_regulatory_laundry_list():
    text = "Laws affect areas including privacy; competition; advertising; employment; and environmental matters."
    assert topic_match_score("competition", text) == 0
    assert topic_match_score("competition", "Competition could adversely impact our market share and financial results.") >= 1


def test_supply_chain_matches_reliable_supply_language():
    text = "Our business depends on our ability to receive consistent and reliable supply from overseas partners."
    span, score = best_topic_passage(text, "supply chain")
    assert span
    assert score >= 1
