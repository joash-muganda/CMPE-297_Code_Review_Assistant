import requests
import json
from typing import Dict, Optional
import time

class CodeReviewClient:
    """A simple client for interacting with the Code Review Assistant API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        
    def submit_review(self, code: str, language: Optional[str] = None) -> Dict:
        """Submit code for review."""
        endpoint = f"{self.base_url}/api/v1/review"
        payload = {
            "code": code,
            "language": language
        }
        
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        return response.json()
    
    def get_metrics(self) -> Dict:
        """Get current performance metrics."""
        endpoint = f"{self.base_url}/api/v1/metrics"
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()
    
    def get_history(self, limit: Optional[int] = None) -> Dict:
        """Get review history."""
        endpoint = f"{self.base_url}/api/v1/history"
        params = {"limit": limit} if limit else {}
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

def main():
    """Example usage of the Code Review Assistant API."""
    client = CodeReviewClient()
    
    # Example 1: Review Python code
    python_code = """
def calculate_factorial(n):
    if n < 0:
        return None
    if n == 0:
        return 1
    result = 1
    for i in range(1, n + 1):
        result = result * i
    return result
    """
    
    print("Submitting Python code for review...")
    review_result = client.submit_review(python_code, language="python")
    print("\nReview Result:")
    print(json.dumps(review_result, indent=2))
    
    # Example 2: Review JavaScript code
    js_code = """
function fetchUserData(userId) {
    fetch(`/api/users/${userId}`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
}
    """
    
    print("\nSubmitting JavaScript code for review...")
    review_result = client.submit_review(js_code, language="javascript")
    print("\nReview Result:")
    print(json.dumps(review_result, indent=2))
    
    # Get metrics
    print("\nFetching metrics...")
    metrics = client.get_metrics()
    print("\nMetrics:")
    print(json.dumps(metrics, indent=2))
    
    # Get review history
    print("\nFetching recent review history...")
    history = client.get_history(limit=5)
    print("\nRecent Reviews:")
    print(json.dumps(history, indent=2))

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the Code Review Assistant API.")
        print("Make sure the server is running and accessible at http://localhost:8000")
    except Exception as e:
        print(f"Error: {str(e)}")
