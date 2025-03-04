from fastapi import APIRouter
from pydantic import BaseModel
from src.app.services.query_service import process_user_query  # Business logic

# Define API Router
router = APIRouter()

# Request model for user query
class QueryRequest(BaseModel):
    query: str

# Response model (if needed)
class QueryResponse(BaseModel):
    response: str

@router.post("/ask", response_model=QueryResponse)
async def handle_user_query(request: QueryRequest):
    """
    Endpoint to handle user queries using LLM.
    """
    response = process_user_query(request.query)
    return {"response": response}
