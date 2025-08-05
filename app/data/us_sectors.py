# app/data/us_sectors.py
"""US sector-specific data and business patterns."""

from typing import Dict, List, Any

# US Sector characteristics and performance patterns
US_SECTOR_DATA = {
    "electronics": {
        "base_performance": {
            "average_monthly_revenue": 125000,    # $125K average monthly
            "typical_profit_margin": 0.15,       # 15% margin
            "growth_rate": 0.08,                 # 8% annual growth
            "volatility": 0.18,                  # Moderate volatility
            "seasonal_peak_months": [11, 12, 1], # Holiday season
            "seasonal_low_months": [2, 3, 4],    # Post-holiday lull
        },
        "location_factors": {
            "urban_high_income": {"multiplier": 1.4, "competition": "high", "rent_factor": 1.8},
            "urban_medium_income": {"multiplier": 1.1, "competition": "very_high", "rent_factor": 1.3},
            "suburban": {"multiplier": 1.0, "competition": "medium", "rent_factor": 1.0},
            "small_town": {"multiplier": 0.7, "competition": "low", "rent_factor": 0.6},
            "mall_location": {"multiplier": 1.2, "competition": "high", "rent_factor": 2.0},
        },
        "business_insights": {
            "high_margin_products": ["accessories", "repair_services", "custom_builds", "business_solutions"],
            "low_margin_products": ["computers", "phones", "tablets", "basic_accessories"],
            "growth_opportunities": ["smart_home", "gaming_setups", "business_tech", "repair_services"],
            "common_challenges": ["online_competition", "rapid_product_cycles", "inventory_management", "price_pressure"],
            "success_factors": ["technical_expertise", "customer_service", "local_relationships", "service_revenue"],
        },
        "market_dynamics": {
            "fed_rate_sensitivity": -0.6,    # Negative (financing sensitive)
            "inflation_sensitivity": -0.5,   # Negative (imported components)
            "demand_elasticity": 0.7,        # Moderately elastic
            "competition_intensity": 0.9,    # Very competitive
            "online_disruption_risk": 0.8,   # High online competition
        }
    },
    
    "food": {
        "base_performance": {
            "average_monthly_revenue": 95000,     # $95K average monthly
            "typical_profit_margin": 0.22,       # 22% margin (higher than retail)
            "growth_rate": 0.06,                 # 6% annual growth
            "volatility": 0.12,                  # Lower volatility (necessity)
            "seasonal_peak_months": [5, 6, 11, 12], # Summer and holidays
            "seasonal_low_months": [1, 2],       # Post-holiday diet season
        },
        "location_factors": {
            "downtown": {"multiplier": 1.3, "competition": "high", "rent_factor": 2.0},
            "business_district": {"multiplier": 1.2, "competition": "medium", "rent_factor": 1.8},
            "residential": {"multiplier": 1.0, "competition": "medium", "rent_factor": 1.2},
            "tourist_area": {"multiplier": 1.5, "competition": "high", "rent_factor": 2.2},
            "strip_mall": {"multiplier": 0.9, "competition": "medium", "rent_factor": 1.0},
        },
        "business_insights": {
            "high_margin_products": ["beverages", "desserts", "specialty_dishes", "catering"],
            "low_margin_products": ["basic_entrees", "sides", "bread", "salads"],
            "growth_opportunities": ["delivery", "catering", "meal_prep", "healthy_options", "ethnic_cuisine"],
            "common_challenges": ["labor_costs", "food_cost_inflation", "health_regulations", "competition"],
            "success_factors": ["food_quality", "consistency", "location", "service_speed", "cleanliness"],
        },
        "market_dynamics": {
            "fed_rate_sensitivity": -0.2,    # Low sensitivity (necessity)
            "inflation_sensitivity": -0.7,   # High sensitivity (food costs)
            "demand_elasticity": 0.4,        # Inelastic (necessity)
            "competition_intensity": 0.9,    # Very competitive
            "delivery_disruption": 0.6,      # Moderate delivery impact
        }
    },
    
    "retail": {
        "base_performance": {
            "average_monthly_revenue": 85000,     # $85K average monthly
            "typical_profit_margin": 0.18,       # 18% margin
            "growth_rate": 0.04,                 # 4% annual growth (slow)
            "volatility": 0.15,                  # Moderate volatility
            "seasonal_peak_months": [11, 12],    # Holiday shopping
            "seasonal_low_months": [1, 2, 3],    # Post-holiday
        },
        "location_factors": {
            "main_street": {"multiplier": 1.1, "competition": "high", "rent_factor": 1.5},
            "shopping_center": {"multiplier": 1.2, "competition": "very_high", "rent_factor": 1.8},
            "neighborhood": {"multiplier": 0.9, "competition": "medium", "rent_factor": 1.0},
            "outlet_mall": {"multiplier": 1.0, "competition": "high", "rent_factor": 1.3},
            "downtown": {"multiplier": 1.0, "competition": "high", "rent_factor": 1.6},
        },
        "business_insights": {
            "high_margin_products": ["accessories", "seasonal_items", "gifts", "specialty_products"],
            "low_margin_products": ["basics", "commodities", "sale_items"],
            "growth_opportunities": ["online_integration", "personal_service", "local_products", "experiences"],
            "common_challenges": ["online_competition", "inventory_management", "foot_traffic", "margins"],
            "success_factors": ["product_curation", "customer_service", "inventory_turnover", "local_connection"],
        },
        "market_dynamics": {
            "fed_rate_sensitivity": -0.4,    # Medium sensitivity
            "inflation_sensitivity": -0.4,   # Medium sensitivity
            "demand_elasticity": 0.8,        # Elastic (discretionary)
            "competition_intensity": 0.9,    # Very competitive
            "online_disruption_risk": 0.9,   # Very high online threat
        }
    },
    
    "auto": {
        "base_performance": {
            "average_monthly_revenue": 180000,    # $180K average monthly
            "typical_profit_margin": 0.12,       # 12% margin
            "growth_rate": 0.03,                 # 3% annual growth
            "volatility": 0.25,                  # High volatility
            "seasonal_peak_months": [3, 4, 9, 10], # Spring and fall
            "seasonal_low_months": [12, 1, 2],   # Winter slow season
        },
        "location_factors": {
            "auto_row": {"multiplier": 1.3, "competition": "very_high", "rent_factor": 1.2},
            "highway_access": {"multiplier": 1.2, "competition": "high", "rent_factor": 1.0},
            "industrial_area": {"multiplier": 1.0, "competition": "medium", "rent_factor": 0.8},
            "suburban": {"multiplier": 0.9, "competition": "medium", "rent_factor": 1.1},
            "downtown": {"multiplier": 0.7, "competition": "low", "rent_factor": 1.8},
        },
        "business_insights": {
            "high_margin_products": ["services", "parts", "accessories", "warranties", "financing"],
            "low_margin_products": ["new_vehicles", "used_vehicles", "basic_maintenance"],
            "growth_opportunities": ["electric_vehicles", "service_focus", "online_sales", "mobile_service"],
            "common_challenges": ["inventory_costs", "manufacturer_relations", "economic_sensitivity", "regulations"],
            "success_factors": ["service_quality", "financing_options", "inventory_management", "customer_trust"],
        },
        "market_dynamics": {
            "fed_rate_sensitivity": -0.8,    # Very high sensitivity (financing)
            "inflation_sensitivity": -0.6,   # High sensitivity
            "demand_elasticity": 0.9,        # Very elastic (major purchase)
            "competition_intensity": 0.7,    # High competition
            "ev_disruption_risk": 0.7,       # High disruption from EVs
        }
    },
    
    "professional_services": {
        "base_performance": {
            "average_monthly_revenue": 75000,     # $75K average monthly
            "typical_profit_margin": 0.28,       # 28% margin (service-based)
            "growth_rate": 0.09,                 # 9% annual growth
            "volatility": 0.10,                  # Low volatility
            "seasonal_peak_months": [1, 3, 4],   # Tax season, planning
            "seasonal_low_months": [7, 8, 12],   # Summer and holidays
        },
        "location_factors": {
            "business_district": {"multiplier": 1.4, "competition": "high", "rent_factor": 2.0},
            "professional_complex": {"multiplier": 1.2, "competition": "medium", "rent_factor": 1.5},
            "suburban_office": {"multiplier": 1.0, "competition": "medium", "rent_factor": 1.2},
            "home_based": {"multiplier": 0.8, "competition": "high", "rent_factor": 0.3},
            "co_working": {"multiplier": 0.9, "competition": "medium", "rent_factor": 0.8},
        },
        "business_insights": {
            "high_margin_products": ["consulting", "specialized_services", "retainer_agreements", "training"],
            "low_margin_products": ["basic_services", "commodity_work", "one_time_projects"],
            "growth_opportunities": ["digital_services", "recurring_revenue", "specialization", "partnerships"],
            "common_challenges": ["client_acquisition", "payment_delays", "competition", "pricing_pressure", "talent_retention"],
           "success_factors": ["expertise", "client_relationships", "reputation", "referrals", "service_quality"],
       },
       "market_dynamics": {
           "fed_rate_sensitivity": -0.3,    # Medium-low sensitivity
           "inflation_sensitivity": -0.2,   # Low sensitivity (service-based)
           "demand_elasticity": 0.5,        # Moderately inelastic (business necessity)
           "competition_intensity": 0.8,    # High competition
           "remote_work_impact": 0.6,       # Moderate impact from remote trends
       }
   },
   
   "manufacturing": {
       "base_performance": {
           "average_monthly_revenue": 450000,   # $450K average monthly
           "typical_profit_margin": 0.14,       # 14% margin
           "growth_rate": 0.05,                 # 5% annual growth
           "volatility": 0.20,                  # Moderate-high volatility
           "seasonal_peak_months": [9, 10, 11], # Fall production
           "seasonal_low_months": [12, 1],      # Holiday shutdown
       },
       "location_factors": {
           "industrial_park": {"multiplier": 1.2, "competition": "medium", "rent_factor": 0.8},
           "manufacturing_zone": {"multiplier": 1.1, "competition": "medium", "rent_factor": 0.7},
           "rural_industrial": {"multiplier": 0.9, "competition": "low", "rent_factor": 0.5},
           "port_access": {"multiplier": 1.3, "competition": "high", "rent_factor": 1.0},
           "urban_industrial": {"multiplier": 1.0, "competition": "high", "rent_factor": 1.2},
       },
       "business_insights": {
           "high_margin_products": ["custom_manufacturing", "specialized_products", "value_added_services"],
           "low_margin_products": ["commodity_products", "standard_manufacturing", "contract_work"],
           "growth_opportunities": ["automation", "reshoring_trends", "sustainability", "customization"],
           "common_challenges": ["labor_shortage", "supply_chain", "regulations", "capital_requirements", "competition"],
           "success_factors": ["efficiency", "quality", "delivery_reliability", "cost_control", "innovation"],
       },
       "market_dynamics": {
           "fed_rate_sensitivity": -0.5,    # High sensitivity (capital intensive)
           "inflation_sensitivity": -0.6,   # High sensitivity (material costs)
           "demand_elasticity": 0.6,        # Moderately elastic
           "competition_intensity": 0.7,    # High competition
           "automation_pressure": 0.8,      # High pressure to automate
       }
   }
}

