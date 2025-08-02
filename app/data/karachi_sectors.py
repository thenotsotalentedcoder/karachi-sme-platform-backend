"""Karachi sector-specific data and patterns."""

from typing import Dict, List, Any

# Sector characteristics and performance patterns
KARACHI_SECTOR_DATA = {
    "electronics": {
        "base_performance": {
            "average_monthly_revenue": 750000,
            "typical_profit_margin": 0.12,
            "growth_rate": 0.18,
            "volatility": 0.15,
            "seasonal_peak_months": [11, 12, 1],  # Nov, Dec, Jan
            "seasonal_low_months": [6, 7, 8],     # Jun, Jul, Aug
        },
        "location_factors": {
            "saddar": {"multiplier": 1.0, "competition": "very_high", "rent_factor": 0.8},
            "clifton": {"multiplier": 1.4, "competition": "medium", "rent_factor": 1.8},
            "dha": {"multiplier": 1.6, "competition": "low", "rent_factor": 2.2},
            "gulshan": {"multiplier": 0.9, "competition": "medium", "rent_factor": 1.0},
            "tariq_road": {"multiplier": 1.1, "competition": "high", "rent_factor": 1.2},
        },
        "business_insights": {
            "high_margin_products": ["mobile_accessories", "repair_services", "gaming_accessories"],
            "low_margin_products": ["smartphones", "laptops", "tablets"],
            "growth_opportunities": ["mobile_repair", "gaming_setup", "smart_home_devices"],
            "common_challenges": ["price_competition", "inventory_management", "fake_products"],
            "success_factors": ["location", "product_mix", "customer_service", "repair_expertise"],
        },
        "market_dynamics": {
            "pkr_sensitivity": -0.4,  # Negative because imports get expensive
            "inflation_sensitivity": -0.3,
            "demand_elasticity": 0.8,
            "competition_intensity": 0.9,
        }
    },
    
    "textile": {
        "base_performance": {
            "average_monthly_revenue": 1200000,
            "typical_profit_margin": 0.18,
            "growth_rate": 0.08,
            "volatility": 0.12,
            "seasonal_peak_months": [9, 10, 11],  # Wedding season
            "seasonal_low_months": [3, 4, 5],     # Post-wedding lull
        },
        "location_factors": {
            "tariq_road": {"multiplier": 1.3, "competition": "high", "rent_factor": 1.5},
            "saddar": {"multiplier": 1.1, "competition": "very_high", "rent_factor": 1.0},
            "korangi": {"multiplier": 0.8, "competition": "medium", "rent_factor": 0.6},
            "clifton": {"multiplier": 1.2, "competition": "medium", "rent_factor": 1.8},
            "gulshan": {"multiplier": 0.9, "competition": "medium", "rent_factor": 1.0},
        },
        "business_insights": {
            "high_margin_products": ["wedding_fabrics", "designer_suits", "premium_cotton"],
            "low_margin_products": ["basic_cotton", "synthetic_fabrics", "bulk_orders"],
            "growth_opportunities": ["online_sales", "custom_tailoring", "export_orders"],
            "common_challenges": ["cotton_price_volatility", "seasonal_demand", "payment_delays"],
            "success_factors": ["fabric_quality", "design_variety", "customer_relationships", "timing"],
        },
        "market_dynamics": {
            "pkr_sensitivity": 0.6,   # Positive because exports benefit
            "inflation_sensitivity": -0.4,
            "demand_elasticity": 0.6,
            "competition_intensity": 0.7,
        }
    },
    
    "auto": {
        "base_performance": {
            "average_monthly_revenue": 900000,
            "typical_profit_margin": 0.15,
            "growth_rate": 0.05,
            "volatility": 0.18,
            "seasonal_peak_months": [12, 1, 2],   # New year car buying
            "seasonal_low_months": [6, 7],        # Monsoon season
        },
        "location_factors": {
            "korangi": {"multiplier": 1.2, "competition": "high", "rent_factor": 0.7},
            "landhi": {"multiplier": 1.0, "competition": "medium", "rent_factor": 0.6},
            "saddar": {"multiplier": 0.9, "competition": "very_high", "rent_factor": 1.2},
            "gulshan": {"multiplier": 1.1, "competition": "medium", "rent_factor": 1.0},
            "north_karachi": {"multiplier": 0.8, "competition": "low", "rent_factor": 0.8},
        },
        "business_insights": {
            "high_margin_products": ["motorcycle_parts", "car_servicing", "custom_modifications"],
            "low_margin_products": ["basic_spare_parts", "oil_change", "bulk_parts"],
            "growth_opportunities": ["electric_vehicle_parts", "motorcycle_accessories", "mobile_services"],
            "common_challenges": ["import_duties", "fake_parts", "payment_terms", "seasonal_demand"],
            "success_factors": ["parts_authenticity", "technical_expertise", "supplier_relationships", "location"],
        },
        "market_dynamics": {
            "pkr_sensitivity": -0.8,  # Very negative due to import dependency
            "inflation_sensitivity": -0.3,
            "demand_elasticity": 0.9,
            "competition_intensity": 0.8,
        }
    },
    
    "food": {
        "base_performance": {
            "average_monthly_revenue": 600000,
            "typical_profit_margin": 0.25,
            "growth_rate": 0.12,
            "volatility": 0.08,
            "seasonal_peak_months": [9, 12],       # Ramadan prep and winter
            "seasonal_low_months": [6, 7],         # Ramadan and summer heat
        },
        "location_factors": {
            "clifton": {"multiplier": 1.5, "competition": "high", "rent_factor": 2.0},
            "dha": {"multiplier": 1.7, "competition": "medium", "rent_factor": 2.5},
            "gulshan": {"multiplier": 1.2, "competition": "medium", "rent_factor": 1.2},
            "saddar": {"multiplier": 1.0, "competition": "very_high", "rent_factor": 1.0},
            "nazimabad": {"multiplier": 0.9, "competition": "medium", "rent_factor": 0.9},
        },
        "business_insights": {
            "high_margin_products": ["specialty_dishes", "beverages", "desserts", "catering"],
            "low_margin_products": ["rice_dishes", "basic_curry", "bread"],
            "growth_opportunities": ["home_delivery", "catering_services", "specialty_cuisine", "healthy_options"],
            "common_challenges": ["ingredient_costs", "staff_management", "food_safety", "competition"],
            "success_factors": ["taste_consistency", "location", "service_speed", "hygiene"],
        },
        "market_dynamics": {
            "pkr_sensitivity": -0.2,  # Slight negative due to imported ingredients
            "inflation_sensitivity": -0.4,
            "demand_elasticity": 0.5,
            "competition_intensity": 0.9,
        }
    },
    
    "retail": {
        "base_performance": {
            "average_monthly_revenue": 500000,
            "typical_profit_margin": 0.20,
            "growth_rate": 0.06,
            "volatility": 0.10,
            "seasonal_peak_months": [11, 12, 1, 8],  # Eid seasons
            "seasonal_low_months": [3, 4, 5],        # Post-celebration lull
        },
        "location_factors": {
            "saddar": {"multiplier": 1.2, "competition": "very_high", "rent_factor": 1.0},
            "tariq_road": {"multiplier": 1.1, "competition": "high", "rent_factor": 1.3},
            "gulshan": {"multiplier": 1.0, "competition": "medium", "rent_factor": 1.0},
            "clifton": {"multiplier": 1.3, "competition": "medium", "rent_factor": 1.8},
            "nazimabad": {"multiplier": 0.9, "competition": "medium", "rent_factor": 0.8},
        },
        "business_insights": {
            "high_margin_products": ["branded_items", "seasonal_goods", "gift_items", "home_decor"],
            "low_margin_products": ["groceries", "basic_necessities", "bulk_items"],
            "growth_opportunities": ["online_presence", "home_delivery", "loyalty_programs", "seasonal_specialization"],
            "common_challenges": ["inventory_management", "price_competition", "supplier_payments", "theft"],
            "success_factors": ["product_variety", "customer_service", "location", "inventory_turnover"],
        },
        "market_dynamics": {
            "pkr_sensitivity": -0.3,  # Mixed impact depending on product mix
            "inflation_sensitivity": -0.5,
            "demand_elasticity": 0.7,
            "competition_intensity": 0.8,
        }
    }
}

