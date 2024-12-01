from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import logging
from .config import Config

class ModelManager:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self._initialize_model()

    def _initialize_model(self):
        """Initialize the model and tokenizer."""
        try:
            logging.info(f"Loading model: {self.model_name}")

            # Load tokenizer with trust_remote_code=True
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True,  # Required for Gemma
                token=Config.HUGGING_FACE_TOKEN
            )
            logging.info("Tokenizer loaded successfully.")

            # Load model with specific configuration for memory management
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                trust_remote_code=True,  # Required for Gemma
                torch_dtype=torch.float32,
                offload_folder="model_cache",  # Specify offload folder
                offload_state_dict=True,  # Enable state dict offloading
                token=Config.HUGGING_FACE_TOKEN
            )
            
            logging.info("Model loaded successfully")

        except Exception as e:
            logging.error(f"Error loading model or tokenizer: {str(e)}")
            raise

    def generate_text(self, input_text: str, max_new_tokens: int = 256):
        """Generate text using the model."""
        try:
            # Create chat messages format
            messages = [
                {"role": "user", "content": input_text}
            ]
            
            # Apply chat template with trust_remote_code=True
            inputs = self.tokenizer.apply_chat_template(
                messages,
                return_tensors="pt",
                return_dict=True,
                trust_remote_code=True  # Required for Gemma chat template
            )
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_new_tokens=max_new_tokens,
                    temperature=0.7,
                    top_p=0.9,
                    trust_remote_code=True  # Required for Gemma generation
                )
            
            # Decode and return the response
            return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
        except Exception as e:
            logging.error(f"Error during text generation: {str(e)}")
            raise

    def _create_code_review_prompt(self, code: str, language: str) -> str:
        """Create a structured prompt for code review."""
        return f"""As an expert code reviewer, analyze the following {language} code and provide specific suggestions for:
1. Code quality improvements
2. Potential bugs or issues
3. Performance optimizations
4. Security concerns
5. Best practices and standards

Code to review:
```{language}
{code}
```

Provide your review in the following format:
- Issues: (list critical problems)
- Improvements: (list suggested enhancements)
- Best Practices: (list recommendations)
- Security: (list security concerns)
"""

    def review_code(self, code: str, language: str) -> str:
        """Perform code review using the model."""
        prompt = self._create_code_review_prompt(code, language)
        return self.generate_text(prompt, max_new_tokens=512)
