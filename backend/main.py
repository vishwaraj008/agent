"""
AI Business Intelligence Agent — FastAPI Application Entry Point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.settings import settings
from routes.query_routes import router as query_router
from utils.logger import logger

app = FastAPI(
    title="AI Business Intelligence Agent",
    description="AI-powered BI assistant that answers business questions using live monday.com data and Google Gemini.",
    version="1.0.0",
)

# Configure CORS origins based on environment
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]

# Add production frontend URL if configured
if settings.FRONTEND_URL:
    origins.append(settings.FRONTEND_URL)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(query_router)


@app.on_event("startup")
async def startup():
    logger.info("=" * 60)
    logger.info("AI Business Intelligence Agent starting up")
    logger.info(f"Environment: {settings.ENV}")
    logger.info(f"API configured: {settings.is_configured}")
    if not settings.is_configured:
        logger.warning("API keys not configured! Set GEMINI_API_KEY, MONDAY_API_KEY, DEALS_BOARD_ID, WORK_ORDERS_BOARD_ID in .env")
    logger.info("=" * 60)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=settings.is_development)
