"""FastAPI application entry point."""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from src.config import settings
from src.api.tasks import router as tasks_router
from src.api.auth import router as auth_router
import logging
import time
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="A persistent, multi-user Todo API built with FastAPI, SQLModel, and PostgreSQL",
    version="1.0.0",
    debug=settings.debug,
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests and their processing time.

    Args:
        request: Incoming HTTP request
        call_next: Next middleware/handler in chain

    Returns:
        Response from the next handler
    """
    start_time = time.time()

    # Log request
    logger.info(f"Request: {request.method} {request.url.path}")

    # Process request
    response = await call_next(request)

    # Calculate processing time
    process_time = time.time() - start_time

    # Log response
    logger.info(
        f"Response: {request.method} {request.url.path} "
        f"Status: {response.status_code} "
        f"Duration: {process_time:.3f}s"
    )

    # Add processing time header
    response.headers["X-Process-Time"] = str(process_time)

    return response


# Global exception handler for database errors
@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handle SQLAlchemy database errors.

    Args:
        request: HTTP request that caused the error
        exc: SQLAlchemy exception

    Returns:
        JSON error response
    """
    logger.error(f"Database error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "A database error occurred. Please try again later.",
            "type": "database_error"
        }
    )


# Global exception handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors with detailed messages.

    Args:
        request: HTTP request that caused the error
        exc: Validation exception

    Returns:
        JSON error response with validation details
    """
    logger.warning(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "type": "validation_error"
        }
    )


# Global exception handler for unexpected errors
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors gracefully.

    Args:
        request: HTTP request that caused the error
        exc: Exception

    Returns:
        JSON error response
    """
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An unexpected error occurred. Please try again later.",
            "type": "internal_error"
        }
    )


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(tasks_router)


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint.

    Returns:
        dict: Health status with timestamp and version

    Example:
        GET /health
        Response: {"status": "healthy", "timestamp": "2026-02-05T19:00:00Z", "version": "1.0.0"}
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": "1.0.0"
    }


@app.get("/", tags=["Root"])
def root():
    """Root endpoint with API information.

    Returns:
        dict: API information

    Example:
        GET /
        Response: {"name": "Phase 2 Todo API", "version": "1.0.0", "docs": "/docs", "health": "/health"}
    """
    return {
        "name": settings.app_name,
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }
