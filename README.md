# Code Review Assistant

An automated code review system powered by Gemma-2b that provides intelligent code analysis, suggestions for improvements, and tracks review metrics.

## Features

- **Automated Code Review**: Submit code snippets or files for AI-powered review
- **Intelligent Analysis**: Get suggestions for improvements, bug fixes, and best practices
- **Multiple Language Support**: Handles Python, JavaScript, Java, C++, and more
- **Performance Monitoring**: Track review metrics and response times
- **Review History**: Maintain a searchable history of all code reviews
- **Interactive Dashboard**: User-friendly interface for code submission and review management
- **Prometheus Integration**: Real-time metrics and monitoring

## Prerequisites

- Docker and Docker Compose
- Python 3.10 or higher (for local development)
- 4GB+ RAM recommended

## Quick Start

1. Clone the repository:

```bash
git clone <repository-url>
cd code-review-assistant
```

2. Create a .env file:

```bash
cp .env.example .env
# Edit .env with your settings
```

3. Start the application using Docker:

```bash
docker-compose up -d
```

4. Access the application:

- Dashboard: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Metrics: http://localhost:9091

## Local Development Setup

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python run_server.py
```

## API Endpoints

- `POST /api/v1/review`: Submit code for review
- `GET /api/v1/metrics`: Get performance metrics
- `GET /api/v1/history`: Get review history
- `POST /api/v1/export-metrics`: Export metrics to file
- `GET /health`: Health check endpoint

## Configuration

Key configuration options in `.env`:

- `DEBUG`: Enable/disable debug mode
- `LOG_LEVEL`: Logging level (INFO, DEBUG, etc.)
- `MODEL_NAME`: Model to use for code review
- `MAX_INPUT_LENGTH`: Maximum code input length
- `ENABLE_METRICS`: Enable/disable Prometheus metrics

## Monitoring

The application includes Prometheus integration for monitoring:

- Response times
- Token usage
- Review counts
- Error rates

Access Prometheus dashboard at http://localhost:9091

## Architecture

The application consists of several key components:

1. **API Server**: FastAPI-based REST API
2. **Model Manager**: Handles Gemma-2b model operations
3. **Dashboard**: Web interface for code submission and review
4. **Metrics**: Prometheus-based monitoring system

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Testing

Run the test suite:

```bash
pytest
```

Run specific tests:

```bash
pytest tests/test_code_review.py
pytest tests/test_model_manager.py
```

## License

[MIT License](LICENSE)

## Support

For support, please open an issue in the GitHub repository.
