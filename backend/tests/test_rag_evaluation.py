from app.services.rag import hybrid_retrieve
from app.services.recommendations import personalized_recommendations
from evaluation.metrics import evaluate

def test_retrieval_returns_ranked_citations():
    hits=hybrid_retrieve("climate change mitigation greenhouse gas emissions",5)
    assert hits
    assert all("source" in hit and "id" in hit for hit in hits)
    assert hits[0]["relevance"] >= hits[-1]["relevance"]

def test_personalization_is_deterministic_and_bounded():
    result=personalized_recommendations(None,[],["biodiversity","nature"])
    assert len(result)==4
    assert result[0]["course_slug"]=="biodiversity"

def test_offline_retrieval_metrics_are_computable():
    metrics=evaluate()
    assert metrics["queries"]==8
    assert 0 <= metrics["recall_at_k"] <= 1