# US Location-specific characteristics by region/market type
US_LOCATION_DATA = {
   "urban_high_income": {
       "characteristics": {
           "foot_traffic": "high",
           "customer_type": "affluent",
           "rent_level": "very_high",
           "competition": "very_high",
           "accessibility": "excellent",
           "parking": "difficult",
           "demographics": {"median_income": 85000, "age_25_44": 35, "college_degree": 55}
       },
       "advantages": [
           "High disposable income customers",
           "Premium pricing acceptance",
           "Diverse customer base",
           "Public transportation access",
           "Business networking opportunities"
       ],
       "challenges": [
           "Very high commercial rents",
           "Intense competition",
           "Parking limitations",
           "High operating costs",
           "Strict regulations"
       ],
       "best_businesses": ["professional_services", "food", "retail", "electronics"],
       "success_factors": ["premium_quality", "exceptional_service", "brand_positioning", "convenience"]
   },
   
   "urban_medium_income": {
       "characteristics": {
           "foot_traffic": "very_high",
           "customer_type": "middle_class",
           "rent_level": "high",
           "competition": "very_high",
           "accessibility": "excellent",
           "parking": "moderate",
           "demographics": {"median_income": 55000, "age_25_44": 32, "college_degree": 35}
       },
       "advantages": [
           "High foot traffic",
           "Good public transportation",
           "Diverse customer base",
           "Value-conscious but willing to spend",
           "Cultural diversity"
       ],
       "challenges": [
           "Extreme competition",
           "Price sensitivity",
           "High rent relative to customer spending",
           "Staff recruitment challenges",
           "Economic sensitivity"
       ],
       "best_businesses": ["food", "retail", "electronics", "auto"],
       "success_factors": ["competitive_pricing", "high_volume", "efficiency", "local_adaptation"]
   },
   
   "suburban": {
       "characteristics": {
           "foot_traffic": "medium",
           "customer_type": "families",
           "rent_level": "medium",
           "competition": "medium",
           "accessibility": "good",
           "parking": "excellent",
           "demographics": {"median_income": 65000, "age_25_44": 28, "college_degree": 42}
       },
       "advantages": [
           "Family-oriented market",
           "Reasonable rents",
           "Good parking availability",
           "Growing population",
           "Chain store acceptance"
       ],
       "challenges": [
           "Car-dependent customers",
           "Competition from chains",
           "Lower foot traffic",
           "Seasonal variations",
           "Economic sensitivity"
       ],
       "best_businesses": ["retail", "food", "auto", "professional_services"],
       "success_factors": ["convenience", "family_focus", "value_proposition", "community_engagement"]
   },
   
   "small_town": {
       "characteristics": {
           "foot_traffic": "low",
           "customer_type": "local_residents",
           "rent_level": "low",
           "competition": "low",
           "accessibility": "good",
           "parking": "excellent",
           "demographics": {"median_income": 45000, "age_25_44": 25, "college_degree": 28}
       },
       "advantages": [
           "Low competition",
           "Very low rents",
           "Strong community loyalty",
           "Personal relationships matter",
           "Lower operating costs"
       ],
       "challenges": [
           "Limited customer base",
           "Lower incomes",
           "Limited growth potential",
           "Seasonal population variations",
           "Limited supplier options"
       ],
       "best_businesses": ["food", "auto", "retail", "professional_services"],
       "success_factors": ["community_connection", "personal_service", "reliability", "local_knowledge"]
   },
   
   "business_district": {
       "characteristics": {
           "foot_traffic": "high_weekdays",
           "customer_type": "professionals",
           "rent_level": "very_high",
           "competition": "high",
           "accessibility": "excellent",
           "parking": "expensive",
           "demographics": {"median_income": 75000, "age_25_44": 45, "college_degree": 65}
       },
       "advantages": [
           "High-income professional customers",
           "Weekday lunch rush",
           "B2B opportunities",
           "Networking potential",
           "Premium pricing acceptance"
       ],
       "challenges": [
           "Very high rents",
           "Limited weekend traffic",
           "Expensive parking",
           "High competition",
           "Economic cycle sensitivity"
       ],
       "best_businesses": ["food", "professional_services", "electronics"],
       "success_factors": ["speed_of_service", "business_focus", "networking", "quality"]
   },
   
   "tourist_area": {
       "characteristics": {
           "foot_traffic": "seasonal_high",
           "customer_type": "tourists_locals",
           "rent_level": "very_high",
           "competition": "high",
           "accessibility": "good",
           "parking": "difficult",
           "demographics": {"seasonal_variation": "extreme", "tourist_spending": "high"}
       },
       "advantages": [
           "High tourist spending",
           "Premium pricing acceptance",
           "Unique products demand",
           "High seasonal revenue",
           "Marketing opportunities"
       ],
       "challenges": [
           "Extreme seasonality",
           "Very high rents",
           "Staff seasonality",
           "Tourist-focused regulations",
           "Economic sensitivity"
       ],
       "best_businesses": ["food", "retail", "electronics"],
       "success_factors": ["seasonal_optimization", "unique_offerings", "tourist_appeal", "efficiency"]
   }
}

