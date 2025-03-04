from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from src.app.services.query_service import process_user_query

# Define API Router
router = APIRouter()

# Updated request model with additional parameters
class QueryRequest(BaseModel):
    query: str
    retriever_name: Optional[str] = None  # ✅ Additional optional parameter
    generator_name: Optional[str] = None  # ✅ Another optional parameter
    embedding_name: Optional[str] = None  # ✅ Another optional parameter

# Response model
class QueryResponse(BaseModel):
    response: str

@router.post("/ask", response_model=QueryResponse)
async def handle_user_query(request: QueryRequest):
    """
    Endpoint to handle user queries using LLM.
    """
    response = process_user_query(
        user_query=request.query,
        retriever_name=request.retriever_name,
        generator_name=request.generator_name,
        embedding_name=request.embedding_name,
    )
    return {"response": response}
