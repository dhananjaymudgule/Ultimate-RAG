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

# gemini_llm.invoke(["who are you?"])
def process_user_query(user_query: str) -> str:
    """
    Processes user queries using an LLM.
    """
    # llm = OpenAI(model_name="gpt-4", openai_api_key=settings.OPENAI_API_KEY)  

    response = gemini_llm.invoke(user_query)  # Get LLM-generated response
    
    return response.content
