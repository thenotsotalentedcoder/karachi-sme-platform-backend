"""Pydantic schemas for US market data."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class USMarketDataBase(BaseModel):
    """Base US market data schema."""
    
    sector: str = Field(..., description="Business sector")
    location_type: str = Field(..., description="US location type (urban_high_income, suburban, etc.)")
    state: str = Field(..., description="US state code")
    metro_area: Optional[str] = Field(None, description="Metropolitan Statistical Area")
    
    # US market metrics
    average_revenue: float = Field(..., ge=0, description="Average annual revenue in area (USD)")
    revenue_growth_rate: float = Field(..., description="Annual revenue growth rate")
    competition_density: str = Field(..., description="low/medium/high/very_high")
    market_size: float = Field(..., ge=0, description="Total addressable market size (USD)")


class USMarketDataResponse(USMarketDataBase):
    """Schema for US market data response."""
    
    id: int
    
    # US location economics
    cost_of_living_index: float = Field(..., description="Cost of living relative to US average")
    average_wages: float = Field(..., description="Average wages in area (USD)")
    business_costs_index: float = Field(..., description="Business operating costs index")
    
    # US demographics
    customer_demographics: Dict[str, Any] = Field(..., description="US demographic data")
    median_household_income: float = Field(..., description="Median household income (USD)")
    population_density: float = Field(..., description="Population per square mile")
    
    # US business environment
    business_formation_rate: float = Field(..., description="New business formation rate")
    failure_rate: float = Field(..., description="Business failure rate")
    economic_development_score: float = Field(..., ge=0, le=100, description="Economic development score")
    
    # US regulatory environment
    regulatory_friendliness: str = Field(..., description="business_friendly/neutral/restrictive")
    tax_burden_score: float = Field(..., ge=0, le=100, description="Tax burden score")
    
    # Market insights
    key_insights: List[str] = Field(default=[], description="Key US market insights")
    growth_drivers: List[str] = Field(default=[], description="Market growth drivers")
    market_challenges: List[str] = Field(default=[], description="Market challenges")
    
    last_updated: datetime
    
    class Config:
        from_attributes = True


class USSectorPerformanceResponse(BaseModel):
    """Schema for US sector performance data."""
    
    id: int
    sector: str
    date: datetime
    
    # US sector metrics
    growth_rate: float = Field(..., description="US sector annual growth rate")
    volatility: float = Field(..., ge=0, description="Sector volatility measure")
    market_sentiment: str = Field(..., description="bullish/neutral/bearish")
    
    # US economic impact factors
    fed_rate_impact: float = Field(..., description="Federal funds rate impact on sector")
    inflation_impact: float = Field(..., description="Inflation impact on sector")
    consumer_confidence_impact: float = Field(..., description="Consumer confidence impact")
    
    # US sector health indicators
    employment_growth: float = Field(..., description="Sector employment growth rate")
    wage_growth: float = Field(..., description="Sector wage growth rate")
    productivity_growth: float = Field(..., description="Sector productivity growth")
    
    # Market dynamics
    key_drivers: List[str] = Field(default=[], description="Key US sector performance drivers")
    market_events: List[Dict[str, Any]] = Field(default=[], description="Significant US market events")
    regulatory_changes: List[str] = Field(default=[], description="Recent US regulatory changes")
    
    # Investment flows
    investment_inflows: Optional[float] = Field(None, description="Sector investment inflows (USD)")
    funding_availability: str = Field(..., description="high/medium/low")
    
    class Config:
        from_attributes = True


class USEconomicIndicatorsResponse(BaseModel):
    """Schema for US economic indicators."""
    
    id: int
    date: datetime
    
    # Federal Reserve indicators
    fed_funds_rate: float = Field(..., description="Federal funds rate (%)")
    inflation_rate_cpi: float = Field(..., description="CPI inflation rate (%)")
    core_inflation_rate: float = Field(..., description="Core CPI inflation rate (%)")
    
    # Employment indicators
    unemployment_rate: float = Field(..., ge=0, le=100, description="US unemployment rate (%)")
    labor_force_participation: float = Field(..., description="Labor force participation rate (%)")
    job_openings_rate: float = Field(..., description="Job openings rate (%)")
    
    # Economic growth
    gdp_growth_rate: float = Field(..., description="Real GDP growth rate (%)")
    personal_consumption_growth: float = Field(..., description="Personal consumption growth (%)")
    business_investment_growth: float = Field(..., description="Business investment growth (%)")
    
    # Consumer and business sentiment
    consumer_confidence: float = Field(..., description="Consumer confidence index")
    small_business_optimism: float = Field(..., description="NFIB small business optimism index")
    business_sentiment: str = Field(..., description="positive/neutral/negative")
    
    # Financial markets
    stock_market_performance: float = Field(..., description="S&P 500 YTD performance (%)")
    bond_yields_10yr: float = Field(..., description="10-year Treasury yield (%)")
    dollar_strength_index: float = Field(..., description="US Dollar Index")
    
    # Industry-specific indicators
    manufacturing_pmi: Optional[float] = Field(None, description="Manufacturing PMI")
    services_pmi: Optional[float] = Field(None, description="Services PMI")
    retail_sales_growth: Optional[float] = Field(None, description="Retail sales growth (%)")
    
    # Small business specific
    small_business_credit_availability: str = Field(..., description="abundant/adequate/tight/very_tight")
    small_business_hiring_plans: str = Field(..., description="expanding/stable/contracting")
    
    class Config:
        from_attributes = True


class USMarketTrendAnalysis(BaseModel):
    """Schema for US market trend analysis."""
    
    sector: str
    location_type: str
    analysis_period: str = Field(..., description="Time period analyzed")
    
    # Trend analysis
    trend_direction: str = Field(..., description="strong_growth/moderate_growth/stable/declining")
    growth_momentum: float = Field(..., description="Growth momentum score (0-100)")
    market_maturity: str = Field(..., description="emerging/growth/mature/declining")
    
    # US competitive landscape
    competitive_intensity: float = Field(..., ge=1, le=10, description="Competition intensity score")
    market_concentration: str = Field(..., description="fragmented/moderate/concentrated")
    barriers_to_entry: str = Field(..., description="low/medium/high")
    
    # Opportunity assessment
    opportunity_score: float = Field(..., ge=0, le=100, description="Market opportunity score")
    risk_factors: List[str] = Field(..., description="Key US market risk factors")
    growth_drivers: List[str] = Field(..., description="US market growth drivers")
    
    # US economic context
    economic_sensitivity: float = Field(..., description="Sensitivity to US economic cycles")
    regulatory_risk: str = Field(..., description="low/medium/high")
    
    # Future outlook
    outlook_12_months: str = Field(..., description="positive/neutral/negative")
    outlook_24_months: str = Field(..., description="positive/neutral/negative")
    key_trends_to_watch: List[str] = Field(..., description="Trends to monitor")


class USLocationAnalysis(BaseModel):
    """Schema for US location-specific analysis."""
    
    location_type: str
    state: str
    metro_area: Optional[str] = None
    
    # Location scoring
    overall_location_score: float = Field(..., ge=0, le=100, description="Overall location score")
    business_friendliness_score: float = Field(..., ge=0, le=100, description="Business friendliness")
    
    # US location advantages/disadvantages
    advantages: List[str] = Field(..., description="Key location advantages")
    disadvantages: List[str] = Field(..., description="Key location disadvantages")
    
    # Sector fit analysis
    best_sectors_for_location: List[str] = Field(..., description="Best performing sectors")
    sector_fit_score: float = Field(..., ge=0, le=100, description="Sector-location fit score")
    
    # US economic factors
    cost_structure: Dict[str, float] = Field(..., description="Cost breakdown (rent, wages, etc.)")
    revenue_potential: Dict[str, float] = Field(..., description="Revenue potential by customer segment")
    
    # Market accessibility
    customer_accessibility: str = Field(..., description="excellent/good/fair/poor")
    supplier_accessibility: str = Field(..., description="excellent/good/fair/poor")
    talent_availability: str = Field(..., description="abundant/adequate/limited/scarce")
    
    # Growth and expansion
    expansion_potential: str = Field(..., description="high/medium/low")
    scalability_factors: List[str] = Field(..., description="Factors affecting scalability")


class USSectorBenchmarks(BaseModel):
    """Schema for US sector benchmarking data."""
    
    sector: str
    benchmark_period: str = Field(..., description="Time period for benchmarks")
    
    # US financial benchmarks
    revenue_benchmarks: Dict[str, float] = Field(..., description="Revenue benchmarks by percentile")
    profit_margin_benchmarks: Dict[str, float] = Field(..., description="Profit margin benchmarks")
    growth_rate_benchmarks: Dict[str, float] = Field(..., description="Growth rate benchmarks")
    
    # US operational benchmarks
    employee_productivity: Dict[str, float] = Field(..., description="Revenue per employee benchmarks")
    inventory_turnover: Optional[Dict[str, float]] = Field(None, description="Inventory turnover rates")
    customer_acquisition_cost: Optional[Dict[str, float]] = Field(None, description="CAC benchmarks")
    
    # US market benchmarks
    market_share_distribution: Dict[str, float] = Field(..., description="Market share distribution")
    pricing_benchmarks: Dict[str, float] = Field(..., description="Pricing benchmarks")
    
    # Success factors
    top_performer_characteristics: List[str] = Field(..., description="Top 10% performer traits")
    common_success_factors: List[str] = Field(..., description="Common success factors")
    common_failure_points: List[str] = Field(..., description="Common failure points")
    
    # US regulatory and compliance
    compliance_requirements: List[str] = Field(..., description="Key US compliance requirements")
    regulatory_costs: Optional[float] = Field(None, description="Average regulatory compliance costs")


class USMarketForecast(BaseModel):
    """Schema for US market forecast data."""
    
    sector: str
    location_type: str
    forecast_period: str = Field(..., description="Forecast time horizon")
    
    # Growth forecasts
    revenue_growth_forecast: float = Field(..., description="Forecasted annual revenue growth")
    market_size_forecast: float = Field(..., description="Forecasted market size (USD)")
    demand_forecast: str = Field(..., description="increasing/stable/decreasing")
    
    # US economic scenario analysis
    base_case_scenario: Dict[str, Any] = Field(..., description="Most likely scenario")
    optimistic_scenario: Dict[str, Any] = Field(..., description="Best case scenario")
    pessimistic_scenario: Dict[str, Any] = Field(..., description="Worst case scenario")
    
    # Key forecast drivers
    key_trends: List[str] = Field(..., description="Key trends shaping the forecast")
    technology_disruptions: List[str] = Field(..., description="Potential technology disruptions")
    regulatory_changes: List[str] = Field(..., description="Expected regulatory changes")
    
    # US economic factors
    economic_assumptions: Dict[str, float] = Field(..., description="Key economic assumptions")
    interest_rate_sensitivity: float = Field(..., description="Sensitivity to rate changes")
    inflation_sensitivity: float = Field(..., description="Sensitivity to inflation")
    
    # Investment climate
    investment_attractiveness: str = Field(..., description="high/medium/low")
    funding_availability_outlook: str = Field(..., description="improving/stable/tightening")
    
    # Confidence and risks
    forecast_confidence: float = Field(..., ge=0, le=1, description="Forecast confidence level")
    key_risks_to_forecast: List[str] = Field(..., description="Key risks to forecast accuracy")


class USCompetitiveAnalysis(BaseModel):
    """Schema for US competitive analysis."""
    
    sector: str
    location_type: str
    analysis_scope: str = Field(..., description="local/regional/national")
    
    # US competitive landscape
    competitor_count_estimate: int = Field(..., ge=0, description="Estimated number of competitors")
    market_concentration: str = Field(..., description="fragmented/moderate/concentrated")
    competitive_intensity: float = Field(..., ge=1, le=10, description="Competition intensity")
    
    # Market structure
    market_leaders: List[str] = Field(..., description="Market leading companies/types")
    market_share_distribution: Dict[str, float] = Field(..., description="Market share breakdown")
    
    # Competitive dynamics
    price_competition_level: str = Field(..., description="intense/moderate/limited")
    innovation_pace: str = Field(..., description="rapid/moderate/slow")
    customer_switching_costs: str = Field(..., description="high/medium/low")
    
    # US market opportunities
    market_gaps: List[str] = Field(..., description="Identified market gaps")
    underserved_segments: List[str] = Field(..., description="Underserved customer segments")
    differentiation_opportunities: List[str] = Field(..., description="Differentiation opportunities")
    
    # Strategic positioning
    recommended_competitive_strategy: str = Field(..., description="cost_leadership/differentiation/focus")
    sustainable_advantages: List[str] = Field(..., description="Potential sustainable advantages")
    
    # Threat assessment
    new_entrant_threat: str = Field(..., description="high/medium/low")
    substitute_threat: str = Field(..., description="high/medium/low")
    supplier_power: str = Field(..., description="high/medium/low")


class USMarketInsightsResponse(BaseModel):
    """Schema for comprehensive US market insights."""
    
    market_data: USMarketDataResponse
    sector_performance: USSectorPerformanceResponse
    economic_indicators: USEconomicIndicatorsResponse
    trend_analysis: USMarketTrendAnalysis
    location_analysis: USLocationAnalysis
    sector_benchmarks: USSectorBenchmarks
    market_forecast: USMarketForecast
    competitive_analysis: USCompetitiveAnalysis
    
    # Summary insights
    key_opportunities: List[str] = Field(..., description="Key market opportunities")
    key_risks: List[str] = Field(..., description="Key market risks")
    strategic_recommendations: List[str] = Field(..., description="Strategic market recommendations")
    
    class Config:
        from_attributes = True


class USInvestmentMarketAnalysis(BaseModel):
    """Schema for US investment market analysis."""
    
    analysis_date: datetime
    market_environment: str = Field(..., description="bullish/bearish/neutral/volatile")
    
    # US market indices performance
    sp500_performance: Dict[str, float] = Field(..., description="S&P 500 performance metrics")
    nasdaq_performance: Dict[str, float] = Field(..., description="NASDAQ performance metrics")
    small_cap_performance: Dict[str, float] = Field(..., description="Small-cap performance metrics")
    
    # Sector rotation analysis
    outperforming_sectors: List[Dict[str, Any]] = Field(..., description="Best performing sectors")
    underperforming_sectors: List[Dict[str, Any]] = Field(..., description="Worst performing sectors")
    sector_rotation_trends: List[str] = Field(..., description="Current rotation trends")
    
    # Economic drivers
    key_market_drivers: List[str] = Field(..., description="Primary market drivers")
    fed_policy_impact: str = Field(..., description="Current Fed policy impact")
    inflation_impact: str = Field(..., description="Inflation impact on markets")
    
    # Investment recommendations by risk level
    conservative_recommendations: List[Dict[str, Any]] = Field(..., description="Conservative investments")
    moderate_recommendations: List[Dict[str, Any]] = Field(..., description="Moderate risk investments")
    aggressive_recommendations: List[Dict[str, Any]] = Field(..., description="High-growth investments")
    
    # US-specific considerations
    tax_implications: Dict[str, Any] = Field(..., description="Current tax considerations")
    regulatory_changes: List[str] = Field(..., description="Relevant regulatory changes")
    
    class Config:
        from_attributes = True


class USRegionalMarketData(BaseModel):
    """Schema for US regional market data."""
    
    region: str = Field(..., description="US region (Northeast, Southeast, Midwest, Southwest, West)")
    states_included: List[str] = Field(..., description="States in this region")
    
    # Regional economic indicators
    regional_gdp_growth: float = Field(..., description="Regional GDP growth rate")
    regional_unemployment: float = Field(..., description="Regional unemployment rate")
    cost_of_living_index: float = Field(..., description="Regional cost of living vs national average")
    
    # Business environment
    business_formation_rate: float = Field(..., description="New business formation rate")
    regulatory_environment: str = Field(..., description="business_friendly/neutral/restrictive")
    tax_environment: Dict[str, float] = Field(..., description="Regional tax rates")
    
    # Demographics
    population_growth: float = Field(..., description="Regional population growth rate")
    median_age: float = Field(..., description="Regional median age")
    education_level: Dict[str, float] = Field(..., description="Education level distribution")
    income_distribution: Dict[str, float] = Field(..., description="Income level distribution")
    
    # Industry composition
    dominant_industries: List[Dict[str, Any]] = Field(..., description="Major industries in region")
    emerging_sectors: List[str] = Field(..., description="Growing sectors in region")
    declining_sectors: List[str] = Field(..., description="Declining sectors in region")
    
    # Market opportunities
    regional_advantages: List[str] = Field(..., description="Regional competitive advantages")
    growth_opportunities: List[str] = Field(..., description="Key growth opportunities")
    market_challenges: List[str] = Field(..., description="Regional market challenges")
    
    class Config:
        from_attributes = True