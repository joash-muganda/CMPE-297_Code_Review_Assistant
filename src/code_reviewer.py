from typing import Dict, List, Optional
import logging
from datetime import datetime
from .model_manager import ModelManager
from .config import Config

logger = logging.getLogger(__name__)

class CodeReview:
    def __init__(self, code: str, language: str, review_id: str):
        self.code = code
        self.language = language
        self.review_id = review_id
        self.timestamp = datetime.now()
        self.suggestions: List[Dict] = []
        self.metrics: Dict = {}

class CodeReviewer:
    def __init__(self, model_manager: ModelManager):
        self.model_manager = model_manager
        self.review_history: List[CodeReview] = []
        
    def _create_review_prompt(self, code: str, language: str) -> str:
        """Create a structured prompt for code review."""
        return f"""As a code reviewer, analyze the following {language} code and provide specific suggestions for:
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

    def review_code(self, code: str, language: str, review_id: str) -> CodeReview:
        """Perform code review using the LLM."""
        try:
            start_time = datetime.now()
            
            # Create review instance
            review = CodeReview(code, language, review_id)
            
            # Generate review prompt
            prompt = self._create_review_prompt(code, language)
            
            # Get model response
            response = self.model_manager.generate_text(
                prompt,
                max_new_tokens=Config.MAX_OUTPUT_LENGTH
            )
            
            # Parse and structure the response
            sections = self._parse_review_response(response)
            
            # Store suggestions
            review.suggestions = sections
            
            # Calculate metrics
            end_time = datetime.now()
            review.metrics = {
                'response_time': (end_time - start_time).total_seconds(),
                'code_length': len(code),
                'suggestion_count': len(sections)
            }
            
            # Store review in history
            self._add_to_history(review)
            
            return review
            
        except Exception as e:
            logger.error(f"Error during code review: {str(e)}")
            raise

    def _parse_review_response(self, response: str) -> List[Dict]:
        """Parse the LLM response into structured sections."""
        sections = []
        current_section = None
        
        for line in response.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('- '):
                if ':' in line:
                    section_type, content = line[2:].split(':', 1)
                    current_section = {
                        'type': section_type.strip(),
                        'items': []
                    }
                    sections.append(current_section)
            elif current_section and line:
                current_section['items'].append(line)
                
        return sections

    def _add_to_history(self, review: CodeReview):
        """Add review to history and maintain size limit."""
        self.review_history.append(review)
        if len(self.review_history) > Config.MAX_HISTORY_ITEMS:
            self.review_history.pop(0)

    def get_review_metrics(self) -> Dict:
        """Calculate aggregate metrics from review history."""
        if not self.review_history:
            return {}
            
        total_reviews = len(self.review_history)
        avg_response_time = sum(r.metrics['response_time'] for r in self.review_history) / total_reviews
        avg_suggestions = sum(r.metrics['suggestion_count'] for r in self.review_history) / total_reviews
        
        return {
            'total_reviews': total_reviews,
            'avg_response_time': avg_response_time,
            'avg_suggestions': avg_suggestions,
            'reviews_today': sum(1 for r in self.review_history if r.timestamp.date() == datetime.now().date())
        }

    def get_review_history(self, limit: Optional[int] = None) -> List[CodeReview]:
        """Get review history with optional limit."""
        if limit:
            return self.review_history[-limit:]
        return self.review_history
