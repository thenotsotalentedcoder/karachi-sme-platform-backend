"""US Small Business Analysis Engine with real-time economic data integration."""

import statistics
import math
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging

from app.utils.calculations import (
    calculate_growth_rate, calculate_volatility, calculate_trend_direction,
    calculate_profit_margin, calculate_cash_runway, normalize_score,
    calculate_percentile_rank
)

logger = logging.getLogger(__name__)


class USBusinessAnalyzer:
    """Advanced business analysis engine for US small and medium enterprises."""
    
    def __init__(self):
        # US industry benchmarks (updated with real US data)
        self.us_industry_benchmarks = {
            "electronics": {
                "average_monthly_revenue": 125000,  # $125K average
                "typical_profit_margin": 0.15,
                "growth_rate": 0.12,
                "employee_productivity": 180000,  # Revenue per employee
                "inventory_turnover": 8.0,
                "cash_runway_months": 4.5
            },
            "food": {
                "average_monthly_revenue": 85000,   # $85K average
                "typical_profit_margin": 0.18,
                "growth_rate": 0.08,
                "employee_productivity": 65000,
                "inventory_turnover": 12.0,
                "cash_runway_months": 3.2
            },
            "retail": {
                "average_monthly_revenue": 95000,   # $95K average
                "typical_profit_margin": 0.22,
                "growth_rate": 0.06,
                "employee_productivity": 110000,
                "inventory_turnover": 6.5,
                "cash_runway_months": 3.8
            },
            "auto": {
                "average_monthly_revenue": 140000,  # $140K average
                "typical_profit_margin": 0.14,
                "growth_rate": 0.04,
                "employee_productivity": 195000,
                "inventory_turnover": 4.2,
                "cash_runway_months": 5.1
            },
            "manufacturing": {
                "average_monthly_revenue": 280000,  # $280K average
                "typical_profit_margin": 0.12,
                "growth_rate": 0.07,
                "employee_productivity": 220000,
                "inventory_turnover": 5.8,
                "cash_runway_months": 6.2
            }
        }
        
        # US location factors (cost of business index by major metros)
        self.us_location_factors = {
            "new_york": {"cost_index": 1.8, "market_size": 1.9, "competition": 0.9},
            "los_angeles": {"cost_index": 1.6, "market_size": 1.7, "competition": 0.85},
            "chicago": {"cost_index": 1.2, "market_size": 1.4, "competition": 0.75},
            "houston": {"cost_index": 1.0, "market_size": 1.3, "competition": 0.7},
            "phoenix": {"cost_index": 0.9, "market_size": 1.1, "competition": 0.65},
            "philadelphia": {"cost_index": 1.3, "market_size": 1.2, "competition": 0.8},
            "san_antonio": {"cost_index": 0.85, "market_size": 0.9, "competition": 0.6},
            "san_diego": {"cost_index": 1.5, "market_size": 1.2, "competition": 0.75},
            "dallas": {"cost_index": 1.0, "market_size": 1.3, "competition": 0.7},
            "austin": {"cost_index": 1.1, "market_size": 1.2, "competition": 0.72},
            "columbus": {"cost_index": 0.9, "market_size": 0.8, "competition": 0.6},
            "charlotte": {"cost_index": 0.95, "market_size": 0.9, "competition": 0.65},
            "indianapolis": {"cost_index": 0.85, "market_size": 0.75, "competition": 0.55},
            "seattle": {"cost_index": 1.4, "market_size": 1.3, "competition": 0.8},
            "denver": {"cost_index": 1.15, "market_size": 1.1, "competition": 0.7},
            "boston": {"cost_index": 1.6, "market_size": 1.4, "competition": 0.85},
            "atlanta": {"cost_index": 1.0, "market_size": 1.2, "competition": 0.72},
            "miami": {"cost_index": 1.3, "market_size": 1.1, "competition": 0.75},
            "nashville": {"cost_index": 0.95, "market_size": 0.85, "competition": 0.6},
            "kansas_city": {"cost_index": 0.8, "market_size": 0.7, "competition": 0.55}
        }
    
    def analyze_business_performance(self, business_data: Dict[str, Any], 
                                   economic_data: Dict[str, Any] = None,
                                   market_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Comprehensive US small business performance analysis.
        
        Integrates real-time economic data, market conditions, and business metrics
        to provide actionable insights for US SMEs.
        """
        
        logger.info(f"Analyzing US business: {business_data.get('business_name', 'Unknown')}")
        
        try:
            # Core financial analysis
            performance_metrics = self._calculate_performance_metrics(business_data)
            
            # Market position analysis with US benchmarks
            market_position = self._analyze_market_position(business_data, market_data)
            
            # Financial health assessment
            financial_health = self._assess_financial_health(business_data, economic_data)
            
            # Growth analysis and projections
            growth_analysis = self._analyze_growth_potential(business_data, economic_data)
            
            # Risk assessment with US economic factors
            risk_assessment = self._assess_business_risks(business_data, economic_data)
            
            # Economic impact analysis
            economic_impact = self._analyze_economic_impact(business_data, economic_data)
            
            # Competitive analysis
            competitive_analysis = self._analyze_competitive_position(business_data, market_data)
            
            # Overall scoring
            overall_score = self._calculate_overall_score(
                performance_metrics, market_position, financial_health, 
                growth_analysis, risk_assessment
            )
            
            # Compile comprehensive analysis
            analysis_result = {
                "business_profile": {
                    "name": business_data.get("business_name", "Unknown"),
                    "sector": business_data.get("sector", "Unknown"),
                    "location": business_data.get("location", "Unknown"),
                    "years_operating": business_data.get("years_in_business", 0),
                    "employees": business_data.get("employees_count", 0)
                },
                "performance_metrics": performance_metrics,
                "market_position": market_position,
                "financial_health": financial_health,
                "growth_analysis": growth_analysis,
                "risk_assessment": risk_assessment,
                "economic_impact": economic_impact,
                "competitive_analysis": competitive_analysis,
                "overall_score": overall_score,
                "analysis_timestamp": datetime.now().isoformat(),
                "analysis_confidence": self._calculate_analysis_confidence(business_data)
            }
            
            logger.info(f"Analysis completed. Overall score: {overall_score['overall_score']:.1f}")
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"Business analysis failed: {str(e)}")
            return {
                "error": f"Analysis failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def _calculate_performance_metrics(self, business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate core business performance metrics."""
        
        monthly_revenue = business_data.get("monthly_revenue", [])
        monthly_expenses = business_data.get("monthly_expenses", 0)
        current_cash = business_data.get("current_cash", 0)
        employees = business_data.get("employees_count", 1)
        
        if not monthly_revenue:
            monthly_revenue = [0] * 6
        
        # Revenue metrics
        current_revenue = monthly_revenue[-1] if monthly_revenue else 0
        revenue_growth_rate = calculate_growth_rate(monthly_revenue) if len(monthly_revenue) >= 2 else 0
        revenue_volatility = calculate_volatility(monthly_revenue) if len(monthly_revenue) >= 3 else 0
        revenue_trend = calculate_trend_direction(monthly_revenue)
        
        # Profitability metrics
        monthly_profit = current_revenue - monthly_expenses
        profit_margin = calculate_profit_margin(current_revenue, monthly_expenses)
        
        # Efficiency metrics
        revenue_per_employee = current_revenue / max(1, employees)
        cash_runway = calculate_cash_runway(current_cash, monthly_expenses)
        
        # Calculate 6-month totals for annualization
        total_6_month_revenue = sum(monthly_revenue)
        annual_revenue_projection = total_6_month_revenue * 2
        annual_profit_projection = monthly_profit * 12
        
        return {
            "current_revenue": current_revenue,
            "monthly_profit": monthly_profit,
            "profit_margin": profit_margin,
            "revenue_growth_rate": revenue_growth_rate,
            "revenue_volatility": revenue_volatility,
            "revenue_trend": revenue_trend,
            "revenue_per_employee": revenue_per_employee,
            "cash_runway_months": cash_runway,
            "annual_revenue_projection": annual_revenue_projection,
            "annual_profit_projection": annual_profit_projection,
            "financial_efficiency_score": self._calculate_efficiency_score(
                profit_margin, revenue_per_employee, cash_runway
            )
        }
    
    def _analyze_market_position(self, business_data: Dict[str, Any], 
                                market_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze business position in US market."""
        
        sector = business_data.get("sector", "retail")
        current_revenue = business_data.get("monthly_revenue", [0])[-1]
        location = business_data.get("location", "national")
        
        # Get industry benchmarks
        industry_benchmark = self.us_industry_benchmarks.get(sector, 
                                                           self.us_industry_benchmarks["retail"])
        
        # Market position calculations
        market_average_revenue = industry_benchmark["average_monthly_revenue"]
        performance_ratio = current_revenue / market_average_revenue if market_average_revenue > 0 else 0
        
        # Percentile ranking (estimated)
        percentile_rank = min(95, performance_ratio * 50)
        
        # Competitive position
        if performance_ratio >= 1.5:
            performance_category = "top_performer"
        elif performance_ratio >= 1.2:
            performance_category = "above_average"
        elif performance_ratio >= 0.8:
            performance_category = "average"
        elif performance_ratio >= 0.6:
            performance_category = "below_average"
        else:
            performance_category = "underperforming"
        
        # Location advantage analysis
        location_clean = location.lower().replace(" ", "_")
        location_factor = self.us_location_factors.get(location_clean, {
            "cost_index": 1.0, "market_size": 1.0, "competition": 0.7
        })
        
        # Market context
        market_context = {
            "sector_health": "stable",  # Would be updated with real market data
            "growth_opportunities": self._assess_growth_opportunities(sector),
            "competitive_intensity": location_factor["competition"],
            "market_size_advantage": location_factor["market_size"],
            "cost_pressure": location_factor["cost_index"],
            "location_advantage": self._calculate_location_advantage(location_factor)
        }
        
        return {
            "market_average_revenue": market_average_revenue,
            "performance_ratio": performance_ratio,
            "percentile_rank": percentile_rank,
            "performance_category": performance_category,
            "market_context": market_context,
            "competitive_strengths": self._identify_competitive_strengths(business_data, performance_ratio),
            "market_opportunities": self._identify_market_opportunities(sector, performance_ratio)
        }
    
    def _assess_financial_health(self, business_data: Dict[str, Any], 
                                economic_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Assess financial health with US economic context."""
        
        monthly_revenue = business_data.get("monthly_revenue", [])
        monthly_expenses = business_data.get("monthly_expenses", 0)
        current_cash = business_data.get("current_cash", 0)
        
        current_revenue = monthly_revenue[-1] if monthly_revenue else 0
        monthly_profit = current_revenue - monthly_expenses
        
        # Cash flow analysis
        cash_runway = calculate_cash_runway(current_cash, monthly_expenses)
        
        # Liquidity assessment
        liquidity_ratio = current_cash / monthly_expenses if monthly_expenses > 0 else 0
        
        # Debt capacity (simplified)
        annual_revenue = current_revenue * 12
        estimated_debt_capacity = annual_revenue * 0.3  # Conservative 30% of revenue
        
        # Financial stress indicators
        stress_indicators = []
        if cash_runway < 3:
            stress_indicators.append("low_cash_runway")
        if monthly_profit < 0:
            stress_indicators.append("negative_cash_flow")
        if current_revenue < monthly_expenses * 1.1:
            stress_indicators.append("thin_margins")
        
        # Financial health score
        health_score = 50  # Baseline
        
        if cash_runway >= 6:
            health_score += 20
        elif cash_runway >= 3:
            health_score += 10
        else:
            health_score -= 15
        
        if monthly_profit > 0:
            health_score += 15
            if monthly_profit > current_revenue * 0.15:  # 15% profit margin
                health_score += 10
        
        # Economic context impact
        if economic_data:
            fed_rate = economic_data.get("fed_funds_rate", 5.0)
            inflation = economic_data.get("inflation_cpi", 3.0)
            
            # High interest rates impact borrowing capacity
            if fed_rate > 6.0:
                health_score -= 10
            elif fed_rate < 3.0:
                health_score += 5
            
            # High inflation impacts costs
            if inflation > 5.0:
                health_score -= 8
            elif inflation < 2.0:
                health_score += 5
        
        health_score = max(0, min(100, health_score))
        
        # Health status
        if health_score >= 80:
            status = "excellent"
        elif health_score >= 65:
            status = "good"
        elif health_score >= 50:
            status = "fair"
        elif health_score >= 30:
            status = "poor"
        else:
            status = "critical"
        
        return {
            "status": status,
            "health_score": health_score,
            "cash_runway_months": cash_runway,
            "liquidity_ratio": liquidity_ratio,
            "monthly_cash_flow": monthly_profit,
            "debt_capacity": estimated_debt_capacity,
            "stress_indicators": stress_indicators,
            "working_capital": current_cash,
            "burn_rate": monthly_expenses,
            "break_even_revenue": monthly_expenses,
            "financial_recommendations": self._generate_financial_recommendations(
                cash_runway, monthly_profit, health_score
            )
        }
    
    def _analyze_growth_potential(self, business_data: Dict[str, Any], 
                                 economic_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze business growth potential and scalability."""
        
        monthly_revenue = business_data.get("monthly_revenue", [])
        sector = business_data.get("sector", "retail")
        years_in_business = business_data.get("years_in_business", 0)
        employees = business_data.get("employees_count", 1)
        
        # Growth trajectory analysis
        revenue_growth_rate = calculate_growth_rate(monthly_revenue) if len(monthly_revenue) >= 2 else 0
        
        # Business maturity assessment
        if years_in_business < 2:
            maturity_stage = "startup"
            growth_multiplier = 1.5
        elif years_in_business < 5:
            maturity_stage = "growth"
            growth_multiplier = 1.2
        elif years_in_business < 10:
            maturity_stage = "mature"
            growth_multiplier = 1.0
        else:
            maturity_stage = "established"
            growth_multiplier = 0.8
        
        # Scalability factors
        revenue_per_employee = (monthly_revenue[-1] / max(1, employees)) if monthly_revenue else 0
        scalability_score = min(100, (revenue_per_employee / 10000) * 50)  # $10K per employee baseline
        
        # Market growth potential
        industry_benchmark = self.us_industry_benchmarks.get(sector, 
                                                           self.us_industry_benchmarks["retail"])
        industry_growth_rate = industry_benchmark["growth_rate"]
        
        # Economic growth factors
        economic_tailwind = 0
        if economic_data:
            gdp_growth = economic_data.get("gdp_growth", 0.025)
            consumer_confidence = economic_data.get("consumer_confidence", 50)
            
            economic_tailwind = (gdp_growth * 100) + (consumer_confidence - 50) * 0.5
            economic_tailwind = max(-20, min(20, economic_tailwind))
        
        # Growth potential score
        growth_score = 50  # Baseline
        growth_score += revenue_growth_rate * 100  # Revenue growth impact
        growth_score += (scalability_score - 50) * 0.3  # Scalability impact
        growth_score += industry_growth_rate * 50  # Industry growth impact
        growth_score += economic_tailwind  # Economic impact
        growth_score *= growth_multiplier  # Maturity adjustment
        
        growth_score = max(0, min(100, growth_score))
        
        # Growth constraints
        constraints = []
        if revenue_per_employee < 50000:  # $50K threshold
            constraints.append("low_employee_productivity")
        if revenue_growth_rate < 0:
            constraints.append("declining_revenue")
        if years_in_business > 10 and revenue_growth_rate < 0.05:
            constraints.append("mature_market_saturation")
        
        # Growth opportunities
        opportunities = self._identify_growth_opportunities(
            sector, revenue_growth_rate, scalability_score, economic_data
        )
        
        return {
            "growth_score": growth_score,
            "revenue_growth_rate": revenue_growth_rate,
            "maturity_stage": maturity_stage,
            "scalability_score": scalability_score,
            "industry_growth_rate": industry_growth_rate,
            "economic_growth_factor": economic_tailwind,
            "growth_constraints": constraints,
            "growth_opportunities": opportunities,
            "revenue_projection_12m": self._project_revenue_growth(monthly_revenue, revenue_growth_rate),
            "expansion_readiness": self._assess_expansion_readiness(business_data)
        }
    
    def _assess_business_risks(self, business_data: Dict[str, Any], 
                              economic_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Comprehensive business risk assessment."""
        
        monthly_revenue = business_data.get("monthly_revenue", [])
        sector = business_data.get("sector", "retail")
        cash_runway = calculate_cash_runway(
            business_data.get("current_cash", 0),
            business_data.get("monthly_expenses", 0)
        )
        
        # Revenue volatility risk
        revenue_volatility = calculate_volatility(monthly_revenue) if len(monthly_revenue) >= 3 else 0
        volatility_risk = min(100, revenue_volatility * 200)  # Scale to 0-100
        
        # Financial risk
        financial_risk = 0
        if cash_runway < 3:
            financial_risk += 30
        if cash_runway < 1:
            financial_risk += 40
        
        current_revenue = monthly_revenue[-1] if monthly_revenue else 0
        monthly_expenses = business_data.get("monthly_expenses", 0)
        if current_revenue < monthly_expenses:
            financial_risk += 25
        
        # Market risk
        market_risk = 30  # Baseline market risk
        sector_risks = {
            "retail": 40,       # High competition, online disruption
            "food": 35,         # Health regulations, competition
            "electronics": 45,  # Technology disruption, supply chain
            "auto": 50,         # Economic sensitivity, EV transition
            "manufacturing": 35 # Supply chain, economic cycles
        }
        market_risk = sector_risks.get(sector, 35)
        
        # Economic risk
        economic_risk = 25  # Baseline
        if economic_data:
            fed_rate = economic_data.get("fed_funds_rate", 5.0)
            inflation = economic_data.get("inflation_cpi", 3.0)
            unemployment = economic_data.get("unemployment_rate", 4.0)
            
            # Interest rate risk
            if fed_rate > 6.0:
                economic_risk += 15
            elif fed_rate < 2.0:
                economic_risk -= 5
            
            # Inflation risk
            if inflation > 5.0:
                economic_risk += 20
            elif inflation > 3.0:
                economic_risk += 10
            
            # Recession risk
            if unemployment > 6.0:
                economic_risk += 15
        
        # Operational risk
        employees = business_data.get("employees_count", 1)
        operational_risk = 20  # Baseline
        
        if employees <= 2:  # Key person dependency
            operational_risk += 25
        elif employees <= 5:
            operational_risk += 15
        
        years_in_business = business_data.get("years_in_business", 0)
        if years_in_business < 2:
            operational_risk += 20
        
        # Overall risk score
        risk_components = {
            "revenue_volatility": volatility_risk,
            "financial_risk": min(100, financial_risk),
            "market_risk": market_risk,
            "economic_risk": min(100, economic_risk),
            "operational_risk": min(100, operational_risk)
        }
        
        overall_risk = (
            risk_components["revenue_volatility"] * 0.2 +
            risk_components["financial_risk"] * 0.3 +
            risk_components["market_risk"] * 0.2 +
            risk_components["economic_risk"] * 0.15 +
            risk_components["operational_risk"] * 0.15
        )
        
        # Risk level classification
        if overall_risk >= 70:
            risk_level = "high"
        elif overall_risk >= 50:
            risk_level = "medium"
        elif overall_risk >= 30:
            risk_level = "low"
        else:
            risk_level = "very_low"
        
        # Risk mitigation recommendations
        mitigation_strategies = self._generate_risk_mitigation_strategies(
            risk_components, business_data
        )
        
        return {
            "risk_level": risk_level,
            "overall_risk_score": overall_risk,
            "risk_components": risk_components,
            "key_vulnerabilities": self._identify_key_vulnerabilities(risk_components),
            "mitigation_strategies": mitigation_strategies,
            "stress_test_scenarios": self._generate_stress_test_scenarios(business_data),
            "risk_monitoring_kpis": self._suggest_risk_monitoring_kpis(sector)
        }
    
    def _analyze_economic_impact(self, business_data: Dict[str, Any], 
                                economic_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze how current US economic conditions impact the business."""
        
        if not economic_data:
            return {"status": "no_economic_data"}
        
        sector = business_data.get("sector", "retail")
        current_revenue = business_data.get("monthly_revenue", [0])[-1]
        
        # Interest rate impact
        fed_rate = economic_data.get("fed_funds_rate", 5.0)
        interest_rate_impact = self._calculate_interest_rate_impact(fed_rate, sector, current_revenue)
        
        # Inflation impact
        inflation = economic_data.get("inflation_cpi", 3.0)
        inflation_impact = self._calculate_inflation_impact(inflation, sector)
        
        # Employment impact
        unemployment = economic_data.get("unemployment_rate", 4.0)
        employment_impact = self._calculate_employment_impact(unemployment, sector)
        
        # Consumer confidence impact
        consumer_confidence = economic_data.get("consumer_confidence", 50)
        consumer_impact = self._calculate_consumer_confidence_impact(consumer_confidence, sector)
        
        # GDP growth impact
        gdp_growth = economic_data.get("gdp_growth", 0.025)
        gdp_impact = self._calculate_gdp_impact(gdp_growth, sector)
        
        # Overall economic impact score
        impact_scores = [
            interest_rate_impact["score"],
            inflation_impact["score"], 
            employment_impact["score"],
            consumer_impact["score"],
            gdp_impact["score"]
        ]
        
        overall_impact_score = sum(impact_scores) / len(impact_scores)
        
        # Economic headwinds/tailwinds
        if overall_impact_score >= 60:
            economic_environment = "strong_tailwinds"
        elif overall_impact_score >= 40:
            economic_environment = "moderate_tailwinds"
        elif overall_impact_score >= -10:
            economic_environment = "neutral"
        elif overall_impact_score >= -40:
            economic_environment = "moderate_headwinds"
        else:
            economic_environment = "strong_headwinds"
        
        return {
            "economic_environment": economic_environment,
            "overall_impact_score": overall_impact_score,
            "interest_rate_impact": interest_rate_impact,
            "inflation_impact": inflation_impact,
            "employment_impact": employment_impact,
            "consumer_confidence_impact": consumer_impact,
            "gdp_growth_impact": gdp_impact,
            "key_economic_factors": self._identify_key_economic_factors(economic_data, sector),
            "economic_recommendations": self._generate_economic_recommendations(
                overall_impact_score, economic_environment, sector
            )
        }
    
    def _analyze_competitive_position(self, business_data: Dict[str, Any], 
                                    market_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze competitive position and market dynamics."""
        
        sector = business_data.get("sector", "retail")
        current_revenue = business_data.get("monthly_revenue", [0])[-1]
        employees = business_data.get("employees_count", 1)
        years_in_business = business_data.get("years_in_business", 0)
        
        # Industry benchmark comparison
        industry_benchmark = self.us_industry_benchmarks.get(sector, 
                                                           self.us_industry_benchmarks["retail"])
        
        # Competitive metrics
        revenue_per_employee = current_revenue / max(1, employees)
        benchmark_productivity = industry_benchmark["employee_productivity"] / 12  # Monthly
        productivity_ratio = revenue_per_employee / benchmark_productivity if benchmark_productivity > 0 else 1
        
        # Market position strengths
        competitive_strengths = []
        competitive_weaknesses = []
        
        if productivity_ratio > 1.2:
            competitive_strengths.append("high_employee_productivity")
        elif productivity_ratio < 0.8:
            competitive_weaknesses.append("low_employee_productivity")
        
        if years_in_business > 5:
            competitive_strengths.append("established_market_presence")
        elif years_in_business < 2:
            competitive_weaknesses.append("limited_market_presence")
        
        # Revenue size classification
        if current_revenue > industry_benchmark["average_monthly_revenue"] * 1.5:
            size_category = "large_for_sector"
            competitive_strengths.append("economies_of_scale")
        elif current_revenue > industry_benchmark["average_monthly_revenue"]:
            size_category = "above_average"
        elif current_revenue > industry_benchmark["average_monthly_revenue"] * 0.5:
            size_category = "average"
        else:
            size_category = "small_player"
            competitive_weaknesses.append("limited_scale")
        
        # Competitive intensity by sector
        competitive_intensity = {
            "retail": 85,
            "food": 90,
            "electronics": 80,
            "auto": 75,
            "manufacturing": 70
        }
        
        sector_intensity = competitive_intensity.get(sector, 80)
        
        # Differentiation opportunities
        differentiation_opportunities = self._identify_differentiation_opportunities(
            sector, size_category, years_in_business
        )
        
        # Competitive advantages
        competitive_advantages = self._assess_competitive_advantages(
            business_data, productivity_ratio, years_in_business
        )
        
        # Market share estimate (very rough)
        estimated_market_share = min(5.0, (current_revenue / industry_benchmark["average_monthly_revenue"]) * 0.1)
        
        return {
            "size_category": size_category,
            "productivity_ratio": productivity_ratio,
            "competitive_intensity": sector_intensity,
            "competitive_strengths": competitive_strengths,
            "competitive_weaknesses": competitive_weaknesses,
            "competitive_advantages": competitive_advantages,
            "differentiation_opportunities": differentiation_opportunities,
            "estimated_market_share": estimated_market_share,
            "competitive_threats": self._identify_competitive_threats(sector),
            "strategic_positioning": self._recommend_strategic_positioning(
                size_category, competitive_strengths, sector
            )
        }
    
    def _calculate_overall_score(self, performance_metrics: Dict[str, Any],
                                market_position: Dict[str, Any],
                                financial_health: Dict[str, Any],
                                growth_analysis: Dict[str, Any],
                                risk_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate comprehensive overall business score."""
        
        # Component weights
        weights = {
            "financial_performance": 0.30,
            "market_position": 0.25,
            "financial_health": 0.20,
            "growth_potential": 0.15,
            "risk_management": 0.10
        }

        # Component scores
        financial_score = performance_metrics.get("financial_efficiency_score", 50)
        market_score = market_position.get("percentile_rank", 50)
        health_score = financial_health.get("health_score", 50)
        growth_score = growth_analysis.get("growth_score", 50)
        risk_score = 100 - risk_assessment.get("overall_risk_score", 50)  # Invert risk

        # Weighted overall score
        overall_score = (
            financial_score * weights["financial_performance"] +
            market_score * weights["market_position"] +
            health_score * weights["financial_health"] +
            growth_score * weights["growth_potential"] +
            risk_score * weights["risk_management"]
        )

        # Score classification
        if overall_score >= 80:
            grade = "A"
            classification = "excellent"
        elif overall_score >= 70:
            grade = "B"
            classification = "good"
        elif overall_score >= 60:
            grade = "C"
            classification = "average"
        elif overall_score >= 50:
            grade = "D"
            classification = "below_average"
        else:
            grade = "F"
            classification = "poor"

        # Component breakdown for transparency
        component_breakdown = {
            "financial_performance": financial_score,
            "market_position": market_score,
            "financial_health": health_score,
            "growth_potential": growth_score,
            "risk_management": risk_score
        }

        return {
            "overall_score": overall_score,
            "grade": grade,
            "classification": classification,
            "component_breakdown": component_breakdown,
            "strengths": self._identify_top_strengths(component_breakdown),
            "improvement_areas": self._identify_improvement_areas(component_breakdown),
            "score_trajectory": self._predict_score_trajectory(component_breakdown)
        }
    
    # Helper methods for calculations
    
    def _calculate_efficiency_score(self, profit_margin: float, revenue_per_employee: float, cash_runway: float) -> float:
        """Calculate financial efficiency score."""
        
        efficiency_score = 50  # Baseline
        
        # Profit margin component
        if profit_margin > 0.20:  # 20%+
            efficiency_score += 25
        elif profit_margin > 0.15:  # 15%+
            efficiency_score += 15
        elif profit_margin > 0.10:  # 10%+
            efficiency_score += 10
        elif profit_margin < 0:
            efficiency_score -= 20
        
        # Revenue per employee component
        if revenue_per_employee > 15000:  # $15K+ per month
            efficiency_score += 15
        elif revenue_per_employee > 10000:  # $10K+ per month
            efficiency_score += 10
        elif revenue_per_employee < 5000:  # Under $5K per month
            efficiency_score -= 10
        
        # Cash runway component
        if cash_runway >= 6:
            efficiency_score += 10
        elif cash_runway >= 3:
            efficiency_score += 5
        elif cash_runway < 2:
            efficiency_score -= 15
        
        return max(0, min(100, efficiency_score))
    
    def _assess_growth_opportunities(self, sector: str) -> List[str]:
        """Identify growth opportunities by sector."""
        
        opportunities = {
            "electronics": [
                "Smart home device integration",
                "Mobile device repair services",
                "E-commerce platform development",
                "B2B technology consulting"
            ],
            "food": [
                "Meal delivery partnerships",
                "Catering service expansion",
                "Health-conscious menu options",
                "Food truck or mobile service"
            ],
            "retail": [
                "Omnichannel sales strategy",
                "Private label products",
                "Subscription service models",
                "Local community partnerships"
            ],
            "auto": [
                "Electric vehicle services",
                "Mobile repair services",
                "Fleet maintenance contracts",
                "Auto detailing services"
            ],
            "manufacturing": [
                "Automation implementation",
                "Custom manufacturing services",
                "Supply chain optimization",
                "Export market development"
            ]
        }
        
        return opportunities.get(sector, [
            "Digital transformation",
            "Customer experience enhancement",
            "Operational efficiency improvements",
            "Market expansion opportunities"
        ])
    
    def _calculate_location_advantage(self, location_factor: Dict[str, float]) -> float:
        """Calculate location advantage score."""
        
        # Higher market size is good, higher cost and competition are bad
        advantage_score = (
            location_factor["market_size"] * 50 +  # Market size benefit
            (2.0 - location_factor["cost_index"]) * 25 +  # Cost advantage (inverted)
            (1.0 - location_factor["competition"]) * 25  # Competition advantage (inverted)
        )
        
        return max(-50, min(50, advantage_score))
    
    def _identify_competitive_strengths(self, business_data: Dict[str, Any], performance_ratio: float) -> List[str]:
        """Identify competitive strengths based on performance."""
        
        strengths = []
        
        if performance_ratio > 1.3:
            strengths.append("strong_revenue_performance")
        
        years_in_business = business_data.get("years_in_business", 0)
        if years_in_business > 5:
            strengths.append("established_reputation")
        
        monthly_revenue = business_data.get("monthly_revenue", [])
        if len(monthly_revenue) >= 3:
            growth_rate = calculate_growth_rate(monthly_revenue)
            if growth_rate > 0.1:  # 10%+ growth
                strengths.append("strong_growth_momentum")
        
        employees = business_data.get("employees_count", 1)
        current_revenue = monthly_revenue[-1] if monthly_revenue else 0
        if current_revenue / max(1, employees) > 12000:  # $12K+ per employee monthly
            strengths.append("high_productivity")
        
        current_cash = business_data.get("current_cash", 0)
        monthly_expenses = business_data.get("monthly_expenses", 0)
        if current_cash > monthly_expenses * 6:  # 6+ months runway
            strengths.append("strong_financial_position")
        
        return strengths
    
    def _identify_market_opportunities(self, sector: str, performance_ratio: float) -> List[str]:
        """Identify market opportunities based on sector and performance."""
        
        opportunities = []
        
        if performance_ratio > 1.2:
            opportunities.append("market_leadership_potential")
            opportunities.append("premium_pricing_opportunity")
        elif performance_ratio < 0.8:
            opportunities.append("market_share_growth_potential")
            opportunities.append("operational_improvement_gains")
        
        # Sector-specific opportunities
        sector_opportunities = {
            "electronics": ["5G technology adoption", "IoT device market", "Remote work solutions"],
            "food": ["Health-conscious trends", "Plant-based options", "Delivery optimization"],
            "retail": ["E-commerce integration", "Experiential retail", "Sustainability focus"],
            "auto": ["EV transition services", "Autonomous vehicle prep", "Connected car services"],
            "manufacturing": ["Automation adoption", "Nearshoring trends", "Sustainability initiatives"]
        }
        
        opportunities.extend(sector_opportunities.get(sector, ["Digital transformation", "Customer experience"]))
        
        return opportunities[:4]  # Return top 4 opportunities
    
    def _generate_financial_recommendations(self, cash_runway: float, monthly_profit: float, health_score: float) -> List[str]:
        """Generate financial recommendations based on health metrics."""
        
        recommendations = []
        
        if cash_runway < 3:
            recommendations.append("Urgent: Improve cash flow or secure emergency funding")
            recommendations.append("Reduce non-essential expenses immediately")
        elif cash_runway < 6:
            recommendations.append("Build cash reserves to 6+ months of expenses")
        
        if monthly_profit < 0:
            recommendations.append("Priority: Achieve positive monthly cash flow")
            recommendations.append("Review pricing strategy and cost structure")
        elif monthly_profit < 5000:
            recommendations.append("Focus on profit margin improvement")
        
        if health_score < 50:
            recommendations.append("Consider professional financial consulting")
            recommendations.append("Implement strict cash flow monitoring")
        
        return recommendations
    
    def _identify_growth_opportunities(self, sector: str, revenue_growth_rate: float, 
                                     scalability_score: float, economic_data: Dict[str, Any] = None) -> List[str]:
        """Identify specific growth opportunities."""
        
        opportunities = []
        
        if revenue_growth_rate < 0.05:  # Low growth
            opportunities.append("operational_efficiency_improvements")
            opportunities.append("new_customer_acquisition_strategies")
        
        if scalability_score < 50:
            opportunities.append("process_automation_opportunities")
            opportunities.append("technology_upgrade_investments")
        
        # Economic environment opportunities
        if economic_data:
            unemployment = economic_data.get("unemployment_rate", 4.0)
            if unemployment > 5.0:
                opportunities.append("talent_acquisition_opportunity")
            
            fed_rate = economic_data.get("fed_funds_rate", 5.0)
            if fed_rate < 3.0:
                opportunities.append("low_cost_expansion_financing")
        
        # Sector-specific growth opportunities
        sector_growth = {
            "electronics": ["subscription_service_models", "repair_service_expansion"],
            "food": ["catering_business_development", "meal_kit_services"],
            "retail": ["e_commerce_channel_development", "private_label_products"],
            "auto": ["electric_vehicle_services", "fleet_management_contracts"],
            "manufacturing": ["custom_manufacturing_services", "export_market_development"]
        }
        
        opportunities.extend(sector_growth.get(sector, ["market_expansion", "service_diversification"]))
        
        return opportunities[:5]  # Return top 5 opportunities
    
    def _project_revenue_growth(self, monthly_revenue: List[float], growth_rate: float) -> Dict[str, float]:
        """Project 12-month revenue growth."""
        
        if not monthly_revenue:
            return {"current_annual": 0, "projected_annual": 0, "growth_amount": 0}
        
        current_monthly = monthly_revenue[-1]
        current_annual = current_monthly * 12
        
        # Apply growth rate for 12-month projection
        projected_annual = current_annual * (1 + growth_rate)
        growth_amount = projected_annual - current_annual
        
        return {
            "current_annual": current_annual,
            "projected_annual": projected_annual,
            "growth_amount": growth_amount,
            "monthly_projection": projected_annual / 12
        }
    
    def _assess_expansion_readiness(self, business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess readiness for business expansion."""
        
        monthly_revenue = business_data.get("monthly_revenue", [])
        current_cash = business_data.get("current_cash", 0)
        monthly_expenses = business_data.get("monthly_expenses", 0)
        employees = business_data.get("employees_count", 1)
        
        readiness_score = 0
        readiness_factors = []
        
        # Financial readiness
        cash_runway = calculate_cash_runway(current_cash, monthly_expenses)
        if cash_runway >= 6:
            readiness_score += 25
            readiness_factors.append("sufficient_cash_reserves")
        elif cash_runway >= 3:
            readiness_score += 15
        
        # Profitability readiness
        if monthly_revenue:
            current_revenue = monthly_revenue[-1]
            monthly_profit = current_revenue - monthly_expenses
            
            if monthly_profit > monthly_expenses * 0.2:  # 20% of expenses
                readiness_score += 25
                readiness_factors.append("strong_profitability")
            elif monthly_profit > 0:
                readiness_score += 15
        
        # Operational readiness
        if employees >= 3:
            readiness_score += 20
            readiness_factors.append("adequate_staffing")
        
        # Market position readiness
        if len(monthly_revenue) >= 6:
            growth_rate = calculate_growth_rate(monthly_revenue)
            if growth_rate > 0.1:  # 10%+ growth
                readiness_score += 20
                readiness_factors.append("growth_momentum")
            elif growth_rate > 0:
                readiness_score += 10
        
        # Years in business
        years_in_business = business_data.get("years_in_business", 0)
        if years_in_business >= 3:
            readiness_score += 10
            readiness_factors.append("market_experience")
        
        # Readiness assessment
        if readiness_score >= 80:
            readiness_level = "highly_ready"
        elif readiness_score >= 60:
            readiness_level = "ready"
        elif readiness_score >= 40:
            readiness_level = "partially_ready"
        else:
            readiness_level = "not_ready"
        
        return {
            "readiness_level": readiness_level,
            "readiness_score": readiness_score,
            "readiness_factors": readiness_factors,
            "expansion_timeline": self._suggest_expansion_timeline(readiness_level),
            "preparation_steps": self._suggest_expansion_preparation(readiness_score, readiness_factors)
        }
    
    def _generate_risk_mitigation_strategies(self, risk_components: Dict[str, float], business_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate risk mitigation strategies."""
        
        strategies = []
        
        # Financial risk mitigation
        if risk_components["financial_risk"] > 60:
            strategies.append({
                "risk_type": "financial",
                "strategy": "Establish emergency credit line",
                "priority": "high",
                "timeline": "immediate"
            })
            strategies.append({
                "risk_type": "financial",
                "strategy": "Implement strict cash flow monitoring",
                "priority": "high",
                "timeline": "this_week"
            })
        
        # Revenue volatility mitigation
        if risk_components["revenue_volatility"] > 50:
            strategies.append({
                "risk_type": "revenue",
                "strategy": "Diversify customer base",
                "priority": "medium",
                "timeline": "3_months"
            })
            strategies.append({
                "risk_type": "revenue",
                "strategy": "Develop recurring revenue streams",
                "priority": "medium",
                "timeline": "6_months"
            })
        
        # Market risk mitigation
        if risk_components["market_risk"] > 60:
            strategies.append({
                "risk_type": "market",
                "strategy": "Monitor competitive landscape",
                "priority": "medium",
                "timeline": "ongoing"
            })
            strategies.append({
                "risk_type": "market",
                "strategy": "Develop unique value proposition",
                "priority": "high",
                "timeline": "3_months"
            })
        
        # Operational risk mitigation
        if risk_components["operational_risk"] > 50:
            employees = business_data.get("employees_count", 1)
            if employees <= 2:
                strategies.append({
                    "risk_type": "operational",
                    "strategy": "Cross-train employees and document processes",
                    "priority": "high",
                    "timeline": "1_month"
                })
        
        return strategies
    
    def _identify_key_vulnerabilities(self, risk_components: Dict[str, float]) -> List[str]:
        """Identify key business vulnerabilities."""
        
        vulnerabilities = []
        
        # Sort risks by severity
        sorted_risks = sorted(risk_components.items(), key=lambda x: x[1], reverse=True)
        
        for risk_type, risk_score in sorted_risks[:3]:  # Top 3 risks
            if risk_score > 60:
                if risk_type == "financial_risk":
                    vulnerabilities.append("cash_flow_instability")
                elif risk_type == "revenue_volatility":
                    vulnerabilities.append("unpredictable_revenue")
                elif risk_type == "market_risk":
                    vulnerabilities.append("competitive_pressure")
                elif risk_type == "economic_risk":
                    vulnerabilities.append("economic_sensitivity")
                elif risk_type == "operational_risk":
                    vulnerabilities.append("operational_dependencies")
        
        return vulnerabilities
    
    def _generate_stress_test_scenarios(self, business_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate stress test scenarios."""
        
        monthly_revenue = business_data.get("monthly_revenue", [])
        monthly_expenses = business_data.get("monthly_expenses", 0)
        current_cash = business_data.get("current_cash", 0)
        
        current_revenue = monthly_revenue[-1] if monthly_revenue else 0
        
        scenarios = [
            {
                "scenario": "20% Revenue Drop",
                "revenue_impact": current_revenue * 0.8,
                "monthly_loss": (current_revenue * 0.8) - monthly_expenses,
                "survival_months": max(0, current_cash / max(1, monthly_expenses - (current_revenue * 0.8))),
                "severity": "moderate"
            },
            {
                "scenario": "40% Revenue Drop",
                "revenue_impact": current_revenue * 0.6,
                "monthly_loss": (current_revenue * 0.6) - monthly_expenses,
                "survival_months": max(0, current_cash / max(1, monthly_expenses - (current_revenue * 0.6))),
                "severity": "severe"
            },
            {
                "scenario": "50% Expense Increase",
                "revenue_impact": current_revenue,
                "monthly_loss": current_revenue - (monthly_expenses * 1.5),
                "survival_months": max(0, current_cash / max(1, (monthly_expenses * 1.5) - current_revenue)),
                "severity": "moderate"
            }
        ]
        
        return scenarios
    
    def _suggest_risk_monitoring_kpis(self, sector: str) -> List[str]:
        """Suggest KPIs for risk monitoring."""
        
        base_kpis = [
            "monthly_cash_flow",
            "cash_runway_months",
            "customer_concentration_ratio",
            "monthly_burn_rate",
            "revenue_volatility_index"
        ]
        
        sector_kpis = {
            "retail": ["inventory_turnover", "same_store_sales", "customer_acquisition_cost"],
            "food": ["food_cost_percentage", "labor_cost_ratio", "customer_satisfaction_score"],
            "electronics": ["warranty_claim_rate", "inventory_obsolescence", "technology_refresh_cycle"],
            "auto": ["parts_availability", "customer_retention_rate", "service_bay_utilization"],
            "manufacturing": ["capacity_utilization", "defect_rate", "supplier_reliability_score"]
        }
        
        return base_kpis + sector_kpis.get(sector, ["industry_specific_metrics"])
    
    def _calculate_interest_rate_impact(self, fed_rate: float, sector: str, revenue: float) -> Dict[str, Any]:
        """Calculate interest rate impact on business."""
        
        # Interest rate sensitivity by sector
        rate_sensitivity = {
            "auto": 0.8,         # High sensitivity (big ticket items)
            "retail": 0.6,       # Medium-high sensitivity
            "manufacturing": 0.5, # Medium sensitivity
            "electronics": 0.4,  # Medium sensitivity
            "food": 0.3          # Lower sensitivity (necessities)
        }
        
        sensitivity = rate_sensitivity.get(sector, 0.5)
        
        # Impact calculation (5% is neutral rate)
        rate_deviation = fed_rate - 5.0
        impact_magnitude = rate_deviation * sensitivity * 10
        
        # Impact on score (0-100 scale, 50 is neutral)
        impact_score = 50 - impact_magnitude
        impact_score = max(-50, min(100, impact_score))
        
        if impact_score > 60:
            impact_description = "favorable_low_rates"
        elif impact_score > 40:
            impact_description = "neutral"
        elif impact_score > 20:
            impact_description = "moderate_pressure"
        else:
            impact_description = "significant_pressure"
        
        return {
            "score": impact_score,
            "description": impact_description,
            "fed_rate": fed_rate,
            "sensitivity": sensitivity,
            "estimated_impact": f"{impact_magnitude:+.1f}% on demand/costs"
        }
    
    def _calculate_inflation_impact(self, inflation_rate: float, sector: str) -> Dict[str, Any]:
        """Calculate inflation impact on business."""
        
        # Inflation impact by sector (ability to pass through costs)
        inflation_pass_through = {
            "food": 0.7,         # Good pass-through ability
            "auto": 0.6,         # Moderate pass-through
            "retail": 0.5,       # Limited pass-through
            "electronics": 0.4,  # Low pass-through (competitive)
            "manufacturing": 0.6  # Moderate pass-through
        }
        
        pass_through = inflation_pass_through.get(sector, 0.5)
        
        # Net inflation impact (what can't be passed through hurts margins)
        net_impact = inflation_rate * (1 - pass_through) * 100
        
        # Score calculation (higher inflation = lower score)
        impact_score = 70 - net_impact  # 3% target inflation = 70 score
        impact_score = max(0, min(100, impact_score))
        
        if impact_score > 65:
            impact_description = "minimal_impact"
        elif impact_score > 50:
            impact_description = "manageable_pressure"
        elif impact_score > 35:
            impact_description = "significant_pressure"
        else:
            impact_description = "severe_margin_pressure"
        
        return {
            "score": impact_score,
            "description": impact_description,
            "inflation_rate": inflation_rate,
            "pass_through_ability": pass_through,
            "net_cost_pressure": f"{net_impact:.1f}%"
        }
    
    def _calculate_employment_impact(self, unemployment_rate: float, sector: str) -> Dict[str, Any]:
        """Calculate employment/labor market impact."""
        
        # Employment impact varies by sector's labor intensity
        labor_intensity = {
            "food": 0.9,         # Very labor intensive
            "retail": 0.8,       # High labor intensity
            "auto": 0.6,         # Moderate labor intensity
            "manufacturing": 0.7, # Moderate-high labor intensity
            "electronics": 0.5   # Lower labor intensity
        }
        
        intensity = labor_intensity.get(sector, 0.7)
        
        # Unemployment impact (lower unemployment = tighter labor market = higher costs)
        # 4% unemployment is considered neutral
        unemployment_pressure = (4.0 - unemployment_rate) * intensity * 10
        
        impact_score = 50 - unemployment_pressure
        impact_score = max(0, min(100, impact_score))
        
        if unemployment_rate < 3.5:
            impact_description = "very_tight_labor_market"
        elif unemployment_rate < 4.5:
            impact_description = "tight_labor_market"
        elif unemployment_rate < 6.0:
            impact_description = "balanced_labor_market"
        else:
            impact_description = "abundant_labor_supply"
        
        return {
            "score": impact_score,
            "description": impact_description,
            "unemployment_rate": unemployment_rate,
            "labor_intensity": intensity,
            "hiring_difficulty": "high" if unemployment_rate < 4.0 else "moderate" if unemployment_rate < 6.0 else "low"
        }
    
    def _calculate_consumer_confidence_impact(self, consumer_confidence: float, sector: str) -> Dict[str, Any]:
        """Calculate consumer confidence impact."""
        
        # Consumer confidence sensitivity by sector
        confidence_sensitivity = {
            "auto": 0.9,         # Very sensitive to confidence
            "electronics": 0.8,  # High sensitivity
            "retail": 0.7,       # Moderate-high sensitivity
            "food": 0.4,         # Lower sensitivity (necessities)
            "manufacturing": 0.5  # Moderate sensitivity (B2B focus)
        }
        
        sensitivity = confidence_sensitivity.get(sector, 0.6)
        
        # Confidence impact (50 is neutral consumer confidence)
        confidence_impact = (consumer_confidence - 50) * sensitivity
        
        impact_score = 50 + confidence_impact
        impact_score = max(0, min(100, impact_score))
        
        if consumer_confidence > 70:
            impact_description = "strong_consumer_demand"
        elif consumer_confidence > 55:
            impact_description = "healthy_consumer_sentiment"
        elif consumer_confidence > 45:
            impact_description = "neutral_consumer_sentiment"
        elif consumer_confidence > 35:
            impact_description = "weak_consumer_confidence"
        else:
            impact_description = "very_weak_consumer_demand"
        
        return {
            "score": impact_score,
            "description": impact_description,
            "consumer_confidence": consumer_confidence,
            "sensitivity": sensitivity,
            "demand_outlook": "strong" if consumer_confidence > 65 else "moderate" if consumer_confidence > 45 else "weak"
        }
    
    def _calculate_gdp_impact(self, gdp_growth: float, sector: str) -> Dict[str, Any]:
        """Calculate GDP growth impact on business."""
        
        # GDP sensitivity by sector
        gdp_sensitivity = {
            "auto": 1.2,         # High sensitivity to economic cycles
            "manufacturing": 1.1, # High sensitivity
            "electronics": 1.0,  # Moderate sensitivity
            "retail": 0.8,       # Moderate sensitivity
            "food": 0.6          # Lower sensitivity
        }
        
        sensitivity = gdp_sensitivity.get(sector, 0.9)
        
        # GDP impact (2.5% is trend growth)
        gdp_deviation = gdp_growth - 0.025  # 2.5% trend
        impact_magnitude = gdp_deviation * sensitivity * 1000  # Scale for scoring
        
        impact_score = 50 + impact_magnitude
        impact_score = max(0, min(100, impact_score))
        
        if gdp_growth > 0.035:  # 3.5%+
            impact_description = "strong_economic_growth"
        elif gdp_growth > 0.025:  # 2.5%+
            impact_description = "healthy_economic_growth"
        elif gdp_growth > 0.01:   # 1%+
            impact_description = "slow_economic_growth"
        elif gdp_growth > 0:
            impact_description = "weak_economic_growth"
        else:
            impact_description = "economic_contraction"
        
        return {
            "score": impact_score,
            "description": impact_description,
            "gdp_growth": gdp_growth,
            "sensitivity": sensitivity,
            "business_cycle_phase": "expansion" if gdp_growth > 0.025 else "slowdown" if gdp_growth > 0 else "recession"
        }
    
    def _identify_key_economic_factors(self, economic_data: Dict[str, Any], sector: str) -> List[str]:
        """Identify key economic factors affecting the business."""
        
        factors = []
        
        fed_rate = economic_data.get("fed_funds_rate", 5.0)
        inflation = economic_data.get("inflation_cpi", 3.0)
        unemployment = economic_data.get("unemployment_rate", 4.0)
        consumer_confidence = economic_data.get("consumer_confidence", 50)
        gdp_growth = economic_data.get("gdp_growth", 0.025)
        
        # Interest rate factors
        if fed_rate > 6.0:
            factors.append(f"High interest rates ({fed_rate:.1f}%) increasing borrowing costs")
        elif fed_rate < 3.0:
            factors.append(f"Low interest rates ({fed_rate:.1f}%) supporting expansion")
        
        # Inflation factors
        if inflation > 5.0:
            factors.append(f"High inflation ({inflation:.1f}%) pressuring costs and margins")
        elif inflation < 2.0:
            factors.append(f"Low inflation ({inflation:.1f}%) supporting stable costs")
        
        # Labor market factors
        if unemployment < 3.5:
            factors.append(f"Very tight labor market ({unemployment:.1f}% unemployment)")
        elif unemployment > 6.0:
            factors.append(f"Loose labor market ({unemployment:.1f}% unemployment)")
        
        # Consumer factors
        if consumer_confidence > 70:
            factors.append(f"Strong consumer confidence ({consumer_confidence:.0f}) boosting demand")
        elif consumer_confidence < 40:
            factors.append(f"Weak consumer confidence ({consumer_confidence:.0f}) restraining demand")
        
        # Growth factors
        if gdp_growth > 0.035:
            factors.append(f"Strong economic growth ({gdp_growth*100:.1f}%) driving expansion")
        elif gdp_growth < 0.01:
            factors.append(f"Slow economic growth ({gdp_growth*100:.1f}%) limiting opportunities")
        
        return factors[:4]  # Return top 4 factors
    
    def _generate_economic_recommendations(self, impact_score: float, environment: str, sector: str) -> List[str]:
        """Generate recommendations based on economic environment."""
        
        recommendations = []
        
        if environment == "strong_headwinds":
            recommendations.extend([
                "Focus on cash flow preservation and cost control",
                "Delay major capital investments until conditions improve",
                "Consider defensive pricing strategies",
                "Strengthen customer relationships to maintain loyalty"
            ])
        elif environment == "moderate_headwinds":
            recommendations.extend([
                "Maintain conservative cash management",
                "Evaluate non-essential spending carefully",
                "Focus on operational efficiency improvements",
                "Monitor customer payment terms closely"
            ])
        elif environment == "strong_tailwinds":
            recommendations.extend([
                "Consider accelerating growth investments",
                "Evaluate expansion opportunities",
                "Build market share while conditions are favorable",
                "Strengthen competitive position for future cycles"
            ])
        elif environment == "moderate_tailwinds":
            recommendations.extend([
                "Selectively invest in growth opportunities",
                "Maintain healthy cash reserves",
                "Focus on sustainable growth strategies",
                "Prepare for potential economic shifts"
            ])
        
        return recommendations[:3]  # Return top 3 recommendations
    
    def _identify_differentiation_opportunities(self, sector: str, size_category: str, years_in_business: int) -> List[str]:
        """Identify differentiation opportunities."""
        
        opportunities = []
        
        # Size-based opportunities
        if size_category == "small_player":
            opportunities.extend([
                "personalized_customer_service",
                "niche_market_specialization",
                "agility_and_quick_response"
            ])
        elif size_category == "large_for_sector":
            opportunities.extend([
                "economies_of_scale_pricing",
                "comprehensive_service_offerings",
                "market_leadership_positioning"
            ])

        # Experience-based opportunities
        if years_in_business > 10:
            opportunities.append("established_reputation_and_trust")
        elif years_in_business < 3:
            opportunities.append("innovative_approaches_and_technology")

        # Sector-specific differentiation
        sector_differentiation = {
            "electronics": [
                "specialized_technical_expertise",
                "extended_warranty_services",
                "custom_integration_solutions"
            ],
            "food": [
                "unique_cuisine_or_flavors",
                "farm_to_table_sourcing",
                "dietary_restriction_specialization"
            ],
            "retail": [
                "curated_product_selection",
                "exceptional_shopping_experience",
                "local_community_connection"
            ],
            "auto": [
                "specialized_vehicle_expertise",
                "comprehensive_service_packages",
                "mobile_or_convenience_services"
            ],
            "manufacturing": [
                "custom_manufacturing_capabilities",
                "rapid_prototyping_services",
                "quality_and_precision_focus"
            ]
        }

        opportunities.extend(sector_differentiation.get(sector, [
            "customer_service_excellence",
            "innovation_and_technology",
            "quality_and_reliability"
        ]))

        return opportunities[:4]  # Return top 4 opportunities
   
    def _assess_competitive_advantages(self, business_data: Dict[str, Any], 
                                     productivity_ratio: float, years_in_business: int) -> List[str]:
        """Assess current competitive advantages."""
        
        advantages = []
        
        # Productivity advantage
        if productivity_ratio > 1.3:
            advantages.append("superior_operational_efficiency")
        elif productivity_ratio > 1.1:
            advantages.append("above_average_productivity")
        
        # Experience advantage
        if years_in_business > 10:
            advantages.append("deep_market_experience")
        elif years_in_business > 5:
            advantages.append("established_market_presence")
        
        # Financial advantage
        monthly_revenue = business_data.get("monthly_revenue", [])
        if monthly_revenue:
            current_revenue = monthly_revenue[-1]
            monthly_expenses = business_data.get("monthly_expenses", 0)
            
            if current_revenue > monthly_expenses * 1.3:  # 30%+ margin
                advantages.append("strong_profitability")
            
            # Growth advantage
            if len(monthly_revenue) >= 3:
                growth_rate = calculate_growth_rate(monthly_revenue)
                if growth_rate > 0.15:  # 15%+ growth
                    advantages.append("strong_growth_momentum")
        
        # Cash position advantage
        current_cash = business_data.get("current_cash", 0)
        monthly_expenses = business_data.get("monthly_expenses", 0)
        cash_runway = calculate_cash_runway(current_cash, monthly_expenses)
        
        if cash_runway > 12:  # 12+ months
            advantages.append("exceptional_financial_stability")
        elif cash_runway > 6:
            advantages.append("strong_financial_position")
        
        return advantages
    
    def _identify_competitive_threats(self, sector: str) -> List[str]:
        """Identify competitive threats by sector."""
        
        threats = {
            "electronics": [
                "online_marketplace_competition",
                "direct_manufacturer_sales",
                "technology_obsolescence",
                "supply_chain_disruptions"
            ],
            "food": [
                "food_delivery_platform_dominance",
                "chain_restaurant_expansion",
                "changing_consumer_preferences",
                "regulatory_compliance_costs"
            ],
            "retail": [
                "e_commerce_displacement",
                "big_box_retailer_competition",
                "changing_shopping_behaviors",
                "supply_chain_cost_pressures"
            ],
            "auto": [
                "electric_vehicle_transition",
                "online_parts_retailers",
                "manufacturer_direct_service",
                "autonomous_vehicle_impact"
            ],
            "manufacturing": [
                "overseas_low_cost_competition",
                "automation_and_ai_adoption",
                "supply_chain_consolidation",
                "regulatory_compliance_costs"
            ]
        }
        
        return threats.get(sector, [
            "new_market_entrants",
            "technology_disruption",
            "economic_downturns",
            "regulatory_changes"
        ])
    
    def _recommend_strategic_positioning(self, size_category: str, competitive_strengths: List[str], sector: str) -> Dict[str, str]:
        """Recommend strategic positioning approach."""
        
        # Base positioning on size and strengths
        if size_category == "large_for_sector":
            if "superior_operational_efficiency" in competitive_strengths:
                strategy = "cost_leadership"
                description = "Leverage scale and efficiency for competitive pricing"
            else:
                strategy = "broad_differentiation"
                description = "Offer comprehensive solutions with market leadership"
        elif size_category == "small_player":
            strategy = "focused_differentiation"
            description = "Target specific niches with specialized offerings"
        else:
            if "strong_profitability" in competitive_strengths:
                strategy = "value_differentiation"
                description = "Compete on value proposition and customer experience"
            else:
                strategy = "operational_excellence"
                description = "Focus on efficiency and service quality"
        
        # Sector-specific refinements
        sector_positioning = {
            "electronics": "technology_and_service_excellence",
            "food": "quality_and_experience_focus",
            "retail": "customer_experience_and_convenience",
            "auto": "reliability_and_expertise",
            "manufacturing": "quality_and_customization"
        }
        
        sector_focus = sector_positioning.get(sector, "operational_excellence")
        
        return {
            "primary_strategy": strategy,
            "description": description,
            "sector_focus": sector_focus,
            "implementation_priority": "high" if size_category == "small_player" else "medium"
        }
    
    def _identify_top_strengths(self, component_breakdown: Dict[str, float]) -> List[str]:
        """Identify top business strengths from component scores."""
        
        strengths = []
        
        # Sort components by score
        sorted_components = sorted(component_breakdown.items(), key=lambda x: x[1], reverse=True)
        
        for component, score in sorted_components:
            if score >= 70:  # Strong performance threshold
                if component == "financial_performance":
                    strengths.append("strong_financial_performance")
                elif component == "market_position":
                    strengths.append("competitive_market_position")
                elif component == "financial_health":
                    strengths.append("solid_financial_foundation")
                elif component == "growth_potential":
                    strengths.append("high_growth_potential")
                elif component == "risk_management":
                    strengths.append("effective_risk_management")
        
        return strengths[:3]  # Return top 3 strengths
    
    def _identify_improvement_areas(self, component_breakdown: Dict[str, float]) -> List[str]:
        """Identify areas needing improvement from component scores."""
        
        improvement_areas = []
        
        # Sort components by score (lowest first)
        sorted_components = sorted(component_breakdown.items(), key=lambda x: x[1])
        
        for component, score in sorted_components:
            if score < 50:  # Below average threshold
                if component == "financial_performance":
                    improvement_areas.append("financial_performance_optimization")
                elif component == "market_position":
                    improvement_areas.append("market_positioning_enhancement")
                elif component == "financial_health":
                    improvement_areas.append("financial_stability_improvement")
                elif component == "growth_potential":
                    improvement_areas.append("growth_strategy_development")
                elif component == "risk_management":
                    improvement_areas.append("risk_mitigation_planning")
        
        return improvement_areas[:3]  # Return top 3 improvement areas
    
    def _predict_score_trajectory(self, component_breakdown: Dict[str, float]) -> str:
        """Predict business score trajectory."""
        
        growth_score = component_breakdown.get("growth_potential", 50)
        health_score = component_breakdown.get("financial_health", 50)
        risk_score = component_breakdown.get("risk_management", 50)
        
        # Trajectory prediction logic
        if growth_score > 70 and health_score > 60:
            return "strongly_improving"
        elif growth_score > 60 and health_score > 50 and risk_score > 60:
            return "improving"
        elif health_score < 40 or risk_score < 30:
            return "deteriorating"
        elif growth_score < 30:
            return "stagnating"
        else:
            return "stable"
    
    def _suggest_expansion_timeline(self, readiness_level: str) -> str:
        """Suggest timeline for expansion based on readiness."""
        
        timelines = {
            "highly_ready": "6-12 months",
            "ready": "12-18 months", 
            "partially_ready": "18-24 months",
            "not_ready": "24+ months"
        }
        
        return timelines.get(readiness_level, "24+ months")
    
    def _suggest_expansion_preparation(self, readiness_score: int, readiness_factors: List[str]) -> List[str]:
        """Suggest preparation steps for expansion."""
        
        preparation_steps = []
        
        if readiness_score < 40:
            preparation_steps.extend([
                "Build cash reserves to 6+ months of expenses",
                "Achieve consistent profitability",
                "Establish operational processes and systems"
            ])
        elif readiness_score < 60:
            preparation_steps.extend([
                "Strengthen management team",
                "Document business processes",
                "Develop expansion business plan"
            ])
        elif readiness_score < 80:
            preparation_steps.extend([
                "Secure expansion financing",
                "Conduct market research for new location",
                "Finalize operational scalability"
            ])
        
        # Add specific steps based on missing factors
        if "sufficient_cash_reserves" not in readiness_factors:
            preparation_steps.append("Build cash reserves for expansion capital")
        
        if "adequate_staffing" not in readiness_factors:
            preparation_steps.append("Hire and train additional staff")
        
        if "growth_momentum" not in readiness_factors:
            preparation_steps.append("Establish consistent revenue growth")
        
        return preparation_steps[:5]  # Return top 5 steps
    
    def _calculate_analysis_confidence(self, business_data: Dict[str, Any]) -> float:
        """Calculate confidence level of the analysis."""
        
        confidence = 50  # Baseline confidence
        
        # Data completeness factors
        monthly_revenue = business_data.get("monthly_revenue", [])
        if len(monthly_revenue) >= 6:
            confidence += 20
        elif len(monthly_revenue) >= 3:
            confidence += 10
        
        # Business maturity factors
        years_in_business = business_data.get("years_in_business", 0)
        if years_in_business >= 3:
            confidence += 15
        elif years_in_business >= 1:
            confidence += 10
        
        # Data consistency factors
        if monthly_revenue and len(monthly_revenue) >= 3:
            volatility = calculate_volatility(monthly_revenue)
            if volatility < 0.2:  # Low volatility = more predictable
                confidence += 10
            elif volatility > 0.5:  # High volatility = less predictable
                confidence -= 10
        
        # Financial data completeness
        required_fields = ["monthly_expenses", "current_cash", "employees_count"]
        complete_fields = sum(1 for field in required_fields if business_data.get(field) is not None)
        confidence += (complete_fields / len(required_fields)) * 15
        
        return max(30, min(95, confidence))  # Confidence between 30-95%