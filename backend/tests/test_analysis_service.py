"""
Tests for analysis_service functions.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from services.analysis_service import (
    analyze_pipeline,
    analyze_revenue_by_sector,
    analyze_conversion_rate,
    analyze_delayed_orders,
    compute_metrics,
)


SAMPLE_DEALS = [
    {"name": "Deal A", "deal_status": "negotiation", "deal_value": 100000.0, "sector": "energy"},
    {"name": "Deal B", "deal_status": "proposal", "deal_value": 200000.0, "sector": "energy"},
    {"name": "Deal C", "deal_status": "won", "deal_value": 150000.0, "sector": "it"},
    {"name": "Deal D", "deal_status": "negotiation", "deal_value": 80000.0, "sector": "healthcare"},
]

SAMPLE_WORK_ORDERS = [
    {"name": "WO-1", "execution_status": "in progress", "delivery_date": "2024-01-15", "order_value": 100000.0},
    {"name": "WO-2", "execution_status": "done", "delivery_date": "2024-06-01", "order_value": 150000.0},
    {"name": "WO-3", "execution_status": "delayed", "delivery_date": "2024-02-01", "order_value": 80000.0},
]


class TestAnalyzePipeline:
    def test_pipeline_health(self):
        result = analyze_pipeline(SAMPLE_DEALS)
        assert result["total_deals"] == 4
        assert result["total_pipeline_value"] == 530000.0
        assert "negotiation" in result["stages"]
        assert result["stages"]["negotiation"] == 2

    def test_empty_deals(self):
        result = analyze_pipeline([])
        assert result["total_deals"] == 0


class TestAnalyzeRevenue:
    def test_revenue_by_sector(self):
        result = analyze_revenue_by_sector(SAMPLE_DEALS)
        assert "energy" in result["sectors"]
        assert result["sectors"]["energy"]["count"] == 2
        assert result["sectors"]["energy"]["value"] == 300000.0

    def test_empty_deals(self):
        result = analyze_revenue_by_sector([])
        assert result["sectors"] == {}


class TestAnalyzeConversion:
    def test_conversion_rate(self):
        result = analyze_conversion_rate(SAMPLE_DEALS, SAMPLE_WORK_ORDERS)
        assert result["total_deals"] == 4
        assert result["total_work_orders"] == 3
        assert result["conversion_rate"] == 75.0

    def test_no_deals(self):
        result = analyze_conversion_rate([], SAMPLE_WORK_ORDERS)
        assert result["conversion_rate"] == 0


class TestAnalyzeDelayed:
    def test_delayed_orders(self):
        result = analyze_delayed_orders(SAMPLE_WORK_ORDERS)
        assert result["total_orders"] == 3
        assert result["delayed_count"] >= 1  # WO-1 and WO-3 are before today

    def test_empty_orders(self):
        result = analyze_delayed_orders([])
        assert result["total_orders"] == 0
        assert result["delayed_count"] == 0


class TestComputeMetrics:
    def test_full_metrics(self):
        result = compute_metrics(SAMPLE_DEALS, SAMPLE_WORK_ORDERS)
        assert "pipeline" in result
        assert "revenue_by_sector" in result
        assert "conversion" in result
        assert "delayed_orders" in result
        assert "overall_summary" in result
