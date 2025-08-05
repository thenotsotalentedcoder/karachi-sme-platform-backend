# app/data/us_economic_factors.py
"""Economic factors and market conditions affecting US small businesses."""

import datetime
from typing import Dict, List, Any
import math

# Current US economic indicators (realistic US data)
CURRENT_US_ECONOMIC_DATA = {
    "fed_funds_rate": 5.25,      # Current Fed funds rate (%)
    "inflation_rate": 3.2,       # Current US inflation rate (%)
    "unemployment_rate": 3.7,    # Current US unemployment rate (%)
    "gdp_growth": 2.4,          # Annual GDP growth rate (%)
    "consumer_confidence": 102.0, # Consumer Confidence Index
    "small_business_optimism": 89.3, # NFIB Small Business Optimism Index
    "dollar_strength_index": 103.5,  # US Dollar Index
    "energy_cost_index": 1.2,   # Energy cost multiplier
    "supply_chain_stress": 0.3,  # 0-1 scale (much better than 2022)
    "housing_market_index": 0.85, # Housing affordability
    "credit_availability": 0.7,   # Small business credit availability
}

# US Seasonal patterns affecting different sectors
US_SEASONAL_PATTERNS = {
    "electronics": {
        1: 0.9,   # January - Post-holiday lull
        2: 0.85,  # February - Slow period
        3: 0.9,   # March - Spring preparation
        4: 1.0,   # April - Normal
        5: 1.05,  # May - Graduation season
        6: 1.1,   # June - Summer prep
        7: 1.0,   # July - Summer activities
        8: 1.2,   # August - Back to school
        9: 1.15,  # September - Fall activities
        10: 1.1,  # October - Pre-holiday
        11: 1.4,  # November - Black Friday
        12: 1.5,  # December - Holiday peak
    },
    "food": {
        1: 0.8,   # January - New Year resolutions (diet focus)
        2: 0.9,   # February - Valentine's boost
        3: 1.0,   # March - Normal
        4: 1.1,   # April - Spring dining
        5: 1.2,   # May - Graduation parties
        6: 1.3,   # June - Wedding season
        7: 1.2,   # July - Summer gatherings
        8: 1.1,   # August - Summer continues
        9: 1.0,   # September - Back to routine
        10: 1.1,  # October - Fall events
        11: 1.3,  # November - Thanksgiving
        12: 1.4,  # December - Holiday parties
    },
    "retail": {
        1: 0.7,   # January - Returns, post-holiday slump
        2: 0.8,   # February - Winter clearance
        3: 0.9,   # March - Spring preparation
        4: 1.0,   # April - Spring shopping
        5: 1.1,   # May - Mother's Day, graduation
        6: 1.0,   # June - Father's Day
        7: 1.0,   # July - Summer activities
        8: 1.2,   # August - Back to school
        9: 1.0,   # September - Fall transition
        10: 1.1,  # October - Halloween
        11: 1.5,  # November - Black Friday
        12: 1.6,  # December - Holiday shopping
    },
    "auto": {
        1: 1.2,   # January - New year car purchases
        2: 1.1,   # February - President's Day sales
        3: 1.0,   # March - Spring prep
        4: 1.1,   # April - Spring car buying
        5: 1.2,   # May - Memorial Day sales
        6: 1.0,   # June - Summer activities
        7: 0.9,   # July - Vacation season
        8: 1.1,   # August - End of summer
        9: 1.2,   # September - New model year
        10: 1.0,  # October - Fall season
        11: 0.9,  # November - Holiday focus elsewhere
        12: 1.3,  # December - Year-end incentives
    },
    "professional_services": {
        1: 1.3,   # January - New year planning
        2: 1.2,   # February - Business planning
        3: 1.4,   # March - Tax season peak
        4: 1.3,   # April - Tax deadline
        5: 1.0,   # May - Normal operations
        6: 0.9,   # June - Summer slowdown
        7: 0.8,   # July - Vacation season
        8: 0.9,   # August - Vacation continues
        9: 1.2,   # September - Back to business
        10: 1.1,  # October - Q4 planning
        11: 1.0,  # November - Holiday prep
        12: 0.9,  # December - Holiday season
    }
}

