"""Application configuration settings for US SME Intelligence Platform."""

import os
from typing import Optional, List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with all API keys and US market configuration."""
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "US SME Intelligence Platform"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "AI-powered real-time business intelligence for US small and medium enterprises"
    
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./us_sme_intelligence.db"
    
    # Security Configuration
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Environment Configuration
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # CORS Configuration
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1", "0.0.0.0"]
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]
    
    # =====================================
    # FINANCIAL DATA APIs (ALL WORKING)
    # =====================================
    
    # Federal Reserve Economic Data (CRITICAL)
    FRED_API_KEY: str = "ab6e2e350e5b747d0213f6d48dcdce2c"
    FRED_BASE_URL: str = "https://api.stlouisfed.org/fred"
    FRED_RATE_LIMIT: int = 120
    
    # Alpha Vantage Market Data (IMPORTANT)
    ALPHA_VANTAGE_API_KEY: str = "5TJ9E1MWHHWZ6WWF"
    ALPHA_VANTAGE_BASE_URL: str = "https://www.alphavantage.co/query"
    ALPHA_VANTAGE_RATE_LIMIT: int = 5
    
    # US Census Bureau (IMPORTANT)
    CENSUS_API_KEY: str = "cdd529a3db9364c6cb448be75de6769ab759aa4e"
    CENSUS_BASE_URL: str = "https://api.census.gov/data"
    CENSUS_RATE_LIMIT: int = 500
    
    # Bureau of Labor Statistics (IMPORTANT)
    BLS_API_KEY: str = "12f631d461e44c53816659a7a69ca22c"
    BLS_BASE_URL: str = "https://api.bls.gov/publicAPI/v2"
    BLS_RATE_LIMIT: int = 500
    
    # =====================================
    # AI/LLM APIs (GEMINI POWERHOUSE)
    # =====================================
    
    # Google Gemini API Keys (7 WORKING KEYS)
    GEMINI_API_KEY_1: str = "AIzaSyDyIaiYiK-2PfZyWDR1OK_7ofMHtSdUL4Q"
    GEMINI_API_KEY_2: str = "AIzaSyBXRDL5DGSOr-Y1jU-tBXAL7oSt8NClTTA"
    GEMINI_API_KEY_3: str = "AIzaSyDtMcC_d3vhxESowuK3OOVBlOIpqLT1oq0"
    GEMINI_API_KEY_4: str = "AIzaSyAHZ9tkz7vrtcNc3xPHhGWcLee7buAHwY0"
    GEMINI_API_KEY_5: str = "AIzaSyAtDgTbUdVTksx8XcBNmzFgKmvDuE1DjXI"
    GEMINI_API_KEY_6: str = "AIzaSyCCDDUCBr-4UCSXng356bHGQJ-N6hJJjOU"
    GEMINI_API_KEY_7: str = "AIzaSyA5vicL0VBZfgdRCUoGHV2kOGoXh7sBBgc"
    
    GEMINI_BASE_URL: str = "https://generativelanguage.googleapis.com/v1beta"
    GEMINI_MODEL: str = "gemini-2.0-flash"
    GEMINI_RATE_LIMIT_PER_KEY: int = 15
    
    # OpenRouter Backup APIs (2 WORKING KEYS)
    OPENROUTER_API_KEY_1: str = "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"
    OPENROUTER_API_KEY_2: str = "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"
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_MODEL: str = "google/gemma-3n-e2b-it:free"
    
    # =====================================
    # CACHING & PERFORMANCE
    # =====================================
    
    # Cache Settings
    CACHE_ECONOMIC_DATA_MINUTES: int = 15
    CACHE_MARKET_DATA_MINUTES: int = 5
    CACHE_ANALYSIS_RESULTS_MINUTES: int = 60
    
    # Rate Limiting
    ENABLE_RATE_LIMITING: bool = True
    DEFAULT_RATE_LIMIT: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()

# Multi-Gemini Keys Configuration
GEMINI_KEYS = [
    settings.GEMINI_API_KEY_1,
    settings.GEMINI_API_KEY_2,
    settings.GEMINI_API_KEY_3,
    settings.GEMINI_API_KEY_4,
    settings.GEMINI_API_KEY_5,
    settings.GEMINI_API_KEY_6,
    settings.GEMINI_API_KEY_7,
]

OPENROUTER_KEYS = [
    settings.OPENROUTER_API_KEY_1,
    settings.OPENROUTER_API_KEY_2,
]