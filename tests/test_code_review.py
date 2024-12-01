import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
import json
from datetime import datetime
from src.api import app
from src.model_manager import ModelManager
from src.code_reviewer import CodeReviewer, CodeReview

@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)

@pytest.fixture
def mock_code_reviewer():
    """Create a mock code reviewer."""
    with patch('src.api.CodeReviewer') as mock:
        reviewer = Mock()
        
        # Mock review response
        review = CodeReview(
            code="test code",
            language="python",
            review_id="test-123"
        )
        review.suggestions = [
            {
                "type": "Issues",
                "items": ["Test issue 1", "Test issue 2"]
            },
            {
                "type": "Improvements",
                "items": ["Test improvement 1"]
            },
            {
                "type": "Best Practices",
                "items": ["Test practice 1"]
            }
        ]
        review.metrics = {
            "response_time": 0.5,
            "code_length": 100,
            "suggestion_count": 4
        }
        review.timestamp = datetime.now()
        
        reviewer.review_code.return_value = review
        
        # Mock metrics
        reviewer.get_review_metrics.return_value = {
            "total_reviews": 10,
            "avg_response_time": 0.5,
            "avg_suggestions": 3.5,
            "reviews_today": 5
        }
        
        # Mock history
        reviewer.get_review_history.return_value = [review]
        
        mock.return_value = reviewer
        yield reviewer

def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert "model_status" in response.json()

def test_review_code_success(client, mock_code_reviewer):
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
    assert "review_id" in data
    assert "suggestions" in data
    assert "metrics" in data
    assert "timestamp" in data
    
    # Verify suggestions structure
    suggestions = data["suggestions"]
    assert isinstance(suggestions, list)
    assert all("type" in s and "items" in s for s in suggestions)
    
    # Verify metrics structure
    metrics = data["metrics"]
    assert "response_time" in metrics
    assert "code_length" in metrics
    assert "suggestion_count" in metrics

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

def test_get_metrics(client, mock_code_reviewer):
    """Test metrics retrieval."""
    response = client.get("/api/v1/metrics")
    
    assert response.status_code == 200
    data = response.json()
    assert "total_reviews" in data
    assert "avg_response_time" in data
    assert "avg_suggestions" in data
    assert "reviews_today" in data

def test_get_history(client, mock_code_reviewer):
    """Test review history retrieval."""
    response = client.get("/api/v1/history")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    
    if len(data) > 0:
        review = data[0]
        assert "review_id" in review
        assert "language" in review
        assert "suggestions" in review
        assert "metrics" in review
        assert "timestamp" in review

def test_get_history_with_limit(client, mock_code_reviewer):
    """Test review history retrieval with limit."""
    limit = 5
    response = client.get(f"/api/v1/history?limit={limit}")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= limit

def test_large_code_review(client, mock_code_reviewer):
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
    assert "review_id" in data
    assert "suggestions" in data
    assert "metrics" in data

def test_concurrent_requests(client, mock_code_reviewer):
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

def test_error_handling(client, mock_code_reviewer):
    """Test error handling in the API."""
    mock_code_reviewer.review_code.side_effect = Exception("Test error")
    
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

def test_different_languages(client, mock_code_reviewer):
    """Test code review with different programming languages."""
    languages = ["python", "javascript", "java", "cpp", "typescript"]
    
    for lang in languages:
        response = client.post(
            "/api/v1/review",
            json={
                "code": "// Test code",
                "language": lang
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "review_id" in data
        assert "suggestions" in data

if __name__ == '__main__':
    pytest.main([__file__])
