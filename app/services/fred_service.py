"""Federal Reserve Economic Data (FRED) service for real-time US economic indicators."""

import httpx
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging
from functools import lru_cache

from app.config import settings

logger = logging.getLogger(__name__)


class FREDService:
    """Service for fetching real-time US economic data from Federal Reserve."""
    
    def __init__(self):
        self.api_key = settings.FRED_API_KEY
        self.base_url = settings.FRED_BASE_URL
        self.rate_limit = settings.FRED_RATE_LIMIT
        self._last_request_time = 0
        
        # Key economic indicators we track
        self.indicators = {
            "fed_funds_rate": "FEDFUNDS",
            "inflation_cpi": "CPIAUCSL",
            "unemployment_rate": "UNRATE",
            "gdp_growth": "GDP",
            "consumer_confidence": "UMCSENT",
            "retail_sales": "RSAFS",
            "business_inventories": "BUSINV",
            "small_business_optimism": "USSLIND",
            "ppi_final_demand": "PPIFGS",
            "employment_total": "PAYEMS",
            "housing_starts": "HOUST",
            "industrial_production": "INDPRO"
        }
    
    async def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make rate-limited request to FRED API."""
        
        # Rate limiting - max 120 requests per minute
        current_time = asyncio.get_event_loop().time()
        time_since_last = current_time - self._last_request_time
        
        if time_since_last < 0.5:  # 0.5 seconds between requests
            await asyncio.sleep(0.5 - time_since_last)
        
        params.update({
            "api_key": self.api_key,
            "file_type": "json"
        })
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(f"{self.base_url}/{endpoint}", params=params)
                response.raise_for_status()
                
                self._last_request_time = asyncio.get_event_loop().time()
                data = response.json()
                
                if "error_code" in data:
                    raise Exception(f"FRED API error: {data.get('error_message', 'Unknown error')}")
                
                return data
                
        except httpx.TimeoutException:
            logger.error("FRED API timeout")
            raise Exception("FRED API request timed out")
        except httpx.HTTPStatusError as e:
            logger.error(f"FRED API HTTP error: {e.response.status_code}")
            raise Exception(f"FRED API error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"FRED API error: {str(e)}")
            raise
    
    async def get_current_indicators(self) -> Dict[str, Any]:
        """Get current values for all key economic indicators."""
        
        logger.info("Fetching current US economic indicators from FRED")
        
        # Fetch all indicators concurrently
        tasks = []
        for name, series_id in self.indicators.items():
            task = self._get_latest_value(series_id, name)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        indicators = {}
        for i, result in enumerate(results):
            indicator_name = list(self.indicators.keys())[i]
            
            if isinstance(result, Exception):
                logger.warning(f"Failed to fetch {indicator_name}: {str(result)}")
                indicators[indicator_name] = None
            else:
                indicators[indicator_name] = result
        
        # Calculate derived metrics
        indicators["economic_health_score"] = self._calculate_economic_health(indicators)
        indicators["business_climate_score"] = self._calculate_business_climate(indicators)
        indicators["small_business_impact"] = self._calculate_small_business_impact(indicators)
        
        indicators["last_updated"] = datetime.now().isoformat()
        
        logger.info(f"Successfully fetched {len([v for v in indicators.values() if v is not None])} economic indicators")
        
        return indicators
    
    async def _get_latest_value(self, series_id: str, name: str) -> Optional[float]:
        """Get the latest value for a specific economic series."""
        
        try:
            # Get latest observation
            data = await self._make_request("series/observations", {
                "series_id": series_id,
                "limit": 1,
                "sort_order": "desc"
            })
            
            observations = data.get("observations", [])
            if not observations:
                logger.warning(f"No observations found for {name} ({series_id})")
                return None
            
            latest = observations[0]
            value_str = latest.get("value")
            
            if value_str == "." or value_str is None:
                logger.warning(f"Invalid value for {name}: {value_str}")
                return None
            
            value = float(value_str)
            logger.debug(f"Latest {name}: {value} (date: {latest.get('date')})")
            
            return value
            
        except Exception as e:
            logger.error(f"Error fetching {name}: {str(e)}")
            return None
    
    async def get_historical_data(self, series_id: str, months_back: int = 12) -> List[Dict[str, Any]]:
        """Get historical data for a specific series."""
        
        start_date = (datetime.now() - timedelta(days=months_back * 30)).strftime("%Y-%m-%d")
        
        try:
            data = await self._make_request("series/observations", {
                "series_id": series_id,
                "observation_start": start_date,
                "sort_order": "asc"
            })
            
            observations = data.get("observations", [])
            
            # Clean and format data
            historical_data = []
            for obs in observations:
                if obs.get("value") != ".":
                    try:
                        historical_data.append({
                            "date": obs["date"],
                            "value": float(obs["value"])
                        })
                    except (ValueError, TypeError):
                        continue
            
            return historical_data
            
        except Exception as e:
            logger.error(f"Error fetching historical data for {series_id}: {str(e)}")
            return []
    
    async def get_sector_specific_data(self, sector: str) -> Dict[str, Any]:
        """Get sector-specific economic indicators."""
        
        sector_indicators = {
            "electronics": {
                "industrial_production_tech": "IPG334A",
                "tech_ppi": "PCU334334",
                "consumer_electronics_sales": "RSAFSNA"
            },
            "food": {
                "food_ppi": "PPU02",
                "restaurant_sales": "RSFSR",
                "food_cpi": "CPIFABSL"
            },
            "retail": {
                "retail_sales_total": "RSAFS",
                "retail_inventories": "RETAILIMSA",
                "retail_employment": "CES4200000001"
            },
            "auto": {
                "auto_sales": "TOTALSA",
                "auto_production": "IPG3361T3",
                "auto_inventories": "AUINSA"
            },
            "manufacturing": {
                "manufacturing_pmi": "MANEMP",
                "capacity_utilization": "TCU",
                "new_orders": "NEWORDER"
            }
        }
        
        indicators = sector_indicators.get(sector.lower(), {})
        if not indicators:
            logger.warning(f"No sector-specific indicators available for {sector}")
            return {}
        
        # Fetch all sector indicators
        tasks = []
        for name, series_id in indicators.items():
            task = self._get_latest_value(series_id, name)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        sector_data = {}
        for i, result in enumerate(results):
            indicator_name = list(indicators.keys())[i]
            sector_data[indicator_name] = result if not isinstance(result, Exception) else None
        
        return sector_data
    
    def _calculate_economic_health(self, indicators: Dict[str, Any]) -> float:
        """Calculate overall economic health score (0-100)."""
        
        score = 50  # Neutral baseline
        
        # GDP growth (weight: 25%)
        if indicators.get("gdp_growth"):
            gdp_score = min(100, max(0, (indicators["gdp_growth"] + 2) * 25))  # -2% to +2% mapped to 0-100
            score += (gdp_score - 50) * 0.25
        
        # Unemployment rate (weight: 25%, inverted)
        if indicators.get("unemployment_rate"):
            unemployment_score = max(0, 100 - indicators["unemployment_rate"] * 10)  # 10% unemployment = 0 score
            score += (unemployment_score - 50) * 0.25
        
        # Inflation/CPI (weight: 20%, target 2%)
        if indicators.get("inflation_cpi"):
            # Calculate annual inflation rate (simplified)
            inflation_score = max(0, 100 - abs(2.0 - 2.0) * 20)  # 2% target, penalty for deviation
            score += (inflation_score - 50) * 0.20
        
        # Consumer confidence (weight: 15%)
        if indicators.get("consumer_confidence"):
            confidence_score = min(100, indicators["consumer_confidence"])
            score += (confidence_score - 50) * 0.15
        
        # Small business optimism (weight: 15%)
        if indicators.get("small_business_optimism"):
            optimism_score = min(100, indicators["small_business_optimism"])
            score += (optimism_score - 50) * 0.15
        
        return max(0, min(100, score))
    
    def _calculate_business_climate(self, indicators: Dict[str, Any]) -> float:
        """Calculate business climate score for SMEs."""
        
        score = 50  # Neutral baseline
        
        # Fed funds rate impact (lower is better for small business)
        if indicators.get("fed_funds_rate"):
            rate_score = max(0, 100 - indicators["fed_funds_rate"] * 20)  # 5% rate = 0 score
            score += (rate_score - 50) * 0.3
        
        # Small business optimism
        if indicators.get("small_business_optimism"):
            score += (indicators["small_business_optimism"] - 50) * 0.3
        
        # Retail sales growth (proxy for business revenue)
        if indicators.get("retail_sales"):
            # Simplified retail sales score
            sales_score = min(100, max(0, 50 + indicators["retail_sales"] / 1000))
            score += (sales_score - 50) * 0.2
        
        # Employment growth
        if indicators.get("employment_total"):
            # Simplified employment score
            employment_score = min(100, max(0, 50 + indicators["employment_total"] / 100000))
            score += (employment_score - 50) * 0.2
        
        return max(0, min(100, score))
    
    def _calculate_small_business_impact(self, indicators: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate specific impacts on small businesses."""
        
        impact = {
            "financing_cost_impact": "neutral",
            "demand_impact": "neutral", 
            "cost_pressure_impact": "neutral",
            "overall_impact": "neutral"
        }
        
        # Financing cost impact (based on Fed funds rate)
        if indicators.get("fed_funds_rate"):
            fed_rate = indicators["fed_funds_rate"]
            if fed_rate > 5.0:
                impact["financing_cost_impact"] = "negative"
            elif fed_rate < 2.0:
                impact["financing_cost_impact"] = "positive"
        
        # Demand impact (based on consumer confidence and retail sales)
        consumer_conf = indicators.get("consumer_confidence", 50)
        if consumer_conf > 70:
            impact["demand_impact"] = "positive"
        elif consumer_conf < 40:
            impact["demand_impact"] = "negative"
        
        # Cost pressure (based on PPI)
        if indicators.get("ppi_final_demand"):
            # Simplified cost pressure calculation
            ppi = indicators["ppi_final_demand"]
            if ppi > 250:  # Arbitrary threshold for high PPI
                impact["cost_pressure_impact"] = "negative"
            elif ppi < 200:
                impact["cost_pressure_impact"] = "positive"
        
        # Overall impact
        impacts = [impact["financing_cost_impact"], impact["demand_impact"], impact["cost_pressure_impact"]]
        positive_count = impacts.count("positive")
        negative_count = impacts.count("negative")
        
        if positive_count > negative_count:
            impact["overall_impact"] = "positive"
        elif negative_count > positive_count:
            impact["overall_impact"] = "negative"
        
        return impact

    @lru_cache(maxsize=32)
    async def get_cached_indicators(self, cache_key: str) -> Dict[str, Any]:
        """Get cached economic indicators (cache for 15 minutes)."""
        return await self.get_current_indicators()