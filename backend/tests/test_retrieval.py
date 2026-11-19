from app.services.retrieval import retrieve, recommend

def test_retrieval_returns_relevant_climate_passage():
    results = retrieve("greenhouse gas emissions and climate mitigation")
    assert results
    returned_ids = {item["id"] for item in results}
    assert returned_ids.intersection({"climate-01", "ipcc-ar6-syr", "unep-emissions-gap-2024", "our-world-in-data-co2"})

def test_recommendation_limit_is_respected():
    assert len(recommend("biodiversity", limit=2)) <= 2

def test_unrelated_query_returns_no_results():
    assert retrieve("quantum entanglement in superconductors") == []
