"""Core business analysis engine for generating insights and recommendations."""

import math
from typing import Dict, List, Any, Optional, Tuple
import statistics

from app.core.karachi_intelligence import KarachiIntelligence
from app.core.market_generator import MarketDataGenerator
from app.data.economic_factors import calculate_economic_impact


class BusinessAnalyzer:
    """Core engine for analyzing business performance and generating insights."""
    
    def __init__(self):
        self.karachi_intel = KarachiIntelligence()
        self.market_generator = MarketDataGenerator()
    
    def analyze_business_performance(self, business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive business performance analysis."""
        
        # Extract key data
        sector = business_data["sector"]
        location = business_data["location_area"]
        monthly_revenue = business_data["monthly_revenue"]
        monthly_expenses = business_data["monthly_expenses"]
        current_cash = business_data["current_cash"]
        years_in_business = business_data["years_in_business"]
        
        # Core calculations
        performance_metrics = self._calculate_performance_metrics(
            monthly_revenue, monthly_expenses, current_cash, years_in_business
        )
        
        # Market position analysis
        market_position = self.karachi_intel.analyze_market_position(
            sector, location, monthly_revenue
        )
        
        # Financial health assessment
        financial_health = self._assess_financial_health(
            monthly_revenue, monthly_expenses, current_cash
        )
        
        # Risk assessment
        risk_assessment = self._assess_business_risk(
            monthly_revenue, sector, location, years_in_business
        )
        
        # Growth potential analysis
        growth_potential = self._analyze_growth_potential(
            business_data, market_position, financial_health
        )
        
        return {
            "performance_metrics": performance_metrics,
            "market_position": market_position,
            "financial_health": financial_health,
            "risk_assessment": risk_assessment,
            "growth_potential": growth_potential,
            "overall_score": self._calculate_overall_score(
                performance_metrics, market_position, financial_health, risk_assessment
            ),
        }
    
    def _calculate_performance_metrics(self, monthly_revenue: List[float], 
                                     monthly_expenses: float, current_cash: float,
                                     years_in_business: int) -> Dict[str, Any]:
        """Calculate core performance metrics."""
        
        if not monthly_revenue or len(monthly_revenue) < 2:
            return self._default_performance_metrics()
        
        # Current metrics
        current_revenue = monthly_revenue[-1]
        profit_margin = max(0, (current_revenue - monthly_expenses) / current_revenue) if current_revenue > 0 else 0
        
        # Growth calculations
        revenue_growth = self._calculate_revenue_growth(monthly_revenue)
        revenue_trend = self._determine_revenue_trend(monthly_revenue)
        revenue_stability = self._calculate_revenue_stability(monthly_revenue)
        
        # Cash flow analysis
        monthly_profit = current_revenue - monthly_expenses
        cash_runway = current_cash / monthly_expenses if monthly_expenses > 0 else float('inf')
        
        # Performance categorization
        performance_category = self._categorize_performance(revenue_growth, profit_margin, cash_runway)
        
        return {
            "current_revenue": current_revenue,
            "monthly_profit": monthly_profit,
            "profit_margin": profit_margin,
            "revenue_growth_rate": revenue_growth,
            "revenue_trend": revenue_trend,
            "revenue_stability": revenue_stability,
            "cash_runway_months": min(cash_runway, 24),  # Cap at 24 months for display
            "performance_category": performance_category,
            "years_in_business": years_in_business,
        }
    
    def _assess_financial_health(self, monthly_revenue: List[float], 
                               monthly_expenses: float, current_cash: float) -> Dict[str, Any]:
        """Assess overall financial health."""
        
        if not monthly_revenue:
            return {"status": "insufficient_data", "score": 0}
        
        current_revenue = monthly_revenue[-1]
        monthly_profit = current_revenue - monthly_expenses
        
        # Financial health indicators
        profitability_score = self._score_profitability(monthly_profit, current_revenue)
        liquidity_score = self._score_liquidity(current_cash, monthly_expenses)
        stability_score = self._score_stability(monthly_revenue)
        
        # Overall financial health score
        overall_score = (profitability_score * 0.4 + liquidity_score * 0.3 + stability_score * 0.3)
        
        # Determine status
        if overall_score >= 80:
            status = "excellent"
            description = "Strong financial position with healthy profits and cash flow"
        elif overall_score >= 65:
            status = "good"
            description = "Solid financial health with minor areas for improvement"
        elif overall_score >= 50:
            status = "fair"
            description = "Adequate financial position but needs attention"
        elif overall_score >= 35:
            status = "poor"
            description = "Financial challenges requiring immediate action"
        else:
            status = "critical"
            description = "Serious financial difficulties - urgent intervention needed"
        
        return {
            "status": status,
            "description": description,
            "score": overall_score,
            "component_scores": {
                "profitability": profitability_score,
                "liquidity": liquidity_score,
                "stability": stability_score,
            },
            "key_strengths": self._identify_financial_strengths(profitability_score, liquidity_score, stability_score),
            "key_concerns": self._identify_financial_concerns(profitability_score, liquidity_score, stability_score),
        }
    
    def _assess_business_risk(self, monthly_revenue: List[float], sector: str, 
                            location: str, years_in_business: int) -> Dict[str, Any]:
        """Assess business risk factors."""
        
        # Calculate risk components
        revenue_volatility = self._calculate_revenue_volatility(monthly_revenue)
        market_risk = self._assess_market_risk(sector, location)
        operational_risk = self._assess_operational_risk(years_in_business, monthly_revenue)
        economic_risk = self._assess_economic_risk(sector)
        
        # Overall risk score (0-100, where 0 = no risk, 100 = maximum risk)
        risk_score = (revenue_volatility * 0.3 + market_risk * 0.3 + 
                     operational_risk * 0.2 + economic_risk * 0.2)
        
        # Risk level categorization
        if risk_score <= 25:
            risk_level = "low"
            description = "Low risk profile with stable business fundamentals"
        elif risk_score <= 50:
            risk_level = "moderate"
            description = "Moderate risk with manageable challenges"
        elif risk_score <= 75:
            risk_level = "high"
            description = "High risk requiring careful management"
        else:
            risk_level = "very_high"
            description = "Very high risk - immediate risk mitigation needed"
        
        return {
            "overall_risk_score": risk_score,
            "risk_level": risk_level,
            "description": description,
            "risk_components": {
                "revenue_volatility": revenue_volatility,
                "market_risk": market_risk,
                "operational_risk": operational_risk,
                "economic_risk": economic_risk,
            },
            "key_risk_factors": self._identify_key_risk_factors(
                revenue_volatility, market_risk, operational_risk, economic_risk, sector
            ),
            "risk_mitigation_priorities": self._recommend_risk_mitigation(
                revenue_volatility, market_risk, operational_risk, economic_risk
            ),
        }
    
    def _analyze_growth_potential(self, business_data: Dict[str, Any], 
                                market_position: Dict[str, Any],
                                financial_health: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze business growth potential and opportunities."""
        
        sector = business_data["sector"]
        location = business_data["location_area"]
        
        # Market opportunity analysis
        market_opportunity = self.market_generator.calculate_market_opportunity(
            sector, location, business_data
        )
        
        # Growth readiness assessment
        expansion_readiness = self.karachi_intel.calculate_expansion_readiness(business_data)
        
        # Growth drivers and barriers
        growth_drivers = self._identify_growth_drivers(business_data, market_position)
        growth_barriers = self._identify_growth_barriers(business_data, financial_health)
        
        # Growth potential score
        market_score = self._score_market_potential(market_opportunity)
        readiness_score = expansion_readiness["overall_score"] * 100
        position_score = market_position["percentile_rank"]
        
        growth_potential_score = (market_score * 0.4 + readiness_score * 0.3 + position_score * 0.3)
        
        return {
            "growth_potential_score": growth_potential_score,
            "market_opportunity": market_opportunity,
            "expansion_readiness": expansion_readiness,
            "growth_drivers": growth_drivers,
            "growth_barriers": growth_barriers,
            "recommended_growth_strategy": self._recommend_growth_strategy(
                growth_potential_score, market_opportunity, expansion_readiness
            ),
        }
    
    def _calculate_overall_score(self, performance_metrics: Dict[str, Any],
                               market_position: Dict[str, Any],
                               financial_health: Dict[str, Any], 
                               risk_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall business health score."""
        
        # Component scores (0-100 scale)
        performance_score = self._normalize_performance_score(performance_metrics)
        market_score = market_position["percentile_rank"]
        financial_score = financial_health["score"]
        risk_penalty = risk_assessment["overall_risk_score"] * 0.5  # Risk reduces score
        
        # Weighted overall score
        overall_score = max(0, (
            performance_score * 0.3 + 
            market_score * 0.25 + 
            financial_score * 0.25 + 
            (100 - risk_penalty) * 0.2
        ))
        
        # Score interpretation
        if overall_score >= 85:
            grade = "A"
            status = "excellent"
            description = "Outstanding business performance across all metrics"
        elif overall_score >= 75:
            grade = "B+"
            status = "very_good"
            description = "Strong business performance with minor improvement areas"
        elif overall_score >= 65:
            grade = "B"
            status = "good"
            description = "Good business performance with clear improvement opportunities"
        elif overall_score >= 55:
            grade = "B-"
            status = "fair"
            description = "Fair performance with several areas needing attention"
        elif overall_score >= 45:
            grade = "C"
            status = "needs_improvement"
            description = "Performance below expectations - improvement plan needed"
        else:
            grade = "D"
            status = "poor"
            description = "Poor performance requiring immediate corrective action"
        
        return {
            "overall_score": overall_score,
            "grade": grade,
            "status": status,
            "description": description,
            "component_breakdown": {
                "performance": performance_score,
                "market_position": market_score,
                "financial_health": financial_score,
                "risk_adjusted": 100 - risk_penalty,
            },
        }
    
    # Helper methods for calculations
    
    def _calculate_revenue_growth(self, monthly_revenue: List[float]) -> float:
        """Calculate average monthly revenue growth rate."""
        if len(monthly_revenue) < 2:
            return 0.0
        
        growth_rates = []
        for i in range(1, len(monthly_revenue)):
            if monthly_revenue[i-1] > 0:
                growth_rate = (monthly_revenue[i] - monthly_revenue[i-1]) / monthly_revenue[i-1]
                growth_rates.append(growth_rate)
        
        return statistics.mean(growth_rates) if growth_rates else 0.0
    
    def _determine_revenue_trend(self, monthly_revenue: List[float]) -> str:
        """Determine overall revenue trend direction."""
        if len(monthly_revenue) < 3:
            return "insufficient_data"
        
        recent_avg = statistics.mean(monthly_revenue[-3:])
        earlier_avg = statistics.mean(monthly_revenue[-6:-3]) if len(monthly_revenue) >= 6 else statistics.mean(monthly_revenue[:-3])
        
        if recent_avg > earlier_avg * 1.05:
            return "increasing"
        elif recent_avg < earlier_avg * 0.95:
            return "declining"
        else:
            return "stable"
    
    def _calculate_revenue_stability(self, monthly_revenue: List[float]) -> float:
        """Calculate revenue stability score (0-1, where 1 = most stable)."""
        if len(monthly_revenue) < 3:
            return 0.5
        
        mean_revenue = statistics.mean(monthly_revenue)
        if mean_revenue == 0:
            return 0
        
        # Calculate coefficient of variation
        std_dev = statistics.stdev(monthly_revenue)
        cv = std_dev / mean_revenue
        
        # Convert to stability score (lower CV = higher stability)
        stability = max(0, 1 - cv)
        return min(1, stability)
    
    def _categorize_performance(self, growth_rate: float, profit_margin: float, cash_runway: float) -> str:
        """Categorize overall business performance."""
        
        # Scoring each component
        growth_score = 1 if growth_rate > 0.1 else 0.5 if growth_rate > 0 else 0
        margin_score = 1 if profit_margin > 0.2 else 0.5 if profit_margin > 0.1 else 0
        cash_score = 1 if cash_runway > 6 else 0.5 if cash_runway > 3 else 0
        
        total_score = growth_score + margin_score + cash_score
        
        if total_score >= 2.5:
            return "excellent"
        elif total_score >= 2.0:
            return "good"
        elif total_score >= 1.5:
            return "fair"
        elif total_score >= 1.0:
            return "poor"
        else:
            return "critical"
    
    def _default_performance_metrics(self) -> Dict[str, Any]:
        """Return default metrics when insufficient data."""
        return {
            "current_revenue": 0,
            "monthly_profit": 0,
            "profit_margin": 0,
            "revenue_growth_rate": 0,
            "revenue_trend": "insufficient_data",
            "revenue_stability": 0,
            "cash_runway_months": 0,
            "performance_category": "insufficient_data",
            "years_in_business": 0,
        }
    
    def _score_profitability(self, monthly_profit: float, current_revenue: float) -> float:
        """Score profitability on 0-100 scale."""
        if current_revenue <= 0:
            return 0
        
        profit_margin = monthly_profit / current_revenue
        
        if profit_margin >= 0.25:
            return 100
        elif profit_margin >= 0.20:
            return 85
        elif profit_margin >= 0.15:
            return 70
        elif profit_margin >= 0.10:
            return 55
        elif profit_margin >= 0.05:
            return 40
        elif profit_margin >= 0:
            return 25
        else:
            return 0
    
    def _score_liquidity(self, current_cash: float, monthly_expenses: float) -> float:
        """Score liquidity on 0-100 scale."""
        if monthly_expenses <= 0:
            return 100
        
        cash_runway = current_cash / monthly_expenses
        
        if cash_runway >= 12:
            return 100
        elif cash_runway >= 6:
            return 85
        elif cash_runway >= 3:
            return 70
        elif cash_runway >= 1:
            return 55
        elif cash_runway >= 0.5:
            return 40
        else:
            return 20
    
    def _score_stability(self, monthly_revenue: List[float]) -> float:
        """Score revenue stability on 0-100 scale."""
        stability = self._calculate_revenue_stability(monthly_revenue)
        return stability * 100
    
    def _identify_financial_strengths(self, profitability: float, liquidity: float, stability: float) -> List[str]:
        """Identify financial strengths."""
        strengths = []
        
        if profitability >= 70:
            strengths.append("Strong profitability")
        if liquidity >= 70:
            strengths.append("Healthy cash position")
        if stability >= 70:
            strengths.append("Stable revenue streams")
        
        return strengths
    
    def _identify_financial_concerns(self, profitability: float, liquidity: float, stability: float) -> List[str]:
        """Identify financial concerns."""
        concerns = []
        
        if profitability < 50:
            concerns.append("Low profit margins")
        if liquidity < 50:
            concerns.append("Cash flow constraints")
        if stability < 50:
            concerns.append("Revenue volatility")
        
        return concerns
    
    def _calculate_revenue_volatility(self, monthly_revenue: List[float]) -> float:
        """Calculate revenue volatility score (0-100)."""
        volatility = self._calculate_volatility(monthly_revenue)
        return min(100, volatility * 100)
    
    def _calculate_volatility(self, values: List[float]) -> float:
        """Calculate coefficient of variation."""
        if not values or len(values) < 2:
            return 0.0
        
        mean_value = sum(values) / len(values)
        if mean_value == 0:
            return 0.0
        
        variance = sum((x - mean_value) ** 2 for x in values) / len(values)
        std_dev = variance ** 0.5
        cv = std_dev / mean_value
        
        return cv
    
    def _assess_market_risk(self, sector: str, location: str) -> float:
        """Assess market risk (0-100 scale)."""
        # Simple risk assessment based on sector and location
        sector_risk = {
            "electronics": 60,
            "textile": 50,
            "auto": 70,
            "food": 40,
            "retail": 55
        }.get(sector, 50)
        
        location_risk = {
            "saddar": 70,  # High competition
            "clifton": 40,
            "dha": 30,
            "gulshan": 50,
            "tariq_road": 65
        }.get(location, 50)
        
        return (sector_risk + location_risk) / 2
    
    def _assess_operational_risk(self, years_in_business: int, monthly_revenue: List[float]) -> float:
        """Assess operational risk (0-100 scale)."""
        experience_risk = max(0, 50 - (years_in_business * 5))
        revenue_risk = self._calculate_revenue_volatility(monthly_revenue) * 0.5
        
        return min(100, experience_risk + revenue_risk)
    
    def _assess_economic_risk(self, sector: str) -> float:
        """Assess economic risk (0-100 scale)."""
        # Based on current economic conditions
        base_risk = 60  # High inflation environment
        
        sector_sensitivity = {
            "electronics": 80,  # High import dependency
            "textile": 50,      # Mixed impact
            "auto": 85,         # Very high import dependency
            "food": 65,         # Medium impact
            "retail": 70        # Consumer spending pressure
        }.get(sector, 60)
        
        return min(100, (base_risk + sector_sensitivity) / 2)
    
    def _identify_key_risk_factors(self, revenue_volatility: float, market_risk: float, 
                                  operational_risk: float, economic_risk: float, sector: str) -> List[str]:
        """Identify key risk factors."""
        factors = []
        
        if revenue_volatility > 60:
            factors.append("High revenue volatility")
        if market_risk > 60:
            factors.append("Competitive market pressure")
        if operational_risk > 60:
            factors.append("Operational vulnerabilities")
        if economic_risk > 60:
            factors.append(f"Economic headwinds affecting {sector} sector")
        
        return factors[:3]
    
    def _recommend_risk_mitigation(self, revenue_volatility: float, market_risk: float,
                                  operational_risk: float, economic_risk: float) -> List[str]:
        """Recommend risk mitigation strategies."""
        recommendations = []
        
        if revenue_volatility > 60:
            recommendations.append("Diversify revenue streams")
        if market_risk > 60:
            recommendations.append("Differentiate from competitors")
        if operational_risk > 60:
            recommendations.append("Strengthen operational processes")
        if economic_risk > 60:
            recommendations.append("Build financial reserves")
        
        return recommendations[:3]
    
    def _identify_growth_drivers(self, business_data: Dict[str, Any], market_position: Dict[str, Any]) -> List[str]:
        """Identify growth drivers."""
        drivers = []
        
        if market_position["performance_ratio"] > 1.1:
            drivers.append("Strong market position")
        
        sector = business_data["sector"]
        if sector == "electronics":
            drivers.append("Growing mobile accessories market")
        elif sector == "food":
            drivers.append("Expanding delivery market")
        
        return drivers
    
    def _identify_growth_barriers(self, business_data: Dict[str, Any], financial_health: Dict[str, Any]) -> List[str]:
        """Identify growth barriers."""
        barriers = []
        
        if financial_health["score"] < 60:
            barriers.append("Financial constraints")
        
        if business_data["current_cash"] < business_data["monthly_expenses"] * 3:
            barriers.append("Limited cash reserves")
        
        return barriers
    
    def _score_market_potential(self, market_opportunity: Dict[str, Any]) -> float:
        """Score market potential (0-100)."""
        return 75  # Placeholder
    
    def _recommend_growth_strategy(self, growth_potential_score: float, 
                                  market_opportunity: Dict[str, Any],
                                  expansion_readiness: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend growth strategy."""
        if growth_potential_score > 80:
            return {"strategy": "aggressive_growth", "focus": "Market expansion"}
        elif growth_potential_score > 60:
            return {"strategy": "steady_growth", "focus": "Operational improvement"}
        else:
            return {"strategy": "consolidation", "focus": "Strengthen fundamentals"}
    
    def _normalize_performance_score(self, performance_metrics: Dict[str, Any]) -> float:
        """Normalize performance metrics to 0-100 scale."""
        growth_rate = performance_metrics["revenue_growth_rate"]
        profit_margin = performance_metrics["profit_margin"]
        
        growth_score = min(100, max(0, (growth_rate + 0.1) * 500))
        margin_score = min(100, profit_margin * 500)
        
        return (growth_score + margin_score) / 2