"""
Tests for API endpoints.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


class TestHealthEndpoint:
    def test_health_check(self):
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "configured" in data
        assert "environment" in data


class TestQueryEndpoint:
    def test_query_with_empty_question(self):
        response = client.post("/api/query", json={"question": ""})
        assert response.status_code == 422  # Validation error

    def test_query_with_short_question(self):
        response = client.post("/api/query", json={"question": "ab"})
        assert response.status_code == 422  # min_length=3

    def test_query_without_body(self):
        response = client.post("/api/query")
        assert response.status_code == 422