def get_us_sector_data(sector: str) -> Dict[str, Any]:
   """Get comprehensive US sector data."""
   return US_SECTOR_DATA.get(sector.lower(), {})

def get_us_location_data(location_type: str) -> Dict[str, Any]:
   """Get comprehensive US location data."""
   return US_LOCATION_DATA.get(location_type.lower(), {})

def get_us_sector_location_multiplier(sector: str, location_type: str) -> float:
   """Get location multiplier for specific sector in US market."""
   sector_data = get_us_sector_data(sector)
   if not sector_data:
       return 1.0
   
   location_factors = sector_data.get("location_factors", {})
   location_data = location_factors.get(location_type.lower(), {})
   
   return location_data.get("multiplier", 1.0)

def get_us_competition_level(sector: str, location_type: str) -> str:
   """Get competition level for sector in US location type."""
   sector_data = get_us_sector_data(sector)
   if not sector_data:
       return "medium"
   
   location_factors = sector_data.get("location_factors", {})
   location_data = location_factors.get(location_type.lower(), {})
   
   return location_data.get("competition", "medium")

def calculate_us_market_opportunity_score(sector: str, location_type: str, 
                                       business_size: str = "small") -> Dict[str, Any]:
   """Calculate market opportunity score for US business."""
   
   sector_data = get_us_sector_data(sector)
   location_data = get_us_location_data(location_type)
   
   if not sector_data or not location_data:
       return {"opportunity_score": 50, "factors": ["Limited data available"]}
   
   # Base opportunity calculation
   base_score = 50
   
   # Sector growth factor
   growth_rate = sector_data["base_performance"]["growth_rate"]
   growth_score = min(25, growth_rate * 250)  # Scale growth rate
   base_score += growth_score
   
   # Location multiplier factor
   location_multiplier = get_us_sector_location_multiplier(sector, location_type)
   location_score = (location_multiplier - 1.0) * 20
   base_score += location_score
   
   # Competition adjustment
   competition_level = get_us_competition_level(sector, location_type)
   competition_adjustments = {"low": 10, "medium": 0, "high": -10, "very_high": -20}
   competition_score = competition_adjustments.get(competition_level, 0)
   base_score += competition_score
   
   # Market size factor (from location demographics)
   location_characteristics = location_data.get("characteristics", {})
   if "demographics" in location_characteristics:
       income = location_characteristics["demographics"].get("median_income", 50000)
       income_score = (income - 50000) / 1000  # Each $1K above $50K adds 1 point
       base_score += min(15, max(-15, income_score))
   
   # Business size factor
   size_adjustments = {"small": 5, "medium": 0, "large": -5}  # Small businesses have slight advantage
   base_score += size_adjustments.get(business_size, 0)
   
   # Cap score between 0-100
   final_score = max(0, min(100, base_score))
   
   # Generate explanatory factors
   factors = []
   if growth_rate > 0.06:
       factors.append(f"Strong sector growth rate of {growth_rate*100:.1f}%")
   if location_multiplier > 1.1:
       factors.append("Favorable location for this sector")
   if competition_level in ["low", "medium"]:
       factors.append(f"Manageable competition level ({competition_level})")
   
   return {
       "opportunity_score": final_score,
       "opportunity_level": "high" if final_score > 70 else "medium" if final_score > 40 else "low",
       "factors": factors,
       "sector_growth": growth_rate,
       "location_multiplier": location_multiplier,
       "competition_level": competition_level
   }

