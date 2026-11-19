"""Hybrid retrieval + optional hosted LLM answer synthesis with source-constrained citations."""
import os
import re
import json
import urllib.request
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.data.knowledge import KNOWLEDGE

def _tokens(text):
    return re.findall(r"[a-z0-9]+", text.lower())

def hybrid_retrieve(query: str, limit: int = 5):
    docs = KNOWLEDGE
    corpus = [f"{d['title']} {d.get('topic','')} {d['text']}" for d in docs]
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1,2), sublinear_tf=True)
    matrix = vectorizer.fit_transform(corpus)
    q = vectorizer.transform([query])
    dense = cosine_similarity(q, matrix).ravel()
    terms = _tokens(query)
    bm25 = []
    for doc, text in zip(docs, corpus):
        tokens = _tokens(text); counts = Counter(tokens)
        overlap = sum(min(counts[t], 2) for t in set(terms))
        bm25.append(overlap / max(1, len(tokens) ** 0.35))
    max_bm = max(bm25, default=1) or 1
    ranked = []
    for i, doc in enumerate(docs):
        score = 0.55 * float(dense[i]) + 0.45 * (bm25[i] / max_bm)
        if score > 0.015:
            ranked.append({**doc, "relevance":round(score,4)})
    return sorted(ranked, key=lambda item:item["relevance"], reverse=True)[:limit]

def answer_with_sources(question: str, hits: list):
    if not hits:
        return {"answer":"I could not retrieve sufficiently relevant evidence from the current curated corpus. Try a narrower question.","sources":[],"grounded":False,"model":"retrieval-only"}
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {"answer":"I found relevant source material, but generative answering is not configured. Review the cited excerpts below; no unsupported synthesis has been generated.","sources":hits,"grounded":True,"model":"retrieval-only"}
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    context = "\n\n".join(f"[{i+1}] {h['title']} | {h.get('source','')}\n{h['text']}" for i,h in enumerate(hits))
    prompt = ("Answer only from the supplied evidence. If evidence is insufficient, say so. "
              "Cite factual claims inline as [1], [2] matching the supplied sources. "
              "Do not invent statistics, dates, or citations. Explain uncertainty.\n\n"
              f"Evidence:\n{context}\n\nQuestion: {question}")
    body = json.dumps({"model":model,"temperature":0.1,"messages":[{"role":"system","content":"You are EcoScholar, an evidence-grounded sustainability tutor."},{"role":"user","content":prompt}]}).encode()
    request = urllib.request.Request("https://api.openai.com/v1/chat/completions", data=body, headers={"Authorization":f"Bearer {api_key}","Content-Type":"application/json"})
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            data = json.loads(response.read())
        answer = data["choices"][0]["message"]["content"]
        return {"answer":answer,"sources":hits,"grounded":True,"model":model}
    except Exception:
        # Fail closed: return evidence, never fabricate a model answer.
        return {"answer":"The language model could not be reached. The retrieved evidence is provided below for manual review.","sources":hits,"grounded":True,"model":"retrieval-fallback"}
