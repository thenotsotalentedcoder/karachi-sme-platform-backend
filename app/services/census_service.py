"""US Census Bureau service for demographic and business statistics."""

import httpx
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

from app.config import settings

logger = logging.getLogger(__name__)


class CensusService:
    """Service for fetching US demographic and business data from Census Bureau."""
    
    def __init__(self):
        self.api_key = settings.CENSUS_API_KEY
        self.base_url = settings.CENSUS_BASE_URL
        self.rate_limit = settings.CENSUS_RATE_LIMIT
    
    async def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make request to Census API."""
        
        if params is None:
            params = {}
        
        params["key"] = self.api_key
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(f"{self.base_url}/{endpoint}", params=params)
                response.raise_for_status()
                
                data = response.json()
                return data
                
        except httpx.TimeoutException:
            logger.error("Census API timeout")
            raise Exception("Census API request timed out")
        except httpx.HTTPStatusError as e:
            logger.error(f"Census API HTTP error: {e.response.status_code}")
            raise Exception(f"Census API error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"Census API error: {str(e)}")
            raise
    
    async def get_demographic_data(self, location: str) -> Dict[str, Any]:
        """Get demographic data for a location."""
        
        logger.info(f"Fetching demographic data for {location}")
        
        try:
            # Determine geographic level and codes
            geo_info = self._parse_location(location)
            
            if geo_info["level"] == "state":
                return await self._get_state_demographics(geo_info["state_code"])
            elif geo_info["level"] == "county":
                return await self._get_county_demographics(geo_info["state_code"], geo_info["county_code"])
            elif geo_info["level"] == "metro":
                return await self._get_metro_demographics(geo_info["metro_code"])
            else:
                # Default to national data
                return await self._get_national_demographics()
                
        except Exception as e:
            logger.error(f"Failed to get demographic data for {location}: {str(e)}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    def _parse_location(self, location: str) -> Dict[str, Any]:
        """Parse location string to determine geographic level and codes."""
        
        # State name/code mapping
        state_mapping = {
            "california": "06", "ca": "06",
            "texas": "48", "tx": "48", 
            "florida": "12", "fl": "12",
            "new york": "36", "ny": "36",
            "pennsylvania": "42", "pa": "42",
            "illinois": "17", "il": "17",
            "ohio": "39", "oh": "39",
            "georgia": "13", "ga": "13",
            "north carolina": "37", "nc": "37",
            "michigan": "26", "mi": "26"
        }
        
        # Major metro area codes
        metro_mapping = {
            "new york": "35620",
            "los angeles": "31080", 
            "chicago": "16980",
            "dallas": "19100",
            "houston": "26420",
            "washington": "47900",
            "miami": "33100",
            "philadelphia": "37980",
            "atlanta": "12060",
            "phoenix": "38060",
            "boston": "14460",
            "san francisco": "41860",
            "detroit": "19820",
            "seattle": "42660",
            "minneapolis": "33460",
            "san diego": "41740",
            "tampa": "45300",
            "denver": "19740",
            "baltimore": "12580",
            "st louis": "41180"
        }
        
        location_clean = location.lower().strip()
        
        # Check if it's a metro area
        if location_clean in metro_mapping:
            return {
                "level": "metro",
                "metro_code": metro_mapping[location_clean],
                "name": location
            }
        
        # Check if it's a state
        if location_clean in state_mapping:
            return {
                "level": "state", 
                "state_code": state_mapping[location_clean],
                "name": location
            }
        
        # Default to national
        return {"level": "national", "name": "United States"}
    
    async def _get_national_demographics(self) -> Dict[str, Any]:
        """Get national demographic data."""
        
        try:
            # Get population and demographic data from ACS
            params = {
                "get": "B01003_001E,B19013_001E,B25077_001E,B08303_001E",
                "for": "us:1"
            }
            
            data = await self._make_request("2022/acs/acs1", params)
            
            if data and len(data) > 1:
                demographics = data[1]  # Skip header row
                
                return {
                    "geographic_level": "national",
                    "total_population": int(demographics[0]) if demographics[0] not in [None, "-666666666"] else None,
                    "median_household_income": int(demographics[1]) if demographics[1] not in [None, "-666666666"] else None,
                    "median_home_value": int(demographics[2]) if demographics[2] not in [None, "-666666666"] else None,
                    "median_commute_time": float(demographics[3]) if demographics[3] not in [None, "-666666666"] else None,
                    "timestamp": datetime.now().isoformat()
                }
            
            return {"error": "No demographic data available"}
            
        except Exception as e:
            logger.error(f"Failed to get national demographics: {str(e)}")
            return {"error": str(e)}
    
    async def _get_state_demographics(self, state_code: str) -> Dict[str, Any]:
        """Get state-level demographic data."""
        
        try:
            # Get comprehensive state demographics
            params = {
                "get": "B01003_001E,B19013_001E,B25077_001E,B08303_001E,B15003_022E,B15003_001E",
                "for": f"state:{state_code}"
            }
            
            data = await self._make_request("2022/acs/acs1", params)
            
            if data and len(data) > 1:
                demographics = data[1]
                
                # Calculate bachelor's degree percentage
                bachelor_or_higher = int(demographics[4]) if demographics[4] not in [None, "-666666666"] else 0
                total_education = int(demographics[5]) if demographics[5] not in [None, "-666666666"] else 1
                education_rate = (bachelor_or_higher / total_education * 100) if total_education > 0 else 0
                
                return {
                    "geographic_level": "state",
                    "state_code": state_code,
                    "total_population": int(demographics[0]) if demographics[0] not in [None, "-666666666"] else None,
                    "median_household_income": int(demographics[1]) if demographics[1] not in [None, "-666666666"] else None,
                    "median_home_value": int(demographics[2]) if demographics[2] not in [None, "-666666666"] else None,
                    "median_commute_time": float(demographics[3]) if demographics[3] not in [None, "-666666666"] else None,
                    "bachelor_degree_rate": education_rate,
                    "timestamp": datetime.now().isoformat()
                }
            
            return {"error": f"No demographic data available for state {state_code}"}
            
        except Exception as e:
            logger.error(f"Failed to get state demographics for {state_code}: {str(e)}")
            return {"error": str(e)}
    
    async def _get_county_demographics(self, state_code: str, county_code: str) -> Dict[str, Any]:
        """Get county-level demographic data."""
        
        try:
            params = {
                "get": "B01003_001E,B19013_001E,B25077_001E,B08303_001E",
                "for": f"county:{county_code}",
                "in": f"state:{state_code}"
            }
            
            data = await self._make_request("2022/acs/acs1", params)
            
            if data and len(data) > 1:
                demographics = data[1]
                
                return {
                    "geographic_level": "county",
                    "state_code": state_code,
                    "county_code": county_code,
                    "total_population": int(demographics[0]) if demographics[0] not in [None, "-666666666"] else None,
                    "median_household_income": int(demographics[1]) if demographics[1] not in [None, "-666666666"] else None,
                    "median_home_value": int(demographics[2]) if demographics[2] not in [None, "-666666666"] else None,
                    "median_commute_time": float(demographics[3]) if demographics[3] not in [None, "-666666666"] else None,
                    "timestamp": datetime.now().isoformat()
                }
            
            return {"error": f"No demographic data available for county {county_code}"}
            
        except Exception as e:
            logger.error(f"Failed to get county demographics: {str(e)}")
            return {"error": str(e)}
    
    async def _get_metro_demographics(self, metro_code: str) -> Dict[str, Any]:
        """Get metropolitan area demographic data."""
        
        try:
            params = {
                "get": "B01003_001E,B19013_001E,B25077_001E,B08303_001E",
                "for": f"metropolitan statistical area/micropolitan statistical area:{metro_code}"
            }
            
            data = await self._make_request("2022/acs/acs1", params)
            
            if data and len(data) > 1:
                demographics = data[1]
                
                return {
                    "geographic_level": "metro",
                    "metro_code": metro_code,
                    "total_population": int(demographics[0]) if demographics[0] not in [None, "-666666666"] else None,
                    "median_household_income": int(demographics[1]) if demographics[1] not in [None, "-666666666"] else None,
                    "median_home_value": int(demographics[2]) if demographics[2] not in [None, "-666666666"] else None,
                    "median_commute_time": float(demographics[3]) if demographics[3] not in [None, "-666666666"] else None,
                    "timestamp": datetime.now().isoformat()
                }
            
            return {"error": f"No demographic data available for metro {metro_code}"}
            
        except Exception as e:
            logger.error(f"Failed to get metro demographics: {str(e)}")
            return {"error": str(e)}
    
    async def get_business_statistics(self, location: str) -> Dict[str, Any]:
        """Get business statistics for a location."""
        
        logger.info(f"Fetching business statistics for {location}")
        
        try:
            geo_info = self._parse_location(location)
            
            if geo_info["level"] == "state":
                return await self._get_state_business_stats(geo_info["state_code"])
            elif geo_info["level"] == "metro":
                return await self._get_metro_business_stats(geo_info["metro_code"])
            else:
                return await self._get_national_business_stats()
                
        except Exception as e:
            logger.error(f"Failed to get business statistics for {location}: {str(e)}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    async def _get_national_business_stats(self) -> Dict[str, Any]:
        """Get national business statistics."""
        
        try:
            # Get business data from Economic Census or County Business Patterns
            # This is a simplified version - actual implementation would use specific Census business APIs
            
            return {
                "geographic_level": "national",
                "total_establishments": 6200000,  # Approximate US small business count
                "total_employment": 47000000,     # Small business employment
                "establishments_by_size": {
                    "1_4_employees": 3800000,
                    "5_9_employees": 1200000,
                    "10_19_employees": 700000,
                    "20_99_employees": 450000,
                    "100_499_employees": 50000
                },
                "establishments_by_sector": await self._get_sector_breakdown_national(),
                "annual_payroll": 1900000000000,  # $1.9 trillion
                "revenue_estimate": 5800000000000,  # $5.8 trillion
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to get national business stats: {str(e)}")
            return {"error": str(e)}
    
    async def _get_state_business_stats(self, state_code: str) -> Dict[str, Any]:
        """Get state business statistics."""
        
        try:
            # State business statistics
            # This would use actual Census Bureau business data APIs
            
            state_multipliers = {
                "06": 0.12,  # California - 12% of US businesses
                "48": 0.09,  # Texas - 9%
                "12": 0.07,  # Florida - 7%
                "36": 0.08,  # New York - 8%
                "42": 0.04,  # Pennsylvania - 4%
            }
            
            multiplier = state_multipliers.get(state_code, 0.02)  # Default 2%
            
            return {
                "geographic_level": "state",
                "state_code": state_code,
                "total_establishments": int(6200000 * multiplier),
                "total_employment": int(47000000 * multiplier),
                "establishments_by_size": {
                    "1_4_employees": int(3800000 * multiplier),
                    "5_9_employees": int(1200000 * multiplier),
                    "10_19_employees": int(700000 * multiplier),
                    "20_99_employees": int(450000 * multiplier),
                    "100_499_employees": int(50000 * multiplier)
                    },
               "establishments_by_sector": await self._get_sector_breakdown_state(state_code),
               "annual_payroll": int(1900000000000 * multiplier),
               "revenue_estimate": int(5800000000000 * multiplier),
               "timestamp": datetime.now().isoformat()
           }
           
        except Exception as e:
            logger.error(f"Failed to get state business stats for {state_code}: {str(e)}")
            return {"error": str(e)}
   
    async def _get_metro_business_stats(self, metro_code: str) -> Dict[str, Any]:
        """Get metropolitan area business statistics."""
        
        try:
            # Metro area business multipliers based on economic size
            metro_multipliers = {
                "35620": 0.08,  # New York metro - 8% of US businesses
                "31080": 0.06,  # Los Angeles - 6%
                "16980": 0.04,  # Chicago - 4%
                "19100": 0.03,  # Dallas - 3%
                "26420": 0.03,  # Houston - 3%
                "47900": 0.03,  # Washington DC - 3%
                "33100": 0.02,  # Miami - 2%
                "37980": 0.03,  # Philadelphia - 3%
                "12060": 0.02,  # Atlanta - 2%
                "38060": 0.02,  # Phoenix - 2%
            }
            
            multiplier = metro_multipliers.get(metro_code, 0.01)  # Default 1%
            
            return {
                "geographic_level": "metro",
                "metro_code": metro_code,
                "total_establishments": int(6200000 * multiplier),
                "total_employment": int(47000000 * multiplier),
                "establishments_by_size": {
                    "1_4_employees": int(3800000 * multiplier),
                    "5_9_employees": int(1200000 * multiplier),
                    "10_19_employees": int(700000 * multiplier),
                    "20_99_employees": int(450000 * multiplier),
                    "100_499_employees": int(50000 * multiplier)
                },
                "establishments_by_sector": await self._get_sector_breakdown_metro(metro_code),
                "annual_payroll": int(1900000000000 * multiplier),
                "revenue_estimate": int(5800000000000 * multiplier),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to get metro business stats for {metro_code}: {str(e)}")
            return {"error": str(e)}
    
    async def _get_sector_breakdown_national(self) -> Dict[str, int]:
        """Get national business count by sector."""
        
        return {
            "retail_trade": 1050000,
            "professional_services": 850000,
            "food_services": 660000,
            "construction": 730000,
            "healthcare": 680000,
            "real_estate": 430000,
            "manufacturing": 250000,
            "transportation": 230000,
            "finance_insurance": 280000,
            "information": 120000,
            "other_services": 540000,
            "arts_entertainment": 140000,
            "educational_services": 80000,
            "utilities": 6000,
            "mining": 24000,
            "management_companies": 48000,
            "administrative_support": 380000,
            "wholesale_trade": 420000
        }
    
    async def _get_sector_breakdown_state(self, state_code: str) -> Dict[str, int]:
        """Get state business count by sector."""
        
        # State-specific sector distributions
        state_multipliers = {
            "06": 0.12,  # California
            "48": 0.09,  # Texas
            "12": 0.07,  # Florida
            "36": 0.08,  # New York
            "42": 0.04,  # Pennsylvania
        }
        
        multiplier = state_multipliers.get(state_code, 0.02)
        national_breakdown = await self._get_sector_breakdown_national()
        
        return {
            sector: int(count * multiplier)
            for sector, count in national_breakdown.items()
        }
    
    async def _get_sector_breakdown_metro(self, metro_code: str) -> Dict[str, int]:
        """Get metro area business count by sector."""
        
        metro_multipliers = {
            "35620": 0.08,  # New York
            "31080": 0.06,  # Los Angeles
            "16980": 0.04,  # Chicago
            "19100": 0.03,  # Dallas
            "26420": 0.03,  # Houston
        }
        
        multiplier = metro_multipliers.get(metro_code, 0.01)
        national_breakdown = await self._get_sector_breakdown_national()
        
        return {
            sector: int(count * multiplier)
            for sector, count in national_breakdown.items()
        }
    
    async def get_industry_data(self, naics_code: str, location: str = "national") -> Dict[str, Any]:
        """Get industry-specific data by NAICS code."""
        
        logger.info(f"Fetching industry data for NAICS {naics_code} in {location}")
        
        try:
            geo_info = self._parse_location(location)
            
            # Industry data by NAICS code
            industry_data = {
                "naics_code": naics_code,
                "industry_name": self._get_industry_name(naics_code),
                "geographic_level": geo_info["level"],
                "establishments": await self._get_industry_establishments(naics_code, geo_info),
                "employment": await self._get_industry_employment(naics_code, geo_info),
                "payroll": await self._get_industry_payroll(naics_code, geo_info),
                "revenue_estimate": await self._estimate_industry_revenue(naics_code, geo_info),
                "average_establishment_size": 0,
                "timestamp": datetime.now().isoformat()
            }
            
            # Calculate average establishment size
            if industry_data["establishments"] and industry_data["employment"]:
                industry_data["average_establishment_size"] = (
                    industry_data["employment"] / industry_data["establishments"]
                )
            
            return industry_data
            
        except Exception as e:
            logger.error(f"Failed to get industry data for NAICS {naics_code}: {str(e)}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    def _get_industry_name(self, naics_code: str) -> str:
        """Get industry name from NAICS code."""
        
        naics_mapping = {
            "44": "Retail Trade",
            "45": "Retail Trade", 
            "54": "Professional, Scientific, and Technical Services",
            "72": "Accommodation and Food Services",
            "23": "Construction",
            "62": "Health Care and Social Assistance",
            "53": "Real Estate and Rental and Leasing",
            "31": "Manufacturing",
            "32": "Manufacturing",
            "33": "Manufacturing",
            "48": "Transportation and Warehousing",
            "49": "Transportation and Warehousing",
            "52": "Finance and Insurance",
            "51": "Information",
            "81": "Other Services (except Public Administration)",
            "71": "Arts, Entertainment, and Recreation",
            "61": "Educational Services",
            "22": "Utilities",
            "21": "Mining, Quarrying, and Oil and Gas Extraction",
            "55": "Management of Companies and Enterprises",
            "56": "Administrative and Support and Waste Management",
            "42": "Wholesale Trade"
        }
        
        # Use first 2 digits for major sector
        major_sector = naics_code[:2]
        return naics_mapping.get(major_sector, f"Industry {naics_code}")
    
    async def _get_industry_establishments(self, naics_code: str, geo_info: Dict[str, Any]) -> int:
        """Get number of establishments for industry."""
        
        # This would use actual Census Bureau industry data
        # For now, return estimated values based on NAICS code
        
        base_establishments = {
            "44": 500000,   # Retail Trade
            "45": 550000,
            "54": 850000,   # Professional Services
            "72": 660000,   # Food Services
            "23": 730000,   # Construction
            "62": 680000,   # Healthcare
            "53": 430000,   # Real Estate
            "31": 83000,    # Manufacturing
            "32": 83000,
            "33": 84000,
            "48": 115000,   # Transportation
            "49": 115000,
            "52": 280000,   # Finance
            "51": 120000,   # Information
            "81": 540000,   # Other Services
        }
        
        major_sector = naics_code[:2]
        base_count = base_establishments.get(major_sector, 50000)
        
        # Apply geographic multiplier
        if geo_info["level"] == "state":
            state_multipliers = {"06": 0.12, "48": 0.09, "12": 0.07, "36": 0.08, "42": 0.04}
            multiplier = state_multipliers.get(geo_info.get("state_code"), 0.02)
            return int(base_count * multiplier)
        elif geo_info["level"] == "metro":
            metro_multipliers = {"35620": 0.08, "31080": 0.06, "16980": 0.04}
            multiplier = metro_multipliers.get(geo_info.get("metro_code"), 0.01)
            return int(base_count * multiplier)
        
        return base_count
    
    async def _get_industry_employment(self, naics_code: str, geo_info: Dict[str, Any]) -> int:
        """Get employment for industry."""
        
        establishments = await self._get_industry_establishments(naics_code, geo_info)
        
        # Average employees per establishment by sector
        avg_employees = {
            "44": 12,   # Retail
            "45": 11,
            "54": 8,    # Professional Services
            "72": 22,   # Food Services
            "23": 9,    # Construction
            "62": 14,   # Healthcare
            "53": 7,    # Real Estate
            "31": 45,   # Manufacturing
            "32": 42,
            "33": 48,
            "48": 14,   # Transportation
            "49": 12,
            "52": 18,   # Finance
            "51": 12,   # Information
            "81": 4,    # Other Services
        }
        
        major_sector = naics_code[:2]
        employees_per_establishment = avg_employees.get(major_sector, 10)
        
        return establishments * employees_per_establishment
    
    async def _get_industry_payroll(self, naics_code: str, geo_info: Dict[str, Any]) -> int:
        """Get industry payroll."""
        
        employment = await self._get_industry_employment(naics_code, geo_info)
        
        # Average annual salary by sector
        avg_salaries = {
            "44": 32000,   # Retail
            "45": 35000,
            "54": 75000,   # Professional Services
            "72": 28000,   # Food Services
            "23": 52000,   # Construction
            "62": 48000,   # Healthcare
            "53": 55000,   # Real Estate
            "31": 58000,   # Manufacturing
            "32": 62000,
            "33": 65000,
            "48": 47000,   # Transportation
            "49": 45000,
            "52": 78000,   # Finance
            "51": 85000,   # Information
            "81": 35000,   # Other Services
        }
        
        major_sector = naics_code[:2]
        avg_salary = avg_salaries.get(major_sector, 45000)
        
        return employment * avg_salary
    
    async def _estimate_industry_revenue(self, naics_code: str, geo_info: Dict[str, Any]) -> int:
        """Estimate industry revenue."""
        
        establishments = await self._get_industry_establishments(naics_code, geo_info)
        
        # Average annual revenue per establishment by sector
        avg_revenue = {
            "44": 1200000,   # Retail
            "45": 980000,
            "54": 650000,    # Professional Services
            "72": 875000,    # Food Services
            "23": 1800000,   # Construction
            "62": 780000,    # Healthcare
            "53": 420000,    # Real Estate
            "31": 4500000,   # Manufacturing
            "32": 3800000,
            "33": 5200000,
            "48": 1100000,   # Transportation
            "49": 950000,
            "52": 2200000,   # Finance
            "51": 1800000,   # Information
            "81": 280000,    # Other Services
        }
        
        major_sector = naics_code[:2]
        revenue_per_establishment = avg_revenue.get(major_sector, 750000)
        
        return establishments * revenue_per_establishment
    
    async def get_consumer_spending_data(self, location: str) -> Dict[str, Any]:
        """Get consumer spending patterns for location."""
        
        logger.info(f"Fetching consumer spending data for {location}")
        
        try:
            demographic_data = await self.get_demographic_data(location)
            
            if "error" in demographic_data:
                return demographic_data
            
            # Calculate consumer spending estimates
            median_income = demographic_data.get("median_household_income", 70000)
            population = demographic_data.get("total_population", 100000)
            
            # Consumer spending categories (percentages of income)
            spending_categories = {
                "housing": 0.33,           # 33% of income
                "transportation": 0.16,    # 16%
                "food": 0.13,             # 13%
                "personal_insurance": 0.11, # 11%
                "healthcare": 0.08,        # 8%
                "entertainment": 0.05,     # 5%
                "apparel": 0.03,          # 3%
                "other": 0.11             # 11%
            }
            
            total_spending_per_household = median_income * 0.85  # 85% of income spent
            total_households = population / 2.5  # Average household size
            
            category_spending = {}
            for category, percentage in spending_categories.items():
                category_spending[category] = {
                    "total_annual": int(total_spending_per_household * percentage * total_households),
                    "per_household": int(total_spending_per_household * percentage),
                    "percentage_of_income": percentage * 100
                }
            
            return {
                "location": location,
                "total_consumer_market": int(total_spending_per_household * total_households),
                "spending_by_category": category_spending,
                "average_household_spending": int(total_spending_per_household),
                "total_households": int(total_households),
                "median_household_income": median_income,
                "spending_power_index": median_income / 70000,  # Relative to national average
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to get consumer spending data for {location}: {str(e)}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    async def get_business_formation_data(self, location: str) -> Dict[str, Any]:
        """Get business formation and startup data."""
        
        logger.info(f"Fetching business formation data for {location}")
        
        try:
            geo_info = self._parse_location(location)
            
            # Business formation rates by geographic level
            if geo_info["level"] == "national":
                new_businesses_monthly = 430000
                business_closure_rate = 0.08
            elif geo_info["level"] == "state":
                state_multipliers = {"06": 0.12, "48": 0.09, "12": 0.07, "36": 0.08}
                multiplier = state_multipliers.get(geo_info.get("state_code"), 0.02)
                new_businesses_monthly = int(430000 * multiplier)
                business_closure_rate = 0.08
            else:
                metro_multipliers = {"35620": 0.08, "31080": 0.06, "16980": 0.04}
                multiplier = metro_multipliers.get(geo_info.get("metro_code"), 0.01)
                new_businesses_monthly = int(430000 * multiplier)
                business_closure_rate = 0.08
            
            return {
                "location": location,
                "geographic_level": geo_info["level"],
                "new_business_applications_monthly": new_businesses_monthly,
                "new_business_applications_annual": new_businesses_monthly * 12,
                "business_closure_rate": business_closure_rate,
                "net_business_formation": int(new_businesses_monthly * 12 * (1 - business_closure_rate)),
                "entrepreneurship_rate": 0.31,  # 31% of adults have entrepreneurial activity
                "high_propensity_applications": int(new_businesses_monthly * 0.25),  # 25% high-propensity
                "startup_survival_rates": {
                    "1_year": 0.80,
                    "2_years": 0.70,
                    "5_years": 0.50,
                    "10_years": 0.35
                },
                "avg_startup_employment": 2.8,
                "sectors_with_high_formation": [
                    "professional_services",
                    "construction", 
                    "retail_trade",
                    "food_services",
                    "other_services"
                ],
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to get business formation data for {location}: {str(e)}")
            return {"error": str(e), "timestamp": datetime.now().isoformat()}