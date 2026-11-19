from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.data.knowledge import KNOWLEDGE

_CORPUS = [f"{d['title']} {d['topic']} {d['text']}" for d in KNOWLEDGE]
_VECTOR = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
_MATRIX = _VECTOR.fit_transform(_CORPUS)

def retrieve(query: str, limit: int = 3):
    q = _VECTOR.transform([query])
    scores = cosine_similarity(q, _MATRIX).ravel()
    ranked = scores.argsort()[::-1][:limit]
    return [{**KNOWLEDGE[i], "relevance": round(float(scores[i]), 4)} for i in ranked if scores[i] > 0]

def recommend(topic: str, limit: int = 3):
    return retrieve(topic, limit)
