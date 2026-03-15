"""
Monday.com API service.
Fetches data from Deals Pipeline and Work Orders boards via GraphQL.
"""

import requests
from config.settings import settings
from utils.data_cleaner import clean_board_data
from utils.logger import logger


BOARD_QUERY = """
query ($boardId: [ID!]!) {
  boards(ids: $boardId) {
    name
    items_page(limit: 500) {
      items {
        name
        column_values {
          text
          column {
            title
          }
        }
      }
    }
  }
}
"""


def _fetch_board(board_id: str, board_name: str) -> list[dict]:
    """
    Fetch and clean data from a monday.com board.
    """
    headers = {
        "Authorization": settings.MONDAY_API_KEY,
        "Content-Type": "application/json",
        "API-Version": "2024-10",
    }

    payload = {
        "query": BOARD_QUERY,
        "variables": {"boardId": [board_id]},
    }

    try:
        logger.info(f"Fetching {board_name} board (ID: {board_id})")
        response = requests.post(settings.MONDAY_API_URL, json=payload, headers=headers, timeout=30)
        response.raise_for_status()

        data = response.json()

        if "errors" in data:
            logger.error(f"Monday.com API error: {data['errors']}")
            raise Exception(f"Monday.com API error: {data['errors']}")

        boards = data.get("data", {}).get("boards", [])
        if not boards:
            logger.warning(f"No board found with ID {board_id}")
            return []

        items = boards[0].get("items_page", {}).get("items", [])
        logger.info(f"Fetched {len(items)} items from {board_name}")

        return clean_board_data(items)

    except requests.RequestException as e:
        logger.error(f"Failed to fetch {board_name}: {str(e)}")
        raise Exception(f"Failed to fetch {board_name} from monday.com: {str(e)}")


def fetch_deals() -> list[dict]:
    """Fetch and clean data from the Deals Pipeline board."""
    return _fetch_board(settings.DEALS_BOARD_ID, "Deals Pipeline")


def fetch_work_orders() -> list[dict]:
    """Fetch and clean data from the Work Orders board."""
    return _fetch_board(settings.WORK_ORDERS_BOARD_ID, "Work Orders")