# Location-specific characteristics
KARACHI_LOCATION_DATA = {
    "saddar": {
        "characteristics": {
            "foot_traffic": "very_high",
            "customer_type": "price_conscious",
            "rent_level": "medium",
            "competition": "very_high",
            "accessibility": "excellent",
            "parking": "difficult",
        },
        "advantages": [
            "Highest foot traffic in Karachi",
            "Central location with metro access",
            "Diverse customer base",
            "Established commercial hub",
            "Good public transportation"
        ],
        "challenges": [
            "Extremely high competition",
            "Parking difficulties",
            "Traffic congestion",
            "Price pressure from competitors",
            "Limited expansion space"
        ],
        "best_businesses": ["electronics", "textile", "retail"],
        "success_factors": ["competitive_pricing", "fast_service", "product_variety"]
    },
    
    "clifton": {
        "characteristics": {
            "foot_traffic": "high",
            "customer_type": "affluent",
            "rent_level": "high",
            "competition": "medium",
            "accessibility": "good",
            "parking": "moderate",
        },
        "advantages": [
            "Affluent customer base",
            "Higher spending power",
            "Premium brand acceptance",
            "Good infrastructure",
            "Upscale location image"
        ],
        "challenges": [
            "High rental costs",
            "Higher customer expectations",
            "Limited budget-conscious customers",
            "Seasonal variations",
            "Competition from branded stores"
        ],
        "best_businesses": ["food", "retail", "electronics"],
        "success_factors": ["quality_products", "excellent_service", "premium_positioning"]
    },
    
    "dha": {
        "characteristics": {
            "foot_traffic": "medium",
            "customer_type": "affluent",
            "rent_level": "very_high",
            "competition": "low",
            "accessibility": "excellent",
            "parking": "excellent",
        },
        "advantages": [
            "Highest income customers",
            "Low competition",
            "Excellent infrastructure",
            "Premium location",
            "Easy parking"
        ],
        "challenges": [
            "Very high rental costs",
            "Limited customer volume",
            "High service expectations",
            "Seasonal resident variations",
            "High initial investment"
        ],
        "best_businesses": ["food", "retail"],
        "success_factors": ["premium_quality", "exceptional_service", "convenience"]
    },
    
    "gulshan": {
        "characteristics": {
            "foot_traffic": "medium",
            "customer_type": "middle_class",
            "rent_level": "medium",
            "competition": "medium",
            "accessibility": "good",
            "parking": "moderate",
        },
        "advantages": [
            "Balanced customer base",
            "Reasonable rental costs",
            "Growing area",
            "Good transportation",
            "Family-oriented market"
        ],
        "challenges": [
            "Moderate competition",
            "Price-sensitive customers",
            "Infrastructure development ongoing",
            "Limited premium market",
            "Seasonal demand variations"
        ],
        "best_businesses": ["retail", "food", "electronics"],
        "success_factors": ["value_for_money", "family_focus", "consistent_quality"]
    },
    
    "tariq_road": {
        "characteristics": {
            "foot_traffic": "high",
            "customer_type": "mixed",
            "rent_level": "medium_high",
            "competition": "high",
            "accessibility": "good",
            "parking": "difficult",
        },
        "advantages": [
            "High foot traffic",
            "Shopping destination",
            "Brand recognition area",
            "Good public transport",
            "Tourist attraction"
        ],
        "challenges": [
            "High competition",
            "Parking problems",
            "Traffic congestion",
            "Higher rents",
            "Crowd management"
        ],
        "best_businesses": ["textile", "retail", "electronics"],
        "success_factors": ["unique_products", "competitive_pricing", "fast_service"]
    },
    
    "korangi": {
        "characteristics": {
            "foot_traffic": "medium",
            "customer_type": "working_class",
            "rent_level": "low",
            "competition": "medium",
            "accessibility": "moderate",
            "parking": "good",
        },
        "advantages": [
            "Low rental costs",
            "Industrial area proximity",
            "Good for manufacturing",
            "Lower competition",
            "Working population market"
        ],
        "challenges": [
            "Lower spending power",
            "Limited luxury market",
            "Infrastructure challenges",
            "Distance from city center",
            "Limited tourist traffic"
        ],
        "best_businesses": ["auto", "textile", "retail"],
        "success_factors": ["affordable_pricing", "practical_products", "bulk_sales"]
    }
}

def get_sector_data(sector: str) -> Dict[str, Any]:
    """Get comprehensive sector data."""
    return KARACHI_SECTOR_DATA.get(sector.lower(), {})

def get_location_data(location: str) -> Dict[str, Any]:
    """Get comprehensive location data."""
    return KARACHI_LOCATION_DATA.get(location.lower(), {})

def get_sector_location_multiplier(sector: str, location: str) -> float:
    """Get location multiplier for specific sector."""
    sector_data = get_sector_data(sector)
    if not sector_data:
        return 1.0
    
    location_factors = sector_data.get("location_factors", {})
    location_data = location_factors.get(location.lower(), {})
    
    return location_data.get("multiplier", 1.0)

def get_competition_level(sector: str, location: str) -> str:
    """Get competition level for sector in location."""
    sector_data = get_sector_data(sector)
    if not sector_data:
        return "medium"
    
    location_factors = sector_data.get("location_factors", {})
    location_data = location_factors.get(location.lower(), {})
    
    return location_data.get("competition", "medium")