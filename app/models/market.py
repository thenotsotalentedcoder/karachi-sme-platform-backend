# app/models/market.py
"""US Market data models."""

from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Text
from sqlalchemy.sql import func
from app.database import Base


class USMarketData(Base):
    """US market data by sector and location."""
    
    __tablename__ = "us_market_data"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Geographic identifiers
    state = Column(String(2), nullable=False, index=True)       # US state code
    metro_area = Column(String(100), nullable=True, index=True) # Metropolitan Statistical Area
    city = Column(String(100), nullable=True, index=True)
    zip_code = Column(String(10), nullable=True, index=True)
    location_type = Column(String(50), nullable=False, index=True) # urban_high_income, suburban, etc.
    
    # Sector information
    sector = Column(String(100), nullable=False, index=True)
    naics_code = Column(String(10), nullable=True, index=True)
    
    # Market size and performance
    total_market_size = Column(Float, nullable=False)           # Total addressable market ($)
    serviceable_market_size = Column(Float, nullable=False)     # Serviceable addressable market ($)
    average_business_revenue = Column(Float, nullable=False)    # Average business revenue in area
    median_business_revenue = Column(Float, nullable=False)     # Median business revenue
    revenue_growth_rate = Column(Float, nullable=False)         # Annual growth rate
    
    # Competition analysis
    total_businesses = Column(Integer, nullable=False)          # Number of businesses in area
    competition_density = Column(String(20), nullable=False)    # "low", "medium", "high", "very_high"
    market_concentration = Column(Float, nullable=False)        # HHI or similar measure
    new_business_formation_rate = Column(Float, nullable=False) # New businesses per year
    business_closure_rate = Column(Float, nullable=False)       # Business closures per year
    
    # Demographics and economics
    population = Column(Integer, nullable=False)                # Total population
    median_household_income = Column(Float, nullable=False)     # Median household income
    unemployment_rate = Column(Float, nullable=False)           # Local unemployment rate
    poverty_rate = Column(Float, nullable=False)                # Local poverty rate
    education_level = Column(JSON, nullable=False)              # Education distribution
    age_distribution = Column(JSON, nullable=False)             # Age distribution
    
    # Business environment
    cost_of_living_index = Column(Float, nullable=False)        # Relative to national average
    commercial_rent_per_sqft = Column(Float, nullable=False)    # Average commercial rent
    minimum_wage = Column(Float, nullable=False)                # Local minimum wage
    tax_environment = Column(JSON, nullable=False)              # Tax rates and structure
    
    # Infrastructure and accessibility
    transportation_score = Column(Float, nullable=False)        # Transportation accessibility
    broadband_availability = Column(Float, nullable=False)      # % with broadband access
    utility_costs = Column(JSON, nullable=False)                # Utility cost breakdown
    
    # Consumer behavior
    consumer_spending_patterns = Column(JSON, nullable=False)   # Spending by category
    shopping_preferences = Column(JSON, nullable=False)         # Online vs offline preferences
    seasonal_patterns = Column(JSON, nullable=False)            # Seasonal variation factors
    
    # Market insights
    growth_drivers = Column(JSON, nullable=True)                # Key growth factors
    market_challenges = Column(JSON, nullable=True)             # Key challenges
    opportunities = Column(JSON, nullable=True)                 # Identified opportunities
    threats = Column(JSON, nullable=True)                       # Market threats
    
    # Data quality and freshness
    data_quality_score = Column(Float, nullable=False, default=0.8)
    last_updated = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self) -> str:
        return f"<USMarketData(sector='{self.sector}', state='{self.state}', location_type='{self.location_type}')>"


