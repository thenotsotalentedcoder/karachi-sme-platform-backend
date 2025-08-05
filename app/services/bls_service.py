"""Bureau of Labor Statistics (BLS) service for US employment and labor market data."""

import httpx
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging
import json

from app.config import settings

logger = logging.getLogger(__name__)


class BLSService:
    """Service for fetching US employment and labor data from Bureau of Labor Statistics."""
    
    def __init__(self):
        self.api_key = settings.BLS_API_KEY
        self.base_url = settings.BLS_BASE_URL
        self.rate_limit = settings.BLS_RATE_LIMIT
        self._last_request_time = 0
        
        # Key BLS series we track for small business intelligence
        self.series_ids = {
            # National Employment
            "total_nonfarm_employment": "CES0000000001",
            "private_employment": "CES0500000001",
            "small_business_employment": "CES0500000001",  # Proxy
            
            # Sector Employment
            "retail_employment": "CES4200000001",
            "food_services_employment": "CES7072000001", 
            "professional_services_employment": "CES5400000001",
            "manufacturing_employment": "CES3000000001",
            "construction_employment": "CES2000000001",
            "healthcare_employment": "CES6500000001",
            
            # Wages and Earnings
            "average_hourly_earnings": "CES0500000003",
            "retail_hourly_earnings": "CES4200000003",
            "food_services_hourly_earnings": "CES7072000003",
            "professional_services_hourly_earnings": "CES5400000003",
            
            # Labor Force Statistics
            "unemployment_rate": "LNS14000000",
            "labor_force_participation": "LNS11300000",
            "employment_population_ratio": "LNS12300000",
            
            # Small Business Specific (Job Openings and Labor Turnover)
            "job_openings_total": "JTS00000000JOL",
            "job_openings_retail": "JTS4400000000JOL",
            "job_openings_food_services": "JTS722000000JOL",
            "quits_rate": "JTS00000000QUR",
            "hires_rate": "JTS00000000HIR",
            
            # Consumer Price Index (impacts small business costs)
            "cpi_all_items": "CUUR0000SA0",
            "cpi_food": "CUUR0000SAF1",
            "cpi_energy": "CUUR0000SA0E",
            "cpi_services": "CUUR0000SAS",
            
            # Producer Price Index (small business input costs)
            "ppi_final_demand": "WPUFD49207",
            "ppi_services": "WPUFD49116",
            "ppi_goods": "WPUFD4131"
        }
    
    async def _make_request(self, series_ids: List[str], start_year: str = None, 
                           end_year: str = None) -> Dict[str, Any]:
        """Make rate-limited request to BLS API."""
        
        # Rate limiting - max 500 requests per day, with spacing
        current_time = asyncio.get_event_loop().time()
        time_since_last = current_time - self._last_request_time
        
        if time_since_last < 1:  # 1 second between requests
            await asyncio.sleep(1 - time_since_last)
        
        # Prepare request data
        data = {
            "seriesid": series_ids,
            "registrationkey": self.api_key
        }
        
        if start_year:
            data["startyear"] = start_year
        if end_year:
            data["endyear"] = end_year
        
        headers = {
            "Content-Type": "application/json"
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/timeseries/data/", 
                    headers=headers, 
                    json=data
                )
                response.raise_for_status()
                
                self._last_request_time = asyncio.get_event_loop().time()
                response_data = response.json()
                
                # Check for API errors
                if response_data.get("status") == "REQUEST_NOT_PROCESSED":
                    error_msg = ", ".join(response_data.get("message", ["Unknown error"]))
                    raise Exception(f"BLS API error: {error_msg}")
                
                return response_data
                
        except httpx.TimeoutException:
            logger.error("BLS API timeout")
            raise Exception("BLS API request timed out")
        except httpx.HTTPStatusError as e:
            logger.error(f"BLS API HTTP error: {e.response.status_code}")
            raise Exception(f"BLS API error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"BLS API error: {str(e)}")
            raise
    
    async def get_current_employment_data(self) -> Dict[str, Any]:
        """Get current employment data relevant to small businesses."""
        
        logger.info("Fetching current employment data from BLS")
        
        try:
            # Get employment series for current year
            current_year = str(datetime.now().year)
            employment_series = [
                self.series_ids["total_nonfarm_employment"],
                self.series_ids["private_employment"],
                self.series_ids["retail_employment"],
                self.series_ids["food_services_employment"],
                self.series_ids["professional_services_employment"],
                self.series_ids["manufacturing_employment"],
                self.series_ids["unemployment_rate"],
                self.series_ids["labor_force_participation"]
            ]
            
            response = await self._make_request(employment_series, current_year, current_year)
            
            # Process employment data
            employment_data = self._process_employment_response(response)
            
            # Calculate derived metrics
            employment_data["small_business_impact"] = self._calculate_small_business_employment_impact(employment_data)
            employment_data["employment_momentum"] = self._calculate_employment_momentum(employment_data)
            employment_data["labor_market_tightness"] = self._calculate_labor_market_tightness(employment_data)
            
            employment_data["timestamp"] = datetime.now().isoformat()
            
            return employment_data
            
        except Exception as e:
            logger.error(f"Failed to get current employment data: {str(e)}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    async def get_sector_employment_data(self, sector: str) -> Dict[str, Any]:
        """Get employment data for specific business sector."""
        
        logger.info(f"Fetching employment data for {sector} sector")
        
        # Map business sectors to BLS series
        sector_mapping = {
            "electronics": ["retail_employment", "manufacturing_employment"],
            "food": ["food_services_employment", "retail_employment"],
            "retail": ["retail_employment"],
            "auto": ["manufacturing_employment", "retail_employment"],
            "manufacturing": ["manufacturing_employment"],
            "professional": ["professional_services_employment"],
            "construction": ["construction_employment"],
            "healthcare": ["healthcare_employment"]
        }
        
        relevant_series = sector_mapping.get(sector.lower(), ["retail_employment"])
        
        try:
            current_year = str(datetime.now().year)
            last_year = str(datetime.now().year - 1)
            
            # Get relevant series IDs
            series_list = [self.series_ids[series] for series in relevant_series]
            
            response = await self._make_request(series_list, last_year, current_year)
            
            sector_data = self._process_sector_employment_response(response, sector, relevant_series)
            
            # Add sector-specific analysis
            sector_data["sector_health_score"] = self._calculate_sector_health_score(sector_data)
            sector_data["employment_trend"] = self._calculate_employment_trend(sector_data)
            sector_data["wage_competitiveness"] = await self._calculate_wage_competitiveness(sector)
            
            sector_data["timestamp"] = datetime.now().isoformat()
            
            return sector_data
            
        except Exception as e:
            logger.error(f"Failed to get sector employment data for {sector}: {str(e)}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    async def get_wage_and_earnings_data(self) -> Dict[str, Any]:
        """Get wage and earnings data affecting small businesses."""
        
        logger.info("Fetching wage and earnings data from BLS")
        
        try:
            current_year = str(datetime.now().year)
            wage_series = [
                self.series_ids["average_hourly_earnings"],
                self.series_ids["retail_hourly_earnings"],
                self.series_ids["food_services_hourly_earnings"],
                self.series_ids["professional_services_hourly_earnings"]
            ]
            
            response = await self._make_request(wage_series, current_year, current_year)
            
            wage_data = self._process_wage_response(response)
            
            # Calculate wage pressure indicators
            wage_data["wage_inflation_rate"] = self._calculate_wage_inflation(wage_data)
            wage_data["small_business_wage_pressure"] = self._calculate_wage_pressure_impact(wage_data)
            wage_data["competitive_wage_levels"] = self._calculate_competitive_wages(wage_data)
            
            wage_data["timestamp"] = datetime.now().isoformat()
            
            return wage_data
            
        except Exception as e:
            logger.error(f"Failed to get wage and earnings data: {str(e)}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    async def get_inflation_and_cost_data(self) -> Dict[str, Any]:
        """Get inflation and cost data impacting small businesses."""
        
        logger.info("Fetching inflation and cost data from BLS")
        
        try:
            current_year = str(datetime.now().year)
            last_year = str(datetime.now().year - 1)
            
            inflation_series = [
                self.series_ids["cpi_all_items"],
                self.series_ids["cpi_food"],
                self.series_ids["cpi_energy"],
                self.series_ids["cpi_services"],
                self.series_ids["ppi_final_demand"],
                self.series_ids["ppi_services"],
                self.series_ids["ppi_goods"]
            ]
            
            response = await self._make_request(inflation_series, last_year, current_year)
            
            inflation_data = self._process_inflation_response(response)
            
            # Calculate small business cost impacts
            inflation_data["input_cost_pressure"] = self._calculate_input_cost_pressure(inflation_data)
            inflation_data["consumer_price_impact"] = self._calculate_consumer_price_impact(inflation_data)
            inflation_data["margin_pressure_score"] = self._calculate_margin_pressure(inflation_data)
            
            inflation_data["timestamp"] = datetime.now().isoformat()
            
            return inflation_data
            
        except Exception as e:
            logger.error(f"Failed to get inflation and cost data: {str(e)}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    async def get_job_market_dynamics(self) -> Dict[str, Any]:
        """Get job market dynamics data (openings, quits, hires)."""
        
        logger.info("Fetching job market dynamics from BLS")
        
        try:
            current_year = str(datetime.now().year)
            job_market_series = [
                self.series_ids["job_openings_total"],
                self.series_ids["job_openings_retail"],
                self.series_ids["job_openings_food_services"],
                self.series_ids["quits_rate"],
                self.series_ids["hires_rate"]
            ]
            
            response = await self._make_request(job_market_series, current_year, current_year)
            
            job_market_data = self._process_job_market_response(response)
            
            # Calculate labor market indicators
            job_market_data["talent_availability"] = self._calculate_talent_availability(job_market_data)
            job_market_data["hiring_difficulty_index"] = self._calculate_hiring_difficulty(job_market_data)
            job_market_data["employee_retention_risk"] = self._calculate_retention_risk(job_market_data)
            
            job_market_data["timestamp"] = datetime.now().isoformat()
            
            return job_market_data
            
        except Exception as e:
            logger.error(f"Failed to get job market dynamics: {str(e)}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    async def get_business_environment_indicators(self) -> Dict[str, Any]:
        """Get overall business environment indicators from BLS data."""
        
        logger.info("Fetching business environment indicators")
        
        try:
            # Gather data from multiple BLS endpoints
            employment_data, wage_data, inflation_data, job_market_data = await asyncio.gather(
                self.get_current_employment_data(),
                self.get_wage_and_earnings_data(),
                self.get_inflation_and_cost_data(),
                self.get_job_market_dynamics(),
                return_exceptions=True
            )
            
            # Combine all indicators
            business_environment = {
                "employment_environment": employment_data if not isinstance(employment_data, Exception) else None,
                "wage_environment": wage_data if not isinstance(wage_data, Exception) else None,
                "cost_environment": inflation_data if not isinstance(inflation_data, Exception) else None,
                "job_market_environment": job_market_data if not isinstance(job_market_data, Exception) else None
            }
            
            # Calculate overall business environment score
            business_environment["overall_business_climate"] = self._calculate_overall_business_climate(business_environment)
            business_environment["small_business_favorability"] = self._calculate_small_business_favorability(business_environment)
            business_environment["key_trends"] = self._identify_key_trends(business_environment)
            
            business_environment["timestamp"] = datetime.now().isoformat()
            
            return business_environment
            
        except Exception as e:
            logger.error(f"Failed to get business environment indicators: {str(e)}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    def _process_employment_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Process employment data response from BLS."""
        
        employment_data = {}
        
        if "Results" not in response or "series" not in response["Results"]:
            return employment_data
        
        for series in response["Results"]["series"]:
            series_id = series["seriesID"]
            series_data = series.get("data", [])
            
            if not series_data:
                continue
            
            # Get latest value
            latest_data = series_data[0]
            latest_value = self._parse_value(latest_data.get("value"))
            
            # Map series ID to readable name
            series_name = self._get_series_name(series_id)
            if series_name:
                employment_data[series_name] = {
                    "current_value": latest_value,
                    "period": latest_data.get("period"),
                    "year": latest_data.get("year"),
                    "series_id": series_id
                }
                
                # Calculate month-over-month change if available
                if len(series_data) > 1:
                    previous_value = self._parse_value(series_data[1].get("value"))
                    if previous_value and latest_value:
                        month_change = ((latest_value - previous_value) / previous_value) * 100
                        employment_data[series_name]["month_over_month_change"] = month_change
        
        return employment_data
    
    def _process_sector_employment_response(self, response: Dict[str, Any], 
                                          sector: str, relevant_series: List[str]) -> Dict[str, Any]:
        """Process sector-specific employment data."""
        
        sector_data = {
            "sector": sector,
            "employment_series": {},
            "sector_employment_total": 0,
            "employment_growth_rate": 0
        }
        
        if "Results" not in response or "series" not in response["Results"]:
            return sector_data
        
        total_employment = 0
        growth_rates = []
        
        for series in response["Results"]["series"]:
            series_id = series["seriesID"]
            series_data = series.get("data", [])
            
            if not series_data:
                continue
            
            series_name = self._get_series_name(series_id)
            if not series_name:
                continue
            
            # Get latest value and calculate trends
            latest_value = self._parse_value(series_data[0].get("value"))
            if latest_value:
                total_employment += latest_value
                
                # Calculate year-over-year growth
                year_ago_data = [d for d in series_data if d.get("year") == str(int(series_data[0]["year"]) - 1) 
                               and d.get("period") == series_data[0]["period"]]
                
                if year_ago_data:
                    year_ago_value = self._parse_value(year_ago_data[0].get("value"))
                    if year_ago_value and year_ago_value > 0:
                        growth_rate = ((latest_value - year_ago_value) / year_ago_value) * 100
                        growth_rates.append(growth_rate)
                
                sector_data["employment_series"][series_name] = {
                    "current_value": latest_value,
                    "period": series_data[0].get("period"),
                    "year": series_data[0].get("year")
                }
        
        sector_data["sector_employment_total"] = total_employment
        if growth_rates:
            sector_data["employment_growth_rate"] = sum(growth_rates) / len(growth_rates)
        
        return sector_data
    
    def _process_wage_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Process wage and earnings data response."""
        
        wage_data = {}
        
        if "Results" not in response or "series" not in response["Results"]:
            return wage_data
        
        for series in response["Results"]["series"]:
            series_id = series["seriesID"]
            series_data = series.get("data", [])
            
            if not series_data:
                continue
            
            latest_value = self._parse_value(series_data[0].get("value"))
            series_name = self._get_series_name(series_id)
            
            if series_name and latest_value:
                wage_data[series_name] = {
                    "current_hourly_rate": latest_value,
                    "period": series_data[0].get("period"),
                    "year": series_data[0].get("year")
                }
                
                # Calculate wage growth
                if len(series_data) > 12:  # Year-over-year comparison
                    year_ago_value = self._parse_value(series_data[12].get("value"))
                    if year_ago_value and year_ago_value > 0:
                        wage_growth = ((latest_value - year_ago_value) / year_ago_value) * 100
                        wage_data[series_name]["annual_wage_growth"] = wage_growth
        
        return wage_data
    
    def _process_inflation_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Process inflation and cost data response."""
        
        inflation_data = {}
        
        if "Results" not in response or "series" not in response["Results"]:
            return inflation_data
        
        for series in response["Results"]["series"]:
            series_id = series["seriesID"]
            series_data = series.get("data", [])
            
            if not series_data or len(series_data) < 2:
                continue
            
            latest_value = self._parse_value(series_data[0].get("value"))
            year_ago_value = None
            
            # Find year-ago value
            latest_period = series_data[0].get("period")
            latest_year = int(series_data[0].get("year"))
            
            for data_point in series_data:
                if (data_point.get("period") == latest_period and 
                    int(data_point.get("year")) == latest_year - 1):
                    year_ago_value = self._parse_value(data_point.get("value"))
                    break
            
            series_name = self._get_series_name(series_id)
            
            if series_name and latest_value:
                inflation_data[series_name] = {
                    "current_index": latest_value,
                    "period": series_data[0].get("period"),
                    "year": series_data[0].get("year")
                }
                
                # Calculate inflation rate
                if year_ago_value and year_ago_value > 0:
                    inflation_rate = ((latest_value - year_ago_value) / year_ago_value) * 100
                    inflation_data[series_name]["annual_inflation_rate"] = inflation_rate
        
        return inflation_data
    
    def _process_job_market_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Process job market dynamics response."""
        
        job_market_data = {}
        
        if "Results" not in response or "series" not in response["Results"]:
            return job_market_data
        
        for series in response["Results"]["series"]:
            series_id = series["seriesID"]
            series_data = series.get("data", [])
            
            if not series_data:
                continue
            
            latest_value = self._parse_value(series_data[0].get("value"))
            series_name = self._get_series_name(series_id)
            
            if series_name and latest_value:
                job_market_data[series_name] = {
                    "current_value": latest_value,
                    "period": series_data[0].get("period"),
                    "year": series_data[0].get("year")
                }
                
                # Calculate trend
                if len(series_data) > 1:
                    previous_value = self._parse_value(series_data[1].get("value"))
                    if previous_value and previous_value > 0:
                        month_change = ((latest_value - previous_value) / previous_value) * 100
                        job_market_data[series_name]["month_over_month_change"] = month_change
        
        return job_market_data
    
    def _get_series_name(self, series_id: str) -> Optional[str]:
        """Map BLS series ID to readable name."""
        
        id_to_name = {v: k for k, v in self.series_ids.items()}
        return id_to_name.get(series_id)
    
    def _parse_value(self, value_str: str) -> Optional[float]:
        """Parse BLS value string to float."""
        
        if not value_str or value_str == "":
            return None
        
        try:
            return float(value_str)
        except (ValueError, TypeError):
            return None
    
    def _calculate_small_business_employment_impact(self, employment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate employment impact on small businesses."""
        
        impact = {
            "talent_availability": "neutral",
            "wage_pressure": "neutral",
            "overall_impact": "neutral"
        }
        
        # Analyze unemployment rate
        unemployment_data = employment_data.get("unemployment_rate", {})
        unemployment_rate = unemployment_data.get("current_value")
        
        if unemployment_rate:
            if unemployment_rate < 4.0:
                impact["talent_availability"] = "tight"
                impact["wage_pressure"] = "high"
            elif unemployment_rate > 6.0:
                impact["talent_availability"] = "abundant"
                impact["wage_pressure"] = "low"
            else:
                impact["talent_availability"] = "balanced"
                impact["wage_pressure"] = "moderate"
        
        # Overall impact assessment
        if impact["talent_availability"] == "tight":
            impact["overall_impact"] = "challenging"
        elif impact["talent_availability"] == "abundant":
            impact["overall_impact"] = "favorable"
        
        return impact
    
    def _calculate_employment_momentum(self, employment_data: Dict[str, Any]) -> float:
        """Calculate employment momentum score."""
        
        momentum_score = 50  # Neutral baseline
        
        # Check month-over-month changes
        private_employment = employment_data.get("private_employment", {})
        mom_change = private_employment.get("month_over_month_change")
        
        if mom_change:
            # Convert percentage change to momentum points
            momentum_score += mom_change * 10  # Scale factor
        
        return max(0, min(100, momentum_score))
    
    def _calculate_labor_market_tightness(self, employment_data: Dict[str, Any]) -> float:
        """Calculate labor market tightness score."""
        
        tightness_score = 50  # Neutral baseline
        
        unemployment_data = employment_data.get("unemployment_rate", {})
        unemployment_rate = unemployment_data.get("current_value")
        
        if unemployment_rate:
            # Lower unemployment = tighter market
            tightness_score = 100 - (unemployment_rate * 10)
        
        return max(0, min(100, tightness_score))
    
    def _calculate_sector_health_score(self, sector_data: Dict[str, Any]) -> float:
        """Calculate sector health score."""
        
        health_score = 50  # Neutral baseline
        
        growth_rate = sector_data.get("employment_growth_rate", 0)
        
        # Positive growth improves health score
        health_score += growth_rate * 5  # Scale factor
        
        return max(0, min(100, health_score))
    
    def _calculate_employment_trend(self, sector_data: Dict[str, Any]) -> str:
        """Calculate employment trend direction."""
        
        growth_rate = sector_data.get("employment_growth_rate", 0)
        
        if growth_rate > 2.0:
            return "strong_growth"
        elif growth_rate > 0.5:
            return "moderate_growth"
        elif growth_rate > -0.5:
            return "stable"
        elif growth_rate > -2.0:
            return "moderate_decline"
        else:
            return "significant_decline"
    
    async def _calculate_wage_competitiveness(self, sector: str) -> Dict[str, Any]:
        """Calculate wage competitiveness for sector."""
        
        # This would compare sector wages to national averages
        # Simplified implementation
        return {
            "competitive_position": "average",
            "wage_premium": 0.0,
            "talent_retention_risk": "moderate"
        }
    
    def _calculate_wage_inflation(self, wage_data: Dict[str, Any]) -> float:
        """Calculate overall wage inflation rate."""
        
        wage_growth_rates = []
        
        for series_name, data in wage_data.items():
            growth_rate = data.get("annual_wage_growth")
            if growth_rate:
                wage_growth_rates.append(growth_rate)
        
        if wage_growth_rates:
            return sum(wage_growth_rates) / len(wage_growth_rates)
        
        return 0.0
    
    def _calculate_wage_pressure_impact(self, wage_data: Dict[str, Any]) -> str:
        """Calculate wage pressure impact on small businesses."""
        
        avg_wage_growth = self._calculate_wage_inflation(wage_data)
        
        if avg_wage_growth > 5.0:
            return "high_pressure"
        elif avg_wage_growth > 3.0:
            return "moderate_pressure"
        elif avg_wage_growth > 0:
            return "low_pressure"
        else:
            return "deflationary"
    
    def _calculate_competitive_wages(self, wage_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate competitive wage levels by sector."""
        
        competitive_wages = {}
        
        for series_name, data in wage_data.items():
            hourly_rate = data.get("current_hourly_rate")
            if hourly_rate:
                # Estimate competitive wage (10% above current)
                competitive_wages[series_name] = hourly_rate * 1.1
        
        return competitive_wages
    
    def _calculate_input_cost_pressure(self, inflation_data: Dict[str, Any]) -> float:
        """Calculate input cost pressure from PPI data."""
        
        ppi_data = inflation_data.get("ppi_final_demand", {})
        ppi_inflation = ppi_data.get("annual_inflation_rate", 0)
        
        # Convert to pressure score
        if ppi_inflation > 5.0:
            return 80  # High pressure
        elif ppi_inflation > 3.0:
            return 60  # Moderate pressure
        elif ppi_inflation > 0:
            return 40  # Low pressure
        else:
            return 20  # Deflationary pressure
    
    def _calculate_consumer_price_impact(self, inflation_data: Dict[str, Any]) -> float:
        """Calculate consumer price impact on demand."""
        
        cpi_data = inflation_data.get("cpi_all_items", {})
        cpi_inflation = cpi_data.get("annual_inflation_rate", 0)
        
        # Higher inflation reduces consumer purchasing power
        if cpi_inflation > 5.0:
            return -20  # Negative impact on demand
        elif cpi_inflation > 3.0:
            return -10  # Moderate negative impact
        elif cpi_inflation > 0:
            return -5   # Small negative impact
        else:
            return 5    # Positive impact (deflation)
    
    def _calculate_margin_pressure(self, inflation_data: Dict[str, Any]) -> float:
        """Calculate margin pressure score."""
        
        input_pressure = self._calculate_input_cost_pressure(inflation_data)
        consumer_impact = self._calculate_consumer_price_impact(inflation_data)
        
        # Margin pressure = input costs rising faster than ability to raise prices
        margin_pressure = input_pressure + abs(consumer_impact)
        
        return min(100, margin_pressure)
    
    def _calculate_talent_availability(self, job_market_data: Dict[str, Any]) -> str:
        """Calculate talent availability assessment."""
        
        job_openings = job_market_data.get("job_openings_total", {})
        quits_rate = job_market_data.get("quits_rate", {})
       
        openings_value = job_openings.get("current_value", 0)
        quits_value = quits_rate.get("current_value", 0)
       
        # High job openings + high quits = tight talent market
        if openings_value > 7000 and quits_value > 2.5:  # Thousands of openings, % quits
            return "very_tight"
        elif openings_value > 6000 and quits_value > 2.0:
            return "tight"
        elif openings_value > 5000:
            return "balanced"
        else:
           return "abundant"
   
    def _calculate_hiring_difficulty(self, job_market_data: Dict[str, Any]) -> float:
        """Calculate hiring difficulty index."""
        
        job_openings = job_market_data.get("job_openings_total", {})
        hires_rate = job_market_data.get("hires_rate", {})
        
        openings_value = job_openings.get("current_value", 0)
        hires_value = hires_rate.get("current_value", 0)
        
        # Higher openings relative to hires = more difficulty
        if hires_value > 0:
            difficulty_ratio = openings_value / (hires_value * 1000)  # Scale hires rate
            return min(100, difficulty_ratio * 10)
        
        return 50  # Neutral if no data
    
    def _calculate_retention_risk(self, job_market_data: Dict[str, Any]) -> str:
        """Calculate employee retention risk."""
        
        quits_rate = job_market_data.get("quits_rate", {})
        quits_value = quits_rate.get("current_value", 0)
        quits_change = quits_rate.get("month_over_month_change", 0)
        
        # High quits rate + increasing = high retention risk
        if quits_value > 3.0 and quits_change > 0:
            return "very_high"
        elif quits_value > 2.5:
            return "high"
        elif quits_value > 2.0:
            return "moderate"
        else:
            return "low"
    
    def _calculate_overall_business_climate(self, business_environment: Dict[str, Any]) -> float:
        """Calculate overall business climate score."""
        
        climate_score = 50  # Neutral baseline
        
        # Employment environment (25% weight)
        employment_env = business_environment.get("employment_environment")
        if employment_env and "employment_momentum" in employment_env:
            employment_score = employment_env["employment_momentum"]
            climate_score += (employment_score - 50) * 0.25
        
        # Wage environment (25% weight) 
        wage_env = business_environment.get("wage_environment")
        if wage_env:
            # Lower wage inflation is better for small business
            wage_inflation = self._calculate_wage_inflation(wage_env)
            wage_score = max(0, 100 - wage_inflation * 10)  # Inverse relationship
            climate_score += (wage_score - 50) * 0.25
        
        # Cost environment (30% weight)
        cost_env = business_environment.get("cost_environment")
        if cost_env:
            margin_pressure = self._calculate_margin_pressure(cost_env)
            cost_score = max(0, 100 - margin_pressure)  # Inverse relationship
            climate_score += (cost_score - 50) * 0.30
        
        # Job market environment (20% weight)
        job_market_env = business_environment.get("job_market_environment")
        if job_market_env:
            hiring_difficulty = self._calculate_hiring_difficulty(job_market_env)
            job_market_score = max(0, 100 - hiring_difficulty)  # Inverse relationship
            climate_score += (job_market_score - 50) * 0.20
        
        return max(0, min(100, climate_score))
    
    def _calculate_small_business_favorability(self, business_environment: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate small business favorability assessment."""
        
        overall_score = self._calculate_overall_business_climate(business_environment)
        
        favorability = {
            "overall_score": overall_score,
            "assessment": "neutral",
            "key_challenges": [],
            "key_advantages": []
        }
        
        # Determine overall assessment
        if overall_score >= 70:
            favorability["assessment"] = "highly_favorable"
        elif overall_score >= 60:
            favorability["assessment"] = "favorable"
        elif overall_score >= 40:
            favorability["assessment"] = "neutral"
        elif overall_score >= 30:
            favorability["assessment"] = "challenging"
        else:
            favorability["assessment"] = "very_challenging"
        
        # Identify key challenges and advantages
        employment_env = business_environment.get("employment_environment", {})
        wage_env = business_environment.get("wage_environment", {})
        cost_env = business_environment.get("cost_environment", {})
        job_market_env = business_environment.get("job_market_environment", {})
        
        # Challenges
        if wage_env and self._calculate_wage_inflation(wage_env) > 5.0:
            favorability["key_challenges"].append("High wage inflation pressures")
        
        if cost_env and self._calculate_margin_pressure(cost_env) > 70:
            favorability["key_challenges"].append("Significant input cost pressures")
        
        if job_market_env and self._calculate_hiring_difficulty(job_market_env) > 70:
            favorability["key_challenges"].append("Difficulty finding qualified workers")
        
        # Advantages
        unemployment_data = employment_env.get("unemployment_rate", {})
        if unemployment_data.get("current_value", 0) > 5.0:
            favorability["key_advantages"].append("Abundant talent pool available")
        
        if employment_env.get("employment_momentum", 50) > 60:
            favorability["key_advantages"].append("Strong employment growth momentum")
        
        return favorability
    
    def _identify_key_trends(self, business_environment: Dict[str, Any]) -> List[str]:
        """Identify key trends affecting small businesses."""
        
        trends = []
        
        employment_env = business_environment.get("employment_environment", {})
        wage_env = business_environment.get("wage_environment", {})
        cost_env = business_environment.get("cost_environment", {})
        job_market_env = business_environment.get("job_market_environment", {})
        
        # Employment trends
        if employment_env.get("employment_momentum", 50) > 60:
            trends.append("Strong job creation momentum supporting consumer spending")
        elif employment_env.get("employment_momentum", 50) < 40:
            trends.append("Weakening employment growth may impact consumer demand")
        
        # Wage trends
        wage_inflation = self._calculate_wage_inflation(wage_env) if wage_env else 0
        if wage_inflation > 5.0:
            trends.append("Accelerating wage growth increasing labor costs")
        elif wage_inflation < 2.0:
            trends.append("Moderate wage growth helping control labor costs")
        
        # Cost trends
        if cost_env:
            input_pressure = self._calculate_input_cost_pressure(cost_env)
            if input_pressure > 70:
                trends.append("Rising input costs pressuring business margins")
            elif input_pressure < 30:
                trends.append("Stable input costs supporting profit margins")
        
        # Labor market trends
        if job_market_env:
            talent_availability = self._calculate_talent_availability(job_market_env)
            if talent_availability in ["very_tight", "tight"]:
                trends.append("Tight labor market increasing competition for workers")
            elif talent_availability == "abundant":
                trends.append("Ample labor supply supporting business expansion")
        
        return trends[:5]  # Return top 5 trends
    
    async def get_regional_employment_data(self, state_code: str = None, metro_area: str = None) -> Dict[str, Any]:
        """Get regional employment data for specific states or metro areas."""
        
        logger.info(f"Fetching regional employment data for state: {state_code}, metro: {metro_area}")
        
        try:
            # Regional series IDs (state/metro specific)
            regional_series = []
            
            if state_code:
                # State-level unemployment rate
                state_unemployment_id = f"LASST{state_code}0000000000003"  # State unemployment rate
                regional_series.append(state_unemployment_id)
            
            if metro_area:
                # Metro area unemployment (would need specific metro area codes)
                # This is a simplified example
                metro_unemployment_id = f"LAUMT{metro_area}0000000003"
                regional_series.append(metro_unemployment_id)
            
            if not regional_series:
                return {"error": "No regional series specified"}
            
            current_year = str(datetime.now().year)
            response = await self._make_request(regional_series, current_year, current_year)
            
            regional_data = self._process_regional_response(response, state_code, metro_area)
            regional_data["timestamp"] = datetime.now().isoformat()
            
            return regional_data
            
        except Exception as e:
            logger.error(f"Failed to get regional employment data: {str(e)}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    def _process_regional_response(self, response: Dict[str, Any], state_code: str, metro_area: str) -> Dict[str, Any]:
        """Process regional employment data response."""
        
        regional_data = {
            "state_code": state_code,
            "metro_area": metro_area,
            "regional_indicators": {}
        }
        
        if "Results" not in response or "series" not in response["Results"]:
            return regional_data
        
        for series in response["Results"]["series"]:
            series_id = series["seriesID"]
            series_data = series.get("data", [])
            
            if not series_data:
                continue
               
            latest_value = self._parse_value(series_data[0].get("value"))
            
            if latest_value:
                # Determine indicator type from series ID
                if "unemployment" in series_id.lower() or series_id.endswith("003"):
                    indicator_name = "unemployment_rate"
                else:
                    indicator_name = f"indicator_{series_id[-3:]}"
                
                regional_data["regional_indicators"][indicator_name] = {
                    "current_value": latest_value,
                    "period": series_data[0].get("period"),
                    "year": series_data[0].get("year"),
                    "series_id": series_id
                }
        
        return regional_data
    
    async def get_industry_specific_data(self, naics_code: str) -> Dict[str, Any]:
        """Get industry-specific employment and wage data by NAICS code."""
        
        logger.info(f"Fetching industry-specific data for NAICS {naics_code}")
        
        # Map NAICS codes to BLS industry series
        naics_to_series = {
            "44": "retail_employment",       # Retail Trade
            "45": "retail_employment",
            "72": "food_services_employment", # Food Services
            "54": "professional_services_employment", # Professional Services
            "23": "construction_employment",  # Construction
            "31": "manufacturing_employment", # Manufacturing
            "32": "manufacturing_employment",
            "33": "manufacturing_employment"
        }
        
        # Use first 2 digits of NAICS code
        naics_sector = naics_code[:2]
        series_name = naics_to_series.get(naics_sector)
        
        if not series_name:
            return {"error": f"No data available for NAICS {naics_code}"}
        
        try:
            # Get both employment and wage data for the industry
            current_year = str(datetime.now().year)
            last_year = str(datetime.now().year - 1)
            
            industry_series = [self.series_ids[series_name]]
            
            # Add wage series if available
            wage_series_name = series_name.replace("employment", "hourly_earnings")
            if wage_series_name in self.series_ids:
                industry_series.append(self.series_ids[wage_series_name])
            
            response = await self._make_request(industry_series, last_year, current_year)
            
            industry_data = {
                "naics_code": naics_code,
                "industry_series": self._process_employment_response(response),
                "industry_health": self._assess_industry_health(response),
                "competitive_position": self._assess_competitive_position(naics_sector),
                "timestamp": datetime.now().isoformat()
            }
            
            return industry_data
            
        except Exception as e:
            logger.error(f"Failed to get industry data for NAICS {naics_code}: {str(e)}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    def _assess_industry_health(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Assess overall health of an industry."""
        
        health_assessment = {
            "employment_trend": "stable",
            "wage_trend": "stable",
            "overall_health": "stable",
            "growth_momentum": 50
        }
        
        if "Results" not in response or "series" not in response["Results"]:
            return health_assessment
        
        employment_growth_rates = []
        wage_growth_rates = []
        
        for series in response["Results"]["series"]:
            series_data = series.get("data", [])
            if len(series_data) < 12:  # Need at least 12 months for YoY comparison
                continue
               
            latest_value = self._parse_value(series_data[0].get("value"))
            year_ago_value = self._parse_value(series_data[12].get("value"))
            
            if latest_value and year_ago_value and year_ago_value > 0:
                growth_rate = ((latest_value - year_ago_value) / year_ago_value) * 100
                
                series_id = series["seriesID"]
                if any(emp_id in series_id for emp_id in ["CES", "employment"]):
                    employment_growth_rates.append(growth_rate)
                elif "earnings" in series_id:
                    wage_growth_rates.append(growth_rate)
        
        # Assess employment trend
        if employment_growth_rates:
            avg_emp_growth = sum(employment_growth_rates) / len(employment_growth_rates)
            if avg_emp_growth > 2.0:
                health_assessment["employment_trend"] = "strong_growth"
            elif avg_emp_growth > 0.5:
                health_assessment["employment_trend"] = "moderate_growth"
            elif avg_emp_growth < -1.0:
                health_assessment["employment_trend"] = "declining"
            
            health_assessment["growth_momentum"] = min(100, max(0, 50 + avg_emp_growth * 10))
        
        # Assess wage trend
        if wage_growth_rates:
            avg_wage_growth = sum(wage_growth_rates) / len(wage_growth_rates)
            if avg_wage_growth > 4.0:
                health_assessment["wage_trend"] = "rapid_growth"
            elif avg_wage_growth > 2.0:
                health_assessment["wage_trend"] = "healthy_growth"
            elif avg_wage_growth < 0:
                health_assessment["wage_trend"] = "declining"
        
        # Overall health assessment
        if (health_assessment["employment_trend"] in ["strong_growth", "moderate_growth"] and 
            health_assessment["wage_trend"] in ["rapid_growth", "healthy_growth"]):
            health_assessment["overall_health"] = "strong"
        elif health_assessment["employment_trend"] == "declining":
            health_assessment["overall_health"] = "weak"
        
        return health_assessment
    
    def _assess_competitive_position(self, naics_sector: str) -> Dict[str, Any]:
        """Assess competitive position of industry sector."""
        
        # Industry competitive characteristics
        sector_characteristics = {
            "44": {"competition": "high", "barriers": "low", "consolidation": "fragmented"},
            "45": {"competition": "high", "barriers": "low", "consolidation": "fragmented"},
            "72": {"competition": "very_high", "barriers": "low", "consolidation": "fragmented"},
            "54": {"competition": "medium", "barriers": "medium", "consolidation": "fragmented"},
            "23": {"competition": "high", "barriers": "medium", "consolidation": "fragmented"},
            "31": {"competition": "medium", "barriers": "high", "consolidation": "consolidated"},
            "32": {"competition": "medium", "barriers": "high", "consolidation": "consolidated"},
            "33": {"competition": "medium", "barriers": "high", "consolidation": "consolidated"}
        }
        
        characteristics = sector_characteristics.get(naics_sector, {
            "competition": "medium",
            "barriers": "medium", 
            "consolidation": "fragmented"
        })
        
        return {
            "competition_level": characteristics["competition"],
            "barriers_to_entry": characteristics["barriers"],
            "market_structure": characteristics["consolidation"],
            "small_business_viability": self._assess_small_business_viability(characteristics)
        }
    
    def _assess_small_business_viability(self, characteristics: Dict[str, str]) -> str:
        """Assess viability for small businesses in industry."""
        
        competition = characteristics["competition"]
        barriers = characteristics["barriers"]
        structure = characteristics["consolidation"]
        
        # High competition + low barriers + fragmented = challenging but viable
        if competition == "very_high" and barriers == "low":
            return "challenging"
        elif competition == "high" and barriers == "medium":
            return "moderate"
        elif barriers == "high":
            return "difficult"
        else:
            return "favorable"
    
    async def get_business_cycle_indicators(self) -> Dict[str, Any]:
        """Get business cycle indicators from BLS data."""
        
        logger.info("Fetching business cycle indicators")
        
        try:
            current_year = str(datetime.now().year)
            last_year = str(datetime.now().year - 1)
            
            # Key business cycle series
            cycle_series = [
                self.series_ids["total_nonfarm_employment"],
                self.series_ids["unemployment_rate"],
                self.series_ids["average_hourly_earnings"],
                self.series_ids["cpi_all_items"],
                self.series_ids["ppi_final_demand"]
            ]
            
            response = await self._make_request(cycle_series, last_year, current_year)
            
            cycle_data = {
                "cycle_indicators": self._process_employment_response(response),
                "cycle_phase": self._determine_business_cycle_phase(response),
                "leading_indicators": self._calculate_leading_indicators(response),
                "small_business_outlook": self._assess_small_business_cycle_outlook(response),
                "timestamp": datetime.now().isoformat()
            }
            
            return cycle_data
            
        except Exception as e:
            logger.error(f"Failed to get business cycle indicators: {str(e)}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    def _determine_business_cycle_phase(self, response: Dict[str, Any]) -> str:
        """Determine current business cycle phase."""
        
        if "Results" not in response or "series" not in response["Results"]:
            return "unknown"
        
        employment_growth = 0
        unemployment_change = 0
        
        for series in response["Results"]["series"]:
            series_id = series["seriesID"]
            series_data = series.get("data", [])
            
            if len(series_data) < 2:
                continue
               
            latest_value = self._parse_value(series_data[0].get("value"))
            previous_value = self._parse_value(series_data[1].get("value"))
            
            if not latest_value or not previous_value:
                continue
               
            if series_id == self.series_ids["total_nonfarm_employment"]:
                employment_growth = ((latest_value - previous_value) / previous_value) * 100
            elif series_id == self.series_ids["unemployment_rate"]:
                unemployment_change = latest_value - previous_value
        
        # Simple business cycle determination
        if employment_growth > 0.2 and unemployment_change < 0:
            return "expansion"
        elif employment_growth < -0.1 and unemployment_change > 0:
            return "recession"
        elif employment_growth > 0 and unemployment_change <= 0:
            return "recovery"
        elif employment_growth <= 0 and unemployment_change >= 0:
            return "contraction"
        else:
            return "transition"
    
    def _calculate_leading_indicators(self, response: Dict[str, Any]) -> Dict[str, float]:
        """Calculate leading economic indicators."""
        
        leading_indicators = {
            "employment_momentum": 50,
            "wage_pressure": 50,
            "cost_pressure": 50
        }
        
        if "Results" not in response or "series" not in response["Results"]:
            return leading_indicators
        
        for series in response["Results"]["series"]:
            series_id = series["seriesID"]
            series_data = series.get("data", [])
            
            if len(series_data) < 3:
                continue
               
            # Calculate 3-month momentum
            recent_values = [self._parse_value(data.get("value")) for data in series_data[:3]]
            recent_values = [v for v in recent_values if v is not None]
            
            if len(recent_values) < 3:
                continue
               
            momentum = ((recent_values[0] - recent_values[2]) / recent_values[2]) * 100
            
            if series_id == self.series_ids["total_nonfarm_employment"]:
                leading_indicators["employment_momentum"] = min(100, max(0, 50 + momentum * 20))
            elif series_id == self.series_ids["average_hourly_earnings"]:
                leading_indicators["wage_pressure"] = min(100, max(0, 50 + momentum * 10))
            elif series_id == self.series_ids["ppi_final_demand"]:
                leading_indicators["cost_pressure"] = min(100, max(0, 50 + momentum * 5))
        
        return leading_indicators
    
    def _assess_small_business_cycle_outlook(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Assess small business outlook based on business cycle."""
        
        cycle_phase = self._determine_business_cycle_phase(response)
        leading_indicators = self._calculate_leading_indicators(response)
        
        outlook = {
            "cycle_phase": cycle_phase,
            "outlook_direction": "neutral",
            "confidence_level": 50,
            "key_opportunities": [],
            "key_risks": []
        }
        
        if cycle_phase == "expansion":
            outlook["outlook_direction"] = "positive"
            outlook["confidence_level"] = 75
            outlook["key_opportunities"] = [
                "Growing consumer demand",
                "Easier access to credit",
                "Expansion opportunities"
            ]
            outlook["key_risks"] = [
                "Rising labor costs",
                "Increased competition"
            ]
        elif cycle_phase == "recession":
            outlook["outlook_direction"] = "negative"
            outlook["confidence_level"] = 25
            outlook["key_opportunities"] = [
                "Lower input costs",
                "Available talent",
                "Market consolidation opportunities"
            ]
            outlook["key_risks"] = [
                "Declining consumer demand",
                "Credit constraints",
                "Cash flow pressures"
            ]
        elif cycle_phase == "recovery":
            outlook["outlook_direction"] = "improving"
            outlook["confidence_level"] = 65
            outlook["key_opportunities"] = [
                "Emerging consumer confidence",
                "Competitive positioning",
                "Investment opportunities"
            ]
            outlook["key_risks"] = [
                "Uncertain recovery pace",
                "Supply chain disruptions"
            ]
        
        return outlook