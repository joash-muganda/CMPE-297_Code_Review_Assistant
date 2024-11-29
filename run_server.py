import uvicorn
import logging
from prometheus_fastapi_instrumentator import Instrumentator
from src.api import app
from src.config import settings, Config

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=settings.LOG_FILE
)
logger = logging.getLogger(__name__)

# Add Prometheus metrics
if settings.ENABLE_METRICS:
    Instrumentator().instrument(app).expose(
        app,
        endpoint="/metrics"
    )

def main():
    """
    Main entry point for the application.
    Starts the FastAPI server with the configured settings.
    """
    try:
        # Print startup configuration information
        print(f"Starting {Config.API_TITLE} on {Config.HOST}:{Config.PORT}...")
        print(f"Model: {Config.MODEL_NAME}")
        print(f"Database URL: {Config.DATABASE_URL}")
        
        logger.info(f"Starting server on {settings.HOST}:{settings.PORT}")
        logger.info(f"Debug mode: {settings.DEBUG}")
        logger.info(f"API Documentation available at: http://{settings.HOST}:{settings.PORT}/docs")
        
        # Configure uvicorn server
        config = uvicorn.Config(
            "src.api:app",
            host=settings.HOST,
            port=settings.PORT,
            reload=settings.DEBUG,
            log_level=settings.LOG_LEVEL.lower(),
            workers=1
        )
        
        # Start server
        server = uvicorn.Server(config)
        server.run()
        
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        raise

if __name__ == "__main__":
    main()
