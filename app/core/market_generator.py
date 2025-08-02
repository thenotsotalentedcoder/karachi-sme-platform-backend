"""Dynamic market data generation for realistic business intelligence."""

import random
import datetime
import math
from typing import Dict, List, Any, Optional

from app.data.karachi_sectors import get_sector_data, get_location_data
from app.data.economic_factors import get_current_economic_indicators, get_seasonal_factor, calculate_economic_impact


class MarketDataGenerator:
    """Generates realistic, dynamic market data based on actual patterns."""
    
    def __init__(self):
        self.economic_data = get_current_economic_indicators()
        self.base_date = datetime.datetime.now()
        random.seed(42)  # For consistent results during demo
    
    def generate_sector_performance(self, sector: str, days: int = 30) -> List[Dict[str, Any]]:
        """Generate realistic sector performance data over time."""
        
        sector_data = get_sector_data(sector)
        if not sector_data:
            raise ValueError(f"No data available for sector: {sector}")
        
        base_performance = sector_data["base_performance"]
        market_dynamics = sector_data["market_dynamics"]
        
        # Calculate economic impacts
        economic_impact = calculate_economic_impact(sector, {})
        
        # Generate daily performance data
        performance_data = []
        current_index = 100  # Base index value
        
        for day in range(days):
            date = self.base_date - datetime.timedelta(days=days-day-1)
            
            # Calculate daily factors
            trend_factor = base_performance["growth_rate"] / 365  # Daily trend
            volatility = base_performance["volatility"] / math.sqrt(365)  # Daily volatility
            seasonal_factor = get_seasonal_factor(sector, date.month) - 1  # Deviation from normal
            economic_factor = economic_impact["total_economic_impact"] / 365  # Daily economic impact
            
            # Random market noise
            noise = random.gauss(0, volatility)
            
            # Combine all factors
            daily_change = trend_factor + seasonal_factor * 0.1 + economic_factor + noise
            current_index *= (1 + daily_change)
            
            performance_data.append({
                "date": date,
                "index_value": current_index,
                "daily_change": daily_change,
                "volume": random.randint(1000000, 5000000),
                "market_sentiment": self._calculate_market_sentiment(daily_change),
            })
        
        return performance_data
    
    def generate_location_market_data(self, sector: str, location: str) -> Dict[str, Any]:
        """Generate comprehensive market data for specific sector-location combination."""
        
        sector_data = get_sector_data(sector)
        location_data = get_location_data(location)
        
        if not sector_data or not location_data:
            raise ValueError(f"No data available for {sector} in {location}")
        
        # Base calculations
        base_revenue = sector_data["base_performance"]["average_monthly_revenue"]
        location_multiplier = sector_data["location_factors"][location]["multiplier"]
        seasonal_factor = get_seasonal_factor(sector)
        
        # Market size and characteristics
        market_average_revenue = base_revenue * location_multiplier * seasonal_factor
        competition_level = sector_data["location_factors"][location]["competition"]
        rent_factor = sector_data["location_factors"][location]["rent_factor"]
        
        # Generate competitor analysis
        competitor_analysis = self._generate_competitor_analysis(competition_level, market_average_revenue)
        
        # Market trends
        market_trends = self._generate_market_trends(sector, location, sector_data)
        
        return {
            "market_size": {
                "average_monthly_revenue": market_average_revenue,
                "total_market_size": market_average_revenue * competitor_analysis["estimated_businesses"],
                "market_growth_rate": sector_data["base_performance"]["growth_rate"],
                "market_maturity": self._assess_market_maturity(sector, location),
            },
            "competition": {
                "level": competition_level,
                "estimated_competitors": competitor_analysis["competitor_count"],
                "market_concentration": competitor_analysis["market_concentration"],
                "top_performers_share": competitor_analysis["top_performers_share"],
            },
            "location_factors": {
                "foot_traffic": location_data["characteristics"]["foot_traffic"],
                "customer_type": location_data["characteristics"]["customer_type"],
                "rent_cost_factor": rent_factor,
                "accessibility": location_data["characteristics"]["accessibility"],
                "advantages": location_data["advantages"][:3],
                "challenges": location_data["challenges"][:3],
            },
            "market_trends": market_trends,
            "economic_context": calculate_economic_impact(sector, {}),
            "seasonal_patterns": self._generate_seasonal_patterns(sector),
        }
    
    def generate_performance_benchmarks(self, sector: str, location: str) -> Dict[str, Any]:
        """Generate performance benchmarks for comparison."""
        
        market_data = self.generate_location_market_data(sector, location)
        base_revenue = market_data["market_size"]["average_monthly_revenue"]
        
        # Generate distribution of business performance
        percentile_benchmarks = {
            "top_10_percent": base_revenue * 1.8,
            "top_25_percent": base_revenue * 1.4,
            "median": base_revenue * 1.0,
            "bottom_25_percent": base_revenue * 0.7,
            "bottom_10_percent": base_revenue * 0.4,
        }
        
        # Operational benchmarks
        sector_data = get_sector_data(sector)
        operational_benchmarks = {
            "profit_margin": {
                "excellent": sector_data["base_performance"]["typical_profit_margin"] * 1.5,
                "good": sector_data["base_performance"]["typical_profit_margin"] * 1.2,
                "average": sector_data["base_performance"]["typical_profit_margin"],
                "poor": sector_data["base_performance"]["typical_profit_margin"] * 0.7,
            },
            "revenue_growth": {
                "excellent": 0.15,  # 15% monthly growth
                "good": 0.08,
                "average": 0.03,
                "poor": -0.05,
            },
            "customer_retention": {
                "excellent": 0.85,
                "good": 0.75,
                "average": 0.65,
                "poor": 0.45,
            }
        }
        
        return {
            "revenue_benchmarks": percentile_benchmarks,
            "operational_benchmarks": operational_benchmarks,
            "success_factors": sector_data["business_insights"]["success_factors"],
            "common_challenges": sector_data["business_insights"]["common_challenges"],
        }
    
    def calculate_market_opportunity(self, sector: str, location: str, business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate market opportunity and potential."""
        
        market_data = self.generate_location_market_data(sector, location)
        current_revenue = business_data.get("monthly_revenue", [0])[-1]
        
        # Market gap analysis
        market_average = market_data["market_size"]["average_monthly_revenue"]
        top_performer_revenue = market_average * 1.8
        
        # Calculate opportunity gaps
        opportunities = []
        
        # Revenue gap to average
        if current_revenue < market_average:
            revenue_gap = market_average - current_revenue
            opportunities.append({
                "type": "revenue_optimization",
                "description": f"Close gap to market average",
                "potential_value": revenue_gap,
                "timeframe": "3-6 months",
                "probability": 0.8,
            })
        
        # Revenue gap to top performers
        if current_revenue < top_performer_revenue:
            top_gap = top_performer_revenue - current_revenue
            opportunities.append({
                "type": "top_performer_gap",
                "description": f"Reach top 10% performance level",
                "potential_value": top_gap,
                "timeframe": "6-12 months",
                "probability": 0.6,
            })
        
        # Market expansion opportunities
        growth_rate = market_data["market_size"]["market_growth_rate"]
        expansion_potential = current_revenue * growth_rate * 12  # Annual potential
        
        opportunities.append({
            "type": "market_growth",
            "description": f"Benefit from {growth_rate*100:.1f}% sector growth",
            "potential_value": expansion_potential,
            "timeframe": "12 months",
            "probability": 0.9,
        })
        
        # Total addressable market
        total_market = market_data["market_size"]["total_market_size"]
        current_market_share = (current_revenue / total_market) * 100 if total_market > 0 else 0
        
        return {
            "current_market_share": current_market_share,
            "market_size": total_market,
            "growth_opportunities": opportunities,
            "market_attractiveness": self._assess_market_attractiveness(market_data),
            "competitive_positioning": self._assess_competitive_position(current_revenue, market_average),
            "recommended_strategy": self._recommend_market_strategy(current_revenue, market_data),
        }
    
    def _calculate_market_sentiment(self, daily_change: float) -> str:
        """Calculate market sentiment based on performance."""
        if daily_change > 0.02:
            return "very_positive"
        elif daily_change > 0.005:
            return "positive"
        elif daily_change > -0.005:
            return "neutral"
        elif daily_change > -0.02:
            return "negative"
        else:
            return "very_negative"
    
    def _generate_competitor_analysis(self, competition_level: str, market_revenue: float) -> Dict[str, Any]:
        """Generate realistic competitor analysis."""
        
        # Estimate number of businesses based on competition level
        business_counts = {
            "very_high": random.randint(20, 30),
            "high": random.randint(12, 20),
            "medium": random.randint(6, 12),
            "low": random.randint(3, 6),
        }
        
        competitor_count = business_counts.get(competition_level, 10)
        
        # Market concentration (how much top players control)
        concentration_levels = {
            "very_high": 0.4,  # Top 20% control 40% of market
            "high": 0.5,
            "medium": 0.6,
            "low": 0.7,
        }
        
        market_concentration = concentration_levels.get(competition_level, 0.5)
        top_performers_share = 1 - market_concentration
        
        return {
            "competitor_count": f"{competitor_count-2}-{competitor_count+2}",
            "estimated_businesses": competitor_count,
            "market_concentration": market_concentration,
            "top_performers_share": top_performers_share,
        }
    
    def _generate_market_trends(self, sector: str, location: str, sector_data: Dict[str, Any]) -> List[str]:
        """Generate current market trends."""
        
        trends = []
        
        # Economic trends
        if self.economic_data["inflation_rate"] > 0.25:
            trends.append("High inflation driving cost pressures")
        
        if self.economic_data["pkr_usd_rate"] > 270:
            if sector in ["electronics", "auto"]:
                trends.append("PKR weakness making imports expensive")
            elif sector == "textile":
                trends.append("PKR weakness boosting export competitiveness")
        
        # Seasonal trends
        current_month = datetime.datetime.now().month
        seasonal_factor = get_seasonal_factor(sector, current_month)
        
        if seasonal_factor > 1.2:
           trends.append(f"Peak season for {sector} - demand up {(seasonal_factor-1)*100:.0f}%")
        elif seasonal_factor < 0.9:
           trends.append(f"Off-season for {sector} - preparing for recovery")
       
        # Sector-specific trends
        sector_trends = {
            "electronics": [
                "Mobile repair services growing 40% annually",
                "Accessories market expanding faster than devices",
                "Gaming accessories showing strong demand"
            ],
            "textile": [
                "Online fabric sales increasing 60% yearly",
                "Wedding market driving premium demand",
                "Custom tailoring services in high demand"
            ],
            "auto": [
                "Motorcycle parts outselling car parts 3:1",
                "Mobile repair services gaining popularity",
                "Electric vehicle parts market emerging"
            ],
            "food": [
                "Home delivery orders up 80% post-COVID",
                "Healthy food options growing 25% annually",
                "Catering services expanding rapidly"
            ],
            "retail": [
                "Social media marketing driving 50% of sales",
                "Customer loyalty programs showing 30% increase",
                "Online-offline integration becoming essential"
            ]
        }

        sector_specific = sector_trends.get(sector, [])
        trends.extend(random.sample(sector_specific, min(2, len(sector_specific))))

        # Location-specific trends
        location_trends = {
            "clifton": ["Premium market growing 15% annually", "Affluent customer base expanding"],
            "dha": ["Luxury segment showing strong growth", "High-end services in demand"],
            "saddar": ["Volume business model most effective", "Price competition intensifying"],
            "gulshan": ["Middle-class market strengthening", "Family-oriented businesses thriving"],
            "tariq_road": ["Shopping destination traffic increasing", "Brand presence becoming important"],
        }

        location_specific = location_trends.get(location, [])
        trends.extend(location_specific[:1])

        return trends[:5]  # Return top 5 trends
    
    def _generate_seasonal_patterns(self, sector: str) -> Dict[str, Any]:
        """Generate seasonal pattern analysis."""
        
        current_month = datetime.datetime.now().month
        seasonal_factor = get_seasonal_factor(sector, current_month)
        
        # Predict next 3 months
        next_months = []
        for i in range(1, 4):
            next_month = (current_month + i - 1) % 12 + 1
            next_factor = get_seasonal_factor(sector, next_month)
            next_months.append({
                "month": next_month,
                "factor": next_factor,
                "trend": "up" if next_factor > seasonal_factor else "down" if next_factor < seasonal_factor else "stable"
            })
        
        return {
            "current_seasonal_factor": seasonal_factor,
            "seasonal_status": "peak" if seasonal_factor > 1.2 else "low" if seasonal_factor < 0.9 else "normal",
            "next_3_months": next_months,
            "peak_months": self._get_peak_months(sector),
            "low_months": self._get_low_months(sector),
        }
    
    def _assess_market_maturity(self, sector: str, location: str) -> str:
        """Assess market maturity level."""
        
        # Factors: competition level, market size, growth rate
        location_data = get_location_data(location)
        sector_data = get_sector_data(sector)
        
        competition = location_data["characteristics"]["competition"]
        growth_rate = sector_data["base_performance"]["growth_rate"]
        
        if competition == "very_high" and growth_rate < 0.05:
            return "mature"
        elif competition in ["high", "very_high"] and growth_rate < 0.1:
            return "maturing"
        elif competition == "medium" and growth_rate > 0.1:
            return "growing"
        elif competition in ["low", "medium"]:
            return "emerging"
        else:
            return "developing"
    
    def _assess_market_attractiveness(self, market_data: Dict[str, Any]) -> str:
        """Assess overall market attractiveness."""
        
        # Scoring factors
        growth_score = market_data["market_size"]["market_growth_rate"] * 10
        competition_scores = {"low": 4, "medium": 3, "high": 2, "very_high": 1}
        competition_score = competition_scores.get(market_data["competition"]["level"], 2)
        
        traffic_scores = {"very_high": 4, "high": 3, "medium": 2, "low": 1}
        traffic_score = traffic_scores.get(market_data["location_factors"]["foot_traffic"], 2)
        
        total_score = growth_score + competition_score + traffic_score
        
        if total_score >= 8:
            return "highly_attractive"
        elif total_score >= 6:
            return "attractive"
        elif total_score >= 4:
            return "moderately_attractive"
        else:
            return "challenging"
    
    def _assess_competitive_position(self, current_revenue: float, market_average: float) -> str:
        """Assess competitive position."""
        
        if current_revenue >= market_average * 1.5:
            return "market_leader"
        elif current_revenue >= market_average * 1.2:
            return "strong_performer"
        elif current_revenue >= market_average * 0.8:
            return "average_performer"
        elif current_revenue >= market_average * 0.6:
            return "below_average"
        else:
            return "struggling"
    
    def _recommend_market_strategy(self, current_revenue: float, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend market strategy based on position and conditions."""
        
        market_average = market_data["market_size"]["average_monthly_revenue"]
        competition_level = market_data["competition"]["level"]
        growth_rate = market_data["market_size"]["market_growth_rate"]
        
        position = self._assess_competitive_position(current_revenue, market_average)
        
        strategies = {
            "market_leader": {
                "primary_strategy": "market_expansion",
                "focus": "Maintain leadership and expand market share",
                "tactics": ["Premium positioning", "Market expansion", "Innovation leadership"],
            },
            "strong_performer": {
                "primary_strategy": "growth_acceleration", 
                "focus": "Accelerate growth to reach market leadership",
                "tactics": ["Aggressive marketing", "Service enhancement", "Market penetration"],
            },
            "average_performer": {
                "primary_strategy": "differentiation",
                "focus": "Differentiate to stand out from competition",
                "tactics": ["Niche specialization", "Service improvement", "Cost optimization"],
            },
            "below_average": {
                "primary_strategy": "performance_improvement",
                "focus": "Fix fundamental business issues",
                "tactics": ["Operational efficiency", "Cost reduction", "Process improvement"],
            },
            "struggling": {
                "primary_strategy": "business_restructuring",
                "focus": "Fundamental business model review",
                "tactics": ["Business model pivot", "Cost restructuring", "Market repositioning"],
            }
        }
        
        strategy = strategies.get(position, strategies["average_performer"])
        
        # Adjust for market conditions
        if competition_level == "very_high":
            strategy["market_condition_advice"] = "Focus on differentiation due to intense competition"
        elif competition_level == "low":
            strategy["market_condition_advice"] = "Aggressive expansion opportunity due to low competition"
        
        if growth_rate > 0.15:
            strategy["growth_condition_advice"] = "Ride the growth wave - invest in market expansion"
        elif growth_rate < 0.02:
            strategy["growth_condition_advice"] = "Focus on efficiency in slow-growth market"
        
        return strategy
    
    def _get_peak_months(self, sector: str) -> List[int]:
        """Get peak season months for sector."""
        
        peak_months = {
            "electronics": [11, 12, 1],
            "textile": [9, 10, 11],
            "auto": [12, 1, 2],
            "food": [9, 12],
            "retail": [11, 12, 1, 8]
        }
        
        return peak_months.get(sector, [])
    
    def _get_low_months(self, sector: str) -> List[int]:
        """Get low season months for sector."""
        
        low_months = {
            "electronics": [6, 7, 8],
            "textile": [3, 4, 5], 
            "auto": [6, 7],
            "food": [6, 7],
            "retail": [3, 4, 5]
        }
        
        return low_months.get(sector, [])