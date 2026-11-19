"""Hybrid TF-IDF + BM25 retrieval and optional citation-checked LLM synthesis."""
import os, re, json, urllib.request
from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.data.knowledge import KNOWLEDGE

def _tokens(text):
    return re.findall(r"[a-z0-9]+", text.lower())

def hybrid_retrieve(query: str, limit: int = 5):
    docs=KNOWLEDGE
    corpus=[f"{d['title']} {d.get('topic','')} {d['text']}" for d in docs]
    tokenized=[_tokens(text) for text in corpus]
    query_tokens=_tokens(query)
    if not query_tokens: return []
    vectorizer=TfidfVectorizer(stop_words="english",ngram_range=(1,2),sublinear_tf=True)
    matrix=vectorizer.fit_transform(corpus)
    dense=cosine_similarity(vectorizer.transform([query]),matrix).ravel()
    bm25=BM25Okapi(tokenized)
    lexical=bm25.get_scores(query_tokens)
    dense_order=dense.argsort()[::-1]
    lexical_order=lexical.argsort()[::-1]
    dense_rank={int(idx):rank+1 for rank,idx in enumerate(dense_order)}
    lexical_rank={int(idx):rank+1 for rank,idx in enumerate(lexical_order)}
    max_score=1/61
    ranked=[]
    for i,doc in enumerate(docs):
        if dense[i] <= 0 and lexical[i] <= 0: continue
        rrf=0.5/(60+dense_rank[i])+0.5/(60+lexical_rank[i])
        ranked.append({**doc,"relevance":round(rrf/max_score,4),"retrieval_scores":{"tfidf":round(float(dense[i]),4),"bm25":round(float(lexical[i]),4)}})
    return sorted(ranked,key=lambda item:item["relevance"],reverse=True)[:max(1,min(limit,10))]

def answer_with_sources(question: str, hits: list):
    if not hits:
        return {"answer":"I could not retrieve sufficiently relevant evidence from the current curated corpus. Try a narrower question.","sources":[],"grounded":False,"model":"retrieval-only"}

    # Groq exposes an OpenAI-compatible chat-completions API. Prefer Groq when
    # configured, while retaining OpenAI as an optional fallback provider.
    groq_key=os.getenv("GROQ_API_KEY")
    openai_key=os.getenv("OPENAI_API_KEY")
    if groq_key:
        api_key=groq_key
        base_url=os.getenv("GROQ_BASE_URL","https://api.groq.com/openai/v1")
        model=os.getenv("GROQ_MODEL","llama-3.3-70b-versatile")
        provider="groq"
    elif openai_key:
        api_key=openai_key
        base_url=os.getenv("OPENAI_BASE_URL","https://api.openai.com/v1")
        model=os.getenv("OPENAI_MODEL","gpt-4o-mini")
        provider="openai"
    else:
        return {"answer":"Relevant evidence was retrieved, but generative answering is not configured. Review the cited excerpts below; no unsupported synthesis has been generated.","sources":hits,"grounded":True,"model":"retrieval-only"}

    context="\n\n".join(f"[{i+1}] {h['title']} | {h.get('source','')} | {h.get('url','')}\n{h['text']}" for i,h in enumerate(hits))
    prompt=("Answer only from the supplied evidence. If it is insufficient, say so. "
            "Cite each material factual claim inline using only the supplied citation labels [1], [2], etc. "
            "Never invent figures, publication dates, source URLs or citations. "
            "Distinguish report findings from your own explanation and note uncertainty.\n\n"
            f"Evidence:\n{context}\n\nQuestion: {question}")
    body=json.dumps({"model":model,"temperature":0.1,"messages":[{"role":"system","content":"You are EcoScholar, an evidence-grounded sustainability tutor. Never claim a dataset has been queried unless its supplied evidence says so."},{"role":"user","content":prompt}]}).encode()
    request=urllib.request.Request(f"{base_url.rstrip('/')}/chat/completions",data=body,headers={"Authorization":f"Bearer {api_key}","Content-Type":"application/json"})
    try:
        with urllib.request.urlopen(request,timeout=25) as response: data=json.loads(response.read())
        answer=data["choices"][0]["message"]["content"]
        cited=[int(n) for n in re.findall(r"\[(\d+)\]",answer)]
        if not cited or any(n<1 or n>len(hits) for n in cited):
            raise ValueError("LLM output omitted or invented a citation identifier")
        return {"answer":answer,"sources":hits,"grounded":True,"model":f"{provider}:{model}"}
    except Exception:
        return {"answer":"The language model response could not be validated or reached. Retrieved evidence is provided below for manual review.","sources":hits,"grounded":True,"model":"retrieval-fallback"}