# US Economic cycle patterns and sector sensitivities
US_ECONOMIC_CYCLES = {
    "fed_rate_impact_by_sector": {
        "electronics": -0.6,        # High sensitivity (financing dependent)
        "food": -0.2,              # Low sensitivity (necessity)
        "retail": -0.4,            # Medium sensitivity
        "auto": -0.8,              # Very high sensitivity (big purchases)
        "professional_services": -0.3, # Medium-low sensitivity
        "manufacturing": -0.5,      # Medium-high sensitivity
        "construction": -0.7,       # High sensitivity (capital intensive)
        "healthcare": -0.1,         # Very low sensitivity
    },
    "inflation_impact_by_sector": {
        "electronics": -0.5,        # Medium negative (imported components)
        "food": -0.7,              # High negative (food inflation)
        "retail": -0.4,            # Medium negative (mixed products)
        "auto": -0.6,              # High negative (material costs)
        "professional_services": -0.2, # Low negative (service-based)
        "manufacturing": -0.6,      # High negative (input costs)
        "construction": -0.8,       # Very high negative (material costs)
        "healthcare": -0.3,         # Medium negative (some cost pass-through)
    },
    "unemployment_correlation": {
        "electronics": 0.4,         # Positive correlation (disposable income)
        "food": -0.1,              # Slight negative (necessity vs dining out)
        "retail": 0.6,             # High positive (discretionary spending)
        "auto": 0.7,               # Very high positive (major purchases)
        "professional_services": 0.3, # Medium positive (business investment)
        "manufacturing": 0.5,       # High positive (business confidence)
        "construction": 0.8,        # Very high positive (investment driven)
        "healthcare": 0.1,          # Very low correlation (necessity)
    }
}

# US Regional economic multipliers
US_REGIONAL_MULTIPLIERS = {
    "northeast": {
        "cost_of_living": 1.15,
        "wage_premium": 1.12,
        "business_costs": 1.18,
        "market_size": 1.10,
    },
    "southeast": {
        "cost_of_living": 0.92,
        "wage_premium": 0.95,
        "business_costs": 0.88,
        "market_size": 1.05,
    },
    "midwest": {
        "cost_of_living": 0.95,
        "wage_premium": 0.98,
        "business_costs": 0.92,
        "market_size": 0.95,
    },
    "southwest": {
        "cost_of_living": 1.02,
        "wage_premium": 1.05,
        "business_costs": 1.00,
        "market_size": 1.08,
    },
    "west": {
        "cost_of_living": 1.25,
        "wage_premium": 1.20,
        "business_costs": 1.22,
        "market_size": 1.15,
    },
}

def get_current_us_economic_indicators() -> Dict[str, float]:
    """Get current US economic indicators."""
    return CURRENT_US_ECONOMIC_DATA.copy()

def get_us_seasonal_factor(sector: str, month: int = None) -> float:
    """Get seasonal adjustment factor for US sector."""
    if month is None:
        month = datetime.datetime.now().month
    
    seasonal_data = US_SEASONAL_PATTERNS.get(sector.lower(), {})
    return seasonal_data.get(month, 1.0)

def calculate_us_economic_impact(sector: str, business_data: Dict[str, Any]) -> Dict[str, float]:
    """Calculate how US economic factors impact the business."""
    economic_data = get_current_us_economic_indicators()
    
    # Get sector-specific sensitivities
    fed_rate_impact = US_ECONOMIC_CYCLES["fed_rate_impact_by_sector"].get(sector.lower(), -0.4)
    inflation_impact = US_ECONOMIC_CYCLES["inflation_impact_by_sector"].get(sector.lower(), -0.5)
    unemployment_correlation = US_ECONOMIC_CYCLES["unemployment_correlation"].get(sector.lower(), 0.3)
    
    # Calculate actual impacts
    fed_rate_effect = (economic_data["fed_funds_rate"] - 2.5) * fed_rate_impact  # 2.5% neutral rate
    inflation_effect = (economic_data["inflation_rate"] - 2.0) * inflation_impact  # 2% Fed target
    unemployment_effect = (4.0 - economic_data["unemployment_rate"]) * unemployment_correlation  # 4% natural rate
    
    return {
        "fed_rate_impact": fed_rate_effect,
        "inflation_impact": inflation_effect,
        "unemployment_impact": unemployment_effect,
        "total_economic_impact": fed_rate_effect + inflation_effect + unemployment_effect,
        "economic_tailwind_score": max(0, fed_rate_effect + inflation_effect + unemployment_effect),
        "economic_headwind_score": max(0, -(fed_rate_effect + inflation_effect + unemployment_effect)),
    }

