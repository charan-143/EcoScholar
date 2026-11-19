from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.course import Course
from app.models.progress import QuizAttempt
from app.schemas.api import AskRequest, QuizRequest, FootprintRequest
from app.services.retrieval import retrieve, recommend

router = APIRouter(prefix="/api")
QUIZZES = {
 "climate-basics": {"questions": ["Which action is mitigation?", "What does adaptation primarily do?", "What drives recent human-caused warming?"], "answers": [1, 0, 2], "options": [["Build flood barriers", "Reduce fossil fuel emissions", "Move homes"], ["Reduce harm from impacts", "Increase emissions", "Measure daily weather"], ["Solar cycles alone", "Ocean tides", "Increasing greenhouse gases"]]},
 "clean-energy": {"questions": ["Why is grid flexibility important?", "What should lifecycle comparisons use?"], "answers": [1, 0], "options": [["To eliminate all transmission", "To balance variable supply and demand", "To avoid maintenance"], ["Consistent boundaries and functional units", "Different units for each option", "Only purchase price"]]},
}

@router.get("/health")
def health(): return {"status":"ok", "service":"ecoscholar-api"}

@router.get("/courses")
def courses(db: Session = Depends(get_db)):
    return [{"slug":c.slug,"title":c.title,"category":c.category,"level":c.level,"duration":c.duration,"description":c.description,"content":c.content} for c in db.query(Course).all()]

@router.get("/recommendations")
def recommendations(topic: str = "climate"):
    return {"topic":topic,"results":recommend(topic)}

@router.post("/assistant/ask")
def ask(payload: AskRequest):
    hits = retrieve(payload.question)
    if not hits:
        return {"answer":"I couldn't find a relevant passage in the current EcoScholar knowledge base. Try a topic such as climate, renewable energy, biodiversity, waste or water.","sources":[],"grounded":False}
    answer = "Here are the most relevant knowledge-base passages. Treat these as a starting point and consult the cited assessment or agency material for authoritative detail."
    return {"answer":answer,"sources":[{"id":h["id"],"title":h["title"],"excerpt":h["text"],"source":h["source"],"relevance":h["relevance"]} for h in hits],"grounded":True}

@router.post("/quizzes/submit")
def submit_quiz(payload: QuizRequest, db: Session = Depends(get_db)):
    quiz = QUIZZES.get(payload.course_slug)
    if not quiz: raise HTTPException(404, "No quiz is available for this course yet")
    if len(payload.answers) != len(quiz["answers"]): raise HTTPException(422, "Answer count does not match quiz")
    score = sum(a == b for a,b in zip(payload.answers, quiz["answers"]))
    db.add(QuizAttempt(course_slug=payload.course_slug, score=score, total=len(quiz["answers"])))
    db.commit()
    return {"score":score,"total":len(quiz["answers"]),"percentage":round(score/len(quiz["answers"])*100),"message":"Review the explanations and retry to strengthen retention."}

@router.get("/quizzes/{course_slug}")
def get_quiz(course_slug: str):
    quiz = QUIZZES.get(course_slug)
    if not quiz: raise HTTPException(404, "Quiz not found")
    return {"course_slug":course_slug,"questions":[{"question":q,"options":o} for q,o in zip(quiz["questions"],quiz["options"])]}

@router.get("/progress")
def progress(db: Session = Depends(get_db)):
    attempts = db.query(QuizAttempt).order_by(QuizAttempt.created_at.desc()).limit(20).all()
    return {"attempts":len(attempts),"average_score":round(sum((a.score/a.total)*100 for a in attempts)/len(attempts),1) if attempts else 0,"recent":[{"course_slug":a.course_slug,"score":a.score,"total":a.total,"created_at":a.created_at} for a in attempts]}

@router.post("/footprint/estimate")
def footprint(payload: FootprintRequest):
    # Illustrative factors only. Replace with region- and year-specific authoritative factors.
    commute = payload.commute_km_week * 52 * 0.12
    electricity = payload.electricity_kwh_month * 12 * 0.7
    flights = payload.flights_short_haul_year * 250
    total = commute + electricity + flights
    return {"estimated_kg_co2e_year":round(total,1),"breakdown_kg_co2e":{"commute":round(commute,1),"electricity":round(electricity,1),"flights":round(flights,1)},"method_note":"Illustrative screening estimate using fixed placeholder factors, not a verified personal carbon footprint. Factors require localization and source review."}
