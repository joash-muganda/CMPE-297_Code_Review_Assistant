from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os
from pydantic import BaseModel
from typing import Optional, List, Dict
import logging
from datetime import datetime

from .config import Config
from .model_manager import ModelManager

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=Config.LOG_FILE
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=Config.API_TITLE,
    description=Config.API_DESCRIPTION,
    version=Config.API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Initialize model manager
model_manager = ModelManager(model_name=Config.MODEL_NAME)

# Pydantic models for request/response
class CodeReviewRequest(BaseModel):
    code: str
    language: Optional[str] = None
    context: Optional[str] = None

class CodeReviewResponse(BaseModel):
    review: str
    metrics: Dict
    timestamp: str

class MetricsResponse(BaseModel):
    total_reviews: int
    avg_response_time: float
    token_usage: int

@app.get("/")
async def root():
    """Serve the main dashboard."""
    return FileResponse(os.path.join(static_dir, "dashboard.html"))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/v1/review", response_model=CodeReviewResponse)
async def review_code(request: CodeReviewRequest):
    """Submit code for review."""
    try:
        result = await model_manager.review_code(request.code, request.language)
        return CodeReviewResponse(
            review=result["review"],
            metrics=result["metrics"],
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        logger.error(f"Error during code review: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/metrics", response_model=MetricsResponse)
async def get_metrics():
    """Get current metrics."""
    try:
        metrics = model_manager.get_metrics()
        return MetricsResponse(
            total_reviews=metrics["total_reviews"],
            avg_response_time=metrics["avg_response_time"],
            token_usage=metrics["token_usage"]
        )
    except Exception as e:
        logger.error(f"Error retrieving metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/history")
async def get_review_history(limit: Optional[int] = None):
    """Get review history."""
    try:
        history = model_manager.get_review_history(limit)
        return {"history": history}
    except Exception as e:
        logger.error(f"Error retrieving review history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/export-metrics")
async def export_metrics(background_tasks: BackgroundTasks):
    """Export metrics to file."""
    try:
        export_path = f"logs/metrics_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        background_tasks.add_task(model_manager.export_metrics, export_path)
        return {"message": f"Metrics export scheduled to {export_path}"}
    except Exception as e:
        logger.error(f"Error scheduling metrics export: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later."}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=Config.DEBUG
    )
