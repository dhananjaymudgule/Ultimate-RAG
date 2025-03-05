# src/app/api/routes/query.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
from src.app.services.query_service import generate_response
from src.app.utils.logger import logger

# Initialize API Router
router = APIRouter()

#  Request Model (Allows Future Expansion)
class QueryRequest(BaseModel):
    query: str
    

#  Response Model
class QueryResponse(BaseModel):
    response: str

@router.post("/ask", response_model=QueryResponse)
async def handle_user_query(request: QueryRequest):
    """
    Handles user queries using LLM-based retrieval and response generation.
    """
    logger.info(f"Received query: {request.query}, Filters: {request.filters}")

    try:
        response = generate_response(question=request.query)

        return {"response": response}

    except Exception as e:
        logger.error(f"Error processing query '{request.query}': {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error while generating response.")
