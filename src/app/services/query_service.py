# query_service.py

# from langchain.llms import OpenAI  
from langchain_google_genai import ChatGoogleGenerativeAI

from src.app.core.config import settings



gemini_llm = ChatGoogleGenerativeAI(
    google_api_key = settings.GEMINI_API_KEY,
    model=settings.GEMINI_LLM_MODEL_NAME,
    temperature=0,
    max_output_tokens=8192,
    timeout=None,
    max_retries=2,
    top_p=1, 
    top_k=32
)



def process_user_query(user_query: str, retriever_name: str = None, generator_name: str = None, embedding_name: str = None) -> str:
    """
    Processes user queries using an LLM with additional parameters.
    """
    # Log parameters (optional for debugging)
    print(f"Query: {user_query}, Retriever: {retriever_name}, Generator: {generator_name}, Embedding: {embedding_name}")

    response = gemini_llm.invoke(user_query)  
    return response.content  # ✅ Return extracted text content

