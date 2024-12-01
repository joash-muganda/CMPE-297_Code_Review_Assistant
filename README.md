# Code Review Assistant

An automated code review system powered by Gemma-2b that provides intelligent code analysis, suggestions for improvements, and tracks review metrics.

## Features

- **Automated Code Review**

  - Analyzes code quality and suggests improvements
  - Identifies potential bugs and security issues
  - Recommends best practices and optimizations
  - Supports multiple programming languages

- **LLMOps Integration**

  - Uses Gemma-2b for intelligent code analysis
  - Tracks model performance and accuracy
  - Monitors response times and token usage
  - Supports A/B testing of different prompts

- **Performance Monitoring**

  - Real-time metrics dashboard
  - Review history tracking
  - Response time monitoring
  - Usage statistics

- **Modern Web Interface**
  - Interactive code submission
  - Syntax highlighting
  - Real-time review results
  - Metrics visualization

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/code-review-assistant.git
cd code-review-assistant
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:

- Copy `.env.example` to `.env`
- Update the configuration values as needed
- Ensure you have a valid Hugging Face API token

## Running the Application

### Using Docker (Recommended)

1. Build and start the containers:

```bash
docker-compose up --build
```

2. Access the application:

- Web Interface: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Metrics: http://localhost:9090

### Manual Setup

1. Start the application:

```bash
python run_server.py
```

2. Access the application at http://localhost:8000

## Usage

### Web Interface

1. Open http://localhost:8000 in your browser
2. Select the programming language
3. Paste your code in the editor
4. Click "Submit for Review"
5. View the detailed review results

### API Endpoints

- `POST /api/v1/review`: Submit code for review

  ```json
  {
    "code": "your code here",
    "language": "python"
  }
  ```

- `GET /api/v1/metrics`: Get system metrics
- `GET /api/v1/history`: Get review history
- `GET /health`: Check system health

### Example Usage

See `examples/demo.py` for detailed usage examples:

```python
from code_review_assistant import CodeReviewer

reviewer = CodeReviewer()
result = reviewer.review_code(
    code="your code here",
    language="python"
)
print(result.suggestions)
```

## Monitoring

### Metrics Dashboard

Access the metrics dashboard at http://localhost:9090 to view:

- Review counts and response times
- Model performance metrics
- System health statistics
- Usage patterns

### Prometheus Integration

Custom metrics are exposed at `/metrics` and include:

- `code_review_requests_total`: Total number of review requests
- `code_review_response_time`: Review response times
- `code_review_token_usage`: Token usage per review
- `code_review_errors_total`: Error counts by type

## Development

### Running Tests

```bash
pytest tests/
```

### Adding New Features

1. Create a new branch:

```bash
git checkout -b feature/your-feature
```

2. Make your changes and add tests
3. Run the test suite
4. Submit a pull request

## Configuration

Key configuration options in `.env`:

```ini
# API Settings
API_VERSION=v1
PORT=8000
DEBUG=false

# Model Settings
MODEL_NAME=google/gemma-2b-it
MAX_INPUT_LENGTH=2048
TEMPERATURE=0.7

# Monitoring Settings
ENABLE_METRICS=true
PROMETHEUS_METRICS_PORT=9090
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