def get_us_market_sentiment(sector: str) -> Dict[str, Any]:
    """Get current US market sentiment for sector."""
    economic_impact = calculate_us_economic_impact(sector, {})
    economic_data = get_current_us_economic_indicators()
    total_impact = economic_impact["total_economic_impact"]
    
    # Adjust sentiment based on overall indicators
    confidence_adjustment = (economic_data["consumer_confidence"] - 100) * 0.01
    optimism_adjustment = (economic_data["small_business_optimism"] - 90) * 0.01
    
    adjusted_impact = total_impact + confidence_adjustment + optimism_adjustment
    
    if adjusted_impact < -0.15:
        sentiment = "negative"
        description = "Economic headwinds are creating significant challenges for small businesses"
    elif adjusted_impact < -0.05:
        sentiment = "cautious"
        description = "Economic conditions are creating some pressure on business performance"
    elif adjusted_impact < 0.05:
        sentiment = "neutral"
        description = "Economic conditions are relatively balanced for small businesses"
    elif adjusted_impact < 0.15:
        sentiment = "positive"
        description = "Economic conditions are generally supportive of business growth"
    else:
        sentiment = "very_positive"
        description = "Economic conditions are very favorable for small business expansion"
    
    return {
        "sentiment": sentiment,
        "description": description,
        "confidence_level": 0.85,
        "key_factors": _get_key_us_economic_factors(sector, economic_impact, economic_data)
    }

def _get_key_us_economic_factors(sector: str, economic_impact: Dict[str, float], 
                                economic_data: Dict[str, float]) -> List[str]:
    """Get key US economic factors affecting the sector."""
    factors = []
    
    # Fed rate impact
    if abs(economic_impact["fed_rate_impact"]) > 0.05:
        if economic_impact["fed_rate_impact"] < 0:
            factors.append(f"Fed funds rate at {economic_data['fed_funds_rate']:.1f}% is constraining business investment")
        else:
            factors.append(f"Current Fed funds rate is supportive of business growth")
    
    # Inflation impact
    if abs(economic_impact["inflation_impact"]) > 0.03:
        if economic_impact["inflation_impact"] < 0:
            factors.append(f"Inflation at {economic_data['inflation_rate']:.1f}% is pressuring margins")
        else:
            factors.append(f"Inflation trends are favorable for business operations")
    
    # Employment market
    if abs(economic_impact["unemployment_impact"]) > 0.03:
        if economic_impact["unemployment_impact"] > 0:
            factors.append(f"Strong job market (unemployment {economic_data['unemployment_rate']:.1f}%) boosting consumer demand")
        else:
            factors.append(f"Rising unemployment may reduce consumer spending")
    
    # Consumer confidence
    if economic_data["consumer_confidence"] > 105:
        factors.append("High consumer confidence supporting discretionary spending")
    elif economic_data["consumer_confidence"] < 95:
        factors.append("Low consumer confidence may reduce business demand")
    
    # Small business optimism
    if economic_data["small_business_optimism"] > 95:
        factors.append("High small business optimism indicates favorable conditions")
    elif economic_data["small_business_optimism"] < 85:
        factors.append("Low small business optimism suggests operational challenges")
    
    # Sector-specific factors
    sector_factors = {
        "electronics": ["Global supply chain improvements supporting inventory"],
        "food": ["Rising food costs affecting both input costs and consumer demand"],
        "retail": ["Consumer spending shift between goods and services"],
        "auto": ["Federal EV incentives reshaping automotive market"],
        "professional_services": ["Remote work trends affecting office-based services"],
        "manufacturing": ["Reshoring trends creating domestic opportunities"],
        "construction": ["Housing market dynamics affecting commercial construction"],
        "healthcare": ["Aging population driving consistent demand growth"]
    }
    
    factors.extend(sector_factors.get(sector.lower(), []))
    
    return factors[:5]  # Return top 5 factors

