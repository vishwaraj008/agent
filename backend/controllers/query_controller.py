"""
Query controller — validates requests and orchestrates the AI service.
"""

from pydantic import BaseModel, Field
from services import ai_service
from utils.logger import logger


class QueryRequest(BaseModel):
    """Request schema for the /query endpoint."""
    question: str = Field(..., min_length=3, max_length=1000, description="The business question to ask")


class QueryResponse(BaseModel):
    """Response schema for the /query endpoint."""
    answer: str
    tool_calls: list[dict]
    metrics: dict = {}


async def handle_query(request: QueryRequest) -> QueryResponse:
    """
    Process a user's business intelligence query.
    - Validates the question
    - Calls the AI service
    - Returns structured response
    """
    logger.info(f"Processing query: {request.question[:80]}...")

    result = await ai_service.process_query(request.question)

    return QueryResponse(
        answer=result["answer"],
        tool_calls=result["tool_calls"],
        metrics=result.get("metrics", {}),
    )
