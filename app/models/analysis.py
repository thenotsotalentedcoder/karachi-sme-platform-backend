# app/models/analysis.py
"""US Analysis result models."""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, Boolean
from sqlalchemy.sql import func
from app.database import Base


class AnalysisResult(Base):
    """Store complete US business analysis results."""
    
    __tablename__ = "analysis_results"
    
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, nullable=False, index=True)
    
    # Overall scores
    overall_score = Column(Float, nullable=False)               # 0-100 overall business health
    confidence_level = Column(Float, nullable=False, default=0.85)
    
    # Performance metrics (vs US benchmarks)
    performance_score = Column(Float, nullable=False)           # Performance vs industry
    revenue_growth_rate = Column(Float, nullable=False)         # Annualized growth rate
    sector_growth_rate = Column(Float, nullable=False)          # US sector average
    performance_ratio = Column(Float, nullable=False)           # Business vs sector performance
    
    # Financial analysis
    revenue_trend = Column(String(20), nullable=False)          # "increasing", "declining", "stable"
    profit_margin = Column(Float, nullable=False)               # Current profit margin
    cash_flow_status = Column(String(20), nullable=False)       # "healthy", "tight", "critical"
    cash_runway_months = Column(Float, nullable=True)           # Months of cash remaining
    financial_health_grade = Column(String(2), nullable=False)  # A, B, C, D, F
    
    # Market position (US market context)
    market_position = Column(String(20), nullable=False)        # "leader", "strong", "average", "weak"
    market_percentile = Column(Float, nullable=True)            # 0-100 percentile rank
    competitive_position = Column(String(20), nullable=False)   # "dominant", "competitive", "struggling"
    
    # Economic sensitivity (US economic factors)
    fed_rate_sensitivity = Column(Float, nullable=False)        # -1 to 1 scale
    inflation_sensitivity = Column(Float, nullable=False)       # -1 to 1 scale
    economic_resilience_score = Column(Float, nullable=False)   # 0-100 recession resistance
    
    # Risk assessment
    overall_risk_level = Column(String(20), nullable=False)     # "low", "medium", "high", "critical"
    financial_risk = Column(Float, nullable=False)              # 0-100 risk score
    market_risk = Column(Float, nullable=False)                 # 0-100 risk score
    operational_risk = Column(Float, nullable=False)            # 0-100 risk score
    volatility_score = Column(Float, nullable=False)            # Revenue volatility measure
    
    # Growth analysis
    growth_potential_score = Column(Float, nullable=False)      # 0-100 growth potential
    scalability_assessment = Column(String(20), nullable=False) # "high", "medium", "low"
    expansion_readiness = Column(String(20), nullable=False)    # "ready", "partial", "not_ready"
    
    # US-specific factors
    location_advantage_score = Column(Float, nullable=True)     # Location effectiveness
    demographic_alignment = Column(Float, nullable=True)        # Target market alignment
    regulatory_compliance = Column(String(20), nullable=True)   # "compliant", "partial", "issues"
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self) -> str:
        return f"<AnalysisResult(id={self.id}, overall_score={self.overall_score}, grade={self.financial_health_grade})>"


class Insight(Base):
    """Store US business insights and observations."""
    
    __tablename__ = "insights"
    
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, nullable=False, index=True)
    
    insight_type = Column(String(50), nullable=False)           # "opportunity", "problem", "warning", "trend"
    category = Column(String(50), nullable=False)               # "financial", "market", "operational", "strategic"
    priority = Column(String(20), nullable=False)               # "critical", "high", "medium", "low"
    urgency = Column(String(20), nullable=False)                # "immediate", "short_term", "medium_term", "long_term"
    
    # Insight content
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    supporting_evidence = Column(JSON, nullable=True)           # Data supporting the insight
    
    # Impact assessment (US dollar amounts)
    potential_impact_amount = Column(Float, nullable=True)      # Potential $ impact
    impact_timeframe = Column(String(50), nullable=True)        # "this month", "this quarter", etc.
    probability = Column(Float, nullable=True)                  # 0-1 probability of impact
    
    # US economic context
    economic_factors = Column(JSON, nullable=True)              # Relevant economic factors
    market_context = Column(JSON, nullable=True)                # Market conditions context
    
    # Confidence and validation
    confidence_score = Column(Float, nullable=False, default=0.8)
    data_quality = Column(String(20), nullable=False, default="good") # "excellent", "good", "fair", "poor"
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self) -> str:
        return f"<Insight(id={self.id}, type='{self.insight_type}', priority='{self.priority}')>"


