from langchain_google_genai import GoogleGenerativeAIEmbeddings
from src.app.core.config import settings

def get_embedding_model():
    """
    Returns the configured embedding model for vector storage and retrieval.
    """
    google_embedding = GoogleGenerativeAIEmbeddings(
        model=settings.GEMINI_EMBEDDING_MODEL_NAME,
        google_api_key=settings.GEMINI_API_KEY
    )

    return google_embedding
