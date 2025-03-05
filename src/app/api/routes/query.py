from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Dict
from src.app.services.query_service import generate_response
from src.app.utils.logger import logger


# Define API Router
router = APIRouter()

#  request model 
class QueryRequest(BaseModel):
    query: str


# Response model
class QueryResponse(BaseModel):
    response: str



@router.post("/ask", response_model=QueryResponse)
async def handle_user_query(request: QueryRequest):
    """
    Endpoint to handle user queries using LLM.
    """
    response = generate_response(
        question=request.query
    )
    return {"response": response}






