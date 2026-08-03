from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine
from app.routers import auth, diagnosis

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "AI-assisted symptom triage tool. Combines a trained ML classifier with an LLM "
        "explanation layer. This tool is for general information only and is NOT a "
        "substitute for professional medical advice, diagnosis, or treatment."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(diagnosis.router)


@app.get("/")
def root():
    return {
        "status": "ok",
        "service": settings.APP_NAME,
        "disclaimer": "This tool provides general health information only and is not a medical diagnosis.",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
