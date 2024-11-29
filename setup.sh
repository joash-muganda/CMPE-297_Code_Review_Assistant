#!/bin/bash

# Exit on error
set -e

echo "Setting up Code Review Assistant..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p logs

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env || echo "Warning: .env.example not found. Please configure .env manually."
fi

# Initialize database
echo "Initializing database..."
python -c "from src.model_manager import ModelManager; ModelManager()"

echo "Setup complete! You can now run the application with:"
echo "python run_server.py"

# Deactivate virtual environment
deactivate
