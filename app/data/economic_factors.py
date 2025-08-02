"""Economic factors and market conditions affecting Pakistani businesses."""

import datetime
from typing import Dict, List, Any
import math

# Current economic indicators (realistic Pakistani data)
CURRENT_ECONOMIC_DATA = {
    "pkr_usd_rate": 278.50,
    "inflation_rate": 0.29,  # 29% annual inflation
    "interest_rate": 0.22,   # 22% policy rate
    "gdp_growth": 0.024,     # 2.4% GDP growth
    "unemployment": 0.063,   # 6.3% unemployment
    "energy_cost_index": 1.85,  # High energy costs
    "supply_chain_stress": 0.7,  # 0-1 scale
}

# Seasonal factors affecting different sectors
SEASONAL_PATTERNS = {
    "electronics": {
        1: 1.2,   # January - New year purchases
        2: 0.9,   # February - Post-holiday lull
        3: 0.95,  # March - Normal
        4: 1.0,   # April - Normal
        5: 0.9,   # May - Pre-summer slowdown
        6: 0.8,   # June - Summer heat, low activity
        7: 0.75,  # July - Ramadan effect (varies by year)
        8: 0.85,  # August - Eid shopping
        9: 1.05,  # September - Back to school/work
        10: 1.1,  # October - Wedding season prep
        11: 1.3,  # November - Wedding season peak
        12: 1.4,  # December - Wedding season + year-end
    },
    "textile": {
        1: 0.9,   # January - Post-wedding lull
        2: 0.85,  # February - Slow period
        3: 0.8,   # March - Lowest demand
        4: 0.85,  # April - Starting to pick up
        5: 0.9,   # May - Summer collection
        6: 1.0,   # June - Eid preparation
        7: 0.8,   # July - Ramadan quiet
        8: 1.2,   # August - Eid shopping
        9: 1.4,   # September - Wedding season starts
        10: 1.5,  # October - Peak wedding season
        11: 1.6,  # November - Peak wedding season
        12: 1.3,  # December - Wedding season continues
    },
    "auto": {
        1: 1.3,   # January - New year car purchases
        2: 1.2,   # February - Still good demand
        3: 1.0,   # March - Normal
        4: 0.95,  # April - Starting to slow
        5: 0.9,   # May - Pre-monsoon
        6: 0.7,   # June - Monsoon season
        7: 0.6,   # July - Heavy monsoon
        8: 0.8,   # August - Post-monsoon recovery
        9: 1.0,   # September - Normal
        10: 1.1,  # October - Good weather
        11: 1.2,  # November - Wedding transport needs
        12: 1.4,  # December - Year-end purchases
    },
    "food": {
        1: 1.0,   # January - Normal
        2: 1.05,  # February - Valentine's effect
        3: 1.0,   # March - Normal
        4: 1.1,   # April - Pleasant weather
        5: 1.0,   # May - Normal
        6: 0.8,   # June - Ramadan fasting
        7: 0.7,   # July - Ramadan continues
        8: 1.3,   # August - Eid celebrations
        9: 1.1,   # September - Post-Eid normal
        10: 1.2,  # October - Wedding catering
        11: 1.3,  # November - Wedding season
        12: 1.4,  # December - Winter celebrations
    },
    "retail": {
        1: 1.1,   # January - New year shopping
        2: 0.9,   # February - Post-holiday
        3: 0.85,  # March - Quiet period
        4: 0.9,   # April - Normal
        5: 1.0,   # May - Normal
        6: 1.2,   # June - Eid shopping
        7: 0.8,   # July - Ramadan quiet
        8: 1.4,   # August - Eid celebrations
        9: 1.0,   # September - Back to normal
        10: 1.2,  # October - Wedding shopping
        11: 1.3,  # November - Wedding season
        12: 1.5,  # December - Year-end festivities
    }
}

# Economic cycle patterns
ECONOMIC_CYCLES = {
    "inflation_impact_by_sector": {
        "electronics": -0.8,  # High negative impact (imported goods)
        "textile": -0.4,      # Medium negative impact
        "auto": -0.9,         # Very high negative impact
        "food": -0.6,         # High negative impact
        "retail": -0.5,       # Medium-high negative impact
    },
    "pkr_devaluation_impact": {
        "electronics": -0.7,  # Negative (imports expensive)
        "textile": 0.4,       # Positive (exports competitive) 
        "auto": -0.9,         # Very negative (import dependent)
        "food": -0.3,         # Slightly negative (some imported ingredients)
        "retail": -0.4,       # Negative (mixed impact)
    },
    "interest_rate_sensitivity": {
        "electronics": -0.6,  # High sensitivity (financing dependent)
        "textile": -0.3,      # Medium sensitivity
        "auto": -0.8,         # Very high sensitivity (big purchases)
        "food": -0.2,         # Low sensitivity (necessity)
        "retail": -0.4,       # Medium sensitivity
    }
}

def get_current_economic_indicators() -> Dict[str, float]:
    """Get current economic indicators."""
    return CURRENT_ECONOMIC_DATA.copy()

