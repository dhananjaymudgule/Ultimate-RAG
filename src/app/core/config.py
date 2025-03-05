#src/app/core/config.py 
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

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
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent  # Points to fastapi_project/

    # Upload directory
    UPLOAD_DIR: Path = BASE_DIR / "uploads"

    class Config:
        env_file = ".env"  # Load environment variables from .env file
        extra = "allow"  # ✅ Allows extra env variables to avoid validation errors

# Create `settings` instance
settings = Settings()

# Ensure the upload directory exists
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
