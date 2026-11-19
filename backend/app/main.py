from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import Base, engine, SessionLocal
from app.models.course import Course
from app.models.progress import QuizAttempt
from app.services.seed import seed_courses
from app.api.routes import router

Base.metadata.create_all(bind=engine)
with SessionLocal() as db:
    seed_courses(db)

app = FastAPI(title="EcoScholar API", version="0.1.0", description="Sustainability learning and evidence-grounded discovery API")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(router)
@app.get("/")
def root(): return {"name":"EcoScholar API","docs":"/docs"}
