from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional, List, Dict
import logging
from datetime import datetime
import os
import uuid

from .config import Config
from .model_manager import ModelManager
from .code_reviewer import CodeReviewer

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

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Mount static files directory
static_dir = os.path.join(current_dir, "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Initialize templates
templates = Jinja2Templates(directory=static_dir)

# Initialize components
model_manager = ModelManager(model_name=Config.MODEL_NAME)
code_reviewer = CodeReviewer(model_manager)

# Pydantic models
class CodeReviewRequest(BaseModel):
    code: str
    language: str
    prompt_version: Optional[str] = "default"

class CodeReviewResponse(BaseModel):
    review_id: str
    suggestions: List[Dict]
    metrics: Dict
    timestamp: str

class MetricsResponse(BaseModel):
    total_reviews: int
    avg_response_time: float
    avg_suggestions: float
    reviews_today: int

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Serve the dashboard page."""
    try:
        return templates.TemplateResponse(
            "dashboard.html",
            {"request": request}
        )
    except Exception as e:
        logger.error(f"Error serving dashboard: {str(e)}")
        raise HTTPException(status_code=500, detail="Error serving dashboard")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "model_status": "loaded"
    }

@app.post("/api/v1/review", response_model=CodeReviewResponse)
async def review_code(request: CodeReviewRequest, background_tasks: BackgroundTasks):
    """Submit code for review."""
    try:
        review_id = str(uuid.uuid4())
        review = code_reviewer.review_code(
            code=request.code,
            language=request.language,
            review_id=review_id
        )
        
        # Add background task to update metrics
        background_tasks.add_task(update_metrics, review)
        
        return CodeReviewResponse(
            review_id=review.review_id,
            suggestions=review.suggestions,
            metrics=review.metrics,
            timestamp=review.timestamp.isoformat()
        )
    except Exception as e:
        logger.error(f"Error during code review: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/metrics", response_model=MetricsResponse)
async def get_metrics():
    """Get review metrics."""
    try:
        metrics = code_reviewer.get_review_metrics()
        return MetricsResponse(**metrics)
    except Exception as e:
        logger.error(f"Error fetching metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/history")
async def get_history(limit: Optional[int] = None):
    """Get review history."""
    try:
        history = code_reviewer.get_review_history(limit)
        return [{
            "review_id": review.review_id,
            "language": review.language,
            "suggestions": review.suggestions,
            "metrics": review.metrics,
            "timestamp": review.timestamp.isoformat()
        } for review in history]
    except Exception as e:
        logger.error(f"Error fetching history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def update_metrics(review):
    """Background task to update metrics."""
    try:
        # Here you could implement additional metric tracking
        # such as saving to a database or updating Prometheus metrics
        logger.info(f"Updated metrics for review {review.review_id}")
    except Exception as e:
        logger.error(f"Error updating metrics: {str(e)}")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later."}
    )
