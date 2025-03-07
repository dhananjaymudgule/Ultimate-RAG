# src/app/core/config.py
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

from src.app.utils.logger import logger

# Load .env file
load_dotenv()

class Settings(BaseSettings):
    # General settings
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    PROJECT_NAME: str = "Ultimate RAG"
    PROJECT_DESCRIPTION: str = "Ultimate RAG"

    # API Keys
    PINECONE_API_KEY: str
    GEMINI_API_KEY: str
    GEMINI_LLM_MODEL_NAME: str
    GEMINI_EMBEDDING_MODEL_NAME: str

    # Base directory (Project root)
    BASE_DIR: Path = Path(__file__).resolve().parents[3]  # Go 4 levels up
    logger.info(f"BASE_DIR: {BASE_DIR}")
    
    # Upload directory
    UPLOAD_DIR: Path = BASE_DIR / "uploads"
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)  # Ensure upload directory exists

    # Logs directory
    LOGS_DIR: Path = BASE_DIR / "evaluations"
    LOGS_DIR.mkdir(parents=True, exist_ok=True)  # Ensure logs directory exists

    # CSV file paths
    RAG_RESULTS_CSV: Path = LOGS_DIR / "rag_results.csv"
    LATENCY_CSV: Path = LOGS_DIR / "retrieval_generation_times.csv"

    # config.json
    CORE_BASE_DIR: Path = Path(__file__).resolve().parents[0]  # Go 0 levels up
    print(f"CORE BASE DIR: {CORE_BASE_DIR}")
    CONFIG_JSON_PATH : Path = CORE_BASE_DIR / "config.json"

    class Config:
        env_file = ".env"  # Load environment variables from .env file
        extra = "allow"  # Allows extra env variables to avoid validation errors

# Create `settings` instance
settings = Settings()
