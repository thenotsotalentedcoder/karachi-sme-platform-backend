"""Main FastAPI application."""

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
import time
import logging

from app.config import settings
from app.database import create_tables
from app.api.api import api_router
from app.utils.validators import ValidationError

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    debug=settings.DEBUG,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Add trusted host middleware for security
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS + ["*"] if settings.DEBUG else settings.ALLOWED_HOSTS
)


# Middleware for request timing and logging
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time to response headers and log requests."""
    start_time = time.time()
    
    # Log incoming request
    logger.info(f"🔄 {request.method} {request.url.path} - Started")
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Add timing header
        response.headers["X-Process-Time"] = str(f"{process_time:.4f}")
        
        # Log response
        logger.info(f"✅ {request.method} {request.url.path} - {response.status_code} - {process_time:.4f}s")
        
        return response
        
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"❌ {request.method} {request.url.path} - Error: {str(e)} - {process_time:.4f}s")
        raise


# Custom exception handlers
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    """Handle custom validation errors."""
    logger.warning(f"Validation error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Validation Error",
            "message": str(exc),
            "type": "validation_error"
        }
    )


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle FastAPI request validation errors."""
    logger.warning(f"Request validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Request Validation Error",
            "message": "Invalid request data",
            "details": exc.errors(),
            "type": "request_validation_error"
        }
    )


@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handle database errors."""
    logger.error(f"Database error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Database Error",
            "message": "A database error occurred. Please try again later.",
            "type": "database_error"
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors."""
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Please try again later.",
            "type": "internal_error"
        }
    )


# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    logger.info("🚀 Starting Karachi SME Intelligence Platform...")
    
    try:
        # Create database tables
        create_tables()
        logger.info("📊 Database tables created successfully")
        
        # Log application info
        logger.info(f"📋 Application: {settings.PROJECT_NAME} v{settings.VERSION}")
        logger.info(f"🌍 Environment: {settings.ENVIRONMENT}")
        logger.info(f"🔧 Debug mode: {settings.DEBUG}")
        logger.info(f"🎯 API base path: {settings.API_V1_STR}")
        
        logger.info("✅ Application startup completed successfully")
        
    except Exception as e:
        logger.error(f"❌ Application startup failed: {str(e)}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    logger.info("🔄 Shutting down Karachi SME Intelligence Platform...")
    
    # Perform cleanup tasks here if needed
    # e.g., close database connections, cleanup temporary files, etc.
    
    logger.info("✅ Application shutdown completed")


# Health check endpoints
@app.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns application status and basic system information.
    """
    return {
        "status": "healthy",
        "application": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "timestamp": time.time(),
        "uptime": "operational"
    }


@app.get("/health/detailed", tags=["health"])
async def detailed_health_check():
    """
    Detailed health check with system diagnostics.
    
    Returns comprehensive system health information.
    """
    try:
        # Test database connection
        from app.database import SessionLocal
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        database_status = "connected"
        
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        database_status = "disconnected"
    
    return {
        "status": "healthy" if database_status == "connected" else "unhealthy",
        "application": {
            "name": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "environment": settings.ENVIRONMENT,
            "debug": settings.DEBUG
        },
        "services": {
            "database": {
                "status": database_status,
                "type": "SQLite"
            },
            "api": {
                "status": "operational",
                "version": "v1"
            }
        },
        "timestamp": time.time(),
        "checks": {
            "database_connection": database_status == "connected",
            "api_routes": True,
            "configuration": True
        }
    }


# Root endpoint
@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint with application information.
    
    Welcome message and basic application details.
    """
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "description": settings.DESCRIPTION,
        "version": settings.VERSION,
        "api_docs": f"{settings.API_V1_STR}/docs",
        "health_check": "/health",
        "endpoints": {
            "business_management": f"{settings.API_V1_STR}/business/",
            "business_analysis": f"{settings.API_V1_STR}/analysis/",
            "market_intelligence": f"{settings.API_V1_STR}/market/"
        },
        "support": {
            "docs": f"{settings.API_V1_STR}/docs",
            "redoc": f"{settings.API_V1_STR}/redoc",
            "health": "/health"
        }
    }


# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)


# Development server configuration
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info" if settings.DEBUG else "warning",
        access_log=settings.DEBUG
    )