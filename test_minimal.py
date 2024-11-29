import pytest
from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_basic_code_review():
    """Test a basic code review request."""
    test_code = """
def add(a, b):
    return a + b
    """
    
    response = client.post(
        "/api/v1/review",
        json={
            "code": test_code,
            "language": "python"
        }
    )
    
    assert response.status_code == 200
    assert "review" in response.json()
    assert "metrics" in response.json()

def test_metrics_endpoint():
    """Test metrics endpoint."""
    response = client.get("/api/v1/metrics")
    assert response.status_code == 200
    assert "total_reviews" in response.json()
    assert "avg_response_time" in response.json()

if __name__ == "__main__":
    pytest.main([__file__])
