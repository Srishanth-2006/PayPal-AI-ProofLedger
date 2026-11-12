import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
DATA_DIR = BASE_DIR / "data"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

class Settings(BaseSettings):
    PROJECT_NAME: str = "ProofLedger"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api"
    
    # PayPal Sandbox Configuration
    PAYPAL_MODE: str = "sandbox"
    PAYPAL_CLIENT_ID: str = ""
    PAYPAL_CLIENT_SECRET: str = ""
    PAYPAL_API_BASE: str = "https://api-m.sandbox.paypal.com"
    PAYPAL_WEBHOOK_ID: str = ""
    
    # AI Engine Configuration
    GEMINI_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    AI_MIN_PASS_SCORE: int = 85
    AI_REVIEW_THRESHOLD: int = 60
    
    # Storage & Proof Ledger
    DATABASE_PATH: str = str(DATA_DIR / "proofledger.db")
    UPLOAD_FOLDER: str = str(UPLOAD_DIR)
    
    # Frontend Host (CORS)
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ]

    model_config = SettingsConfigDict(
        env_file=[str(BASE_DIR / ".env"), ".env"],
        env_file_encoding="utf-8",
        extra="allow"
    )

settings = Settings()
