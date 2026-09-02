from filingsgraph.retrieval.filters import infer_query_filters, matches_filters


def test_infer_explicit_metadata_filters():
    f = infer_query_filters("What did NVDA disclose in FY2025 Item 1A about export controls?", ["NVDA", "AMD"])
    assert f == {"ticker": "NVDA", "fiscal_year": 2025, "section": "Item 1A"}


def test_infer_temporal_year_list():
    f = infer_query_filters("How did AMD risk disclosure change from FY2024 to FY2025?", ["NVDA", "AMD"])
    assert f["ticker"] == "AMD"
    assert f["fiscal_year"] == [2024, 2025]


def test_infer_graph_does_not_force_single_company():
    f = infer_query_filters("Which selected companies share exposure to supply chain risk in FY2025?", ["NVDA", "AMD"])
    assert "ticker" not in f
    assert f["fiscal_year"] == 2025


def test_matches_list_filter():
    assert matches_filters({"fiscal_year": 2025}, {"fiscal_year": [2024, 2025]})
    assert not matches_filters({"fiscal_year": 2023}, {"fiscal_year": [2024, 2025]})
