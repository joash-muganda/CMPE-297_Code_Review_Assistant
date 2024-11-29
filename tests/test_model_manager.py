import pytest
import asyncio
from unittest.mock import Mock, patch
from datetime import datetime
from src.model_manager import ModelManager

@pytest.fixture
def model_manager():
    """Create a ModelManager instance for testing."""
    with patch('src.model_manager.AutoModelForCausalLM'), \
         patch('src.model_manager.AutoTokenizer'):
        manager = ModelManager()
        return manager

@pytest.mark.asyncio
async def test_review_code_success(model_manager):
    """Test successful code review."""
    # Mock tokenizer and model outputs
    model_manager.tokenizer.encode = Mock(return_value=[1, 2, 3])
    model_manager.tokenizer.decode = Mock(return_value="Great code! Here are some suggestions...")
    model_manager.model.generate = Mock(return_value=[[1, 2, 3, 4]])
    
    code = """
    def example_function():
        return "Hello, World!"
    """
    
    result = await model_manager.review_code(code)
    
    assert isinstance(result, dict)
    assert "review" in result
    assert "metrics" in result
    assert "response_time" in result["metrics"]
    assert "tokens_used" in result["metrics"]

@pytest.mark.asyncio
async def test_review_code_with_long_input(model_manager):
    """Test code review with long input."""
    long_code = "print('hello')\n" * 1000
    
    result = await model_manager.review_code(long_code)
    
    assert isinstance(result, dict)
    assert "review" in result
    assert len(model_manager.review_history) == 1

def test_get_metrics(model_manager):
    """Test metrics retrieval."""
    metrics = model_manager.get_metrics()
    
    assert isinstance(metrics, dict)
    assert "total_reviews" in metrics
    assert "avg_response_time" in metrics
    assert "token_usage" in metrics
    assert metrics["total_reviews"] >= 0

def test_get_review_history(model_manager):
    """Test review history retrieval."""
    # Add some test reviews
    model_manager.review_history = [
        {
            "timestamp": datetime.now().isoformat(),
            "code_snippet": "print('test')",
            "review": "Good code",
            "response_time": 0.5,
            "tokens_used": 100
        },
        {
            "timestamp": datetime.now().isoformat(),
            "code_snippet": "def test(): pass",
            "review": "Could be improved",
            "response_time": 0.6,
            "tokens_used": 120
        }
    ]
    
    # Test without limit
    history = model_manager.get_review_history()
    assert len(history) == 2
    
    # Test with limit
    limited_history = model_manager.get_review_history(limit=1)
    assert len(limited_history) == 1

@pytest.mark.asyncio
async def test_review_code_error_handling(model_manager):
    """Test error handling during code review."""
    # Mock model to raise an exception
    model_manager.model.generate = Mock(side_effect=Exception("Model error"))
    
    with pytest.raises(Exception):
        await model_manager.review_code("def broken_code():")

def test_export_metrics(model_manager, tmp_path):
    """Test metrics export functionality."""
    # Add some test metrics
    model_manager.metrics["total_reviews"] = 10
    model_manager.metrics["avg_response_time"] = 0.5
    model_manager.metrics["token_usage"] = 1000
    
    # Export to temporary file
    export_path = tmp_path / "test_metrics.json"
    model_manager.export_metrics(str(export_path))
    
    # Verify file exists and contains valid JSON
    assert export_path.exists()
    content = export_path.read_text()
    assert "metrics" in content
    assert "review_history" in content

@pytest.mark.asyncio
async def test_concurrent_reviews(model_manager):
    """Test handling multiple concurrent reviews."""
    code_samples = [
        "def test1(): pass",
        "def test2(): pass",
        "def test3(): pass"
    ]
    
    # Run multiple reviews concurrently
    tasks = [model_manager.review_code(code) for code in code_samples]
    results = await asyncio.gather(*tasks)
    
    assert len(results) == 3
    assert all(isinstance(result, dict) for result in results)
    assert len(model_manager.review_history) == 3

def test_model_initialization_error():
    """Test error handling during model initialization."""
    with patch('src.model_manager.AutoModelForCausalLM', 
              side_effect=Exception("Model load error")), \
         patch('src.model_manager.AutoTokenizer'):
        with pytest.raises(Exception):
            ModelManager()

if __name__ == '__main__':
    pytest.main([__file__])
