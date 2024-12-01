import uvicorn
import logging
from prometheus_fastapi_instrumentator import Instrumentator
from src.api import app
from src.config import Config

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=Config.LOG_FILE
)
logger = logging.getLogger(__name__)

# Add Prometheus metrics
if Config.ENABLE_METRICS:
    Instrumentator().instrument(app).expose(
        app,
        endpoint="/metrics"
    )

if __name__ == "__main__":
    try:
        # Print startup configuration information
        print(f"Starting {Config.API_TITLE} on {Config.HOST}:{Config.PORT}...")
        print(f"Model: {Config.MODEL_NAME}")
        print(f"Database URL: {Config.DATABASE_URL}")
        
        # Start uvicorn server
        uvicorn.run(
            app,  # Pass the app instance directly
            host=Config.HOST,
            port=Config.PORT,
            reload=Config.DEBUG,
            log_level=Config.LOG_LEVEL.lower()
        )
        
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        raise
