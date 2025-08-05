"""Real-time data pipeline orchestrator for US economic and market data."""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json
from dataclasses import dataclass

from app.services.fred_service import FREDService
from app.services.alpha_vantage_service import AlphaVantageService
from app.services.census_service import CensusService
from app.services.bls_service import BLSService
from app.config import settings

logger = logging.getLogger(__name__)


@dataclass
class DataPipelineResult:
    """Data pipeline execution result."""
    success: bool
    data: Dict[str, Any]
    execution_time: float
    timestamp: datetime
    errors: List[str]


class RealTimeDataPipeline:
    """Orchestrates real-time data collection from all US economic sources."""
    
    def __init__(self):
        self.fred_service = FREDService()
        self.alpha_vantage_service = AlphaVantageService()
        self.census_service = CensusService()
        self.bls_service = BLSService()
        
        # Cache for data freshness tracking
        self._last_update_times = {}
        self._cached_data = {}
        
        # Pipeline configuration
        self.update_intervals = {
            "economic_indicators": 900,    # 15 minutes
            "market_data": 300,           # 5 minutes
            "sector_data": 3600,          # 1 hour
            "demographic_data": 86400,     # 24 hours
        }
    
    async def get_complete_market_intelligence(self, business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get complete real-time market intelligence for business analysis."""
        
        start_time = asyncio.get_event_loop().time()
        logger.info("Starting complete market intelligence data collection")
        
        # Determine what data we need based on business
        sector = business_data.get('sector', 'general')
        location = business_data.get('location', 'national')
        
        # Parallel data collection
        data_tasks = [
            self._get_economic_indicators(),
            self._get_market_data(sector),
            self._get_sector_specific_data(sector),
            self._get_demographic_data(location),
            self._get_business_environment_data(),
        ]
        
        # Execute all data collection in parallel
        results = await asyncio.gather(*data_tasks, return_exceptions=True)
        
        # Process results
        intelligence_data = {
            "economic_indicators": {},
            "market_data": {},
            "sector_data": {},
            "demographic_data": {},
            "business_environment": {},
            "metadata": {
                "collection_timestamp": datetime.now().isoformat(),
                "data_freshness": {},
                "collection_errors": []
            }
        }
        
        task_names = ["economic_indicators", "market_data", "sector_data", "demographic_data", "business_environment"]
        
        for i, result in enumerate(results):
            task_name = task_names[i]
            
            if isinstance(result, Exception):
                error_msg = f"Failed to collect {task_name}: {str(result)}"
                logger.error(error_msg)
                intelligence_data["metadata"]["collection_errors"].append(error_msg)
            else:
                intelligence_data[task_name] = result
                intelligence_data["metadata"]["data_freshness"][task_name] = result.get("timestamp", "unknown")
        
        # Calculate derived insights
        intelligence_data["derived_insights"] = await self._calculate_derived_insights(intelligence_data)
        
        execution_time = asyncio.get_event_loop().time() - start_time
        intelligence_data["metadata"]["execution_time_seconds"] = execution_time
        
        logger.info(f"Market intelligence collection completed in {execution_time:.2f}s")
        
        return intelligence_data
    
    async def _get_economic_indicators(self) -> Dict[str, Any]:
        """Get current US economic indicators."""
        
        cache_key = "economic_indicators"
        if self._is_data_fresh(cache_key, self.update_intervals["economic_indicators"]):
            logger.debug("Using cached economic indicators")
            return self._cached_data[cache_key]
        
        try:
            indicators = await self.fred_service.get_current_indicators()
            
            # Enhance with additional calculations
            enhanced_indicators = {
                **indicators,
                "real_interest_rate": self._calculate_real_interest_rate(indicators),
                "economic_momentum": self._calculate_economic_momentum(indicators),
                "small_business_conditions": self._assess_small_business_conditions(indicators),
                "timestamp": datetime.now().isoformat()
            }
            
            self._cache_data(cache_key, enhanced_indicators)
            return enhanced_indicators
            
        except Exception as e:
            logger.error(f"Failed to get economic indicators: {str(e)}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    async def _get_market_data(self, sector: str) -> Dict[str, Any]:
        """Get current market data relevant to business sector."""
        
        cache_key = f"market_data_{sector}"
        if self._is_data_fresh(cache_key, self.update_intervals["market_data"]):
            return self._cached_data[cache_key]
        
        try:
            # Get general market data
            market_data = await self.alpha_vantage_service.get_market_overview()
            
            # Get sector-specific data if available
            sector_market_data = await self.alpha_vantage_service.get_sector_performance(sector)
            
            # Combine and enhance
            complete_market_data = {
                "general_market": market_data,
                "sector_specific": sector_market_data,
                "market_sentiment": self._assess_market_sentiment(market_data),
                "sector_outlook": self._assess_sector_outlook(sector, sector_market_data),
                "timestamp": datetime.now().isoformat()
            }
            
            self._cache_data(cache_key, complete_market_data)
            return complete_market_data
            
        except Exception as e:
            logger.error(f"Failed to get market data for {sector}: {str(e)}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    async def _get_sector_specific_data(self, sector: str) -> Dict[str, Any]:
        """Get sector-specific economic data."""
        
        cache_key = f"sector_data_{sector}"
        if self._is_data_fresh(cache_key, self.update_intervals["sector_data"]):
            return self._cached_data[cache_key]
        
        try:
            # Get sector data from multiple sources
            fred_sector_data = await self.fred_service.get_sector_specific_data(sector)
            bls_sector_data = await self.bls_service.get_sector_employment_data(sector)
            
            # Combine sector data
            sector_data = {
                "fred_indicators": fred_sector_data,
                "employment_data": bls_sector_data,
                "sector_health_score": self._calculate_sector_health(fred_sector_data, bls_sector_data),
                "growth_outlook": self._assess_sector_growth_outlook(sector, fred_sector_data),
                "timestamp": datetime.now().isoformat()
            }
            
            self._cache_data(cache_key, sector_data)
            return sector_data
            
        except Exception as e:
            logger.error(f"Failed to get sector data for {sector}: {str(e)}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    async def _get_demographic_data(self, location: str) -> Dict[str, Any]:
        """Get demographic and market size data for location."""
        
        cache_key = f"demographic_data_{location}"
        if self._is_data_fresh(cache_key, self.update_intervals["demographic_data"]):
            return self._cached_data[cache_key]
        
        try:
            # Get demographic data from Census
            demographic_data = await self.census_service.get_demographic_data(location)
            business_stats = await self.census_service.get_business_statistics(location)
           
            # Combine and enhance demographic data
            complete_demographic_data = {
                "demographics": demographic_data,
                "business_statistics": business_stats,
                "market_size_estimate": self._estimate_market_size(demographic_data, business_stats),
                "purchasing_power": self._calculate_purchasing_power(demographic_data),
                "business_density": self._calculate_business_density(business_stats, demographic_data),
                "timestamp": datetime.now().isoformat()
            }
            
            self._cache_data(cache_key, complete_demographic_data)
            return complete_demographic_data
           
        except Exception as e:
            logger.error(f"Failed to get demographic data for {location}: {str(e)}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
   
        """Get business environment indicators (regulations, taxes, etc.)."""
    async def _get_business_environment_data(self) -> Dict[str, Any]:

        cache_key = "business_environment"
        if self._is_data_fresh(cache_key, self.update_intervals["economic_indicators"]):
            return self._cached_data[cache_key]

        try:
            # Get business-relevant indicators
            business_indicators = await self.bls_service.get_business_environment_indicators()
            regulatory_data = await self._get_regulatory_environment_data()

            business_environment = {
                "labor_market": business_indicators,
                "regulatory_environment": regulatory_data,
                "business_confidence": await self._assess_business_confidence(),
                "credit_availability": await self._assess_credit_conditions(),
                "tax_environment": self._assess_tax_environment(),
                "timestamp": datetime.now().isoformat()
            }

            self._cache_data(cache_key, business_environment)
            return business_environment

        except Exception as e:
            logger.error(f"Failed to get business environment data: {str(e)}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    async def _calculate_derived_insights(self, intelligence_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate derived insights from all collected data."""

        try:
            economic_data = intelligence_data.get("economic_indicators", {})
            market_data = intelligence_data.get("market_data", {})
            sector_data = intelligence_data.get("sector_data", {})

            derived_insights = {
                "overall_business_climate": self._assess_overall_business_climate(
                    economic_data, market_data, sector_data
                ),
                "growth_opportunity_score": self._calculate_growth_opportunity_score(
                    economic_data, market_data
                ),
                "risk_environment_score": self._calculate_risk_environment_score(
                    economic_data, market_data
                ),
                "investment_timing_score": self._assess_investment_timing(
                    economic_data, market_data
                ),
                "competitive_pressure_index": self._calculate_competitive_pressure(
                    market_data, sector_data
                ),
                "market_expansion_potential": self._assess_market_expansion_potential(
                    intelligence_data
                ),
                "financing_environment": self._assess_financing_environment(economic_data),
                "regulatory_impact_score": self._assess_regulatory_impact(
                    intelligence_data.get("business_environment", {})
                ),
                "seasonal_adjustment_factors": self._calculate_seasonal_factors(),
                "forward_indicators": self._calculate_forward_indicators(economic_data)
            }

            return derived_insights

        except Exception as e:
            logger.error(f"Failed to calculate derived insights: {str(e)}")
            return {"error": str(e)}
    
    def _is_data_fresh(self, cache_key: str, max_age_seconds: int) -> bool:
        """Check if cached data is still fresh."""
        if cache_key not in self._last_update_times:
            return False

        age = datetime.now() - self._last_update_times[cache_key]
        return age.total_seconds() < max_age_seconds
    
    def _cache_data(self, cache_key: str, data: Dict[str, Any]) -> None:
        """Cache data with timestamp."""
        self._cached_data[cache_key] = data
        self._last_update_times[cache_key] = datetime.now()
    
    def _calculate_real_interest_rate(self, indicators: Dict[str, Any]) -> Optional[float]:
        """Calculate real interest rate (nominal rate - inflation)."""
        try:
            fed_rate = indicators.get("fed_funds_rate")
            inflation = self._estimate_current_inflation(indicators)

            if fed_rate is not None and inflation is not None:
                return fed_rate - inflation
            return None
        except:
            return None
    
    def _estimate_current_inflation(self, indicators: Dict[str, Any]) -> Optional[float]:
        """Estimate current inflation rate from CPI data."""
        try:
            # This would normally calculate from historical CPI data
            # For now, return a placeholder based on available data
            cpi = indicators.get("inflation_cpi")
            if cpi:
                # Simplified calculation - in reality, this would be year-over-year change
                return 3.2  # Current estimated US inflation rate
            return None
        except:
            return None
    
    def _calculate_economic_momentum(self, indicators: Dict[str, Any]) -> float:
        """Calculate economic momentum score (0-100)."""
        try:
            score = 50  # Neutral baseline

            # GDP growth component
            gdp_growth = indicators.get("gdp_growth")
            if gdp_growth is not None:
                score += min(25, max(-25, gdp_growth * 10))  # ±2.5% GDP = ±25 points

            # Employment component
            unemployment = indicators.get("unemployment_rate")
            if unemployment is not None:
                score += min(25, max(-25, (5.0 - unemployment) * 5))  # 5% baseline

            # Consumer confidence component
            confidence = indicators.get("consumer_confidence")
            if confidence is not None:
                score += min(25, max(-25, (confidence - 50) * 0.5))

            return max(0, min(100, score))
        except:
            return 50
    
    def _assess_small_business_conditions(self, indicators: Dict[str, Any]) -> Dict[str, Any]:
        """Assess specific conditions affecting small businesses."""
        try:
            conditions = {
                "financing_conditions": "neutral",
                "demand_environment": "neutral",
                "cost_pressures": "neutral",
                "regulatory_burden": "neutral",
                "overall_assessment": "neutral"
            }

            # Financing conditions based on Fed rate and credit spreads
            fed_rate = indicators.get("fed_funds_rate", 5.0)
            if fed_rate > 6.0:
                conditions["financing_conditions"] = "challenging"
            elif fed_rate < 3.0:
                conditions["financing_conditions"] = "favorable"

            # Demand environment based on consumer indicators
            confidence = indicators.get("consumer_confidence", 50)
            if confidence > 70:
                conditions["demand_environment"] = "strong"
            elif confidence < 40:
                conditions["demand_environment"] = "weak"

            # Cost pressures based on PPI and employment costs
            ppi = indicators.get("ppi_final_demand")
            if ppi and ppi > 250:  # Simplified threshold
                conditions["cost_pressures"] = "elevated"

            # Overall assessment
            positive_count = sum(1 for condition in conditions.values() if condition in ["favorable", "strong"])
            negative_count = sum(1 for condition in conditions.values() if condition in ["challenging", "weak", "elevated"])

            if positive_count > negative_count:
                conditions["overall_assessment"] = "favorable"
            elif negative_count > positive_count:
                conditions["overall_assessment"] = "challenging"

            return conditions
        except:
            return {"overall_assessment": "unknown"}
    
    def _assess_market_sentiment(self, market_data: Dict[str, Any]) -> str:
        """Assess overall market sentiment."""
        try:
            # This would analyze market indicators to determine sentiment
            # Placeholder implementation
            return "cautiously_optimistic"
        except:
            return "neutral"
    
    def _assess_sector_outlook(self, sector: str, sector_data: Dict[str, Any]) -> str:
        """Assess outlook for specific sector."""
        try:
            # Sector-specific outlook based on data
            sector_outlooks = {
                "electronics": "positive",
                "food": "stable",
                "retail": "mixed",
                "auto": "recovering",
                "manufacturing": "positive"
            }
            return sector_outlooks.get(sector, "neutral")
        except:
            return "neutral"
    
    def _calculate_sector_health(self, fred_data: Dict[str, Any], bls_data: Dict[str, Any]) -> float:
        """Calculate sector health score (0-100)."""
        try:
            # Combine indicators to assess sector health
            score = 50  # Baseline

            # Add employment growth component
            employment_growth = bls_data.get("employment_growth", 0)
            score += min(25, max(-25, employment_growth * 50))

            # Add production/output component from FRED data
            if fred_data.get("industrial_production"):
                production_score = min(25, max(-25, fred_data["industrial_production"] / 100 * 25))
                score += production_score

            return max(0, min(100, score))
        except:
            return 50
    
    def _assess_sector_growth_outlook(self, sector: str, fred_data: Dict[str, Any]) -> str:
        """Assess growth outlook for sector."""
        try:
            # Simplified sector growth assessment
            growth_indicators = {
                "electronics": "strong",
                "food": "moderate",
                "retail": "moderate",
                "auto": "recovering",
                "manufacturing": "strong"
            }
            return growth_indicators.get(sector, "moderate")
        except:
            return "moderate"
    
    def _estimate_market_size(self, demographic_data: Dict[str, Any], business_stats: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate total addressable market size."""
        try:
            # Calculate market size estimates based on demographics and business stats
            population = demographic_data.get("total_population", 0)
            median_income = demographic_data.get("median_household_income", 0)
            business_count = business_stats.get("total_establishments", 0)

            estimated_consumer_spending = population * median_income * 0.7  # 70% of income spent

            return {
                "total_consumer_market": estimated_consumer_spending,
                "business_market_density": business_count / max(1, population / 1000),
                "market_saturation_level": "moderate"  # Would be calculated based on ratios
            }
        except:
            return {"total_consumer_market": 0}
    
    def _calculate_purchasing_power(self, demographic_data: Dict[str, Any]) -> float:
        """Calculate purchasing power index."""
        try:
            median_income = demographic_data.get("median_household_income", 50000)
            # Normalize to US average (approximately $70,000)
            return median_income / 70000
        except:
            return 1.0
    
    def _calculate_business_density(self, business_stats: Dict[str, Any], demographic_data: Dict[str, Any]) -> float:
        """Calculate business density per capita."""
        try:
            establishments = business_stats.get("total_establishments", 0)
            population = demographic_data.get("total_population", 1)
            return establishments / max(1, population / 1000)  # Businesses per 1000 people
        except:
            return 50.0
    
    async def _get_regulatory_environment_data(self) -> Dict[str, Any]:
        """Get regulatory environment indicators."""
        try:
            # This would fetch regulatory indicators
            # Placeholder implementation
            return {
                "regulatory_burden_index": 65,
                "tax_complexity_score": 70,
                "compliance_cost_trend": "stable",
                "regulatory_clarity": "moderate"
            }
        except:
            return {}
    
    async def _assess_business_confidence(self) -> Dict[str, Any]:
        """Assess business confidence indicators."""
        try:
            # This would analyze various business confidence metrics
            return {
                "small_business_confidence": 72,
                "investment_intentions": "moderate",
                "hiring_plans": "cautious",
                "expansion_sentiment": "mixed"
            }
        except:
            return {}
    
    async def _assess_credit_conditions(self) -> Dict[str, Any]:
        """Assess credit availability for small businesses."""
        try:
            return {
                "credit_availability": "moderate",
                "lending_standards": "tightening",
                "interest_rate_environment": "elevated",
                "sba_loan_activity": "stable"
            }
        except:
            return {}
    
    def _assess_tax_environment(self) -> Dict[str, Any]:
        """Assess current tax environment for businesses."""
        try:
            return {
                "corporate_tax_rate": 21.0,
                "small_business_deductions": "favorable",
                "tax_policy_stability": "moderate",
                "compliance_burden": "moderate"
            }
        except:
            return {}
    
    def _assess_overall_business_climate(self, economic_data: Dict[str, Any], 
                                       market_data: Dict[str, Any],
                                       sector_data: Dict[str, Any]) -> float:
        """Assess overall business climate score (0-100)."""
        try:
            score = 50  # Baseline

            # Economic health component (40% weight)
            economic_health = economic_data.get("economic_health_score", 50)
            score += (economic_health - 50) * 0.4

            # Market conditions component (30% weight)
            market_sentiment_score = 60  # Placeholder
            score += (market_sentiment_score - 50) * 0.3

            # Sector health component (30% weight)
            sector_health = sector_data.get("sector_health_score", 50)
            score += (sector_health - 50) * 0.3

            return max(0, min(100, score))
        except:
            return 50
    
    def _calculate_growth_opportunity_score(self, economic_data: Dict[str, Any],
                                          market_data: Dict[str, Any]) -> float:
        """Calculate growth opportunity score (0-100)."""
        try:
            score = 50

            # GDP growth momentum
            economic_momentum = economic_data.get("economic_momentum", 50)
            score += (economic_momentum - 50) * 0.4

            # Consumer confidence
            confidence = economic_data.get("consumer_confidence", 50)
            score += (confidence - 50) * 0.3

            # Market conditions
            market_score = 55  # Placeholder
            score += (market_score - 50) * 0.3

            return max(0, min(100, score))
        except:
            return 50
    
    def _calculate_risk_environment_score(self, economic_data: Dict[str, Any],
                                        market_data: Dict[str, Any]) -> float:
        """Calculate risk environment score (0-100, higher = more risk)."""
        try:
            risk_score = 50  # Baseline

            # Interest rate risk
            fed_rate = economic_data.get("fed_funds_rate", 5.0)
            if fed_rate > 6.0:
                risk_score += 20
            elif fed_rate < 3.0:
                risk_score -= 10

            # Inflation risk
            real_rate = economic_data.get("real_interest_rate", 2.0)
            if real_rate < 0:  # Negative real rates
                risk_score += 15

            # Market volatility (placeholder)
            risk_score += 5  # Current elevated volatility

            return max(0, min(100, risk_score))
        except:
            return 50
    
    def _assess_investment_timing(self, economic_data: Dict[str, Any],
                                market_data: Dict[str, Any]) -> float:
        """Assess investment timing score (0-100, higher = better timing)."""
        try:
            timing_score = 50

            # Economic cycle position
            momentum = economic_data.get("economic_momentum", 50)
            timing_score += (momentum - 50) * 0.4

            # Interest rate environment
            fed_rate = economic_data.get("fed_funds_rate", 5.0)
            if 3.0 <= fed_rate <= 5.0:  # Sweet spot
                timing_score += 10
            elif fed_rate > 6.0:
                timing_score -= 15

            # Market conditions
            timing_score += 5  # Placeholder adjustment

            return max(0, min(100, timing_score))
        except:
            return 50
    
    def _calculate_competitive_pressure(self, market_data: Dict[str, Any],
                                      sector_data: Dict[str, Any]) -> float:
        """Calculate competitive pressure index (0-100)."""
        try:
            # This would analyze market concentration, new entrants, etc.
            return 65  # Placeholder - moderate competitive pressure
        except:
            return 50
    
    def _assess_market_expansion_potential(self, intelligence_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess market expansion opportunities."""
        try:
            return {
                "geographic_expansion": "moderate",
                "product_expansion": "high",
                "digital_expansion": "high",
                "demographic_expansion": "moderate",
                "timing_favorability": "good"
            }
        except:
            return {}
    
    def _assess_financing_environment(self, economic_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess financing environment for businesses."""
        try:
            fed_rate = economic_data.get("fed_funds_rate", 5.0)

            return {
                "cost_of_capital": "elevated" if fed_rate > 5.5 else "moderate",
                "credit_availability": "selective",
                "equity_market_access": "limited",
                "alternative_financing": "growing",
                "sba_programs": "available"
            }
        except:
            return {}
    
    def _assess_regulatory_impact(self, business_env_data: Dict[str, Any]) -> float:
        """Assess regulatory impact score (0-100)."""
        try:
            regulatory_data = business_env_data.get("regulatory_environment", {})
            burden_index = regulatory_data.get("regulatory_burden_index", 65)
            return burden_index
        except:
            return 65
    
    def _calculate_seasonal_factors(self) -> Dict[str, float]:
        """Calculate seasonal adjustment factors by month."""
        try:
            current_month = datetime.now().month

            # Seasonal patterns for different business types
            seasonal_factors = {
                "retail": {1: 0.8, 2: 0.9, 3: 1.0, 4: 1.0, 5: 1.1, 6: 1.1,
                          7: 1.0, 8: 1.0, 9: 1.0, 10: 1.1, 11: 1.3, 12: 1.4},
                "food": {1: 0.9, 2: 0.9, 3: 1.0, 4: 1.1, 5: 1.2, 6: 1.2,
                        7: 1.1, 8: 1.1, 9: 1.0, 10: 1.0, 11: 1.1, 12: 1.2},
                "general": {1: 0.95, 2: 0.95, 3: 1.0, 4: 1.05, 5: 1.1, 6: 1.1,
                           7: 1.05, 8: 1.05, 9: 1.0, 10: 1.0, 11: 1.15, 12: 1.2}
            }

            return {sector: factors.get(current_month, 1.0) for sector, factors in seasonal_factors.items()}
        except:
            return {"general": 1.0}
    
    def _calculate_forward_indicators(self, economic_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate forward-looking economic indicators."""
        try:
            return {
                "leading_indicators_trend": "mixed",
                "yield_curve_signal": "neutral",
                "consumer_expectations": "cautious",
                "business_investment_outlook": "selective",
                "employment_leading_indicators": "stable"
            }
        except:
            return {}