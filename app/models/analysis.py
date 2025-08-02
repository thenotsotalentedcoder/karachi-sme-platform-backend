"""Analysis result models."""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, Boolean
from sqlalchemy.sql import func
from app.database import Base


class AnalysisResult(Base):
    """Store complete analysis results."""
    
    __tablename__ = "analysis_results"
    
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, nullable=False, index=True)
    
    # Performance metrics
    performance_score = Column(Float, nullable=False)  # 0-100 scale
    business_growth_rate = Column(Float, nullable=False)  # Monthly growth rate
    sector_growth_rate = Column(Float, nullable=False)  # Sector average growth
    performance_ratio = Column(Float, nullable=False)  # Business vs sector
    
    # Financial analysis
    revenue_trend = Column(String(20), nullable=False)  # "increasing", "declining", "stable"
    profit_margin = Column(Float, nullable=False)
    cash_flow_status = Column(String(20), nullable=False)  # "healthy", "tight", "critical"
    
    # Market position
    market_position = Column(String(20), nullable=False)  # "leader", "average", "lagging"
    competition_level = Column(String(20), nullable=False)  # "low", "medium", "high"
    
    # Risk assessment
    business_risk_level = Column(String(20), nullable=False)  # "low", "medium", "high"
    volatility_score = Column(Float, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self) -> str:
        return f"<AnalysisResult(id={self.id}, score={self.performance_score})>"


class Insight(Base):
    """Store generated insights."""
    
    __tablename__ = "insights"
    
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, nullable=False, index=True)
    
    insight_type = Column(String(50), nullable=False)  # "problem", "opportunity", "warning"
    priority = Column(String(20), nullable=False)  # "high", "medium", "low"
    
    # Insight content
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    impact_amount = Column(Float, nullable=True)  # Expected Rs. impact
    timeframe = Column(String(50), nullable=True)  # "this week", "next month"
    
    # Supporting data
    supporting_data = Column(JSON, nullable=True)
    confidence_score = Column(Float, nullable=False, default=0.8)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self) -> str:
        return f"<Insight(id={self.id}, type='{self.insight_type}', priority='{self.priority}')>"


class Recommendation(Base):
    """Store actionable recommendations."""
    
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, nullable=False, index=True)
    
    category = Column(String(50), nullable=False)  # "immediate", "strategic", "investment"
    action_type = Column(String(50), nullable=False)  # "pricing", "inventory", "marketing"
    
    # Recommendation content
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    specific_action = Column(Text, nullable=False)
    
    # Expected outcomes
    expected_outcome = Column(Text, nullable=False)
    expected_amount = Column(Float, nullable=True)  # Expected Rs. benefit
    timeframe = Column(String(50), nullable=False)
    investment_required = Column(Float, nullable=True)
    
    # Implementation details
    difficulty_level = Column(String(20), nullable=False)  # "easy", "medium", "hard"
    implementation_steps = Column(JSON, nullable=True)
    
    # Tracking
    is_implemented = Column(Boolean, default=False)
    implementation_date = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self) -> str:
        return f"<Recommendation(id={self.id}, category='{self.category}')>"