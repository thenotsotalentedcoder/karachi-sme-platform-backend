"""Market data models."""

from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Text
from sqlalchemy.sql import func
from app.database import Base


class KarachiMarketData(Base):
    """Karachi market data by sector and location."""
    
    __tablename__ = "karachi_market_data"
    
    id = Column(Integer, primary_key=True, index=True)
    sector = Column(String(100), nullable=False, index=True)
    location_area = Column(String(100), nullable=False, index=True)
    
    # Market metrics
    average_revenue = Column(Float, nullable=False)
    revenue_growth_rate = Column(Float, nullable=False)
    competition_density = Column(String(20), nullable=False)  # "low", "medium", "high"
    market_size = Column(Float, nullable=False)
    
    # Location factors
    rent_cost_per_sqft = Column(Float, nullable=False)
    foot_traffic_level = Column(String(20), nullable=False)
    customer_demographics = Column(JSON, nullable=False)
    accessibility_score = Column(Float, nullable=False)  # 1-10 scale
    
    # Economic indicators
    local_purchasing_power = Column(Float, nullable=False)
    seasonal_factors = Column(JSON, nullable=False)
    
    # Additional context
    key_insights = Column(JSON, nullable=True)
    last_updated = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self) -> str:
        return f"<KarachiMarketData(sector='{self.sector}', area='{self.location_area}')>"


class SectorPerformance(Base):
    """Sector performance data over time."""
    
    __tablename__ = "sector_performance"
    
    id = Column(Integer, primary_key=True, index=True)
    sector = Column(String(100), nullable=False, index=True)
    date = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # Performance metrics
    growth_rate = Column(Float, nullable=False)
    volatility = Column(Float, nullable=False)
    market_sentiment = Column(String(20), nullable=False)  # "positive", "neutral", "negative"
    
    # External factors
    economic_impact = Column(Float, nullable=False)  # Impact of economic conditions
    seasonal_impact = Column(Float, nullable=False)  # Seasonal adjustment
    policy_impact = Column(Float, nullable=False)  # Government policy impact
    
    # Supporting data
    key_drivers = Column(JSON, nullable=True)
    market_events = Column(JSON, nullable=True)
    
    def __repr__(self) -> str:
        return f"<SectorPerformance(sector='{self.sector}', date='{self.date}')>"


class EconomicIndicators(Base):
    """Economic indicators affecting businesses."""
    
    __tablename__ = "economic_indicators"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # Currency and inflation
    pkr_usd_rate = Column(Float, nullable=False)
    inflation_rate = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)
    
    # Economic health
    gdp_growth_rate = Column(Float, nullable=False)
    unemployment_rate = Column(Float, nullable=False)
    consumer_confidence = Column(Float, nullable=False)
    
    # Business environment
    ease_of_business_index = Column(Float, nullable=False)
    tax_policy_impact = Column(Float, nullable=False)
    regulatory_environment = Column(String(20), nullable=False)
    
    # Market conditions
    supply_chain_status = Column(String(20), nullable=False)
    energy_cost_index = Column(Float, nullable=False)
    
    def __repr__(self) -> str:
        return f"<EconomicIndicators(date='{self.date}', pkr_rate={self.pkr_usd_rate})>"