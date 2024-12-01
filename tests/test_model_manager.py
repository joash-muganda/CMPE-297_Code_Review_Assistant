import pytest
from unittest.mock import Mock, patch
import torch
from src.model_manager import ModelManager
from src.config import Config

@pytest.fixture
def mock_tokenizer():
    tokenizer = Mock()
    tokenizer.encode.return_value = torch.tensor([[1, 2, 3]])
    tokenizer.decode.return_value = "Test generated text"
    tokenizer.return_tensors = "pt"
    return tokenizer

@pytest.fixture
def mock_model():
    model = Mock()
    model.generate.return_value = torch.tensor([[1, 2, 3, 4]])
    model.device = torch.device("cpu")
    return model

@pytest.fixture
def model_manager(mock_tokenizer, mock_model):
    with patch('transformers.AutoTokenizer.from_pretrained') as mock_get_tokenizer:
        with patch('transformers.AutoModelForCausalLM.from_pretrained') as mock_get_model:
            mock_get_tokenizer.return_value = mock_tokenizer
            mock_get_model.return_value = mock_model
            
            manager = ModelManager(model_name=Config.MODEL_NAME)
            return manager

def test_model_initialization(model_manager, mock_tokenizer, mock_model):
    """Test successful model initialization."""
    assert model_manager.tokenizer == mock_tokenizer
    assert model_manager.model == mock_model
    assert model_manager.model_name == Config.MODEL_NAME

def test_generate_text(model_manager, mock_tokenizer, mock_model):
    """Test text generation."""
    input_text = "Test input"
    result = model_manager.generate_text(input_text)
    
    # Verify tokenizer was called correctly
    mock_tokenizer.assert_called_with(input_text, return_tensors="pt")
    
    # Verify model.generate was called
    assert mock_model.generate.called
    
    # Verify output
    assert isinstance(result, str)
    assert result == "Test generated text"

def test_generate_text_with_params(model_manager, mock_tokenizer, mock_model):
    """Test text generation with custom parameters."""
    input_text = "Test input"
    max_new_tokens = 100
    
    result = model_manager.generate_text(input_text, max_new_tokens=max_new_tokens)
    
    # Verify model.generate was called with correct parameters
    generate_kwargs = mock_model.generate.call_args[1]
    assert generate_kwargs["max_new_tokens"] == max_new_tokens
    assert "temperature" in generate_kwargs
    assert "top_p" in generate_kwargs

@patch('transformers.AutoTokenizer.from_pretrained')
@patch('transformers.AutoModelForCausalLM.from_pretrained')
def test_model_initialization_error(mock_get_model, mock_get_tokenizer):
    """Test error handling during model initialization."""
    mock_get_tokenizer.side_effect = Exception("Failed to load tokenizer")
    
    with pytest.raises(Exception) as exc_info:
        ModelManager(model_name=Config.MODEL_NAME)
    
    assert "Failed to load tokenizer" in str(exc_info.value)

def test_generate_text_error(model_manager, mock_tokenizer, mock_model):
    """Test error handling during text generation."""
    mock_model.generate.side_effect = Exception("Generation error")
    
    with pytest.raises(Exception) as exc_info:
        model_manager.generate_text("Test input")
    
    assert "Generation error" in str(exc_info.value)

def test_model_device(model_manager):
    """Test model device handling."""
    assert hasattr(model_manager.model, 'device')
    assert isinstance(model_manager.model.device, torch.device)

def test_token_length_limit(model_manager, mock_tokenizer, mock_model):
    """Test handling of token length limits."""
    # Create a long input text
    long_input = "test " * 1000
    
    result = model_manager.generate_text(long_input)
    
    # Verify the model still generates output
    assert isinstance(result, str)
    assert result == "Test generated text"

def test_model_parameters(model_manager, mock_model):
    """Test model generation parameters."""
    input_text = "Test input"
    result = model_manager.generate_text(
        input_text,
        max_new_tokens=50,
    )
    
    # Verify generation parameters
    generate_kwargs = mock_model.generate.call_args[1]
    assert generate_kwargs["temperature"] == 0.7  # Default from config
    assert generate_kwargs["top_p"] == 0.9  # Default from config
    assert generate_kwargs["max_new_tokens"] == 50

if __name__ == '__main__':
    pytest.main([__file__])
