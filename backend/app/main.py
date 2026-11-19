from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api import resumes, interviews


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,

    allow_origins=settings.ALLOWED_ORIGINS,

    allow_credentials=True,

    allow_methods=["GET", "POST"],

    allow_headers=["Authorization", "Content-Type"]
)

app.include_router(resumes.router)
app.include_router(interviews.router)


@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "AI Interview Platform"
    }
@app.get("/")
def home():
    return {
        "message": "Candidate Screening API is running"
    }