def get_seasonal_factor(sector: str, month: int = None) -> float:
    """Get seasonal adjustment factor for sector."""
    if month is None:
        month = datetime.datetime.now().month
    
    seasonal_data = SEASONAL_PATTERNS.get(sector.lower(), {})
    return seasonal_data.get(month, 1.0)

def calculate_economic_impact(sector: str, business_data: Dict[str, Any]) -> Dict[str, float]:
    """Calculate how economic factors impact the business."""
    economic_data = get_current_economic_indicators()
    
    # Get sector-specific sensitivities
    inflation_impact = ECONOMIC_CYCLES["inflation_impact_by_sector"].get(sector.lower(), -0.5)
    pkr_impact = ECONOMIC_CYCLES["pkr_devaluation_impact"].get(sector.lower(), -0.3)
    interest_impact = ECONOMIC_CYCLES["interest_rate_sensitivity"].get(sector.lower(), -0.4)
    
    # Calculate actual impacts
    inflation_effect = economic_data["inflation_rate"] * inflation_impact
    pkr_effect = ((economic_data["pkr_usd_rate"] - 250) / 250) * pkr_impact  # 250 as baseline
    interest_effect = (economic_data["interest_rate"] - 0.15) * interest_impact  # 15% as baseline
    
    return {
        "inflation_impact": inflation_effect,
        "currency_impact": pkr_effect,
        "interest_rate_impact": interest_effect,
        "total_economic_impact": inflation_effect + pkr_effect + interest_effect,
        "economic_headwind_score": max(0, -(inflation_effect + pkr_effect + interest_effect)),
    }

def get_market_sentiment(sector: str) -> Dict[str, Any]:
    """Get current market sentiment for sector."""
    economic_impact = calculate_economic_impact(sector, {})
    total_impact = economic_impact["total_economic_impact"]
    
    if total_impact < -0.15:
        sentiment = "negative"
        description = "Economic headwinds are creating significant challenges"
    elif total_impact < -0.05:
        sentiment = "cautious"
        description = "Economic conditions are creating some pressure"
    elif total_impact < 0.05:
        sentiment = "neutral"
        description = "Economic conditions are relatively stable"
    elif total_impact < 0.15:
        sentiment = "positive"
        description = "Economic conditions are supportive"
    else:
        sentiment = "very_positive"
        description = "Economic conditions are very favorable"
    
    return {
        "sentiment": sentiment,
        "description": description,
        "confidence_level": 0.8,
        "key_factors": _get_key_economic_factors(sector, economic_impact)
    }

def _get_key_economic_factors(sector: str, economic_impact: Dict[str, float]) -> List[str]:
    """Get key economic factors affecting the sector."""
    factors = []
    
    # Analyze each factor
    if abs(economic_impact["inflation_impact"]) > 0.05:
        if economic_impact["inflation_impact"] < 0:
            factors.append(f"High inflation (29%) is reducing purchasing power")
        else:
            factors.append(f"Inflation trends are supportive")
    
    if abs(economic_impact["currency_impact"]) > 0.03:
        if economic_impact["currency_impact"] < 0:
            factors.append(f"PKR weakness (278/USD) is increasing import costs")
        else:
            factors.append(f"PKR levels are supporting exports")
    
    if abs(economic_impact["interest_rate_impact"]) > 0.03:
        if economic_impact["interest_rate_impact"] < 0:
            factors.append(f"High interest rates (22%) are constraining growth")
        else:
            factors.append(f"Interest rate environment is supportive")
    
    # Add sector-specific factors
    sector_factors = {
        "electronics": ["Supply chain constraints from global chip shortage"],
        "textile": ["Cotton price volatility affecting margins"],
        "auto": ["Import duties and regulatory changes"],
        "food": ["Rising energy and ingredient costs"],
        "retail": ["Consumer spending pressure from inflation"]
    }
    
    factors.extend(sector_factors.get(sector.lower(), []))
    
    return factors[:4]  # Return top 4 factors

def project_economic_trends(months_ahead: int = 6) -> Dict[str, Any]:
    """Project economic trends for planning purposes."""
    current_data = get_current_economic_indicators()
    
    # Simple projection based on current trends
    projected_data = {
        "pkr_usd_rate": current_data["pkr_usd_rate"] * (1 + 0.01 * months_ahead),  # Gradual weakening
        "inflation_rate": max(0.15, current_data["inflation_rate"] - 0.02 * months_ahead),  # Gradual decline
        "interest_rate": max(0.12, current_data["interest_rate"] - 0.01 * months_ahead),  # Gradual easing
        "gdp_growth": min(0.04, current_data["gdp_growth"] + 0.003 * months_ahead),  # Gradual improvement
    }
    
    return {
        "projected_indicators": projected_data,
        "key_trends": [
            "PKR expected to weaken gradually",
            "Inflation projected to decline slowly", 
            "Interest rates likely to ease",
            "GDP growth expected to improve gradually"
        ],
        "confidence_level": max(0.3, 0.8 - 0.05 * months_ahead),  # Lower confidence for longer projections
        "planning_recommendations": [
            "Plan for continued currency pressure",
            "Prepare for gradual inflation relief",
            "Consider investment timing with interest rate cycle",
            "Focus on cost efficiency in near term"
        ]
    }