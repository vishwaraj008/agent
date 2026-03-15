"""
Structured logging for the AI BI Agent.
Logs tool calls, API requests, and agent reasoning steps.
"""

import logging
import sys
from datetime import datetime


def setup_logger(name: str = "bi_agent") -> logging.Logger:
    """Create and configure a structured logger."""
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


logger = setup_logger()


class ToolCallTracker:
    """Tracks tool calls made during a query for transparency."""

    def __init__(self):
        self.calls: list[dict] = []

    def record(self, tool_name: str, description: str, status: str = "success", data: dict | None = None):
        """Record a tool call."""
        entry = {
            "tool": tool_name,
            "description": description,
            "status": status,
            "timestamp": datetime.now().isoformat(),
        }
        if data:
            entry["data"] = data
        self.calls.append(entry)
        logger.info(f"Tool Call: {tool_name} — {description} [{status}]")

    def get_trace(self) -> list[dict]:
        """Return the full tool call trace."""
        return self.calls

    def reset(self):
        """Clear all recorded calls."""
        self.calls = []