def get_us_naics_sector_mapping() -> Dict[str, str]:
   """Map NAICS codes to our business sectors."""
   return {
       # Electronics/Technology
       "443142": "electronics",  # Electronics Stores
       "541511": "electronics",  # Custom Computer Programming Services
       "811212": "electronics",  # Computer and Office Machine Repair
       
       # Food Services
       "722511": "food",         # Full-Service Restaurants
       "722513": "food",         # Limited-Service Restaurants
       "722320": "food",         # Caterers
       "445110": "food",         # Supermarkets and Other Grocery Stores
       
       # Retail
       "448110": "retail",       # Men's Clothing Stores
       "448120": "retail",       # Women's Clothing Stores
       "452311": "retail",       # Warehouse Clubs and Supercenters
       "445120": "retail",       # Convenience Stores
       
       # Automotive
       "441110": "auto",         # New Car Dealers
       "441120": "auto",         # Used Car Dealers
       "811111": "auto",         # General Automotive Repair
       "441310": "auto",         # Automotive Parts and Accessories Stores
       
       # Professional Services
       "541211": "professional_services",  # Offices of Certified Public Accountants
       "541110": "professional_services",  # Offices of Lawyers
       "541611": "professional_services",  # Administrative Management Consulting
       "541614": "professional_services",  # Process and Logistics Consulting
       
       # Manufacturing
       "311111": "manufacturing", # Dog and Cat Food Manufacturing  
       "315210": "manufacturing", # Cut and Sew Apparel Contractors
       "332710": "manufacturing", # Machine Shops
       "333249": "manufacturing", # Other Industrial Machinery Manufacturing
   }

