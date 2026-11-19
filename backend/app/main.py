import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import Base, engine, SessionLocal
from app.models.course import Course
from app.models.progress import QuizAttempt
from app.models.user import User
from app.services.seed import seed_courses
from app.api.routes import router
from app.api.auth import router as auth_router
Base.metadata.create_all(bind=engine)
with SessionLocal() as db: seed_courses(db)
app=FastAPI(title="EcoScholar API",version="0.3.0",description="Authenticated sustainability learning with evaluated hybrid retrieval")
allowed=[x.strip() for x in os.getenv("API_ALLOWED_ORIGINS","http://localhost:3000").split(",") if x.strip()]
app.add_middleware(CORSMiddleware,allow_origins=allowed,allow_origin_regex=r"https://[a-zA-Z0-9-]+\.vercel\.app",allow_credentials=False,allow_methods=["GET","POST","PATCH","OPTIONS"],allow_headers=["Content-Type","Authorization"])
app.include_router(router)
app.include_router(auth_router)
@app.get("/")
def root(): return {"name":"EcoScholar API","version":"0.3.0","docs":"/docs"}
