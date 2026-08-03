from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "AI Medical Diagnosis Assistant"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    SECRET_KEY: str = "CHANGE_ME_IN_PRODUCTION_USE_A_LONG_RANDOM_STRING"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    DATABASE_URL: str = "sqlite:///./medical_assistant.db"

    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]

    # LLM (Gemini) for plain-language explanations
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash"

    # Google Places API for "nearby specialists"
    GOOGLE_PLACES_API_KEY: str = ""

    TOP_K_PREDICTIONS: int = 5

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
