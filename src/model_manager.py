from transformers import AutoTokenizer, AutoModelForCausalLM
import logging
import json
from datetime import datetime
from typing import Dict, List, Optional
import torch
from .config import Config


class ModelManager:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.metrics = {
            "total_reviews": 0,
            "total_response_time": 0,
            "token_usage": 0
        }
        self.review_history = []
        self._initialize_model()

    def _initialize_model(self):
        """Initialize the model and tokenizer."""
        try:
            logging.info(f"Loading model: {self.model_name}")

            # Load tokenizer with remote code trust enabled
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True,
                token=Config.HUGGING_FACE_TOKEN
            )
            logging.info("Tokenizer loaded successfully.")

            # Load model with remote code trust enabled
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                trust_remote_code=True,
                token=Config.HUGGING_FACE_TOKEN
            )
            logging.info("Model loaded successfully.")

        except Exception as e:
            logging.error(f"Error loading model or tokenizer: {str(e)}")
            raise

    async def review_code(self, code: str, language: Optional[str] = None) -> Dict:
        """Review code and provide feedback."""
        start_time = datetime.now()
        try:
            # Prepare prompt
            prompt = f"""Review the following {language if language else ''} code and provide feedback:

{code}

Review:"""
            
            # Generate review
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=500,
                temperature=0.7,
                top_p=0.9
            )
            review = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            review = review.replace(prompt, "").strip()

            # Update metrics
            response_time = (datetime.now() - start_time).total_seconds()
            self.metrics["total_reviews"] += 1
            self.metrics["total_response_time"] += response_time
            self.metrics["token_usage"] += len(outputs[0])

            # Add to history
            history_entry = {
                "code_snippet": code,
                "language": language,
                "review": review,
                "timestamp": datetime.now().isoformat(),
                "response_time": response_time
            }
            self.review_history.append(history_entry)

            return {
                "review": review,
                "metrics": {
                    "response_time": response_time,
                    "tokens_used": len(outputs[0])
                }
            }

        except Exception as e:
            logging.error(f"Error during code review: {str(e)}")
            raise

    def get_metrics(self) -> Dict:
        """Get current metrics."""
        try:
            return {
                "total_reviews": self.metrics["total_reviews"],
                "avg_response_time": (
                    self.metrics["total_response_time"] / self.metrics["total_reviews"]
                    if self.metrics["total_reviews"] > 0
                    else 0
                ),
                "token_usage": self.metrics["token_usage"]
            }
        except Exception as e:
            logging.error(f"Error retrieving metrics: {str(e)}")
            raise

    def get_review_history(self, limit: Optional[int] = None) -> List[Dict]:
        """Get review history."""
        try:
            history = sorted(
                self.review_history,
                key=lambda x: x["timestamp"],
                reverse=True
            )
            return history[:limit] if limit else history
        except Exception as e:
            logging.error(f"Error retrieving review history: {str(e)}")
            raise

    def export_metrics(self, export_path: str):
        """Export metrics to file."""
        try:
            export_data = {
                "metrics": self.metrics,
                "history": self.review_history,
                "export_timestamp": datetime.now().isoformat()
            }
            with open(export_path, 'w') as f:
                json.dump(export_data, f, indent=2)
            logging.info(f"Metrics exported to {export_path}")
        except Exception as e:
            logging.error(f"Error exporting metrics: {str(e)}")
            raise
