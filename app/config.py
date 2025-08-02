"""Application configuration settings."""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Karachi SME Intelligence Platform"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "AI-powered business intelligence for Karachi SMEs"
    
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./karachi_sme.db"
    
    # Security Configuration
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Environment Configuration
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # CORS Configuration
    ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1", "0.0.0.0"]
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()