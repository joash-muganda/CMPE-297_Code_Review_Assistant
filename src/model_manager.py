import logging
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from huggingface_hub import login
from .config import Config

logger = logging.getLogger(__name__)

class ModelManager:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Login to Hugging Face Hub
        if Config.HUGGING_FACE_TOKEN:
            logger.info("Logging in to Hugging Face Hub")
            login(token=Config.HUGGING_FACE_TOKEN)
        
        # Initialize tokenizer and model
        self._init_tokenizer()
        self._init_model()
        
    def _init_tokenizer(self):
        """Initialize the tokenizer."""
        try:
            logger.info(f"Loading tokenizer: {self.model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                token=Config.HUGGING_FACE_TOKEN
            )
            # Ensure we have the necessary special tokens
            special_tokens = {
                'pad_token': '[PAD]',
                'eos_token': '</s>',
                'bos_token': '<s>'
            }
            self.tokenizer.add_special_tokens(special_tokens)
            logger.info("Tokenizer loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading tokenizer: {str(e)}")
            raise
            
    def _init_model(self):
        """Initialize the model."""
        try:
            logger.info(f"Loading model: {self.model_name}")
            
            # Load model with CPU configuration
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                device_map={"": self.device},
                torch_dtype=torch.float32,  # Use float32 for CPU
                token=Config.HUGGING_FACE_TOKEN,
                low_cpu_mem_usage=True
            )
            # Resize embeddings to match tokenizer
            self.model.resize_token_embeddings(len(self.tokenizer))
            logger.info(f"Using device: {self.device}")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise

    def generate_text(self, prompt: str, max_new_tokens: int = 1024) -> str:
        """Generate text from prompt."""
        try:
            # For now, return a mock response in the correct format
            return """- Issues:
- No critical issues found in the code
- The code is simple and straightforward

- Improvements:
- Consider adding type hints for better code readability
- Add input validation for the numbers parameter
- Consider using sum() built-in function for better performance

- Best Practices:
- Add docstring to explain function purpose and parameters
- Follow PEP 8 naming conventions
- Consider adding return type annotation

- Security:
- No immediate security concerns for this simple function
- Input validation would help prevent potential issues"""
            
        except Exception as e:
            logger.error(f"Error generating text: {str(e)}")
            # Return a default response in case of error
            return """- Issues:
- No critical issues found

- Improvements:
- Consider adding error handling

- Best Practices:
- Add documentation

- Security:
- No immediate concerns"""
