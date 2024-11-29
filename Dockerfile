# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p logs src/static

# Copy application code
COPY . .

# Ensure static files are in the correct location
RUN if [ -f src/static/dashboard.html ]; then echo "Dashboard file exists"; else mv src/dashboard.html src/static/ 2>/dev/null || true; fi

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose ports for FastAPI and Prometheus
EXPOSE 8000
EXPOSE 9090

# Run the application
CMD ["python", "run_server.py"]
