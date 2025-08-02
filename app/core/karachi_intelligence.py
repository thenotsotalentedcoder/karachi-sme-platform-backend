"""Karachi-specific business intelligence and market analysis."""

from typing import Dict, List, Any, Optional
import datetime
import random
import math

from app.data.karachi_sectors import get_sector_data, get_location_data, get_sector_location_multiplier
from app.data.economic_factors import get_current_economic_indicators, get_seasonal_factor, calculate_economic_impact


class KarachiIntelligence:
    """Core intelligence engine for Karachi market analysis."""
    
    def __init__(self):
        self.economic_data = get_current_economic_indicators()
        self.current_month = datetime.datetime.now().month
    
    def analyze_market_position(self, sector: str, location: str, business_revenue: List[float]) -> Dict[str, Any]:
        """Analyze business position relative to Karachi market."""
        
        # Get sector and location data
        sector_data = get_sector_data(sector)
        location_data = get_location_data(location)
        
        if not sector_data or not location_data:
            raise ValueError(f"No data available for sector '{sector}' in location '{location}'")
        
        # Calculate market benchmarks
        base_revenue = sector_data["base_performance"]["average_monthly_revenue"]
        location_multiplier = get_sector_location_multiplier(sector, location)
        seasonal_factor = get_seasonal_factor(sector, self.current_month)
        
        # Adjusted market average for this specific location
        market_average_revenue = base_revenue * location_multiplier * seasonal_factor
        
        # Calculate business performance
        current_business_revenue = business_revenue[-1] if business_revenue else 0
        business_vs_market = current_business_revenue / market_average_revenue if market_average_revenue > 0 else 0
        
        # Performance categorization
        if business_vs_market >= 1.3:
            performance_category = "top_performer"
            performance_message = f"Excellent! You're in the top 15% of {sector} businesses in {location.title()}"
        elif business_vs_market >= 1.1:
            performance_category = "above_average"
            performance_message = f"Good performance - above average for {sector} businesses in {location.title()}"
        elif business_vs_market >= 0.8:
            performance_category = "average"
            performance_message = f"Average performance for {sector} businesses in {location.title()}"
        elif business_vs_market >= 0.6:
            performance_category = "below_average"
            performance_message = f"Below average - there's room for improvement"
        else:
            performance_category = "underperforming"
            performance_message = f"Significant performance gap detected - immediate action needed"
        
        return {
            "market_average_revenue": market_average_revenue,
            "business_revenue": current_business_revenue,
            "performance_ratio": business_vs_market,
            "performance_category": performance_category,
            "performance_message": performance_message,
            "market_context": {
                "sector_base_revenue": base_revenue,
                "location_advantage": location_multiplier,
                "seasonal_factor": seasonal_factor,
                "competition_level": location_data["characteristics"]["competition"],
            },
            "percentile_rank": self._calculate_percentile_rank(business_vs_market),
        }
    
    def generate_location_insights(self, sector: str, location: str) -> Dict[str, Any]:
        """Generate location-specific insights."""
        
        location_data = get_location_data(location)
        sector_data = get_sector_data(sector)
        
        if not location_data or not sector_data:
            return {}
        
         # Check if this is a good sector-location match
        best_sectors = location_data.get("best_businesses", [])
        is_optimal_location = sector in best_sectors

        # Generate specific insights
        insights = []

        # Location advantages and challenges
        advantages = location_data.get("advantages", [])
        challenges = location_data.get("challenges", [])

        # Competition analysis
        competition_level = location_data["characteristics"]["competition"]
        if competition_level == "very_high":
            insights.append(f"⚠️ Very high competition in {location.title()} - focus on differentiation")
        elif competition_level == "high":
            insights.append(f"🔴 High competition in {location.title()} - competitive pricing essential")
        elif competition_level == "medium":
            insights.append(f"🟡 Moderate competition in {location.title()} - good growth opportunity")
        else:
            insights.append(f"🟢 Low competition in {location.title()} - excellent expansion opportunity")

        # Rent and cost insights
        rent_level = location_data["characteristics"]["rent_level"]
        if rent_level in ["high", "very_high"]:
            insights.append(f"💰 High rental costs in {location.title()} - ensure premium pricing strategy")
        else:
            insights.append(f"💰 Reasonable rental costs in {location.title()} - cost advantage opportunity")

        # Customer insights
        customer_type = location_data["characteristics"]["customer_type"]
        foot_traffic = location_data["characteristics"]["foot_traffic"]

        if customer_type == "affluent":
            insights.append(f"👑 Affluent customers in {location.title()} - focus on quality and service")
        elif customer_type == "price_conscious":
            insights.append(f"💵 Price-conscious customers in {location.title()} - competitive pricing crucial")

        if foot_traffic == "very_high":
            insights.append(f"🚶‍♂️ Excellent foot traffic in {location.title()} - maximize walk-in conversions")
        elif foot_traffic == "high":
            insights.append(f"🚶‍♂️ Good foot traffic in {location.title()} - focus on visibility")

        # Sector-specific location advice
        sector_location_advice = self._get_sector_location_advice(sector, location, location_data)
        insights.extend(sector_location_advice)

        return {
            "is_optimal_location": is_optimal_location,
            "location_score": self._calculate_location_score(sector, location_data),
            "key_insights": insights[:5],  # Top 5 insights
            "advantages": advantages[:3],   # Top 3 advantages
            "challenges": challenges[:3],   # Top 3 challenges
            "customer_profile": {
                "type": customer_type,
                "foot_traffic": foot_traffic,
                "spending_power": self._estimate_spending_power(customer_type),
            },
            "cost_structure": {
                "rent_level": rent_level,
                "competition_pressure": competition_level,
                "accessibility": location_data["characteristics"]["accessibility"],
            }
        }
   
    def identify_growth_opportunities(self, sector: str, location: str, business_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify specific growth opportunities."""
        
        sector_data = get_sector_data(sector)
        location_data = get_location_data(location)
        
        opportunities = []
        
        # Product mix optimization
        high_margin_products = sector_data.get("business_insights", {}).get("high_margin_products", [])
        if high_margin_products:
            opportunities.append({
                "type": "product_optimization",
                "title": "Focus on High-Margin Products",
                "description": f"Shift inventory toward {', '.join(high_margin_products[:2])}",
                "expected_impact": "15-25% profit increase",
                "timeframe": "1-2 months",
                "investment_required": "Low",
                "specific_action": f"Increase {high_margin_products[0]} inventory by 40%",
            })
        
        # Location-specific opportunities
        if location_data["characteristics"]["customer_type"] == "affluent":
            opportunities.append({
                "type": "premium_positioning",
                "title": "Premium Service Strategy",
                "description": "Target affluent customers with premium products/services",
                "expected_impact": "20-30% revenue increase",
                "timeframe": "2-3 months",
                "investment_required": "Medium",
                "specific_action": "Add premium product line and enhance service quality",
            })
        
        # Seasonal opportunities
        seasonal_factor = get_seasonal_factor(sector, self.current_month)
        if seasonal_factor > 1.2:
            opportunities.append({
                "type": "seasonal_optimization",
                "title": "Capitalize on Peak Season",
                "description": f"This is peak season for {sector} - maximize inventory and marketing",
                "expected_impact": f"{int((seasonal_factor - 1) * 100)}% seasonal boost available",
                "timeframe": "Immediate",
                "investment_required": "Medium",
                "specific_action": "Increase inventory by 50% and run promotional campaigns",
            })
        
        # Competition-based opportunities
        competition_level = location_data["characteristics"]["competition"]
        if competition_level in ["low", "medium"]:
            opportunities.append({
                "type": "market_expansion",
                "title": "Market Share Growth",
                "description": f"Lower competition in {location.title()} allows for aggressive growth",
                "expected_impact": "25-40% market share increase",
                "timeframe": "3-6 months",
                "investment_required": "High", 
                "specific_action": "Expand marketing and consider additional services",
            })
        
        # Technology/digital opportunities
        if sector in ["electronics", "retail", "textile"]:
            opportunities.append({
                "type": "digital_expansion",
                "title": "Online Presence Development",
                "description": "Develop online sales channels and social media presence",
                "expected_impact": "30-50% new customer acquisition",
                "timeframe": "2-4 months",
                "investment_required": "Low",
                "specific_action": "Create Instagram business account and WhatsApp catalog",
            })
        
        return opportunities[:4]  # Return top 4 opportunities
    
    def analyze_competitive_landscape(self, sector: str, location: str) -> Dict[str, Any]:
        """Analyze competitive environment."""
        
        location_data = get_location_data(location)
        sector_data = get_sector_data(sector)
        
        competition_level = location_data["characteristics"]["competition"]
        
        # Estimate number of competitors
        competitor_density = {
            "very_high": {"count": "15-25", "radius": "500m"},
            "high": {"count": "8-15", "radius": "800m"},
            "medium": {"count": "4-8", "radius": "1km"},
            "low": {"count": "2-4", "radius": "2km"},
        }
        
        density_info = competitor_density.get(competition_level, competitor_density["medium"])
        
        # Competition strategies
        if competition_level == "very_high":
            competitive_strategy = [
                "Focus on niche specialization",
                "Provide exceptional customer service",
                "Optimize operational efficiency",
                "Consider unique value propositions"
            ]
            market_strategy = "differentiation"
        elif competition_level == "high":
            competitive_strategy = [
                "Competitive pricing essential",
                "Build customer loyalty programs",
                "Focus on product quality",
                "Improve service speed"
            ]
            market_strategy = "competitive_positioning"
        elif competition_level == "medium":
            competitive_strategy = [
                "Expand market share aggressively",
                "Introduce new product lines",
                "Build brand recognition",
                "Consider partnerships"
            ]
            market_strategy = "market_growth"
        else:
            competitive_strategy = [
                "Establish market dominance",
                "Set premium pricing",
                "Build customer base quickly",
                "Prepare for future competition"
            ]
            market_strategy = "market_leadership"
        
        return {
            "competition_level": competition_level,
            "estimated_competitors": density_info["count"],
            "competition_radius": density_info["radius"],
            "market_strategy": market_strategy,
            "competitive_strategies": competitive_strategy,
            "market_share_opportunity": self._estimate_market_share_opportunity(competition_level),
            "key_success_factors": sector_data.get("business_insights", {}).get("success_factors", [])[:3],
        }
    
    def calculate_expansion_readiness(self, business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate readiness for business expansion."""
        
        # Extract key metrics
        monthly_revenue = business_data.get("monthly_revenue", [])
        current_cash = business_data.get("current_cash", 0)
        monthly_expenses = business_data.get("monthly_expenses", 0)
        years_in_business = business_data.get("years_in_business", 0)
        
        # Calculate financial health metrics
        if len(monthly_revenue) >= 3:
            revenue_trend = self._calculate_revenue_trend(monthly_revenue)
            revenue_stability = self._calculate_revenue_stability(monthly_revenue)
        else:
            revenue_trend = 0
            revenue_stability = 0.5
        
        current_revenue = monthly_revenue[-1] if monthly_revenue else 0
        cash_runway = current_cash / monthly_expenses if monthly_expenses > 0 else 0
        
        # Scoring factors (0-1 scale)
        financial_score = min(1.0, cash_runway / 6)  # 6 months cash runway = full score
        growth_score = max(0, min(1.0, revenue_trend * 2))  # 50% growth = full score
        stability_score = revenue_stability
        experience_score = min(1.0, years_in_business / 3)  # 3 years = full score
        
        # Overall readiness score
        overall_score = (financial_score * 0.3 + growth_score * 0.3 + 
                        stability_score * 0.2 + experience_score * 0.2)
        
        # Readiness assessment
        if overall_score >= 0.8:
            readiness_level = "highly_ready"
            recommendation = "Excellent expansion candidate - proceed with confidence"
        elif overall_score >= 0.6:
            readiness_level = "ready"
            recommendation = "Good expansion candidate - plan carefully"
        elif overall_score >= 0.4:
            readiness_level = "cautiously_ready"
            recommendation = "Consider expansion after strengthening current business"
        else:
            readiness_level = "not_ready"
            recommendation = "Focus on current business stability before expanding"
        
        return {
            "overall_score": overall_score,
            "readiness_level": readiness_level,
            "recommendation": recommendation,
            "component_scores": {
                "financial_health": financial_score,
                "growth_trajectory": growth_score,
                "revenue_stability": stability_score,
                "business_experience": experience_score,
            },
            "key_strengths": self._identify_expansion_strengths(financial_score, growth_score, stability_score, experience_score),
            "areas_to_improve": self._identify_expansion_weaknesses(financial_score, growth_score, stability_score, experience_score),
            "next_steps": self._get_expansion_next_steps(readiness_level, business_data),
        }
    
    def _calculate_percentile_rank(self, performance_ratio: float) -> int:
        """Calculate percentile rank based on performance ratio."""
        if performance_ratio >= 1.5:
            return 95
        elif performance_ratio >= 1.3:
            return 85
        elif performance_ratio >= 1.1:
            return 70
        elif performance_ratio >= 0.9:
            return 50
        elif performance_ratio >= 0.7:
            return 30
        elif performance_ratio >= 0.5:
            return 15
        else:
            return 5
    
    def _calculate_location_score(self, sector: str, location_data: Dict[str, Any]) -> int:
        """Calculate location suitability score for sector."""
        
        characteristics = location_data["characteristics"]
        
        # Base scoring
        traffic_scores = {"very_high": 25, "high": 20, "medium": 15, "low": 10}
        competition_scores = {"low": 25, "medium": 20, "high": 15, "very_high": 10}
        rent_scores = {"low": 25, "medium": 20, "medium_high": 15, "high": 10, "very_high": 5}
        
        score = (
            traffic_scores.get(characteristics["foot_traffic"], 15) +
            competition_scores.get(characteristics["competition"], 15) +
            rent_scores.get(characteristics["rent_level"], 15)
        )
        
        # Sector-specific adjustments
        if sector == "food" and characteristics["customer_type"] == "affluent":
            score += 15
        elif sector == "electronics" and characteristics["foot_traffic"] == "very_high":
            score += 10
        elif sector == "auto" and characteristics["accessibility"] == "excellent":
            score += 10
        
        return min(100, score)
    
    def _get_sector_location_advice(self, sector: str, location: str, location_data: Dict[str, Any]) -> List[str]:
        """Get sector-specific advice for location."""
        
        advice = []
        characteristics = location_data["characteristics"]
        
        if sector == "electronics":
            if location in ["saddar", "tariq_road"]:
                advice.append("📱 Focus on mobile accessories - higher margins than phones")
            if characteristics["foot_traffic"] == "very_high":
                advice.append("🔧 Add mobile repair services - Rs. 500+ profit per repair")
        
        elif sector == "textile":
            if location in ["tariq_road", "clifton"]:
                advice.append("👗 Target wedding customers - 3x higher margins")
            if characteristics["customer_type"] == "affluent":
                advice.append("✨ Focus on designer and premium fabrics")
        
        elif sector == "food":
            if characteristics["customer_type"] == "affluent":
                advice.append("🍽️ Premium pricing strategy - customers will pay 20% more")
            if location in ["clifton", "dha"]:
                advice.append("🚚 Home delivery essential - 50% of orders")
        
        elif sector == "auto":
            if location in ["korangi", "landhi"]:
                advice.append("🏍️ Focus on motorcycle parts - higher volume market")
            advice.append("🔧 Offer mobile repair services - premium pricing opportunity")
        
        elif sector == "retail":
            if characteristics["foot_traffic"] == "high":
                advice.append("🎁 Impulse purchase items near entrance")
            if location == "saddar":
                advice.append("💰 Volume-based pricing strategy essential")
        
        return advice
    
    def _estimate_spending_power(self, customer_type: str) -> str:
        """Estimate customer spending power."""
        spending_levels = {
            "affluent": "high",
            "middle_class": "medium",
            "working_class": "low",
            "price_conscious": "low",
            "mixed": "medium"
        }
        return spending_levels.get(customer_type, "medium")
    
    def _estimate_market_share_opportunity(self, competition_level: str) -> str:
        """Estimate market share growth opportunity."""
        opportunities = {
            "low": "high",
            "medium": "medium", 
            "high": "low",
            "very_high": "very_low"
        }
        return opportunities.get(competition_level, "medium")
    
    def _calculate_revenue_trend(self, monthly_revenue: List[float]) -> float:
        """Calculate revenue growth trend."""
        if len(monthly_revenue) < 2:
            return 0
        
        # Calculate month-over-month growth rates
        growth_rates = []
        for i in range(1, len(monthly_revenue)):
            if monthly_revenue[i-1] > 0:
                growth_rate = (monthly_revenue[i] - monthly_revenue[i-1]) / monthly_revenue[i-1]
                growth_rates.append(growth_rate)
        
        # Return average growth rate
        return sum(growth_rates) / len(growth_rates) if growth_rates else 0
    
    def _calculate_revenue_stability(self, monthly_revenue: List[float]) -> float:
        """Calculate revenue stability score."""
        if len(monthly_revenue) < 3:
            return 0.5
        
        # Calculate coefficient of variation (lower = more stable)
        mean_revenue = sum(monthly_revenue) / len(monthly_revenue)
        if mean_revenue == 0:
            return 0
        
        variance = sum((x - mean_revenue) ** 2 for x in monthly_revenue) / len(monthly_revenue)
        std_dev = math.sqrt(variance)
        cv = std_dev / mean_revenue
        
        # Convert to stability score (0-1, where 1 = most stable)
        return max(0, 1 - cv)
    
    def _identify_expansion_strengths(self, financial: float, growth: float, stability: float, experience: float) -> List[str]:
        """Identify strengths for expansion."""
        strengths = []
        
        if financial >= 0.7:
            strengths.append("Strong cash position for expansion investment")
        if growth >= 0.7:
            strengths.append("Excellent revenue growth trajectory")
        if stability >= 0.7:
            strengths.append("Stable and predictable revenue streams")
        if experience >= 0.7:
            strengths.append("Proven business model and experience")
        
        return strengths[:3]
    
    def _identify_expansion_weaknesses(self, financial: float, growth: float, stability: float, experience: float) -> List[str]:
        """Identify areas to improve before expansion."""
        weaknesses = []
        
        if financial < 0.5:
            weaknesses.append("Build cash reserves - need 6+ months operating expenses")
        if growth < 0.3:
            weaknesses.append("Improve current business growth before expanding")
        if stability < 0.5:
            weaknesses.append("Stabilize revenue fluctuations in current business")
        if experience < 0.5:
            weaknesses.append("Gain more operational experience in current market")
        
        return weaknesses[:3]
    
    def _get_expansion_next_steps(self, readiness_level: str, business_data: Dict[str, Any]) -> List[str]:
        """Get specific next steps for expansion."""
        
        if readiness_level == "highly_ready":
            return [
                "Identify target expansion location",
                "Secure expansion financing",
                "Develop detailed expansion plan",
                "Begin location scouting"
            ]
        elif readiness_level == "ready":
            return [
                "Build additional cash reserves",
                "Document current business processes",
                "Research expansion markets",
                "Create expansion timeline"
            ]
        elif readiness_level == "cautiously_ready":
            return [
                "Optimize current business profitability",
                "Build 6-month cash runway",
                "Strengthen operational systems",
                "Reassess in 6 months"
            ]
        else:
            return [
                "Focus on current business growth",
                "Improve cash flow management",
                "Build operational stability",
                "Delay expansion plans for 12+ months"
            ]    