"""
Data cleaning utilities for normalizing messy monday.com board data.
Handles currency formats, dates, nulls, and inconsistent labels.
"""

import re
from datetime import datetime
from typing import Any


def clean_currency(value: str | None) -> float:
    """
    Convert currency strings to numeric values.
    Examples:
        '₹1,20,000' → 120000.0
        '$5,000.50' → 5000.5
        '1,20,000' → 120000.0
        '' → 0.0
    """
    if not value or str(value).strip() in ("", "None", "null", "NULL", "-"):
        return 0.0

    cleaned = str(value).strip()
    # Remove currency symbols
    cleaned = re.sub(r"[₹$€£¥]", "", cleaned)
    # Remove spaces
    cleaned = cleaned.replace(" ", "")

    # Handle Indian number format (1,20,000) vs Western (120,000)
    # Detect: if there are multiple commas and last group before decimal is 3 digits
    if "," in cleaned:
        parts = cleaned.split(".")
        integer_part = parts[0].replace(",", "")
        decimal_part = parts[1] if len(parts) > 1 else "0"
        cleaned = f"{integer_part}.{decimal_part}"

    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def clean_text(value: str | None) -> str:
    """
    Normalize text labels to lowercase, stripped.
    Examples:
        'Energy Sector' → 'energy sector'
        '  IT Services  ' → 'it services'
        None → 'unknown'
    """
    if not value or str(value).strip() in ("", "None", "null", "NULL", "-"):
        return "unknown"
    return str(value).strip().lower()


def clean_date(value: str | None) -> str | None:
    """
    Parse various date formats and return ISO 8601 string.
    Examples:
        '2024-03-15' → '2024-03-15'
        '15/03/2024' → '2024-03-15'
        '15-Mar-2024' → '2024-03-15'
        '' → None
    """
    if not value or str(value).strip() in ("", "None", "null", "NULL", "-"):
        return None

    date_str = str(value).strip()
    formats = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%d-%m-%Y",
        "%d-%b-%Y",
        "%B %d, %Y",
        "%b %d, %Y",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%d %H:%M:%S",
    ]

    for fmt in formats:
        try:
            parsed = datetime.strptime(date_str, fmt)
            return parsed.strftime("%Y-%m-%d")
        except ValueError:
            continue

    return date_str


def clean_null(value: Any, default: Any = "unknown") -> Any:
    """
    Replace null/empty values with a default.
    """
    if value is None:
        return default
    if isinstance(value, str) and value.strip() in ("", "None", "null", "NULL", "-"):
        return default
    return value


def clean_board_item(item: dict) -> dict:
    """
    Clean a single monday.com board item.
    Extracts column values and normalizes them.
    """
    cleaned = {"name": item.get("name", "unknown")}

    column_values = item.get("column_values", [])
    for col in column_values:
        title = col.get("column", {}).get("title", "").strip()
        text = col.get("text", "")

        if not title:
            continue

        key = title.lower().replace(" ", "_")

        # Apply type-specific cleaning based on column title keywords
        title_lower = title.lower()
        if any(kw in title_lower for kw in ["value", "revenue", "amount", "price", "cost", "budget"]):
            cleaned[key] = clean_currency(text)
        elif any(kw in title_lower for kw in ["date", "deadline", "due"]):
            cleaned[key] = clean_date(text)
        elif any(kw in title_lower for kw in ["status", "stage", "sector", "category", "type"]):
            cleaned[key] = clean_text(text)
        else:
            cleaned[key] = clean_null(text)

    return cleaned


def clean_board_data(items: list[dict]) -> list[dict]:
    """
    Clean an entire list of monday.com board items.
    """
    return [clean_board_item(item) for item in items]
