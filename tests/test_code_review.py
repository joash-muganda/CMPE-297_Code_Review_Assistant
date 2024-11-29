import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
import json
from src.api import app
from src.model_manager import ModelManager

@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)

@pytest.fixture
def mock_model_manager():
    """Create a mock model manager."""
    with patch('src.api.ModelManager') as mock:
        manager = Mock()
        manager.review_code.return_value = {
            "review": "Test review content",
            "metrics": {
                "response_time": 0.5,
                "tokens_used": 100
            }
        }
        manager.get_metrics.return_value = {
            "total_reviews": 10,
            "avg_response_time": 0.5,
            "token_usage": 1000
        }
        manager.get_review_history.return_value = [
            {
                "timestamp": "2024-01-01T00:00:00",
                "code_snippet": "test code",
                "review": "test review",
                "response_time": 0.5,
                "tokens_used": 100
            }
        ]
        mock.return_value = manager
        yield manager

def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "healthy"

def test_review_code_success(client, mock_model_manager):
    """Test successful code review submission."""
    test_code = """
    def test_function():
        return "Hello, World!"
    """
    
    response = client.post(
        "/api/v1/review",
        json={
            "code": test_code,
            "language": "python"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "review" in data
    assert "metrics" in data
    assert "timestamp" in data

def test_review_code_empty(client):
    """Test code review with empty code."""
    response = client.post(
        "/api/v1/review",
        json={
            "code": "",
            "language": "python"
        }
    )
    
    assert response.status_code == 422

def test_review_code_invalid_json(client):
    """Test code review with invalid JSON."""
    response = client.post(
        "/api/v1/review",
        data="invalid json"
    )
    
    assert response.status_code == 422

def test_get_metrics(client, mock_model_manager):
    """Test metrics retrieval."""
    response = client.get("/api/v1/metrics")
    
    assert response.status_code == 200
    data = response.json()
    assert "total_reviews" in data
    assert "avg_response_time" in data
    assert "token_usage" in data

def test_get_history(client, mock_model_manager):
    """Test review history retrieval."""
    response = client.get("/api/v1/history")
    
    assert response.status_code == 200
    data = response.json()
    assert "history" in data
    assert isinstance(data["history"], list)

def test_get_history_with_limit(client, mock_model_manager):
    """Test review history retrieval with limit."""
    response = client.get("/api/v1/history?limit=5")
    
    assert response.status_code == 200
    data = response.json()
    assert "history" in data
    assert isinstance(data["history"], list)

def test_export_metrics(client, mock_model_manager):
    """Test metrics export."""
    response = client.post("/api/v1/export-metrics")
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Metrics export scheduled" in data["message"]

def test_large_code_review(client, mock_model_manager):
    """Test code review with large input."""
    large_code = "print('hello')\n" * 1000
    
    response = client.post(
        "/api/v1/review",
        json={
            "code": large_code,
            "language": "python"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "review" in data
    assert "metrics" in data

def test_concurrent_requests(client, mock_model_manager):
    """Test handling of concurrent requests."""
    import asyncio
    import httpx
    
    async def make_request():
        async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post(
                "/api/v1/review",
                json={
                    "code": "print('test')",
                    "language": "python"
                }
            )
            return response.status_code
    
    async def test_concurrent():
        tasks = [make_request() for _ in range(5)]
        results = await asyncio.gather(*tasks)
        return results
    
    results = asyncio.run(test_concurrent())
    assert all(status == 200 for status in results)

def test_error_handling(client, mock_model_manager):
    """Test error handling in the API."""
    mock_model_manager.review_code.side_effect = Exception("Test error")
    
    response = client.post(
        "/api/v1/review",
        json={
            "code": "print('test')",
            "language": "python"
        }
    )
    
    assert response.status_code == 500
    data = response.json()
    assert "detail" in data

if __name__ == '__main__':
    pytest.main([__file__])
