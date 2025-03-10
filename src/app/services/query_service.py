# src/app/services/query_service.py

from src.app.prompts.prompt_templates import chat_prompt
from src.app.services.retrieval_service import retrieve_documents  
from src.app.core.config import settings
from src.app.utils.logger import logger
from src.app.evaluators.log_time import log_latency
from src.app.evaluators.log_queries import log_query

from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Optional, Dict


# LLM Selection Function
def get_llm():
    
    llm = ChatGoogleGenerativeAI(
            google_api_key=settings.GEMINI_API_KEY,
            model=settings.GEMINI_LLM_MODEL_NAME,
            temperature=0,
            max_output_tokens=8192,
            timeout=None,
            max_retries=2,
            top_p=0.5,
            top_k=5
        )
       
    return llm
    
    

# Generate Response
@log_latency()
def generate_response(question: str) -> dict:
    """
    Dynamically retrieves documents and generates an LLM response.
    """
    try:
        #  Retrieve documents using selected retriever
        retrieved_docs = retrieve_documents(question)

        # check retrival
        # logger.info(f"retrieved_docs: {retrieved_docs}")

        #  Extract text content from retrieved docs
        docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)

        #  Format prompt
        formatted_prompt = chat_prompt.invoke({"question": question, "context": docs_content})

        #  Select LLM dynamically
        llm = get_llm()

        #  Generate response
        response = llm.invoke(formatted_prompt)

        # Log query, context, and answer
        log_query(retriever = "",
                  generator = settings.GEMINI_LLM_MODEL_NAME, 
                  question = question, 
                  retrieved_context = docs_content, 
                  generated_answer = response.content)
        

        final_response = {
            "response": response.content,
            "retrieved_context": docs_content
            }

        return final_response
    except Exception as e:
        logger.error(f"Error processing query '{question}': {str(e)}", exc_info=True)

        return f"Error generating response: {str(e)}"



