"""
Application configuration loaded from environment variables.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from .env file."""

    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    MONDAY_API_KEY: str = os.getenv("MONDAY_API_KEY", "")
    DEALS_BOARD_ID: str = os.getenv("DEALS_BOARD_ID", "")
    WORK_ORDERS_BOARD_ID: str = os.getenv("WORK_ORDERS_BOARD_ID", "")
    PORT: int = int(os.getenv("PORT", "8000"))
    ENV: str = os.getenv("ENV", "development")

    MONDAY_API_URL: str = "https://api.monday.com/v2"

    @property
    def is_development(self) -> bool:
        return self.ENV == "development"

    @property
    def is_configured(self) -> bool:
        """Check if all required API keys are set."""
        return bool(self.GEMINI_API_KEY and self.MONDAY_API_KEY and self.DEALS_BOARD_ID and self.WORK_ORDERS_BOARD_ID)


settings = Settings()
