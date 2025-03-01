# sec.app.core.config.py

import os
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Settings(BaseSettings):
    # General settings
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", 8000))
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Ultimate RAG")
    PROJECT_DESCRIPTION: str = os.getenv("PROJECT_DESCRIPTION", "Ultimate RAG")

    # Base directory (Project root)
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent  # Points to fastapi_project/

    # Upload directory
    UPLOAD_DIR: Path = BASE_DIR / "uploads"
    print(UPLOAD_DIR)

    class Config:
        env_file = ".env"  # Load environment variables from .env file

# Create `settings` instance
settings = Settings()

# Ensure the upload directory exists
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
