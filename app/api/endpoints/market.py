"""Market data and intelligence endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.market import (
   KarachiMarketDataResponse, SectorPerformanceResponse, 
   EconomicIndicatorsResponse, MarketInsightsResponse,
   MarketTrendAnalysis, LocationAnalysis, SectorBenchmarks,
   MarketForecast, CompetitiveAnalysis
)
from app.core.market_generator import MarketDataGenerator
from app.core.karachi_intelligence import KarachiIntelligence
from app.data.karachi_sectors import get_sector_data, get_location_data
from app.data.economic_factors import get_current_economic_indicators, get_seasonal_factor

router = APIRouter()

# Initialize market intelligence engines
market_generator = MarketDataGenerator()
karachi_intel = KarachiIntelligence()


@router.get("/market/{sector}/{location}", response_model=KarachiMarketDataResponse)
async def get_market_data(
   sector: str,
   location: str,
   db: Session = Depends(get_db)
):
   """
   Get comprehensive market data for specific sector and location in Karachi.
   
   Returns market size, competition level, demographic data, and key insights
   for the specified sector-location combination.
   """
   try:
       # Validate sector and location
       valid_sectors = ["electronics", "textile", "auto", "food", "retail"]
       valid_locations = ["clifton", "dha", "saddar", "tariq_road", "gulshan", 
                         "gulistan_e_johar", "korangi", "landhi", "north_karachi", "nazimabad"]
       
       if sector.lower() not in valid_sectors:
           raise HTTPException(
               status_code=status.HTTP_400_BAD_REQUEST,
               detail=f"Invalid sector. Must be one of: {', '.join(valid_sectors)}"
           )
       
       location_clean = location.lower().replace(' ', '_').replace('-', '_')
       if location_clean not in valid_locations:
           raise HTTPException(
               status_code=status.HTTP_400_BAD_REQUEST,
               detail=f"Invalid location. Must be one of: {', '.join(valid_locations)}"
           )
       
       # Generate market data
       market_data = market_generator.generate_location_market_data(sector.lower(), location_clean)
       
       # Get additional context
       sector_data = get_sector_data(sector.lower())
       location_data = get_location_data(location_clean)
       
       # Create response
       response = KarachiMarketDataResponse(
           id=1,  # Placeholder
           sector=sector.lower(),
           location_area=location_clean,
           average_revenue=market_data["market_size"]["average_monthly_revenue"],
           revenue_growth_rate=market_data["market_size"]["market_growth_rate"],
           competition_density=market_data["competition"]["level"],
           market_size=market_data["market_size"]["total_market_size"],
           rent_cost_per_sqft=sector_data["location_factors"][location_clean]["rent_factor"] * 1000,
           foot_traffic_level=location_data["characteristics"]["foot_traffic"],
           customer_demographics={
               "customer_type": location_data["characteristics"]["customer_type"],
               "spending_power": "high" if location_clean in ["clifton", "dha"] else "medium",
               "age_groups": {"25-35": 30, "35-45": 40, "45-55": 30},  # Placeholder
               "income_levels": {"high": 40, "medium": 50, "low": 10} if location_clean in ["clifton", "dha"] else {"high": 20, "medium": 60, "low": 20}
           },
           accessibility_score=8.0 if location_data["characteristics"]["accessibility"] == "excellent" else 6.0,
           local_purchasing_power=1.5 if location_clean in ["clifton", "dha"] else 1.0,
           seasonal_factors=market_data["seasonal_patterns"],
           key_insights=location_data["advantages"][:3],
           last_updated="2024-01-01T00:00:00Z"  # Placeholder
       )
       
       return response
       
   except Exception as e:
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail=f"Failed to get market data: {str(e)}"
       )


@router.get("/market/sectors/{sector}/performance")
async def get_sector_performance(
   sector: str,
   days: int = 30,
   db: Session = Depends(get_db)
):
   """
   Get sector performance data over time.
   
   Returns growth rates, volatility, market sentiment, and key drivers
   for the specified sector in Karachi.
   """
   try:
       valid_sectors = ["electronics", "textile", "auto", "food", "retail"]
       
       if sector.lower() not in valid_sectors:
           raise HTTPException(
               status_code=status.HTTP_400_BAD_REQUEST,
               detail=f"Invalid sector. Must be one of: {', '.join(valid_sectors)}"
           )
       
       # Generate sector performance data
       performance_data = market_generator.generate_sector_performance(sector.lower(), days)
       
       # Calculate aggregated metrics
       daily_changes = [data["daily_change"] for data in performance_data]
       avg_daily_change = sum(daily_changes) / len(daily_changes)
       volatility = (sum((x - avg_daily_change) ** 2 for x in daily_changes) / len(daily_changes)) ** 0.5
       
       # Determine market sentiment
       if avg_daily_change > 0.005:
           sentiment = "positive"
       elif avg_daily_change < -0.005:
           sentiment = "negative"
       else:
           sentiment = "neutral"
       
       # Get economic and seasonal impacts
       economic_indicators = get_current_economic_indicators()
       seasonal_factor = get_seasonal_factor(sector.lower())
       
       response = SectorPerformanceResponse(
           id=1,  # Placeholder
           sector=sector.lower(),
           date="2024-01-01T00:00:00Z",  # Placeholder
           growth_rate=avg_daily_change * 30,  # Monthly growth rate
           volatility=volatility,
           market_sentiment=sentiment,
           economic_impact=-0.1 if economic_indicators["inflation_rate"] > 0.25 else 0.05,
           seasonal_impact=seasonal_factor - 1.0,
           policy_impact=0.02,  # Placeholder
           key_drivers=[
               f"Economic conditions: {'Challenging' if economic_indicators['inflation_rate'] > 0.25 else 'Supportive'}",
               f"Seasonal factors: {'Peak season' if seasonal_factor > 1.1 else 'Normal period'}",
               "Market demand trends",
               "Competition dynamics"
           ],
           market_events=[
               {"event": "Economic policy changes", "impact": "medium", "date": "2024-01-15"},
               {"event": "Seasonal demand shift", "impact": "high", "date": "2024-01-01"}
           ]
       )
       
       return response
       
   except Exception as e:
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail=f"Failed to get sector performance: {str(e)}"
       )


@router.get("/market/economic-indicators", response_model=EconomicIndicatorsResponse)
async def get_economic_indicators(db: Session = Depends(get_db)):
   """
   Get current economic indicators affecting Pakistani businesses.
   
   Returns PKR rates, inflation, interest rates, GDP growth, and other
   key economic metrics that impact business performance.
   """
   try:
       indicators = get_current_economic_indicators()
       
       response = EconomicIndicatorsResponse(
           id=1,  # Placeholder
           date="2024-01-01T00:00:00Z",  # Placeholder
           pkr_usd_rate=indicators["pkr_usd_rate"],
           inflation_rate=indicators["inflation_rate"],
           interest_rate=indicators["interest_rate"],
           gdp_growth_rate=indicators["gdp_growth"],
           unemployment_rate=indicators["unemployment"],
           consumer_confidence=65.0,  # Placeholder
           ease_of_business_index=72.0,  # Placeholder
           tax_policy_impact=0.05,  # Placeholder
           regulatory_environment="stable",
           supply_chain_status="constrained" if indicators["supply_chain_stress"] > 0.6 else "normal",
           energy_cost_index=indicators["energy_cost_index"]
       )
       
       return response
       
   except Exception as e:
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail=f"Failed to get economic indicators: {str(e)}"
       )


@router.get("/market/{sector}/{location}/trends")
async def get_market_trends(
   sector: str,
   location: str,
   db: Session = Depends(get_db)
):
   """
   Get market trend analysis for specific sector and location.
   
   Returns trend direction, growth momentum, market maturity,
   and competitive dynamics analysis.
   """
   try:
       # Validate inputs
       valid_sectors = ["electronics", "textile", "auto", "food", "retail"]
       if sector.lower() not in valid_sectors:
           raise HTTPException(status_code=400, detail="Invalid sector")
       
       location_clean = location.lower().replace(' ', '_').replace('-', '_')
       
       # Generate market data for trend analysis
       market_data = market_generator.generate_location_market_data(sector.lower(), location_clean)
       sector_data = get_sector_data(sector.lower())
       
       # Analyze trends
       growth_rate = market_data["market_size"]["market_growth_rate"]
       competition_level = market_data["competition"]["level"]
       
       # Determine trend direction
       if growth_rate > 0.1:
           trend_direction = "strongly_positive"
       elif growth_rate > 0.05:
           trend_direction = "positive"
       elif growth_rate > 0:
           trend_direction = "stable_growth"
       elif growth_rate > -0.05:
           trend_direction = "stable"
       else:
           trend_direction = "declining"
       
       # Calculate growth momentum (0-100 scale)
       momentum_score = min(100, max(0, (growth_rate + 0.1) * 500))
       
       # Assess market maturity
       competition_maturity_scores = {"low": 1, "medium": 2, "high": 3, "very_high": 4}
       maturity_score = competition_maturity_scores.get(competition_level, 2)
       
       if maturity_score <= 1:
           market_maturity = "emerging"
       elif maturity_score <= 2:
           market_maturity = "growing"
       elif maturity_score <= 3:
           market_maturity = "mature"
       else:
           market_maturity = "saturated"
       
       # Competitive intensity (1-10 scale)
       intensity_scores = {"low": 3, "medium": 5, "high": 7, "very_high": 9}
       competitive_intensity = intensity_scores.get(competition_level, 5)
       
       # Opportunity score based on growth and competition
       opportunity_score = min(100, (growth_rate * 200) + (10 - competitive_intensity) * 10)
       
       response = MarketTrendAnalysis(
           sector=sector.lower(),
           location_area=location_clean,
           trend_direction=trend_direction,
           growth_momentum=momentum_score,
           market_maturity=market_maturity,
           competitive_intensity=competitive_intensity,
           opportunity_score=opportunity_score,
           risk_factors=sector_data.get("business_insights", {}).get("common_challenges", [])[:3],
           growth_drivers=sector_data.get("business_insights", {}).get("growth_opportunities", [])[:3],
           market_challenges=[
               f"{competition_level.title()} competition",
               "Economic pressure from inflation",
               "Supply chain constraints"
           ]
       )
       
       return response
       
   except Exception as e:
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail=f"Failed to get market trends: {str(e)}"
       )


@router.get("/market/locations/{location}/analysis")
async def get_location_analysis(
   location: str,
   db: Session = Depends(get_db)
):
   """
   Get comprehensive location analysis for Karachi areas.
   
   Returns location advantages, disadvantages, best sectors,
   and expansion potential analysis.
   """
   try:
       location_clean = location.lower().replace(' ', '_').replace('-', '_')
       location_data = get_location_data(location_clean)
       
       if not location_data:
           raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail=f"Location data not found for {location}"
           )
       
       # Calculate location score
       characteristics = location_data["characteristics"]
       
       # Scoring factors
       traffic_scores = {"very_high": 25, "high": 20, "medium": 15, "low": 10}
       rent_scores = {"low": 25, "medium": 20, "medium_high": 15, "high": 10, "very_high": 5}
       competition_scores = {"low": 25, "medium": 20, "high": 15, "very_high": 10}
       
       location_score = (
           traffic_scores.get(characteristics["foot_traffic"], 15) +
           rent_scores.get(characteristics["rent_level"], 15) +
           competition_scores.get(characteristics["competition"], 15) +
           15  # Base accessibility score
       )
       
       # Rent affordability
       if characteristics["rent_level"] in ["low", "medium"]:
           rent_affordability = "affordable"
       elif characteristics["rent_level"] == "medium_high":
           rent_affordability = "moderate"
       else:
           rent_affordability = "expensive"
       
       # Customer accessibility
       accessibility_mapping = {
           "excellent": "very_accessible",
           "good": "accessible", 
           "moderate": "moderately_accessible",
           "poor": "difficult_access"
       }
       customer_accessibility = accessibility_mapping.get(characteristics["accessibility"], "accessible")
       
       # Competition analysis
       competition_analysis = {
           "competition_level": characteristics["competition"],
           "market_saturation": "high" if characteristics["competition"] in ["high", "very_high"] else "medium",
           "new_entrant_difficulty": "high" if characteristics["competition"] == "very_high" else "medium",
           "pricing_pressure": "intense" if characteristics["competition"] == "very_high" else "moderate"
       }
       
       # Expansion potential
       if characteristics["competition"] in ["low", "medium"] and characteristics["foot_traffic"] in ["high", "very_high"]:
           expansion_potential = "high"
       elif characteristics["competition"] == "medium":
           expansion_potential = "medium"
       else:
           expansion_potential = "low"
       
       response = LocationAnalysis(
           location_area=location_clean,
           location_score=location_score,
           advantages=location_data["advantages"][:3],
           disadvantages=location_data["challenges"][:3],
           best_sectors=location_data["best_businesses"],
           rent_affordability=rent_affordability,
           customer_accessibility=customer_accessibility,
           competition_analysis=competition_analysis,
           expansion_potential=expansion_potential
       )
       
       return response
       
   except Exception as e:
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail=f"Failed to get location analysis: {str(e)}"
       )


@router.get("/market/{sector}/benchmarks")
async def get_sector_benchmarks(
   sector: str,
   location: Optional[str] = None,
   db: Session = Depends(get_db)
):
   """
   Get performance benchmarks for sector.
   
   Returns financial and operational benchmarks that businesses
   can use to measure their performance against industry standards.
   """
   try:
       valid_sectors = ["electronics", "textile", "auto", "food", "retail"]
       if sector.lower() not in valid_sectors:
           raise HTTPException(status_code=400, detail="Invalid sector")
       
       location_clean = "saddar"  # Default location
       if location:
           location_clean = location.lower().replace(' ', '_').replace('-', '_')
       
       # Generate benchmarks
       benchmarks = market_generator.generate_performance_benchmarks(sector.lower(), location_clean)
       sector_data = get_sector_data(sector.lower())
       
       response = SectorBenchmarks(
           sector=sector.lower(),
           location_area=location_clean,
           performance_benchmarks={
               "revenue_top_10_percent": benchmarks["revenue_benchmarks"]["top_10_percent"],
               "revenue_median": benchmarks["revenue_benchmarks"]["median"],
               "revenue_bottom_25_percent": benchmarks["revenue_benchmarks"]["bottom_25_percent"],
           },
           financial_benchmarks={
               "profit_margin_excellent": benchmarks["operational_benchmarks"]["profit_margin"]["excellent"],
               "profit_margin_average": benchmarks["operational_benchmarks"]["profit_margin"]["average"],
               "revenue_growth_excellent": benchmarks["operational_benchmarks"]["revenue_growth"]["excellent"],
               "revenue_growth_average": benchmarks["operational_benchmarks"]["revenue_growth"]["average"],
           },
           operational_benchmarks={
               "customer_retention_excellent": benchmarks["operational_benchmarks"]["customer_retention"]["excellent"],
               "customer_retention_average": benchmarks["operational_benchmarks"]["customer_retention"]["average"],
               "inventory_turnover": 6.0,  # Placeholder
               "employee_productivity": 150000,  # Revenue per employee placeholder
           },
           top_performer_characteristics=[
               "Focus on high-margin products",
               "Strong customer relationships",
               "Efficient operations",
               "Strategic location advantage"
           ],
           common_challenges=sector_data.get("business_insights", {}).get("common_challenges", [])[:3],
           success_factors=sector_data.get("business_insights", {}).get("success_factors", [])[:3]
       )
       
       return response
       
   except Exception as e:
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail=f"Failed to get sector benchmarks: {str(e)}"
       )


@router.get("/market/{sector}/forecast")
async def get_market_forecast(
   sector: str,
   months: int = 6,
   db: Session = Depends(get_db)
):
   """
   Get market forecast for sector.
   
   Returns growth projections, market size forecasts, key trends,
   and potential disruptions for planning purposes.
   """
   try:
       valid_sectors = ["electronics", "textile", "auto", "food", "retail"]
       if sector.lower() not in valid_sectors:
           raise HTTPException(status_code=400, detail="Invalid sector")
       
       sector_data = get_sector_data(sector.lower())
       current_growth = sector_data["base_performance"]["growth_rate"]
       
       # Generate forecast
       forecast_growth = current_growth * 0.9  # Slightly conservative
       
       # Sector-specific trends and disruptions
       sector_trends = {
           "electronics": ["5G adoption accelerating", "Mobile repair services growing", "Smart home devices demand"],
           "textile": ["Online sales increasing", "Sustainable fashion trends", "Custom tailoring demand"],
           "auto": ["Electric vehicle transition", "Motorcycle market growth", "Mobile services expansion"],
           "food": ["Home delivery dominance", "Health-conscious consumers", "Cloud kitchen concepts"],
           "retail": ["Omnichannel integration", "Social media commerce", "Personalization trends"]
       }
       
       sector_disruptions = {
           "electronics": ["AI-powered devices", "Cryptocurrency adoption", "5G infrastructure"],
           "textile": ["E-commerce dominance", "Fast fashion competition", "Sustainability regulations"],
           "auto": ["Electric vehicle subsidies", "Import policy changes", "Ride-sharing growth"],
           "food": ["Dark kitchen models", "Food delivery platforms", "Health regulations"],
           "retail": ["E-commerce growth", "Social commerce", "Cashless payments"]
       }
       
       # Investment climate assessment
       economic_indicators = get_current_economic_indicators()
       
       if economic_indicators["inflation_rate"] > 0.25:
           investment_climate = "challenging"
       elif economic_indicators["interest_rate"] > 0.20:
           investment_climate = "cautious"
       else:
           investment_climate = "favorable"
       
       response = MarketForecast(
           sector=sector.lower(),
           location_area="karachi",
           forecast_period=f"{months} months",
           growth_forecast=forecast_growth,
           market_size_forecast=500000000 * (1 + forecast_growth) ** (months / 12),  # Placeholder
           key_trends=sector_trends.get(sector.lower(), ["General market evolution"]),
           potential_disruptions=sector_disruptions.get(sector.lower(), ["Technology changes"]),
           investment_climate=investment_climate,
           confidence_level=0.75
       )
       
       return response
       
   except Exception as e:
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail=f"Failed to get market forecast: {str(e)}"
       )


@router.get("/market/{sector}/{location}/competition")
async def get_competitive_analysis(
   sector: str,
   location: str,
   db: Session = Depends(get_db)
):
   """
   Get competitive analysis for specific sector and location.
   
   Returns competitor count, market share distribution, competitive
   advantages to leverage, and market gaps to exploit.
   """
   try:
       location_clean = location.lower().replace(' ', '_').replace('-', '_')
       
       # Generate market data
       market_data = market_generator.generate_location_market_data(sector.lower(), location_clean)
       sector_data = get_sector_data(sector.lower())
       
       competition_level = market_data["competition"]["level"]
       
       # Estimate competitor counts
       competitor_counts = {
           "very_high": 25, "high": 15, "medium": 8, "low": 4
       }
       competitor_count = competitor_counts.get(competition_level, 8)
       
       # Market share distribution (simplified)
       if competition_level == "very_high":
           market_share_dist = {"top_3": 30, "next_7": 40, "others": 30}
       elif competition_level == "high":
           market_share_dist = {"top_3": 40, "next_5": 35, "others": 25}
       else:
           market_share_dist = {"top_2": 50, "next_3": 30, "others": 20}
       
       # Competitive advantages and threats
       advantages = sector_data.get("business_insights", {}).get("success_factors", [])[:3]
       threats = [
           f"{competition_level.title()} price competition",
           "New market entrants",
           "Customer switching costs low"
       ]
       
       # Market gaps (opportunities)
       gaps = sector_data.get("business_insights", {}).get("growth_opportunities", [])[:3]
       
       # Differentiation opportunities
       differentiators = [
           "Superior customer service",
           "Specialized product offerings",
           "Technology integration",
           "Location advantage"
       ]
       
       response = CompetitiveAnalysis(
           sector=sector.lower(),
           location_area=location_clean,
           competitor_count=competitor_count,
           market_share_distribution=market_share_dist,
           competitive_advantages=advantages,
           competitive_threats=threats,
           market_gaps=gaps,
           differentiation_opportunities=differentiators
       )
       
       return response
       
   except Exception as e:
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail=f"Failed to get competitive analysis: {str(e)}"
       )


@router.get("/market/overview")
async def get_market_overview(db: Session = Depends(get_db)):
   """
   Get overall Karachi market overview.
   
   Returns high-level statistics and trends across all sectors and locations.
   """
   try:
       # Generate overview statistics
       overview = {
           "total_market_size": "Rs. 50 billion annually",
           "active_sectors": 5,
           "covered_locations": 10,
           "total_businesses": "3.3 million SMEs",
           "growth_rate": "6.5% annually",
           "top_growing_sectors": ["electronics", "food", "retail"],
           "most_competitive_areas": ["saddar", "tariq_road"],
           "best_expansion_opportunities": ["gulshan", "north_karachi"],
           "economic_outlook": "cautiously optimistic",
           "key_challenges": [
               "High inflation impact",
               "PKR volatility",
               "Supply chain constraints"
           ],
           "key_opportunities": [
               "Digital transformation",
               "Home delivery services",
               "Premium market growth"
           ]
       }
       
       return overview
       
   except Exception as e:
       raise HTTPException(
           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
           detail=f"Failed to get market overview: {str(e)}"
       )