"""Content-based TF-IDF recommendations blended with observed learner mastery."""
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

COURSE_PROFILES={
 "climate-basics":"climate change greenhouse gas emissions adaptation mitigation resilience climate risk",
 "clean-energy":"renewable energy solar wind electricity power grid storage energy transition",
 "biodiversity":"biodiversity nature ecosystems habitat species conservation restoration ecological diversity",
 "circular-economy":"circular economy waste materials reuse repair recycling product design resource efficiency",
}

def personalized_recommendations(user, attempts, interests=None, limit=4):
    interests={x.strip().lower() for x in (interests or []) if x.strip()}
    mastery=defaultdict(list)
    for attempt in attempts:
        mastery[attempt.course_slug].append(float(attempt.score)/max(1,attempt.total))
    slugs=list(COURSE_PROFILES)
    vectorizer=TfidfVectorizer(stop_words="english",ngram_range=(1,2),sublinear_tf=True)
    matrix=vectorizer.fit_transform([COURSE_PROFILES[slug] for slug in slugs])
    profile=vectorizer.transform([" ".join(sorted(interests))]) if interests else None
    similarities=cosine_similarity(profile,matrix).ravel() if profile is not None else [0.0]*len(slugs)
    results=[]
    for i,slug in enumerate(slugs):
        recent=mastery.get(slug,[])
        avg=sum(recent[-3:])/len(recent[-3:]) if recent else None
        gap_score=(1-avg) if avg is not None else 0.35
        score=0.7*float(similarities[i])+0.3*gap_score
        if similarities[i]>=0.12: reason="Content-based TF-IDF match to your stated interests"
        elif avg is not None: reason="Suggested to strengthen a topic with lower recent quiz mastery"
        else: reason="Suggested as a complementary next learning path"
        results.append({"course_slug":slug,"score":round(score,4),"reason":reason,"signals":{"tfidf_interest_similarity":round(float(similarities[i]),4),"recent_quiz_mastery":round(avg,3) if avg is not None else None}})
    return sorted(results,key=lambda item:item["score"],reverse=True)[:max(1,min(limit,len(slugs)))]
