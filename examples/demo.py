"""
Code Review Assistant Demo Script
This script demonstrates the core functionality of the Code Review Assistant.
"""

import requests
import json
from pprint import pprint
from time import sleep

# Configuration
API_URL = "http://localhost:8000"

def print_section(title):
    """Print a section header."""
    print("\n" + "="*50)
    print(title)
    print("="*50)

def submit_code_review(code, language):
    """Submit code for review."""
    response = requests.post(
        f"{API_URL}/api/v1/review",
        json={
            "code": code,
            "language": language
        }
    )
    return response.json()

def get_metrics():
    """Get system metrics."""
    response = requests.get(f"{API_URL}/api/v1/metrics")
    return response.json()

def get_history(limit=5):
    """Get review history."""
    response = requests.get(f"{API_URL}/api/v1/history?limit={limit}")
    return response.json()

def main():
    """Run the demo."""
    print_section("Code Review Assistant Demo")
    
    # Example 1: Review Python code with potential issues
    python_code = """
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total/len(numbers)  # Potential division by zero

def process_data(data):
    results = []
    for item in data:
        if item > 0:
            results.append(item)
        else:
            continue  # Unnecessary continue
    return results
    """
    
    print("\nSubmitting Python code for review...")
    python_result = submit_code_review(python_code, "python")
    print("\nPython Code Review Results:")
    pprint(python_result)
    
    # Example 2: Review JavaScript code with security concerns
    javascript_code = """
function authenticateUser(username, password) {
    // Store password in localStorage
    localStorage.setItem('password', password);
    
    // Construct SQL query
    const query = `SELECT * FROM users WHERE username='${username}'`;
    
    // Make API call
    fetch('/api/auth', {
        method: 'POST',
        body: JSON.stringify({ query })
    });
}
    """
    
    print("\nSubmitting JavaScript code for review...")
    js_result = submit_code_review(javascript_code, "javascript")
    print("\nJavaScript Code Review Results:")
    pprint(js_result)
    
    # Example 3: Review code with performance issues
    performance_code = """
def find_duplicates(items):
    duplicates = []
    for i in range(len(items)):
        for j in range(len(items)):
            if i != j and items[i] == items[j] and items[i] not in duplicates:
                duplicates.append(items[i])
    return duplicates

def process_large_list(items):
    result = []
    for item in items:
        if item not in result:  # Inefficient lookup
            result.append(item)
    return result
    """
    
    print("\nSubmitting code with performance issues for review...")
    perf_result = submit_code_review(performance_code, "python")
    print("\nPerformance Code Review Results:")
    pprint(perf_result)
    
    # Get system metrics
    print("\nRetrieving system metrics...")
    metrics = get_metrics()
    print("\nSystem Metrics:")
    pprint(metrics)
    
    # Get review history
    print("\nRetrieving review history...")
    history = get_history(limit=3)
    print("\nRecent Review History:")
    pprint(history)

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the API server.")
        print("Please ensure the server is running at", API_URL)
    except Exception as e:
        print("\nError occurred:", str(e))
