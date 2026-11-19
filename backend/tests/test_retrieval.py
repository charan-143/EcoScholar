from app.services.retrieval import retrieve, recommend


def test_retrieval_returns_relevant_climate_passage():
    results = retrieve("greenhouse gas emissions and climate mitigation")
    assert results
    assert results[0]["id"] == "climate-01"
    assert results[0]["relevance"] > 0


def test_recommendation_respects_limit():
    results = recommend("biodiversity", limit=2)
    assert len(results) <= 2
    assert results
    assert results[0]["id"] == "biodiversity-01"


def test_unknown_query_returns_no_unrelated_passages():
    assert retrieve("quantum entanglement in particle accelerators") == []
