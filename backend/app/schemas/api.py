from pydantic import BaseModel, Field

class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=1000)

class QuizRequest(BaseModel):
    course_slug: str
    answers: list[int]

class FootprintRequest(BaseModel):
    commute_km_week: float = Field(ge=0, le=5000)
    electricity_kwh_month: float = Field(ge=0, le=100000)
    flights_short_haul_year: int = Field(ge=0, le=100)
