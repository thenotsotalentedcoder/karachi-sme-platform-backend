# app/models/business.py
"""US Business data models."""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, Boolean
from sqlalchemy.sql import func
from app.database import Base


class Business(Base):
    """US Business information model."""
    
    __tablename__ = "businesses"
    
    id = Column(Integer, primary_key=True, index=True)
    business_name = Column(String(255), nullable=False)
    
    # US Business identification
    ein_number = Column(String(20), nullable=True, index=True)  # Employer Identification Number
    naics_code = Column(String(10), nullable=True, index=True)  # North American Industry Classification
    business_structure = Column(String(50), nullable=True)      # LLC, Corp, Partnership, etc.
    
    # Industry and location (US-focused)
    sector = Column(String(100), nullable=False, index=True)    # electronics, food, retail, auto, professional_services
    industry_description = Column(Text, nullable=True)
    
    # US Location data
    street_address = Column(String(255), nullable=True)
    city = Column(String(100), nullable=False, index=True)
    state = Column(String(2), nullable=False, index=True)       # 2-letter state codes
    zip_code = Column(String(10), nullable=False, index=True)   # ZIP or ZIP+4
    county = Column(String(100), nullable=True)
    metro_area = Column(String(100), nullable=True)             # Metropolitan Statistical Area
    location_type = Column(String(50), nullable=True)           # urban_high_income, suburban, etc.
    
    # Financial data (12 months for better analysis)
    monthly_revenue = Column(JSON, nullable=False)              # List of 12 months revenue
    monthly_expenses = Column(JSON, nullable=False)             # List of 12 months expenses
    cost_of_goods_sold = Column(JSON, nullable=True)           # List of 12 months COGS
    current_cash = Column(Float, nullable=False)
    business_assets = Column(Float, nullable=True)
    outstanding_debt = Column(Float, nullable=True)
    business_credit_score = Column(Integer, nullable=True)      # Business credit score
    
    # Business operations
    years_in_business = Column(Integer, nullable=False)
    employees_count = Column(Integer, nullable=False)
    is_seasonal_business = Column(Boolean, default=False)
    business_model = Column(String(100), nullable=True)         # B2B, B2C, B2B2C, etc.
    
    # US-specific customer data
    primary_customer_type = Column(JSON, nullable=True)         # List of customer types
    revenue_streams = Column(JSON, nullable=True)               # List of revenue sources
    target_market = Column(Text, nullable=True)
    marketing_channels = Column(JSON, nullable=True)            # List of marketing channels
    
    # Competition and market
    main_competitors = Column(JSON, nullable=True)              # List of competitor names
    unique_value_proposition = Column(Text, nullable=True)
    competitive_advantages = Column(JSON, nullable=True)
    
    # Business goals and challenges (US-focused)
    business_goals = Column(JSON, nullable=True)                # US business goals
    main_challenges = Column(JSON, nullable=True)               # US business challenges
    expansion_plans = Column(JSON, nullable=True)               # Expansion plans
    investment_interests = Column(JSON, nullable=True)          # Investment preferences
    
    # Additional US business info
    certifications = Column(JSON, nullable=True)                # Business certifications
    licenses = Column(JSON, nullable=True)                      # Required licenses
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self) -> str:
        return f"<Business(id={self.id}, name='{self.business_name}', sector='{self.sector}', state='{self.state}')>"


class BusinessAnalysisHistory(Base):
    """Store historical analysis results for US businesses."""
    
    __tablename__ = "business_analysis_history"
    
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, nullable=False, index=True)
    
    # Analysis results
    overall_score = Column(Float, nullable=False)               # 0-100 overall business score
    performance_score = Column(Float, nullable=False)           # Performance vs industry
    financial_health_score = Column(Float, nullable=False)      # Financial health
    market_position_score = Column(Float, nullable=False)       # Market position
    growth_potential_score = Column(Float, nullable=False)      # Growth potential
    risk_score = Column(Float, nullable=False)                  # Risk assessment
    
    # Key insights and recommendations
    main_insight = Column(JSON, nullable=False)                 # Primary business insight
    recommendations = Column(JSON, nullable=False)              # Action recommendations
    investment_advice = Column(JSON, nullable=False)            # Investment recommendations
    
    # US Economic context at time of analysis
    economic_indicators_snapshot = Column(JSON, nullable=False) # Fed rate, inflation, etc.
    market_data_snapshot = Column(JSON, nullable=False)         # Market conditions
    sector_performance_snapshot = Column(JSON, nullable=False)  # Sector benchmarks
    
    # Analysis metadata
    analysis_version = Column(String(20), nullable=False, default="1.0")
    confidence_level = Column(Float, nullable=False, default=0.85)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self) -> str:
        return f"<BusinessAnalysisHistory(id={self.id}, business_id={self.business_id}, score={self.overall_score})>"