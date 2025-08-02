"""API router configuration."""

from fastapi import APIRouter

from app.api.endpoints import business, analysis, market

# Create main API router
api_router = APIRouter()

# Include all endpoint routers with prefixes and tags
api_router.include_router(
    business.router,
    prefix="/business",
    tags=["business"],
    responses={
        404: {"description": "Business not found"},
        400: {"description": "Invalid business data"}
    }
)

api_router.include_router(
    analysis.router,
    prefix="/analysis", 
    tags=["analysis"],
    responses={
        404: {"description": "Analysis not found"},
        400: {"description": "Invalid analysis request"},
        500: {"description": "Analysis processing failed"}
    }
)

api_router.include_router(
    market.router,
    prefix="/market",
    tags=["market"],
    responses={
        404: {"description": "Market data not found"},
        400: {"description": "Invalid market parameters"}
    }
)