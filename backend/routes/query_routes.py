"""
API route definitions for the BI Agent.
"""

from fastapi import APIRouter, HTTPException
from controllers.query_controller import QueryRequest, QueryResponse, handle_query
from config.settings import settings

router = APIRouter(prefix="/api", tags=["Query"])


@router.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """
    Process a business intelligence query.

    Accepts a natural language question and returns AI-generated insights
    with full tool call transparency.
    """
    try:
        return await handle_query(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "configured": settings.is_configured,
        "environment": settings.ENV,
    }
