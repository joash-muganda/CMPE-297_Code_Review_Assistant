import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from a .env file
load_dotenv()

class Config:
    """Application Configuration"""

    # API Settings
    API_VERSION = os.getenv("API_VERSION", "v1")
    API_TITLE = os.getenv("API_TITLE", "Code Review Assistant API")
    API_DESCRIPTION = os.getenv("API_DESCRIPTION", "An automated code review system powered by Gemma-2b-it")
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

    # Model Settings
    MODEL_NAME = os.getenv("MODEL_NAME", "google/gemma-2-2b-it")
    MAX_INPUT_LENGTH = int(os.getenv("MAX_INPUT_LENGTH", 2048))
    MAX_OUTPUT_LENGTH = int(os.getenv("MAX_OUTPUT_LENGTH", 1024))
    TEMPERATURE = float(os.getenv("TEMPERATURE", 0.7))
    TOP_P = float(os.getenv("TOP_P", 0.95))
    HUGGING_FACE_TOKEN = os.getenv("HUGGING_FACE_TOKEN", "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")

    # Database Settings
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./code_review.db")

    # Monitoring Settings
    PROMETHEUS_METRICS_PORT = int(os.getenv("PROMETHEUS_METRICS_PORT", 9090))
    ENABLE_METRICS = os.getenv("ENABLE_METRICS", "true").lower() == "true"

    # Security Settings
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key-change-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    # Logging Settings
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs/code_review.log")

    # Review History Settings
    MAX_HISTORY_ITEMS = int(os.getenv("MAX_HISTORY_ITEMS", 1000))
    HISTORY_RETENTION_DAYS = int(os.getenv("HISTORY_RETENTION_DAYS", 30))

    @staticmethod
    def validate():
        """Validate configuration settings. Raise exceptions for invalid values."""
        # Log configuration values for debugging
        logger.info("Configuration Values:")
        logger.info(f"MODEL_NAME: {Config.MODEL_NAME}")
        logger.info(f"HUGGING_FACE_TOKEN: {'Set' if Config.HUGGING_FACE_TOKEN else 'Not Set'}")
        logger.info(f"HOST: {Config.HOST}")
        logger.info(f"PORT: {Config.PORT}")
        logger.info(f"DEBUG: {Config.DEBUG}")

        if not Config.HUGGING_FACE_TOKEN:
            raise ValueError("HUGGING_FACE_TOKEN must be set to access Hugging Face gated models.")
        if Config.TEMPERATURE < 0 or Config.TEMPERATURE > 1:
            raise ValueError("TEMPERATURE must be between 0 and 1.")
        if Config.TOP_P < 0 or Config.TOP_P > 1:
            raise ValueError("TOP_P must be between 0 and 1.")

# Create settings instance
settings = Config()

# Validate configuration at startup
settings.validate()