def project_us_economic_trends(months_ahead: int = 6) -> Dict[str, Any]:
    """Project US economic trends for business planning purposes."""
    current_data = get_current_us_economic_indicators()
    
    # Fed policy expectations
    expected_rate_path = {
        3: max(4.5, current_data["fed_funds_rate"] - 0.25),   # Modest easing expected
        6: max(4.0, current_data["fed_funds_rate"] - 0.75),   # Further easing likely
        12: max(3.5, current_data["fed_funds_rate"] - 1.25),  # Longer-term normalization
    }
    
    # Inflation trajectory
    expected_inflation = {
        3: max(2.5, current_data["inflation_rate"] - 0.3),
        6: max(2.2, current_data["inflation_rate"] - 0.6),
        12: max(2.0, current_data["inflation_rate"] - 1.0),
    }
    
    # Select appropriate timeframe
    target_months = min(max(months_ahead, 3), 12)
    timeframes = [3, 6, 12]
    selected_timeframe = min(timeframes, key=lambda x: abs(x - target_months))
    
    projected_data = {
        "fed_funds_rate": expected_rate_path[selected_timeframe],
        "inflation_rate": expected_inflation[selected_timeframe],
        "unemployment_rate": min(4.5, current_data["unemployment_rate"] + 0.1 * (months_ahead / 6)),
        "consumer_confidence": max(95, current_data["consumer_confidence"] - 2 * (months_ahead / 6)),
        "gdp_growth": max(1.5, current_data["gdp_growth"] - 0.1 * (months_ahead / 6)),
    }
    
    return {
        "projected_indicators": projected_data,
        "key_trends": [
            "Fed expected to ease rates gradually",
            "Inflation projected to move toward 2% target",
            "Labor market expected to cool modestly",
            "Consumer confidence may moderate",
            "GDP growth likely to slow but remain positive"
        ],
        "confidence_level": max(0.4, 0.9 - 0.05 * (months_ahead / 3)),
        "planning_recommendations": [
            "Prepare for lower interest rate environment",
            "Plan for continued but moderating inflation pressure",
            "Consider expansion timing with economic cycle",
            "Focus on operational efficiency and cost management",
            "Monitor consumer spending patterns closely"
        ],
        "small_business_implications": {
            "financing": "Borrowing costs may decrease, improving investment opportunities",
            "demand": "Consumer demand likely to moderate but remain stable",
            "costs": "Input cost pressures should ease gradually",
            "competition": "Market consolidation possible as weaker players struggle",
            "opportunities": "Economic transition creates opportunities for agile businesses"
        }
    }

def get_regional_adjustment_factors(state_or_region: str) -> Dict[str, float]:
    """Get regional economic adjustment factors."""
    # Map states to regions (simplified)
    state_to_region = {
        "california": "west", "oregon": "west", "washington": "west", "nevada": "west",
        "texas": "southwest", "arizona": "southwest", "new_mexico": "southwest", "oklahoma": "southwest",
        "florida": "southeast", "georgia": "southeast", "north_carolina": "southeast", "virginia": "southeast",
        "new_york": "northeast", "pennsylvania": "northeast", "massachusetts": "northeast", "new_jersey": "northeast",
        "illinois": "midwest", "ohio": "midwest", "michigan": "midwest", "wisconsin": "midwest",
    }
    
    region = state_to_region.get(state_or_region.lower(), "midwest")  # Default to midwest
    return US_REGIONAL_MULTIPLIERS.get(region, US_REGIONAL_MULTIPLIERS["midwest"])

def calculate_sector_resilience_score(sector: str) -> Dict[str, Any]:
    """Calculate how resilient a sector is to economic downturns."""
    
    # Recession resilience scores (0-1 scale, higher = more resilient)
    resilience_scores = {
        "food": 0.85,                    # High resilience (necessity)
        "healthcare": 0.90,              # Very high resilience (necessity + aging population)
        "professional_services": 0.60,   # Medium resilience (depends on business investment)
        "retail": 0.40,                  # Lower resilience (discretionary spending)
        "electronics": 0.45,             # Lower resilience (discretionary, but essential items resilient)
        "auto": 0.30,                    # Low resilience (major purchases delayed)
        "construction": 0.25,            # Very low resilience (investment driven)
        "manufacturing": 0.50,           # Medium resilience (mixed depending on end market)
    }
    
    base_score = resilience_scores.get(sector.lower(), 0.50)
    
    # Factors that affect resilience
    resilience_factors = {
        "high_resilience": [
            "Essential service or product",
            "Low customer acquisition cost",
            "Recurring revenue model",
            "Local market focus",
            "Low capital requirements"
        ],
        "medium_resilience": [
            "Mixed essential/discretionary products",
            "Established customer base",
            "Some recurring revenue",
            "Regional market presence",
            "Moderate capital needs"
        ],
        "low_resilience": [
            "Primarily discretionary spending",
            "High customer acquisition cost",
            "Project-based revenue",
            "National competition",
            "High capital requirements"
        ]
    }
    
    if base_score >= 0.7:
        resilience_category = "high_resilience"
    elif base_score >= 0.5:
        resilience_category = "medium_resilience"
    else:
        resilience_category = "low_resilience"
    
    return {
        "resilience_score": base_score,
        "resilience_category": resilience_category,
        "key_factors": resilience_factors[resilience_category],
        "recession_preparation": {
            "cash_reserves_months": max(3, int(6 * (1 - base_score))),
            "diversification_priority": "high" if base_score < 0.5 else "medium",
            "cost_flexibility_needed": "high" if base_score < 0.4 else "medium"
        }
    }