import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import Base, engine, SessionLocal
from app.models.course import Course
from app.models.progress import QuizAttempt
from app.services.seed import seed_courses
from app.api.routes import router

# MVP bootstrap. Use Alembic migrations before production deployments.
Base.metadata.create_all(bind=engine)
with SessionLocal() as db:
    seed_courses(db)

app = FastAPI(
    title="EcoScholar API",
    version="0.2.0",
    description="Sustainability learning and evidence-grounded discovery API",
)
allowed_origins = [
    origin.strip()
    for origin in os.getenv("API_ALLOWED_ORIGINS", "http://localhost:3000").split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"https://[a-zA-Z0-9-]+\.vercel\.app",
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)
app.include_router(router)

@app.get("/")
def root():
    return {"name": "EcoScholar API", "version": "0.2.0", "docs": "/docs"}
