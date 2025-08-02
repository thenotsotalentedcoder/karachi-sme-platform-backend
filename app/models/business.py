"""Business data models."""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.sql import func
from app.database import Base


class Business(Base):
    """Business information model."""
    
    __tablename__ = "businesses"
    
    id = Column(Integer, primary_key=True, index=True)
    business_name = Column(String(255), nullable=False)
    sector = Column(String(100), nullable=False, index=True)
    location_area = Column(String(100), nullable=False, index=True)
    business_type = Column(String(100), nullable=False)
    
    # Financial data
    monthly_revenue = Column(JSON, nullable=False)  # List of 6 months revenue
    monthly_expenses = Column(Float, nullable=False)
    current_cash = Column(Float, nullable=False)
    employees_count = Column(Integer, nullable=False)
    years_in_business = Column(Integer, nullable=False)
    
    # Business context
    primary_customers = Column(String(100), nullable=False)
    main_challenges = Column(JSON, nullable=True)  # List of challenges
    business_goals = Column(JSON, nullable=True)  # List of goals
    
    # Additional info
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self) -> str:
        return f"<Business(id={self.id}, name='{self.business_name}', sector='{self.sector}')>"


class BusinessAnalysisHistory(Base):
    """Store historical analysis results for businesses."""
    
    __tablename__ = "business_analysis_history"
    
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, nullable=False, index=True)
    
    # Analysis results
    performance_score = Column(Float, nullable=False)
    main_insight = Column(JSON, nullable=False)
    recommendations = Column(JSON, nullable=False)
    investment_advice = Column(JSON, nullable=False)
    
    # Market context at time of analysis
    market_data_snapshot = Column(JSON, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self) -> str:
        return f"<BusinessAnalysisHistory(id={self.id}, business_id={self.business_id})>"