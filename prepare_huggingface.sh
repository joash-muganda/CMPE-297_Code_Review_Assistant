#!/bin/bash

# Create a new directory for Hugging Face deployment
mkdir -p huggingface_deploy

# Copy necessary files
cp -r src huggingface_deploy/
cp requirements.txt huggingface_deploy/
cp README-HF.md huggingface_deploy/README.md
cp Dockerfile.huggingface huggingface_deploy/Dockerfile
cp .gitignore-hf huggingface_deploy/.gitignore

# Create empty logs directory
mkdir -p huggingface_deploy/logs

echo "Files prepared for Hugging Face deployment in huggingface_deploy directory"
echo "Next steps:"
echo "1. Go to huggingface.co/spaces"
echo "2. Create a new Space"
echo "3. Choose Docker as the SDK"
echo "4. Upload the contents of huggingface_deploy directory"
echo "5. Set the required environment variables in the Space settings"
