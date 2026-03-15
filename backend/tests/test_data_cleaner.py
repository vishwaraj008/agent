"""
Tests for data_cleaner utility functions.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.data_cleaner import clean_currency, clean_text, clean_date, clean_null, clean_board_data


class TestCleanCurrency:
    def test_indian_format(self):
        assert clean_currency("₹1,20,000") == 120000.0

    def test_western_format(self):
        assert clean_currency("$5,000.50") == 5000.5

    def test_plain_number(self):
        assert clean_currency("50000") == 50000.0

    def test_empty(self):
        assert clean_currency("") == 0.0

    def test_none(self):
        assert clean_currency(None) == 0.0

    def test_null_string(self):
        assert clean_currency("NULL") == 0.0

    def test_dash(self):
        assert clean_currency("-") == 0.0


class TestCleanText:
    def test_normalize(self):
        assert clean_text("Energy Sector") == "energy sector"

    def test_strip(self):
        assert clean_text("  IT Services  ") == "it services"

    def test_none(self):
        assert clean_text(None) == "unknown"

    def test_empty(self):
        assert clean_text("") == "unknown"

    def test_null_string(self):
        assert clean_text("NULL") == "unknown"


class TestCleanDate:
    def test_iso_format(self):
        assert clean_date("2024-03-15") == "2024-03-15"

    def test_slash_format(self):
        assert clean_date("15/03/2024") == "2024-03-15"

    def test_named_month(self):
        assert clean_date("15-Mar-2024") == "2024-03-15"

    def test_none(self):
        assert clean_date(None) is None

    def test_empty(self):
        assert clean_date("") is None


class TestCleanNull:
    def test_none(self):
        assert clean_null(None) == "unknown"

    def test_empty(self):
        assert clean_null("") == "unknown"

    def test_null_string(self):
        assert clean_null("NULL") == "unknown"

    def test_valid_value(self):
        assert clean_null("hello") == "hello"

    def test_custom_default(self):
        assert clean_null(None, default=0) == 0


class TestCleanBoardData:
    def test_clean_items(self):
        items = [
            {
                "name": "Test Deal",
                "column_values": [
                    {"text": "₹1,00,000", "column": {"title": "Deal Value"}},
                    {"text": "Energy Sector", "column": {"title": "Sector"}},
                    {"text": "2024-03-15", "column": {"title": "Close Date"}},
                    {"text": "negotiation", "column": {"title": "Deal Status"}},
                ]
            }
        ]
        result = clean_board_data(items)
        assert len(result) == 1
        assert result[0]["name"] == "Test Deal"
        assert result[0]["deal_value"] == 100000.0
        assert result[0]["sector"] == "energy sector"
        assert result[0]["close_date"] == "2024-03-15"
        assert result[0]["deal_status"] == "negotiation"

    def test_empty_items(self):
        assert clean_board_data([]) == []
