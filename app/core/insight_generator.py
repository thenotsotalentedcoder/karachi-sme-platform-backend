"""Generate simple, actionable business insights using intelligent algorithms."""

from typing import Dict, List, Any, Optional, Tuple
import random
from datetime import datetime

from app.core.karachi_intelligence import KarachiIntelligence
from app.data.karachi_sectors import get_sector_data
from app.data.economic_factors import calculate_economic_impact


class InsightGenerator:
    """Generate simple, clear, actionable business insights."""
    
    def __init__(self):
        self.karachi_intel = KarachiIntelligence()
    
    def generate_main_insight(self, analysis_result: Dict[str, Any], 
                            business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate the main insight - the big message for the business owner."""
        
        sector = business_data["sector"]
        location = business_data["location_area"]
        monthly_revenue = business_data["monthly_revenue"]
        
        # Get key metrics
        performance_metrics = analysis_result["performance_metrics"]
        market_position = analysis_result["market_position"]
        financial_health = analysis_result["financial_health"]
        
        current_revenue = performance_metrics["current_revenue"]
        market_average = market_position["market_average_revenue"]
        performance_ratio = market_position["performance_ratio"]
        revenue_trend = performance_metrics["revenue_trend"]
        
        # Determine the main insight type and message
        insight = self._determine_primary_insight(
            performance_ratio, revenue_trend, current_revenue, 
            market_average, sector, location, financial_health
        )
        
        return {
            "insight_type": insight["type"],
            "urgency": insight["urgency"],
            "title": insight["title"],
            "main_message": insight["message"],
            "supporting_facts": insight["facts"],
            "confidence_level": insight["confidence"],
            "emotional_tone": insight["tone"],
        }
    
    def generate_problem_insights(self, analysis_result: Dict[str, Any],
                                business_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate specific problem identification insights."""
        
        insights = []
        
        # Revenue performance problems
        revenue_insights = self._analyze_revenue_problems(analysis_result, business_data)
        insights.extend(revenue_insights)
        
        # Market position problems
        market_insights = self._analyze_market_problems(analysis_result, business_data)
        insights.extend(market_insights)
        
        # Financial health problems
        financial_insights = self._analyze_financial_problems(analysis_result, business_data)
        insights.extend(financial_insights)
        
        # Competition problems
        competition_insights = self._analyze_competition_problems(analysis_result, business_data)
        insights.extend(competition_insights)
        
        # Return top 3 most important problems
        return sorted(insights, key=lambda x: x["impact_score"], reverse=True)[:3]
    
    def generate_opportunity_insights(self, analysis_result: Dict[str, Any],
                                    business_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate opportunity identification insights."""
        
        insights = []
        
        # Market opportunities
        market_opportunities = self._identify_market_opportunities(analysis_result, business_data)
        insights.extend(market_opportunities)
        
        # Product/service opportunities
        product_opportunities = self._identify_product_opportunities(analysis_result, business_data)
        insights.extend(product_opportunities)
        
        # Operational opportunities
        operational_opportunities = self._identify_operational_opportunities(analysis_result, business_data)
        insights.extend(operational_opportunities)
        
        # Financial opportunities
        financial_opportunities = self._identify_financial_opportunities(analysis_result, business_data)
        insights.extend(financial_opportunities)
        
        # Return top 3 opportunities
        return sorted(insights, key=lambda x: x["potential_value"], reverse=True)[:3]
    
    def _determine_primary_insight(self, performance_ratio: float, revenue_trend: str,
                                 current_revenue: float, market_average: float,
                                 sector: str, location: str, 
                                 financial_health: Dict[str, Any]) -> Dict[str, Any]:
        """Determine the primary insight for the business."""
        
        # Performance gap analysis
        revenue_gap = market_average - current_revenue
        gap_percentage = abs(performance_ratio - 1) * 100
        
        # Critical financial issues take priority
        if financial_health["status"] == "critical":
            return {
                "type": "critical_financial",
                "urgency": "immediate",
                "title": "🚨 URGENT: Cash Flow Crisis Detected",
                "message": f"Your {sector} business is facing serious financial difficulties. Immediate action required to avoid closure.",
                "facts": [
                    f"Current financial health: {financial_health['status'].title()}",
                    f"Monthly losses detected",
                    f"Cash runway critically low"
                ],
                "confidence": 0.95,
                "tone": "urgent"
            }
        
        # Major underperformance
        elif performance_ratio < 0.7 and revenue_trend == "declining":
            return {
                "type": "underperforming_declining",
                "urgency": "high", 
                "title": "🔴 YOUR BUSINESS IS FALLING BEHIND",
                "message": f"Your {sector} shop in {location.title()} is earning Rs. {current_revenue:,.0f} while similar businesses average Rs. {market_average:,.0f}. The gap is growing.",
                "facts": [
                    f"You're {gap_percentage:.0f}% below market average",
                    f"Revenue trend: {revenue_trend}",
                    f"Monthly gap: Rs. {revenue_gap:,.0f}"
                ],
                "confidence": 0.9,
                "tone": "concerned"
            }
        
        # Underperforming but stable
        elif performance_ratio < 0.8:
            problem_cause = self._identify_underperformance_cause(sector, location, performance_ratio)
            return {
                "type": "underperforming_stable",
                "urgency": "medium",
                "title": "📊 YOU'RE MISSING OUT ON PROFITS",
                "message": f"Your {sector} business could earn Rs. {revenue_gap:,.0f} more monthly. {problem_cause}",
                "facts": [
                    f"Current revenue: Rs. {current_revenue:,.0f}",
                    f"Market potential: Rs. {market_average:,.0f}",
                    f"Missing opportunity: Rs. {revenue_gap:,.0f}/month"
                ],
                "confidence": 0.85,
                "tone": "motivational"
            }
        
        # Good performance with growth potential
        elif performance_ratio > 1.2 and revenue_trend == "increasing":
            return {
                "type": "high_performer",
                "urgency": "low",
                "title": "🟢 EXCELLENT! YOU'RE A TOP PERFORMER",
                "message": f"Your {sector} business is crushing it! You're earning {gap_percentage:.0f}% more than average. Time to think bigger.",
                "facts": [
                    f"Revenue: Rs. {current_revenue:,.0f} vs market Rs. {market_average:,.0f}",
                    f"Performance: Top {100-self._calculate_percentile(performance_ratio):.0f}% in {location.title()}",
                    f"Trend: {revenue_trend}"
                ],
                "confidence": 0.9,
                "tone": "celebratory"
            }
        
        # Average performance - improvement possible
        elif 0.8 <= performance_ratio <= 1.2:
            improvement_area = self._identify_improvement_opportunity(sector, location)
            return {
                "type": "average_performance",
                "urgency": "medium",
                "title": "📈 GOOD FOUNDATION, READY FOR GROWTH",
                "message": f"Your {sector} business is performing normally. {improvement_area} could boost profits significantly.",
                "facts": [
                    f"Current position: Average performer in {location.title()}",
                    f"Revenue stability: {revenue_trend}",
                    f"Growth potential: High"
                ],
                "confidence": 0.8,
                "tone": "encouraging"
            }
        
        # Strong performance but declining
        elif performance_ratio > 1.0 and revenue_trend == "declining":
            return {
                "type": "declining_leader",
                "urgency": "high",
                "title": "⚠️ WARNING: STRONG BUSINESS WEAKENING",
                "message": f"You're still above average but losing ground fast. Revenue dropped while market stayed strong.",
                "facts": [
                    f"Still {gap_percentage:.0f}% above market average",
                    f"But revenue is {revenue_trend}",
                    f"Market is stable - problem is internal"
                ],
                "confidence": 0.88,
                "tone": "warning"
            }
        
        # Default case
        else:
            return {
                "type": "mixed_signals",
                "urgency": "medium",
                "title": "📊 MIXED SIGNALS IN YOUR BUSINESS",
                "message": f"Your {sector} business shows both strengths and challenges. Let's focus on the biggest opportunities.",
                "facts": [
                    f"Revenue: Rs. {current_revenue:,.0f}",
                    f"Market position: {'Above' if performance_ratio > 1 else 'Below'} average",
                    f"Trend: {revenue_trend}"
                ],
                "confidence": 0.75,
                "tone": "analytical"
            }
    
    def _analyze_revenue_problems(self, analysis_result: Dict[str, Any],
                                business_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze revenue-specific problems."""
        
        problems = []
        performance_metrics = analysis_result["performance_metrics"]
        
        # Declining revenue
        if performance_metrics["revenue_trend"] == "declining":
            revenue_data = business_data["monthly_revenue"]
            decline_amount = revenue_data[0] - revenue_data[-1] if len(revenue_data) >= 2 else 0
            
            problems.append({
                "type": "revenue_decline",
                "title": "Revenue Dropping Fast",
                "description": f"Monthly revenue declined by Rs. {decline_amount:,.0f} over 6 months",
                "impact_amount": decline_amount * 12,  # Annual impact
                "impact_score": 90,
                "urgency": "high",
                "root_cause": self._identify_revenue_decline_cause(business_data),
            })
        
        # Low revenue growth
        elif performance_metrics["revenue_growth_rate"] < 0.02:  # Less than 2% monthly growth
            problems.append({
                "type": "stagnant_revenue",
                "title": "Revenue Growth Stalled",
                "description": "Business growth has plateaued - missing market opportunities",
                "impact_amount": performance_metrics["current_revenue"] * 0.15,  # 15% potential increase
                "impact_score": 70,
                "urgency": "medium",
                "root_cause": "Need new growth strategies and market expansion",
            })
        
        # Revenue volatility
        if performance_metrics["revenue_stability"] < 0.6:
            problems.append({
                "type": "revenue_volatility",
                "title": "Unpredictable Revenue Swings",
                "description": "Revenue fluctuates too much - hard to plan and manage cash flow",
                "impact_amount": performance_metrics["current_revenue"] * 0.1,
                "impact_score": 60,
                "urgency": "medium",
                "root_cause": "Need more stable customer base and revenue streams",
            })
        
        return problems
    
    def _analyze_market_problems(self, analysis_result: Dict[str, Any],
                               business_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze market position problems."""
        
        problems = []
        market_position = analysis_result["market_position"]
        sector = business_data["sector"]
        location = business_data["location_area"]
        
        # Significantly below market average
        if market_position["performance_ratio"] < 0.7:
            gap = market_position["market_average_revenue"] - market_position["business_revenue"]
            
            problems.append({
                "type": "market_underperformance",
                "title": "Falling Behind Competitors",
                "description": f"Other {sector} businesses in {location.title()} are earning Rs. {gap:,.0f} more per month",
                "impact_amount": gap,
                "impact_score": 85,
                "urgency": "high",
                "root_cause": self._identify_competitive_disadvantage(sector, location, market_position),
            })
        
        # High competition area
        competition_level = market_position["market_context"]["competition_level"]
        if competition_level in ["high", "very_high"]:
            problems.append({
                "type": "intense_competition",
                "title": f"{competition_level.replace('_', ' ').title()} Competition Pressure",
                "description": f"Too many competitors in {location.title()} - price pressure and customer loss",
                "impact_amount": market_position["business_revenue"] * 0.12,
                "impact_score": 75,
                "urgency": "medium",
                "root_cause": "Need differentiation strategy to stand out from competitors",
            })
        
        return problems
    
    def _analyze_financial_problems(self, analysis_result: Dict[str, Any],
                                  business_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze financial health problems."""
        
        problems = []
        financial_health = analysis_result["financial_health"]
        performance_metrics = analysis_result["performance_metrics"]
        
        # Low profit margins
        if performance_metrics["profit_margin"] < 0.15:  # Less than 15%
            problems.append({
                "type": "low_profit_margin",
                "title": "Profit Margins Too Low",
                "description": f"Only {performance_metrics['profit_margin']*100:.1f}% profit margin - should be 20%+",
                "impact_amount": performance_metrics["current_revenue"] * 0.05,  # 5% improvement potential
                "impact_score": 80,
                "urgency": "high",
                "root_cause": "Either prices too low or costs too high - need pricing/cost review",
            })
        
        # Cash flow problems
        if performance_metrics["cash_runway_months"] < 3:
            problems.append({
                "type": "cash_flow_crisis",
                "title": "Dangerous Cash Flow Situation",
                "description": f"Only {performance_metrics['cash_runway_months']:.1f} months of cash left",
                "impact_amount": business_data["monthly_expenses"] * 6,  # Need 6 months runway
                "impact_score": 95,
                "urgency": "immediate",
                "root_cause": "Need immediate cash flow improvement and expense control",
            })
        
        return problems
    
    def _analyze_competition_problems(self, analysis_result: Dict[str, Any],
                                    business_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze competition-related problems."""
        
        problems = []
        sector = business_data["sector"]
        location = business_data["location_area"]
        
        # Get sector data for insights
        sector_data = get_sector_data(sector)
        if not sector_data:
            return problems
        
        # Low margin products focus
        current_revenue = analysis_result["performance_metrics"]["current_revenue"]
        market_average = analysis_result["market_position"]["market_average_revenue"]
        
        if current_revenue < market_average * 0.8:
            low_margin_products = sector_data["business_insights"]["low_margin_products"]
            
            problems.append({
                "type": "wrong_product_focus",
                "title": "Focusing on Wrong Products",
                "description": f"Too much focus on {low_margin_products[0]} - low profit items",
                "impact_amount": current_revenue * 0.18,  # 18% potential improvement
                "impact_score": 82,
                "urgency": "medium",
                "root_cause": f"Switch from {low_margin_products[0]} to higher-margin alternatives",
            })
        
        return problems
    
    def _identify_market_opportunities(self, analysis_result: Dict[str, Any],
                                     business_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify market-based opportunities."""
        
        opportunities = []
        sector = business_data["sector"]
        location = business_data["location_area"]
        sector_data = get_sector_data(sector)
        
        if not sector_data:
            return opportunities
        
        # High-margin product opportunities
        high_margin_products = sector_data["business_insights"]["high_margin_products"]
        current_revenue = analysis_result["performance_metrics"]["current_revenue"]
        
        opportunities.append({
            "type": "product_mix_optimization",
            "title": f"Switch to {high_margin_products[0].replace('_', ' ').title()}",
            "description": f"Focus on {high_margin_products[0]} - 40% profit vs current 12%",
            "potential_value": current_revenue * 0.25,  # 25% revenue increase potential
            "timeframe": "1-2 months",
            "implementation_ease": "easy",
            "specific_action": f"Reduce current inventory, stock more {high_margin_products[0]}",
        })
        
        # Growth opportunities from sector data
        growth_opportunities = sector_data["business_insights"]["growth_opportunities"]
        if growth_opportunities:
            opportunities.append({
                "type": "new_service_opportunity",
                "title": f"Add {growth_opportunities[0].replace('_', ' ').title()} Service",
                "description": f"{growth_opportunities[0]} market is growing 40% annually in Karachi",
                "potential_value": current_revenue * 0.3,
                "timeframe": "2-3 months",
                "implementation_ease": "medium",
                "specific_action": f"Learn {growth_opportunities[0]} skills and promote new service",
            })
        
        return opportunities
    
    def _identify_product_opportunities(self, analysis_result: Dict[str, Any],
                                      business_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify product/service opportunities."""
        
        opportunities = []
        sector = business_data["sector"]
        current_revenue = analysis_result["performance_metrics"]["current_revenue"]
        
        # Sector-specific opportunities
        if sector == "electronics":
            opportunities.append({
                "type": "repair_service_addition",
                "title": "Add Mobile Repair Service",
                "description": "Rs. 500 profit per repair - 10 repairs daily = Rs. 150K monthly",
                "potential_value": 150000,
                "timeframe": "2-4 weeks",
                "implementation_ease": "easy",
                "specific_action": "Buy repair kit (Rs. 25K), learn basic repairs, put up sign",
            })
        
        elif sector == "food":
            opportunities.append({
                "type": "delivery_service",
                "title": "Start Home Delivery",
                "description": "50% of food orders now delivery - missing huge market",
                "potential_value": current_revenue * 0.5,
                "timeframe": "1-2 weeks", 
                "implementation_ease": "easy",
                "specific_action": "Partner with Foodpanda or start WhatsApp delivery service",
            })
        
        elif sector == "textile":
            opportunities.append({
                "type": "wedding_specialization",
                "title": "Focus on Wedding Market",
                "description": "Wedding fabrics sell for 3x regular price - it's wedding season",
                "potential_value": current_revenue * 0.8,
                "timeframe": "immediate",
                "implementation_ease": "easy",
                "specific_action": "Stock red/gold fabrics, target bridal customers",
            })
        
        return opportunities
    
    def _identify_operational_opportunities(self, analysis_result: Dict[str, Any],
                                          business_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify operational improvement opportunities."""
        
        opportunities = []
        current_revenue = analysis_result["performance_metrics"]["current_revenue"]
        profit_margin = analysis_result["performance_metrics"]["profit_margin"]
        
        # Low profit margin improvement
        if profit_margin < 0.18:
            opportunities.append({
                "type": "margin_improvement",
                "title": "Improve Profit Margins",
                "description": f"Current {profit_margin*100:.1f}% margin - target 22% through pricing/costs",
                "potential_value": current_revenue * 0.05,  # 5% revenue increase from better margins
                "timeframe": "1 month",
                "implementation_ease": "medium",
                "specific_action": "Review all prices and supplier costs - optimize mix",
            })
        
        # Digital presence opportunity
        opportunities.append({
            "type": "digital_presence",
            "title": "Build Online Presence", 
            "description": "70% of customers check online first - you're invisible",
            "potential_value": current_revenue * 0.3,
            "timeframe": "2-3 weeks",
            "implementation_ease": "easy",
            "specific_action": "Create Instagram business page, post daily photos",
        })
        
        return opportunities
    
    def _identify_financial_opportunities(self, analysis_result: Dict[str, Any],
                                        business_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify financial optimization opportunities."""
        
        opportunities = []
        current_cash = business_data["current_cash"]
        monthly_expenses = business_data["monthly_expenses"]
        
        # Investment opportunity
        if current_cash > monthly_expenses * 3:  # Have excess cash
            investment_amount = min(current_cash * 0.3, 200000)  # Max 30% or 200K
            
            opportunities.append({
                "type": "investment_opportunity",
                "title": "Invest Idle Cash",
                "description": f"Rs. {current_cash:,.0f} sitting idle - inflation eating 29% yearly",
                "potential_value": investment_amount * 0.18,  # 18% annual return
                "timeframe": "immediate",
                "implementation_ease": "easy",
                "specific_action": f"Invest Rs. {investment_amount:,.0f} in sector stocks or business expansion",
            })
        
        return opportunities
    
    # Helper methods
    
    def _identify_underperformance_cause(self, sector: str, location: str, performance_ratio: float) -> str:
        """Identify likely cause of underperformance."""
        
        if performance_ratio < 0.6:
            return "Major operational issues or wrong business model"
        elif performance_ratio < 0.8:
            if sector == "electronics":
                return "Likely selling phones instead of accessories"
            elif sector == "food":
                return "Missing delivery market or location issues"
            elif sector == "textile":
                return "Not targeting wedding customers"
            elif sector == "auto":
                return "Wrong parts mix or location problem"
            else:
                return "Product mix or pricing strategy needs review"
        else:
            return "Minor optimization needed"
    
    def _calculate_percentile(self, performance_ratio: float) -> int:
        """Calculate approximate percentile rank."""
        if performance_ratio >= 1.8:
            return 95
        elif performance_ratio >= 1.5:
            return 85
        elif performance_ratio >= 1.2:
            return 70
        elif performance_ratio >= 1.0:
            return 50
        elif performance_ratio >= 0.8:
            return 30
        elif performance_ratio >= 0.6:
            return 15
        else:
            return 5
    
    def _identify_improvement_opportunity(self, sector: str, location: str) -> str:
        """Identify the best improvement opportunity."""
        
        sector_opportunities = {
            "electronics": "Adding mobile repair services",
            "food": "Starting home delivery", 
            "textile": "Targeting wedding customers",
            "auto": "Focusing on motorcycle parts",
            "retail": "Building online presence"
        }
        
        return sector_opportunities.get(sector, "Optimizing product mix")
    
    def _identify_revenue_decline_cause(self, business_data: Dict[str, Any]) -> str:
        """Identify likely cause of revenue decline."""
        
        sector = business_data["sector"]
        
        # Calculate economic impact
        economic_impact = calculate_economic_impact(sector, business_data)
        
        if economic_impact["total_economic_impact"] < -0.1:
            return "Economic conditions (inflation, PKR weakness) hurting sector"
        else:
            return "Internal business issues - competition or operational problems"
    
    def _identify_competitive_disadvantage(self, sector: str, location: str, 
                                         market_position: Dict[str, Any]) -> str:
        """Identify why business is behind competitors."""
        
        performance_ratio = market_position["performance_ratio"]
        
        if performance_ratio < 0.5:
            return "Fundamental business model or location issues"
        elif performance_ratio < 0.7:
            return "Wrong product focus or pricing strategy"
        else:
            return "Operational efficiency or customer service issues"