class Recommendation(Base):
    """Store actionable US business recommendations."""
    
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, nullable=False, index=True)
    
    # Recommendation classification
    category = Column(String(50), nullable=False)               # "immediate", "strategic", "investment", "operational"
    action_type = Column(String(50), nullable=False)            # "pricing", "marketing", "financing", "expansion"
    priority = Column(String(20), nullable=False)               # "critical", "high", "medium", "low"
    
    # Recommendation content
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    specific_action = Column(Text, nullable=False)
    rationale = Column(Text, nullable=False)                    # Why this recommendation
    
    # Expected outcomes (US business context)
    expected_outcome = Column(Text, nullable=False)
    expected_revenue_impact = Column(Float, nullable=True)      # Expected revenue change
    expected_cost_impact = Column(Float, nullable=True)         # Expected cost change
    expected_roi = Column(Float, nullable=True)                 # Expected ROI percentage
    timeframe = Column(String(50), nullable=False)              # Implementation timeframe
    
    # Implementation details
    investment_required = Column(Float, nullable=True)          # Required investment ($)
    difficulty_level = Column(String(20), nullable=False)       # "easy", "medium", "hard", "very_hard"
    implementation_steps = Column(JSON, nullable=True)          # Step-by-step plan
    required_resources = Column(JSON, nullable=True)            # Required resources
    success_metrics = Column(JSON, nullable=True)               # How to measure success
    
    # Risk and dependencies
    implementation_risks = Column(JSON, nullable=True)          # Potential risks
    dependencies = Column(JSON, nullable=True)                  # Prerequisites
    alternative_approaches = Column(JSON, nullable=True)        # Alternative ways to achieve goal
    
    # US regulatory and compliance considerations
    regulatory_considerations = Column(JSON, nullable=True)     # Regulatory factors
    tax_implications = Column(JSON, nullable=True)              # Tax considerations
    
    # Tracking and follow-up
    is_implemented = Column(Boolean, default=False)
    implementation_date = Column(DateTime(timezone=True), nullable=True)
    implementation_notes = Column(Text, nullable=True)
    actual_outcome = Column(Text, nullable=True)
    actual_roi = Column(Float, nullable=True)                   # Actual ROI achieved
    
    # Performance tracking
    success_probability = Column(Float, nullable=False, default=0.7) # 0-1 success probability
    effectiveness_score = Column(Float, nullable=True)          # Post-implementation effectiveness
    lessons_learned = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self) -> str:
        return f"<Recommendation(id={self.id}, category='{self.category}', priority='{self.priority}')>"
    
    
class InvestmentRecommendation(Base):
   """Store US investment recommendations for business owners."""
   
   __tablename__ = "investment_recommendations"
   
   id = Column(Integer, primary_key=True, index=True)
   analysis_id = Column(Integer, nullable=False, index=True)
   
   # Investment classification
   investment_type = Column(String(50), nullable=False)        # "business_reinvestment", "market_investment", "real_estate"
   investment_category = Column(String(50), nullable=False)    # "growth", "income", "diversification", "tax_optimization"
   risk_level = Column(String(20), nullable=False)             # "conservative", "moderate", "aggressive"
   
   # Investment details
   title = Column(String(255), nullable=False)
   description = Column(Text, nullable=False)
   rationale = Column(Text, nullable=False)
   
   # Financial projections (US dollars)
   recommended_amount = Column(Float, nullable=False)          # Recommended investment amount
   minimum_amount = Column(Float, nullable=True)               # Minimum viable amount
   expected_annual_return = Column(Float, nullable=False)      # Expected annual return %
   time_horizon = Column(String(50), nullable=False)           # "short_term", "medium_term", "long_term"
   
   # Risk assessment
   risk_factors = Column(JSON, nullable=True)                  # Specific risk factors
   volatility_estimate = Column(Float, nullable=True)          # Expected volatility
   downside_protection = Column(Float, nullable=True)          # Downside risk %
   
   # US-specific considerations
   tax_advantages = Column(JSON, nullable=True)                # Tax benefits
   regulatory_protection = Column(JSON, nullable=True)         # Regulatory protections
   liquidity_considerations = Column(Text, nullable=True)      # Liquidity factors
   
   # Implementation guidance
   implementation_steps = Column(JSON, nullable=True)          # How to implement
   recommended_timing = Column(String(100), nullable=True)     # When to implement
   exit_strategy = Column(Text, nullable=True)                 # Exit considerations
   
   # Performance tracking
   is_implemented = Column(Boolean, default=False)
   implementation_date = Column(DateTime(timezone=True), nullable=True)
   actual_return = Column(Float, nullable=True)                # Actual return achieved
   
   # Timestamps
   created_at = Column(DateTime(timezone=True), server_default=func.now())
   updated_at = Column(DateTime(timezone=True), onupdate=func.now())
   
   def __repr__(self) -> str:
       return f"<InvestmentRecommendation(id={self.id}, type='{self.investment_type}', amount=${self.recommended_amount})>"