"""Generate specific, actionable recommendations with concrete steps and outcomes."""

from typing import Dict, List, Any, Optional, Tuple
import datetime

from app.core.karachi_intelligence import KarachiIntelligence
from app.data.karachi_sectors import get_sector_data
from app.data.economic_factors import get_seasonal_factor


class RecommendationEngine:
    """Generate specific, actionable recommendations for business improvement."""
    
    def __init__(self):
        self.karachi_intel = KarachiIntelligence()
    
    def generate_immediate_actions(self, analysis_result: Dict[str, Any],
                                 business_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate actions to take this week."""
        
        actions = []
        
        # Priority 1: Fix critical financial issues
        financial_actions = self._generate_financial_actions(analysis_result, business_data)
        actions.extend(financial_actions)
        
        # Priority 2: Address revenue problems
        revenue_actions = self._generate_revenue_actions(analysis_result, business_data)
        actions.extend(revenue_actions)
        
        # Priority 3: Quick wins
        quick_win_actions = self._generate_quick_wins(analysis_result, business_data)
        actions.extend(quick_win_actions)
        
        # Return top 3 immediate actions
        return sorted(actions, key=lambda x: x["impact_score"], reverse=True)[:3]
    
    def generate_strategic_actions(self, analysis_result: Dict[str, Any],
                                 business_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate strategic actions for next 3-6 months."""
        
        actions = []
        
        # Market expansion opportunities
        expansion_actions = self._generate_expansion_actions(analysis_result, business_data)
        actions.extend(expansion_actions)
        
        # Business model improvements
        business_model_actions = self._generate_business_model_actions(analysis_result, business_data)
        actions.extend(business_model_actions)
        
        # Competitive positioning
        competitive_actions = self._generate_competitive_actions(analysis_result, business_data)
        actions.extend(competitive_actions)
        
        # Return top 3 strategic actions
        return sorted(actions, key=lambda x: x["potential_value"], reverse=True)[:3]
    
    def generate_investment_recommendations(self, analysis_result: Dict[str, Any],
                                          business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate investment recommendations and advice."""
        
        current_cash = business_data["current_cash"]
        monthly_expenses = business_data["monthly_expenses"]
        monthly_revenue = business_data["monthly_revenue"]
        sector = business_data["sector"]
        
        # Calculate available investment capital
        available_capital = self._calculate_investment_capacity(
            current_cash, monthly_expenses, monthly_revenue
        )
        
        # Assess risk profile
        risk_profile = self._assess_investment_risk_profile(analysis_result, business_data)
        
        # Generate investment options
        investment_options = self._generate_investment_options(
            available_capital, risk_profile, sector, business_data
        )
        
        # Investment strategy
        investment_strategy = self._recommend_investment_strategy(
            available_capital, risk_profile, analysis_result
        )
        
        return {
            "available_capital": available_capital,
            "risk_profile": risk_profile,
            "investment_options": investment_options,
            "recommended_strategy": investment_strategy,
            "investment_reasoning": self._generate_investment_reasoning(
                available_capital, risk_profile, sector
            ),
        }
    
    def generate_action_plan(self, analysis_result: Dict[str, Any],
                           business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive 90-day action plan."""
        
        # Get all recommendations
        immediate_actions = self.generate_immediate_actions(analysis_result, business_data)
        strategic_actions = self.generate_strategic_actions(analysis_result, business_data)
        investment_advice = self.generate_investment_recommendations(analysis_result, business_data)
        
        # Create timeline
        week_1_2_actions = self._create_week_1_2_plan(immediate_actions, business_data)
        week_3_6_actions = self._create_week_3_6_plan(immediate_actions, strategic_actions, business_data)
        week_7_12_actions = self._create_week_7_12_plan(strategic_actions, investment_advice, business_data)
        
        # Key metrics to track
        key_metrics = self._define_key_metrics(analysis_result, business_data)
        
        # Success milestones
        success_milestones = self._define_success_milestones(analysis_result, business_data)
        
        return {
            "timeline": {
                "week_1_2": week_1_2_actions,
                "week_3_6": week_3_6_actions,
                "week_7_12": week_7_12_actions,
            },
            "key_metrics": key_metrics,
            "success_milestones": success_milestones,
            "total_expected_impact": self._calculate_total_expected_impact(
                immediate_actions, strategic_actions
            ),
        }
    
    def _generate_financial_actions(self, analysis_result: Dict[str, Any],
                                  business_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate financial improvement actions."""
        
        actions = []
        financial_health = analysis_result["financial_health"]
        performance_metrics = analysis_result["performance_metrics"]
        
        # Critical cash flow issues
        if performance_metrics["cash_runway_months"] < 3:
            actions.append({
                "category": "cash_flow_emergency",
                "title": "Fix Cash Flow Crisis",
                "description": "Only {:.1f} months of cash left - immediate action required".format(
                    performance_metrics["cash_runway_months"]
                ),
                "specific_actions": [
                    "Collect all outstanding payments this week",
                    "Negotiate 30-day payment terms with suppliers",
                    "Reduce inventory purchases by 50%",
                    "Cut non-essential expenses immediately"
                ],
                "expected_outcome": "Extend cash runway to 6+ months",
                "timeframe": "This week",
                "investment_required": 0,
                "expected_benefit": business_data["monthly_expenses"] * 3,
                "impact_score": 95,
                "difficulty": "medium",
            })
        
        # Low profit margins
        if performance_metrics["profit_margin"] < 0.15:
            current_revenue = performance_metrics["current_revenue"]
            target_improvement = current_revenue * 0.05  # 5% improvement
            
            actions.append({
                "category": "margin_improvement",
                "title": "Increase Profit Margins",
                "description": f"Current {performance_metrics['profit_margin']*100:.1f}% margin too low - target 20%+",
                "specific_actions": [
                    "Review all product pricing - increase by 8-12%",
                    "Negotiate better supplier terms",
                    "Focus on higher-margin products",
                    "Reduce waste and operational costs"
                ],
                "expected_outcome": f"Increase monthly profit by Rs. {target_improvement:,.0f}",
                "timeframe": "2-4 weeks",
                "investment_required": 0,
                "expected_benefit": target_improvement,
                "impact_score": 80,
                "difficulty": "easy",
            })
        
        return actions
    
    def _generate_revenue_actions(self, analysis_result: Dict[str, Any],
                                business_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate revenue improvement actions."""
        
        actions = []
        sector = business_data["sector"]
        location = business_data["location_area"]
        current_revenue = analysis_result["performance_metrics"]["current_revenue"]
        market_position = analysis_result["market_position"]
        
        # Underperforming vs market
        if market_position["performance_ratio"] < 0.8:
            revenue_gap = market_position["market_average_revenue"] - current_revenue
            
            # Sector-specific revenue actions
            if sector == "electronics":
                actions.append({
                    "category": "product_mix_optimization",
                    "title": "Switch to High-Profit Accessories",
                    "description": "Stop selling phones (8% margin), focus on accessories (40% margin)",
                    "specific_actions": [
                        "Stop ordering new phones this month",
                        "Stock mobile covers, chargers, earphones",
                        "Add phone repair service",
                        "Put 'Mobile Repair' sign outside"
                    ],
                    "expected_outcome": f"Close Rs. {revenue_gap:,.0f} monthly gap with market",
                    "timeframe": "4-6 weeks",
                    "investment_required": 50000,
                    "expected_benefit": revenue_gap * 0.7,  # 70% of gap closure
                    "impact_score": 85,
                    "difficulty": "easy",
                })
            
            elif sector == "food":
                actions.append({
                    "category": "delivery_expansion",
                    "title": "Start Home Delivery Service",
                    "description": "50% of food orders now delivery - you're missing huge market",
                    "specific_actions": [
                        "Register with Foodpanda/Careem",
                        "Create WhatsApp delivery menu",
                        "Hire 1 delivery person",
                        "Promote delivery on social media"
                    ],
                    "expected_outcome": f"Add Rs. {current_revenue * 0.4:,.0f} monthly delivery revenue",
                    "timeframe": "2-3 weeks",
                    "investment_required": 30000,
                    "expected_benefit": current_revenue * 0.4,
                    "impact_score": 88,
                    "difficulty": "easy",
                })
            
            elif sector == "textile":
                seasonal_factor = get_seasonal_factor("textile")
                if seasonal_factor > 1.2:  # Wedding season
                    actions.append({
                        "category": "seasonal_optimization",
                        "title": "Capitalize on Wedding Season",
                        "description": "Wedding season = 3x higher margins - focus everything here",
                        "specific_actions": [
                            "Stock red, gold, and premium fabrics",
                            "Target bridal shops and customers",
                            "Increase wedding fabric prices by 20%",
                            "Partner with tailors for referrals"
                        ],
                        "expected_outcome": f"Earn Rs. {current_revenue * 0.6:,.0f} extra in wedding season",
                        "timeframe": "Immediate",
                        "investment_required": 100000,
                        "expected_benefit": current_revenue * 0.6,
                        "impact_score": 90,
                        "difficulty": "easy",
                    })
            
            elif sector == "auto":
                actions.append({
                    "category": "service_addition",
                    "title": "Add Mobile Auto Repair",
                    "description": "Go to customer location - charge premium for convenience",
                    "specific_actions": [
                        "Buy portable repair tools",
                        "Create mobile repair service",
                        "Charge 50% premium for home service",
                        "Market to busy professionals"
                    ],
                    "expected_outcome": f"Add Rs. {current_revenue * 0.3:,.0f} monthly service revenue",
                    "timeframe": "3-4 weeks",
                    "investment_required": 80000,
                    "expected_benefit": current_revenue * 0.3,
                    "impact_score": 75,
                    "difficulty": "medium",
                })
        
        return actions
    
    def _generate_quick_wins(self, analysis_result: Dict[str, Any],
                           business_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate quick win actions for immediate impact."""
        
        actions = []
        sector = business_data["sector"]
        current_revenue = analysis_result["performance_metrics"]["current_revenue"]
        
        # Digital presence (universal quick win)
        actions.append({
            "category": "digital_presence",
            "title": "Create Instagram Business Page",
            "description": "70% of customers check online first - you're invisible",
            "specific_actions": [
                "Create Instagram business account",
                "Post 3 photos daily of products",
                "Add WhatsApp number and location",
                "Ask customers to follow and share"
            ],
            "expected_outcome": f"Attract {int(current_revenue * 0.15 / 5000)} new customers monthly",
            "timeframe": "This weekend",
            "investment_required": 0,
            "expected_benefit": current_revenue * 0.15,
            "impact_score": 70,
            "difficulty": "easy",
        })
        
        # Customer retention improvement
        actions.append({
            "category": "customer_retention",
            "title": "Start Customer Loyalty Program",
            "description": "Keep existing customers - cheaper than finding new ones",
            "specific_actions": [
                "Create simple punch card system",
                "Give discount after 10 purchases",
                "Remember regular customer names",
                "Send WhatsApp offers to regulars"
            ],
            "expected_outcome": "Increase repeat customers by 40%",
            "timeframe": "1 week",
            "investment_required": 5000,
            "expected_benefit": current_revenue * 0.12,
            "impact_score": 65,
            "difficulty": "easy",
        })
        
        return actions
    
    def _generate_expansion_actions(self, analysis_result: Dict[str, Any],
                                  business_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate expansion and growth actions."""
        
        actions = []
        expansion_readiness = self.karachi_intel.calculate_expansion_readiness(business_data)
        current_revenue = analysis_result["performance_metrics"]["current_revenue"]
        sector = business_data["sector"]
        location = business_data["location_area"]
        
        # Only recommend expansion if ready
        if expansion_readiness["readiness_level"] in ["ready", "highly_ready"]:
            
            # Second location expansion
            best_expansion_location = self._recommend_expansion_location(sector, location)
            expansion_investment = self._estimate_expansion_investment(sector)
            
            actions.append({
                "category": "location_expansion",
                "title": f"Open Second Location in {best_expansion_location}",
                "description": f"Your business model is proven - replicate in {best_expansion_location}",
                "specific_actions": [
                    f"Scout locations in {best_expansion_location}",
                    "Negotiate lease terms",
                    "Hire and train local manager",
                    "Replicate successful processes"
                ],
                "expected_outcome": f"Add Rs. {current_revenue * 0.8:,.0f} monthly from second location",
                "timeframe": "4-6 months",
                "investment_required": expansion_investment,
                "expected_benefit": current_revenue * 0.8,
                "impact_score": 85,
                "difficulty": "hard",
                "prerequisites": ["Strong cash flow", "Proven processes", "Management systems"]
            })
        
        # Market expansion within current location
        market_expansion = self._identify_market_expansion_opportunity(sector, location, current_revenue)
        if market_expansion:
            actions.append(market_expansion)
        
        return actions
    
    def _generate_investment_options(self, available_capital: float, risk_profile: str,
                                   sector: str, business_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate specific investment recommendations."""
        
        options = []
        
        if available_capital < 50000:
            return [{
                "type": "insufficient_capital",
                "title": "Build Cash Reserves First",
                "description": "Focus on business growth before investing",
                "recommendation": "Save until you have Rs. 50K+ available"
            }]
        
        # Business reinvestment (always top priority)
        business_investment = min(available_capital * 0.6, 200000)
        options.append({
            "type": "business_reinvestment",
            "title": "Reinvest in Your Business",
            "amount": business_investment,
            "description": self._get_business_reinvestment_advice(sector, business_investment),
            "expected_return": 0.25,  # 25% annual return
            "risk_level": "medium",
            "timeframe": "3-6 months",
            "priority": 1,
        })
        
        # Sector-related stocks
        if available_capital > 100000:
            stock_investment = min(available_capital * 0.3, 150000)
            options.append({
                "type": "sector_stocks",
                "title": f"Invest in {sector.title()} Sector Stocks",
                "amount": stock_investment,
                "description": f"Your {sector} expertise helps you understand these companies",
                "expected_return": 0.18,  # 18% annual return
                "risk_level": risk_profile,
                "timeframe": "12+ months",
                "priority": 2,
                "specific_stocks": self._recommend_sector_stocks(sector),
            })
        
        # Safe investments for conservative profile
        if risk_profile in ["low", "medium"] and available_capital > 150000:
            safe_investment = min(available_capital * 0.2, 100000)
            options.append({
                "type": "safe_investments",
                "title": "Government Bonds/Fixed Deposits",
                "amount": safe_investment,
                "description": "Safe returns to protect against inflation",
                "expected_return": 0.15,  # 15% annual return
                "risk_level": "low",
                "timeframe": "12 months",
                "priority": 3,
            })
        
        return options
    
    def _calculate_investment_capacity(self, current_cash: float, monthly_expenses: float,
                                     monthly_revenue: List[float]) -> float:
        """Calculate safe investment capacity."""
        
        # Must keep 3 months expenses as emergency fund
        emergency_fund = monthly_expenses * 3
        
        # Calculate average monthly profit
        if monthly_revenue:
            current_monthly_revenue = monthly_revenue[-1]
            monthly_profit = max(0, current_monthly_revenue - monthly_expenses)
        else:
            monthly_profit = 0
        
        # Available for investment = Cash - Emergency fund
        available = max(0, current_cash - emergency_fund)
        
        # Conservative approach: max 40% of available cash or 6 months profit
        max_investment = min(available * 0.4, monthly_profit * 6)
        
        return max(0, max_investment)
    
    def _assess_investment_risk_profile(self, analysis_result: Dict[str, Any],
                                      business_data: Dict[str, Any]) -> str:
        """Assess business owner's investment risk profile."""
        
        # Factors for risk assessment
        revenue_stability = analysis_result["performance_metrics"]["revenue_stability"]
        financial_health_score = analysis_result["financial_health"]["score"]
        years_in_business = business_data["years_in_business"]
        cash_runway = analysis_result["performance_metrics"]["cash_runway_months"]
        
        # Calculate risk tolerance score
        stability_score = revenue_stability * 30
        health_score = financial_health_score * 0.3
        experience_score = min(years_in_business * 5, 20)
        cash_score = min(cash_runway * 2, 20)
        
        total_risk_score = stability_score + health_score + experience_score + cash_score
        
        if total_risk_score >= 70:
            return "high"
        elif total_risk_score >= 50:
            return "medium"
        else:
            return "low"
    
    def _recommend_expansion_location(self, sector: str, current_location: str) -> str:
        """Recommend best expansion location."""
        
        # Avoid same location, recommend complementary areas
        expansion_recommendations = {
            "saddar": "Gulshan",  # From high competition to medium
            "clifton": "DHA",     # Similar affluent market
            "gulshan": "Nazimabad",  # Similar middle-class market
            "tariq_road": "Clifton",  # From commercial to residential
            "dha": "Clifton",     # Similar market
            "korangi": "Landhi",  # Similar industrial area
        }
        
        return expansion_recommendations.get(current_location, "Gulshan")
    
    def _estimate_expansion_investment(self, sector: str) -> float:
        """Estimate investment required for expansion."""
        
        investment_estimates = {
            "electronics": 800000,  # Inventory + setup
            "textile": 1200000,     # Higher inventory needs
            "auto": 600000,         # Parts + tools
            "food": 900000,         # Kitchen + setup
            "retail": 500000,       # Inventory + basic setup
        }
        
        return investment_estimates.get(sector, 700000)
    
    def _get_business_reinvestment_advice(self, sector: str, amount: float) -> str:
        """Get sector-specific reinvestment advice."""
        
        advice = {
            "electronics": f"Buy Rs. {amount:,.0f} worth of mobile accessories and repair tools",
            "textile": f"Stock Rs. {amount:,.0f} premium wedding fabrics for peak season",
            "auto": f"Invest Rs. {amount:,.0f} in motorcycle parts and mobile repair setup",
            "food": f"Use Rs. {amount:,.0f} for delivery setup and kitchen improvements",
            "retail": f"Invest Rs. {amount:,.0f} in high-margin branded products",
        }
        
        return advice.get(sector, f"Reinvest Rs. {amount:,.0f} in business growth")
    
    def _recommend_sector_stocks(self, sector: str) -> List[str]:
        """Recommend related stocks for sector expertise."""
        
        stock_recommendations = {
            "electronics": ["TechCo", "ElectronicsCorp", "TelecomGiant"],
            "textile": ["TextileMills", "FabricCorp", "GarmentIndustries"],
            "auto": ["AutoParts", "MotorCorp", "VehicleAssembly"],
            "food": ["FoodIndustries", "BeverageCorp", "AgricultureCo"],
            "retail": ["RetailChain", "ConsumerGoods", "TradingCorp"],
        }
        
        return stock_recommendations.get(sector, ["DiversifiedCorp", "GrowthStocks"])
    
    def _create_week_1_2_plan(self, immediate_actions: List[Dict[str, Any]],
                            business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create detailed plan for weeks 1-2."""
        
        return {
            "focus": "Quick Wins & Crisis Management",
            "actions": [action for action in immediate_actions if action["timeframe"] in ["This week", "1 week", "This weekend"]],
            "key_tasks": [
                "Address any cash flow issues",
                "Implement highest-impact quick fixes",
                "Start customer retention program",
                "Create digital presence"
            ],
            "success_metric": "Fix immediate problems and stabilize operations",
            "budget_required": sum(action.get("investment_required", 0) for action in immediate_actions),
        }
    
    def _create_week_3_6_plan(self, immediate_actions: List[Dict[str, Any]],
                            strategic_actions: List[Dict[str, Any]],
                            business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create detailed plan for weeks 3-6."""
        
        medium_term_actions = [action for action in immediate_actions + strategic_actions 
                              if "week" in action["timeframe"] or "month" in action["timeframe"]]
        
        return {
            "focus": "Operational Improvements & Growth Setup",
            "actions": medium_term_actions[:3],
            "key_tasks": [
                "Optimize product mix and pricing",
                "Improve operational efficiency", 
                "Build customer base and retention",
                "Prepare for strategic growth"
            ],
            "success_metric": "15% improvement in monthly profits",
            "budget_required": sum(action.get("investment_required", 0) for action in medium_term_actions[:3]),
        }
    
    def _create_week_7_12_plan(self, strategic_actions: List[Dict[str, Any]],
                             investment_advice: Dict[str, Any],
                             business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create detailed plan for weeks 7-12."""
        
        return {
            "focus": "Strategic Growth & Investment",
            "actions": strategic_actions,
            "key_tasks": [
                "Execute growth strategies",
                "Consider expansion opportunities",
                "Implement investment plan",
                "Build long-term competitive advantages"
            ],
            "success_metric": "Position for sustainable long-term growth",
            "budget_required": investment_advice.get("available_capital", 0),
        }
    
    def _define_key_metrics(self, analysis_result: Dict[str, Any],
                          business_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Define key metrics to track progress."""
        
        current_revenue = analysis_result["performance_metrics"]["current_revenue"]
        current_margin = analysis_result["performance_metrics"]["profit_margin"]
        
        return [
            {
                "metric": "Monthly Revenue",
                "current": f"Rs. {current_revenue:,.0f}",
                "target": f"Rs. {current_revenue * 1.2:,.0f}",
                "tracking": "Track weekly, target +5% monthly growth"
            },
            {
                "metric": "Profit Margin",
                "current": f"{current_margin*100:.1f}%",
                "target": "22%+",
                "tracking": "Calculate monthly, optimize pricing/costs"
            },
            {
                "metric": "Customer Count",
                "current": "Track starting now",
                "target": "+10 new customers weekly",
                "tracking": "Daily count of new vs repeat customers"
            },
            {
                "metric": "Cash Flow",
                "current": f"Rs. {business_data['current_cash']:,.0f}",
                "target": f"Rs. {business_data['monthly_expenses'] * 6:,.0f}",
                "tracking": "Weekly cash position monitoring"
            }
        ]
    
    def _define_success_milestones(self, analysis_result: Dict[str, Any],
                                 business_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Define success milestones for tracking progress."""
        
        current_revenue = analysis_result["performance_metrics"]["current_revenue"]
        
        return [
            {
                "timeframe": "30 days",
                "milestone": "Operational Stability",
                "targets": [
                    f"Monthly revenue: Rs. {current_revenue * 1.1:,.0f}",
                    "Profit margin: 18%+",
                    "Cash runway: 6+ months",
                    "Digital presence established"
                ]
            },
            {
                "timeframe": "60 days", 
                "milestone": "Growth Momentum",
                "targets": [
                    f"Monthly revenue: Rs. {current_revenue * 1.25:,.0f}",
                    "Profit margin: 20%+",
                    "Customer base: +50 new customers",
                    "Process optimization complete"
                ]
            },
            {
                "timeframe": "90 days",
                "milestone": "Sustainable Growth",
                "targets": [
                    f"Monthly revenue: Rs. {current_revenue * 1.4:,.0f}",
                    "Profit margin: 22%+",
                    "Market position: Above average",
                    "Ready for expansion/investment"
                ]
            }
        ]
    
    def _calculate_total_expected_impact(self, immediate_actions: List[Dict[str, Any]],
                                       strategic_actions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate total expected impact from all recommendations."""
        
        total_investment = sum(action.get("investment_required", 0) 
                              for action in immediate_actions + strategic_actions)
        
        total_benefit = sum(action.get("expected_benefit", 0) 
                           for action in immediate_actions + strategic_actions)
        
        roi = ((total_benefit - total_investment) / total_investment * 100) if total_investment > 0 else 0
        
        return {
            "total_investment_required": total_investment,
            "total_expected_monthly_benefit": total_benefit,
            "expected_roi": f"{roi:.0f}%",
            "payback_period_months": total_investment / total_benefit if total_benefit > 0 else 0,
            "confidence_level": 0.8,
        }
    
    def _identify_market_expansion_opportunity(self, sector: str, location: str,
                                             current_revenue: float) -> Optional[Dict[str, Any]]:
        """Identify market expansion opportunities within current location."""
        
        # Sector-specific expansion opportunities
        if sector == "electronics" and location in ["saddar", "gulshan"]:
            return {
                "category": "service_expansion",
                "title": "Add Gaming Setup Services",
                "description": "Gaming market growing 40% - setup and maintenance services",
                "specific_actions": [
                    "Learn gaming hardware setup",
                    "Partner with gaming accessories suppliers", 
                    "Target young customers and gaming cafes",
                    "Charge Rs. 2000+ per gaming setup"
                ],
                "expected_outcome": f"Add Rs. {current_revenue * 0.2:,.0f} monthly gaming revenue",
                "timeframe": "2-3 months",
                "investment_required": 60000,
                "expected_benefit": current_revenue * 0.2,
                "impact_score": 70,
                "difficulty": "medium",
            }
        
        elif sector == "food" and location in ["clifton", "dha"]:
            return {
                "category": "premium_service",
                "title": "Add Corporate Catering",
                "description": "Target offices and events - higher margins than regular customers",
                "specific_actions": [
                    "Create corporate catering menu",
                    "Target nearby offices and businesses",
                    "Offer bulk discounts and delivery",
                    "Build relationships with event planners"
                ],
                "expected_outcome": f"Add Rs. {current_revenue * 0.35:,.0f} monthly catering revenue",
                "timeframe": "6-8 weeks",
                "investment_required": 40000,
                "expected_benefit": current_revenue * 0.35,
                "impact_score": 75,
                "difficulty": "medium",
            }
        
        return None
    
    def _generate_investment_reasoning(self, available_capital: float, 
                                     risk_profile: str, sector: str) -> str:
        """Generate investment reasoning based on profile."""
        
        if available_capital < 50000:
            return "Focus on building cash reserves and growing your business before investing in external opportunities."
        
        elif risk_profile == "low":
            return f"Your {sector} business shows stable patterns. Conservative investment approach recommended with emphasis on business reinvestment and safe returns."
        
        elif risk_profile == "medium":
           return f"Balanced approach recommended: reinvest majority in your {sector} business (you know this market), put some in related stocks, keep emergency fund."
       
        else:  # high risk tolerance
            return f"Your strong {sector} business performance allows for more aggressive investment. Focus on high-growth opportunities while maintaining business momentum."
        
    def _recommend_investment_strategy(self, available_capital: float, 
                                 risk_profile: str, analysis_result: Dict[str, Any]) -> str:
        """Recommend overall investment strategy based on profile and capital."""
        
        performance_score = analysis_result["overall_score"]["overall_score"]
        financial_health = analysis_result["financial_health"]["status"]
        
        if available_capital < 50000:
            return "Focus on business growth and building cash reserves before external investments"
        
        elif risk_profile == "low":
            if financial_health in ["excellent", "good"]:
                return "Conservative approach: 60% business reinvestment, 30% safe investments, 10% emergency fund"
            else:
                return "Priority on business stability: 80% business improvement, 20% emergency fund"
        
        elif risk_profile == "medium":
            if performance_score >= 70:
                return "Balanced growth: 50% business expansion, 30% sector investments, 20% diversified portfolio"
            else:
                return "Business-first approach: 70% business improvement, 20% safe investments, 10% sector exposure"
        
        else:  # high risk profile
            if performance_score >= 80:
                return "Aggressive growth: 40% business expansion, 40% growth investments, 20% sector opportunities"
            else:
                return "Strategic risk-taking: 60% business optimization, 30% growth investments, 10% opportunities"