class USSectorPerformance(Base):
    """US sector performance data over time."""
    
    __tablename__ = "us_sector_performance"
    
    id = Column(Integer, primary_key=True, index=True)
    sector = Column(String(100), nullable=False, index=True)
    date = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # National sector metrics
    national_growth_rate = Column(Float, nullable=False)        # National sector growth
    employment_growth = Column(Float, nullable=False)           # Employment growth in sector
    productivity_growth = Column(Float, nullable=False)         # Productivity improvements
    wage_growth = Column(Float, nullable=False)                 # Average wage growth
    
    # Performance indicators
    revenue_per_employee = Column(Float, nullable=False)        # Average revenue per employee
    profit_margin_average = Column(Float, nullable=False)       # Sector average profit margin
    return_on_assets = Column(Float, nullable=False)            # Average ROA
    inventory_turnover = Column(Float, nullable=False)          # Average inventory turnover
    
    # Market dynamics
    market_volatility = Column(Float, nullable=False)           # Revenue volatility measure
    competitive_intensity = Column(Float, nullable=False)       # Competition level (1-10)
    innovation_rate = Column(Float, nullable=False)             # Rate of innovation/disruption
    consolidation_trend = Column(Float, nullable=False)         # Market consolidation rate
    
    # Economic sensitivity
    fed_rate_correlation = Column(Float, nullable=False)        # Correlation with Fed rates
    inflation_correlation = Column(Float, nullable=False)       # Correlation with inflation
    gdp_correlation = Column(Float, nullable=False)             # Correlation with GDP
    consumer_confidence_correlation = Column(Float, nullable=False) # Correlation with confidence
    
    # External factors
    regulatory_impact = Column(Float, nullable=False)           # Regulatory burden score
    technology_disruption = Column(Float, nullable=False)       # Technology disruption risk
    global_competition = Column(Float, nullable=False)          # International competition
    supply_chain_resilience = Column(Float, nullable=False)     # Supply chain stability
    
    # Forward-looking indicators
    investment_flow = Column(Float, nullable=False)             # Investment in sector
    startup_activity = Column(Float, nullable=False)            # New company formation
    patent_activity = Column(Float, nullable=False)             # Innovation metrics
    talent_attraction = Column(Float, nullable=False)           # Ability to attract talent
    
    # Supporting data
    key_performance_drivers = Column(JSON, nullable=True)       # Main performance factors
    major_market_events = Column(JSON, nullable=True)           # Significant events
    outlook_factors = Column(JSON, nullable=True)               # Forward-looking factors
    
    def __repr__(self) -> str:
        return f"<USSectorPerformance(sector='{self.sector}', date='{self.date}')>"


class USEconomicIndicators(Base):
    """US economic indicators affecting small businesses."""
    
    __tablename__ = "us_economic_indicators"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # Federal Reserve and monetary policy
    fed_funds_rate = Column(Float, nullable=False)              # Federal funds rate
    discount_rate = Column(Float, nullable=False)               # Fed discount rate
    ten_year_treasury = Column(Float, nullable=False)           # 10-year Treasury yield
    yield_curve_spread = Column(Float, nullable=False)          # 10Y-2Y spread
    
    # Inflation and prices
    cpi_all_items = Column(Float, nullable=False)               # Consumer Price Index
    cpi_core = Column(Float, nullable=False)                    # Core CPI (ex food & energy)
    ppi_final_demand = Column(Float, nullable=False)            # Producer Price Index
    pce_price_index = Column(Float, nullable=False)             # Personal Consumption Expenditures
    
    # Employment and labor
    unemployment_rate = Column(Float, nullable=False)           # National unemployment rate
    labor_force_participation = Column(Float, nullable=False)   # Labor force participation
    job_openings_rate = Column(Float, nullable=False)           # Job openings to total employment
    quits_rate = Column(Float, nullable=False)                  # Voluntary quit rate
    average_hourly_earnings = Column(Float, nullable=False)     # Average hourly earnings growth
    
    # Economic growth
    gdp_growth_rate = Column(Float, nullable=False)             # Real GDP growth (annualized)
    gdp_per_capita = Column(Float, nullable=False)              # GDP per capita
    productivity_growth = Column(Float, nullable=False)         # Labor productivity growth
    industrial_production = Column(Float, nullable=False)       # Industrial production index
    
    # Consumer and business sentiment
    consumer_confidence = Column(Float, nullable=False)         # Conference Board Consumer Confidence
    consumer_sentiment = Column(Float, nullable=False)          # University of Michigan Consumer Sentiment
    business_confidence = Column(Float, nullable=False)         # Business roundtable CEO survey
    small_business_optimism = Column(Float, nullable=False)     # NFIB Small Business Optimism
    
    # Financial conditions
    stock_market_sp500 = Column(Float, nullable=False)          # S&P 500 index level
    dollar_index = Column(Float, nullable=False)                # US Dollar Index (DXY)
    corporate_bond_spreads = Column(Float, nullable=False)      # Investment grade credit spreads
    bank_lending_standards = Column(Float, nullable=False)      # Lending standards index
    
    # Housing market
    housing_starts = Column(Float, nullable=False)              # New housing starts
    home_sales = Column(Float, nullable=False)                  # Existing home sales
    home_price_index = Column(Float, nullable=False)            # National home price index
    mortgage_rates = Column(Float, nullable=False)              # 30-year fixed mortgage rate
    
    # Small business specific indicators
    sba_loan_volume = Column(Float, nullable=False)             # SBA loan origination volume
    small_business_lending = Column(Float, nullable=False)      # Commercial lending to small biz
    business_formation_rate = Column(Float, nullable=False)     # New business application rate
    business_closure_rate = Column(Float, nullable=False)       # Business closure rate
    
    # Regional economic health
    regional_fed_surveys = Column(JSON, nullable=False)         # Regional Fed manufacturing surveys
    state_coincident_indices = Column(JSON, nullable=False)     # State economic health indices
    metro_area_performance = Column(JSON, nullable=False)       # Major metro area indicators
    
    def __repr__(self) -> str:
        return f"<USEconomicIndicators(date='{self.date}', fed_rate={self.fed_funds_rate}%)>"


