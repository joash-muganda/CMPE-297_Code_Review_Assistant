# Use NVIDIA CUDA base image
FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-distutils \
    python3.11-dev \
    python3-pip \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create necessary directories
RUN mkdir -p logs src/static

# Update alternatives to use Python 3.11
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

# Upgrade pip and install numpy first
RUN python3.11 -m pip install --upgrade pip
RUN python3.11 -m pip install --no-cache-dir "numpy<2.0.0"

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install PyTorch with CUDA support
RUN python3.11 -m pip install --no-cache-dir torch==2.1.0 --extra-index-url https://download.pytorch.org/whl/cu121

# Install other Python dependencies
RUN python3.11 -m pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Ensure proper permissions for logs directory
RUN chmod 777 logs

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV TORCH_CUDA_ARCH_LIST="7.5 8.0 8.6"
ENV CUDA_VISIBLE_DEVICES=0

# Expose ports for FastAPI and Prometheus
EXPOSE 8000 9090

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application with Python 3.11
CMD ["python3.11", "-m", "run_server"]
