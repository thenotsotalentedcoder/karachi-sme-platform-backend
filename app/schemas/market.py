"""Pydantic schemas for market data."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class MarketDataBase(BaseModel):
    """Base market data schema."""
    
    sector: str = Field(..., description="Business sector")
    location_area: str = Field(..., description="Karachi location area")
    average_revenue: float = Field(..., ge=0, description="Average revenue in area")
    revenue_growth_rate: float = Field(..., description="Revenue growth rate")
    competition_density: str = Field(..., description="Competition density level")
    market_size: float = Field(..., ge=0, description="Total market size")


class KarachiMarketDataResponse(MarketDataBase):
    """Schema for Karachi market data response."""
    
    id: int
    rent_cost_per_sqft: float = Field(..., ge=0, description="Rent cost per square foot")
    foot_traffic_level: str = Field(..., description="Foot traffic level")
    customer_demographics: Dict[str, Any] = Field(..., description="Customer demographics data")
    accessibility_score: float = Field(..., ge=1, le=10, description="Accessibility score")
    local_purchasing_power: float = Field(..., description="Local purchasing power index")
    seasonal_factors: Dict[str, Any] = Field(..., description="Seasonal variation factors")
    key_insights: Optional[List[str]] = Field(default=[], description="Key market insights")
    last_updated: datetime
    
    class Config:
        from_attributes = True


class SectorPerformanceResponse(BaseModel):
    """Schema for sector performance data."""
    
    id: int
    sector: str
    date: datetime
    growth_rate: float = Field(..., description="Sector growth rate")
    volatility: float = Field(..., ge=0, description="Sector volatility")
    market_sentiment: str = Field(..., description="Market sentiment")
    economic_impact: float = Field(..., description="Economic conditions impact")
    seasonal_impact: float = Field(..., description="Seasonal impact factor")
    policy_impact: float = Field(..., description="Government policy impact")
    key_drivers: Optional[List[str]] = Field(default=[], description="Key performance drivers")
    market_events: Optional[List[Dict[str, Any]]] = Field(default=[], description="Significant market events")
    
    class Config:
        from_attributes = True


class EconomicIndicatorsResponse(BaseModel):
    """Schema for economic indicators."""
    
    id: int
    date: datetime
    pkr_usd_rate: float = Field(..., gt=0, description="PKR to USD exchange rate")
    inflation_rate: float = Field(..., description="Annual inflation rate")
    interest_rate: float = Field(..., description="Interest rate")
    gdp_growth_rate: float = Field(..., description="GDP growth rate")
    unemployment_rate: float = Field(..., ge=0, le=100, description="Unemployment rate")
    consumer_confidence: float = Field(..., description="Consumer confidence index")
    ease_of_business_index: float = Field(..., description="Ease of doing business index")
    tax_policy_impact: float = Field(..., description="Tax policy impact score")
    regulatory_environment: str = Field(..., description="Regulatory environment status")
    supply_chain_status: str = Field(..., description="Supply chain status")
    energy_cost_index: float = Field(..., description="Energy cost index")
    
    class Config:
        from_attributes = True


class MarketTrendAnalysis(BaseModel):
    """Schema for market trend analysis."""
    
    sector: str
    location_area: str
    trend_direction: str = Field(..., description="Overall trend direction")
    growth_momentum: float = Field(..., description="Growth momentum score")
    market_maturity: str = Field(..., description="Market maturity level")
    competitive_intensity: float = Field(..., ge=1, le=10, description="Competitive intensity score")
    opportunity_score: float = Field(..., ge=0, le=100, description="Market opportunity score")
    risk_factors: List[str] = Field(..., description="Key risk factors")
    growth_drivers: List[str] = Field(..., description="Key growth drivers")
    market_challenges: List[str] = Field(..., description="Market challenges")


class LocationAnalysis(BaseModel):
    """Schema for location-specific analysis."""
    
    location_area: str
    location_score: float = Field(..., ge=0, le=100, description="Overall location score")
    advantages: List[str] = Field(..., description="Location advantages")
    disadvantages: List[str] = Field(..., description="Location disadvantages")
    best_sectors: List[str] = Field(..., description="Best performing sectors in this location")
    rent_affordability: str = Field(..., description="Rent affordability level")
    customer_accessibility: str = Field(..., description="Customer accessibility level")
    competition_analysis: Dict[str, Any] = Field(..., description="Competition analysis")
    expansion_potential: str = Field(..., description="Expansion potential")


class SectorBenchmarks(BaseModel):
    """Schema for sector benchmarking data."""
    
    sector: str
    location_area: str
    performance_benchmarks: Dict[str, float] = Field(..., description="Performance benchmarks")
    financial_benchmarks: Dict[str, float] = Field(..., description="Financial benchmarks")
    operational_benchmarks: Dict[str, float] = Field(..., description="Operational benchmarks")
    top_performer_characteristics: List[str] = Field(..., description="Top performer traits")
    common_challenges: List[str] = Field(..., description="Common sector challenges")
    success_factors: List[str] = Field(..., description="Key success factors")


class MarketForecast(BaseModel):
    """Schema for market forecast data."""
    
    sector: str
    location_area: str
    forecast_period: str = Field(..., description="Forecast time period")
    growth_forecast: float = Field(..., description="Forecasted growth rate")
    market_size_forecast: float = Field(..., description="Forecasted market size")
    key_trends: List[str] = Field(..., description="Key upcoming trends")
    potential_disruptions: List[str] = Field(..., description="Potential market disruptions")
    investment_climate: str = Field(..., description="Investment climate outlook")
    confidence_level: float = Field(..., ge=0, le=1, description="Forecast confidence level")


class CompetitiveAnalysis(BaseModel):
    """Schema for competitive analysis."""
    
    sector: str
    location_area: str
    competitor_count: int = Field(..., ge=0, description="Number of competitors in area")
    market_share_distribution: Dict[str, float] = Field(..., description="Market share distribution")
    competitive_advantages: List[str] = Field(..., description="Competitive advantages to leverage")
    competitive_threats: List[str] = Field(..., description="Competitive threats to address")
    market_gaps: List[str] = Field(..., description="Identified market gaps")
    differentiation_opportunities: List[str] = Field(..., description="Differentiation opportunities")


class MarketInsightsResponse(BaseModel):
    """Schema for comprehensive market insights."""
    
    market_data: KarachiMarketDataResponse
    sector_performance: SectorPerformanceResponse
    economic_indicators: EconomicIndicatorsResponse
    trend_analysis: MarketTrendAnalysis
    location_analysis: LocationAnalysis
    sector_benchmarks: SectorBenchmarks
    market_forecast: MarketForecast
    competitive_analysis: CompetitiveAnalysis
    
    # Summary insights
    key_opportunities: List[str] = Field(..., description="Key market opportunities")
    key_risks: List[str] = Field(..., description="Key market risks")
    strategic_recommendations: List[str] = Field(..., description="Strategic market recommendations")
    
    class Config:
        from_attributes = True