class USMarketForecast(Base):
    """US market forecasts and projections."""
    
    __tablename__ = "us_market_forecasts"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Forecast identification
    sector = Column(String(100), nullable=False, index=True)
    location_type = Column(String(50), nullable=True, index=True)
    forecast_date = Column(DateTime(timezone=True), nullable=False, index=True)
    forecast_horizon = Column(String(20), nullable=False)       # "3_months", "6_months", "1_year", "2_years"
    
    # Economic forecasts
    gdp_growth_forecast = Column(Float, nullable=False)         # Projected GDP growth
    inflation_forecast = Column(Float, nullable=False)          # Projected inflation rate
    fed_rate_forecast = Column(Float, nullable=False)           # Projected Fed funds rate
    unemployment_forecast = Column(Float, nullable=False)       # Projected unemployment
    
    # Sector forecasts
    sector_growth_forecast = Column(Float, nullable=False)      # Projected sector growth
    demand_forecast = Column(Float, nullable=False)             # Demand growth projection
    pricing_forecast = Column(Float, nullable=False)            # Price trend projection
    competition_forecast = Column(Float, nullable=False)        # Competition intensity
    
    # Business environment forecasts
    cost_inflation_forecast = Column(Float, nullable=False)     # Input cost inflation
    wage_growth_forecast = Column(Float, nullable=False)        # Wage inflation projection
    rent_growth_forecast = Column(Float, nullable=False)        # Commercial rent growth
    energy_cost_forecast = Column(Float, nullable=False)        # Energy cost changes
    
    # Market opportunity forecasts
    market_size_forecast = Column(Float, nullable=False)        # Total market size projection
    new_business_opportunity = Column(Float, nullable=False)    # New business opportunity score
    expansion_favorability = Column(Float, nullable=False)      # Expansion timing score
    
    # Risk forecasts
    recession_probability = Column(Float, nullable=False)       # Probability of recession
    sector_disruption_risk = Column(Float, nullable=False)     # Technology disruption risk
    regulatory_risk = Column(Float, nullable=False)            # Regulatory change risk
    
    # Supporting analysis
    key_assumptions = Column(JSON, nullable=False)              # Forecast assumptions
    scenario_analysis = Column(JSON, nullable=False)            # Best/worst/likely scenarios
    confidence_intervals = Column(JSON, nullable=False)         # Confidence bands
    risk_factors = Column(JSON, nullable=False)                 # Key risk factors
    
    # Model performance
    model_accuracy = Column(Float, nullable=True)               # Historical accuracy
    forecast_confidence = Column(Float, nullable=False)         # Confidence level
    last_updated = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self) -> str:
        return f"<USMarketForecast(sector='{self.sector}', horizon='{self.forecast_horizon}')>"