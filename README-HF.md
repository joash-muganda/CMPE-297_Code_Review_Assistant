# Code Review Assistant - Hugging Face Space

This is a FastAPI application that provides automated code reviews using the Gemma model. It's deployed on Hugging Face Spaces.

## Features

- Automated code review using Gemma model
- Support for multiple programming languages
- Real-time feedback
- Performance metrics tracking
- Review history

## Environment Variables

The following environment variables need to be set in your Hugging Face Space:

- `HUGGING_FACE_TOKEN`: Your Hugging Face API token
- `MODEL_NAME`: google/gemma-2-2b-it
- `DEBUG`: false
- `LOG_LEVEL`: INFO
- `PORT`: 7860

## Deployment Instructions

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click "New Space"
3. Choose:
   - Owner: Your account
   - Space name: code-review-assistant
   - License: Choose appropriate license
   - SDK: Docker
4. Upload these files:
   - All project files
   - Rename `Dockerfile.huggingface` to `Dockerfile`
5. Set the environment variables in Space Settings
6. Deploy!

## Usage

Once deployed, you can access the application at:
`https://huggingface.co/spaces/[YOUR-USERNAME]/code-review-assistant`

## API Documentation

Access the API documentation at:
`https://huggingface.co/spaces/[YOUR-USERNAME]/code-review-assistant/docs`
