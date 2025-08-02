"""Common dependencies for FastAPI endpoints."""

from typing import Generator
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db


def get_database_session() -> Generator[Session, None, None]:
    """Get database session dependency."""
    return get_db()


def validate_business_sector(sector: str) -> str:
    """Validate that the business sector is supported."""
    valid_sectors = {
        "electronics",
        "textile", 
        "auto",
        "food",
        "retail"
    }
    
    if sector.lower() not in valid_sectors:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported sector: {sector}. Valid sectors: {', '.join(valid_sectors)}"
        )
    
    return sector.lower()


def validate_karachi_location(location: str) -> str:
    """Validate that the location is in Karachi."""
    valid_locations = {
        "clifton",
        "dha", 
        "saddar",
        "tariq_road",
        "gulshan",
        "gulistan_e_johar",
        "korangi",
        "landhi",
        "north_karachi",
        "nazimabad"
    }
    
    location_clean = location.lower().replace(" ", "_").replace("-", "_")
    
    if location_clean not in valid_locations:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported location: {location}. Valid locations: {', '.join(valid_locations)}"
        )
    
    return location_clean


class CommonDependencies:
    """Collection of common dependencies."""
    
    @staticmethod
    def get_db() -> Generator[Session, None, None]:
        """Database session dependency."""
        return get_database_session()
    
    @staticmethod
    def validate_sector(sector: str) -> str:
        """Sector validation dependency."""
        return validate_business_sector(sector)
    
    @staticmethod
    def validate_location(location: str) -> str:
        """Location validation dependency."""
        return validate_karachi_location(location)