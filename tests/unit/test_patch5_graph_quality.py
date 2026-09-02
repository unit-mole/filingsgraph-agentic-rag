from filingsgraph.graph.extraction import graph_evidence_quality


def test_manufacturing_legal_injunction_is_rejected():
    text = "Litigation could result in an injunction stopping us from manufacturing or selling certain products."
    assert graph_evidence_quality("semiconductor manufacturing", text) == 0.0


def test_manufacturing_foundry_disruption_is_retained():
    text = "Geopolitical changes could disrupt our wafer foundries and manufacturing facilities and adversely affect delivery."
    assert graph_evidence_quality("semiconductor manufacturing", text) > 0


def test_regulatory_laundry_list_is_not_competition_exposure():
    text = "Laws affect areas including privacy; competition; advertising; employment; and environmental matters."
    assert graph_evidence_quality("competition", text) == 0.0