def classify_us_location_type(city: str, state: str, zip_code: str = None) -> str:
   """Classify US location into our location types."""
   
   # Major high-income urban areas
   high_income_cities = [
       "manhattan", "san francisco", "palo alto", "beverly hills", "georgetown",
       "back bay", "upper east side", "tribeca", "pacific heights"
   ]
   
   # Major urban areas
   major_cities = [
       "new york", "los angeles", "chicago", "houston", "phoenix", "philadelphia",
       "san antonio", "san diego", "dallas", "san jose", "austin", "jacksonville"
   ]
   
   # Business districts (usually part of major cities)
   business_districts = [
       "financial district", "downtown", "midtown", "loop", "central business district"
   ]
   
   # Tourist areas
   tourist_areas = [
       "times square", "hollywood", "south beach", "french quarter", "fisherman's wharf",
       "las vegas strip", "orlando", "key west", "napa valley"
   ]
   
   city_lower = city.lower()
   
   # Check for specific high-income areas
   if any(area in city_lower for area in high_income_cities):
       return "urban_high_income"
   
   # Check for business districts
   if any(district in city_lower for district in business_districts):
       return "business_district"
   
   # Check for tourist areas
   if any(area in city_lower for area in tourist_areas):
       return "tourist_area"
   
   # Check for major cities
   if any(city_name in city_lower for city_name in major_cities):
       return "urban_medium_income"
   
   # Use ZIP code if available for more precise classification
   if zip_code:
       # This is simplified - in reality, you'd use demographic databases
       zip_int = int(zip_code[:5]) if zip_code.isdigit() and len(zip_code) >= 5 else 0
       
       # High-income ZIP patterns (simplified examples)
       if zip_int in range(10001, 10299):  # Manhattan
           return "urban_high_income"
       elif zip_int in range(94101, 94199):  # San Francisco
           return "urban_high_income"
       elif zip_int in range(90210, 90220):  # Beverly Hills area
           return "urban_high_income"
   
   # Default classifications by state patterns
   suburban_states = ["connecticut", "new jersey", "massachusetts"]
   if state.lower() in suburban_states:
       return "suburban"
   
   # Small town default for rural areas
   rural_states = ["wyoming", "montana", "north dakota", "south dakota", "vermont"]
   if state.lower() in rural_states:
       return "small_town"
   
   # Default to suburban for most US locations
   return "suburban"