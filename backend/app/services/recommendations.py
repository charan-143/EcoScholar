"""Transparent hybrid learner recommendations; no black-box claims."""
from collections import defaultdict
from app.data.knowledge import KNOWLEDGE

COURSE_TAGS = {
 "climate-basics":{"climate","energy","adaptation","mitigation","emissions"},
 "clean-energy":{"energy","renewable","electricity","grid","climate"},
 "biodiversity":{"biodiversity","ecosystem","habitat","nature"},
 "circular-economy":{"waste","materials","reuse","repair","circular"},
}

def personalized_recommendations(user, attempts, interests=None, limit=4):
    interests = {x.strip().lower() for x in (interests or []) if x.strip()}
    mastery = defaultdict(list)
    for attempt in attempts:
        mastery[attempt.course_slug].append(float(attempt.score) / max(1, attempt.total))
    scores=[]
    for slug,tags in COURSE_TAGS.items():
        recent=mastery.get(slug, [])
        avg=sum(recent[-3:])/len(recent[-3:]) if recent else None
        interest_score=len(tags & interests)/max(1,len(interests)) if interests else 0
        # Prioritise relevant interests and topics with weak observed quiz performance.
        gap_score=(1-avg) if avg is not None else 0.35
        score=0.55*interest_score+0.45*gap_score
        scores.append({"course_slug":slug,"score":round(score,4),"reason":"Matches your stated interests" if interest_score else ("Suggested to strengthen a topic with lower recent quiz scores" if avg is not None else "A useful next topic based on the starter learning path"),"signals":{"interest_match":round(interest_score,3),"recent_quiz_mastery":round(avg,3) if avg is not None else None}})
    return sorted(scores,key=lambda x:x["score"],reverse=True)[:limit]
