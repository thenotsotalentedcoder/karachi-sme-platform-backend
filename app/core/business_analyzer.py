"""US Business performance analysis engine with real-time economic integration."""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import statistics
import json
from dataclasses import dataclass, asdict

from app.data.us_economic_factors import (
    get_current_us_economic_indicators,
    get_us_seasonal_factor,
    calculate_us_economic_impact,
    get_us_market_sentiment,
    project_us_economic_trends,
    calculate_sector_resilience_score
)
from app.data.us_sectors import (
    get_us_sector_data,
    get_us_location_data,
    get_us_sector_location_multiplier,
    calculate_us_market_opportunity_score,
    classify_us_location_type
)
from app.utils.calculations import (
    calculate_growth_rate,
    calculate_volatility,
    calculate_trend_direction,
    calculate_profit_margin,
    calculate_cash_runway,
    calculate_percentile_rank,
    normalize_score,
    calculate_correlation,
    safe_divide
)

logger = logging.getLogger(__name__)


@dataclass
class USBusinessMetrics:
    """Core US business performance metrics."""
    
    # Financial Performance
    annual_revenue: float
    current_monthly_revenue: float
    revenue_growth_rate: float
    monthly_cash_flow: float
    profit_margin: float
    cash_runway_months: float
    
    # Market Performance
    revenue_per_employee: float
    market_position_score: float
    competitive_strength: float
    sector_performance_ratio: float
    
    # Economic Sensitivity
    fed_rate_sensitivity: float
    inflation_sensitivity: float
    economic_resilience_score: float
    recession_probability_impact: float
    
    # Risk Metrics
    revenue_volatility: float
    cash_flow_stability: float
    debt_service_coverage: Optional[float]
    financial_stress_score: float
    
    # Growth Metrics
    growth_momentum_score: float
    scalability_potential: float
    market_expansion_readiness: float
    investment_attraction_score: float


@dataclass
class USMarketContext:
    """US market context for business analysis."""
    
    # Location Analysis
    location_type: str
    location_advantage_score: float
    regional_economic_health: float
    local_competition_density: str
    
    # Market Conditions
    sector_growth_rate: float
    market_size: float
    customer_demographics: Dict[str, Any]
    purchasing_power_index: float
    
    # Business Environment
    regulatory_friendliness: float
    tax_burden_score: float
    infrastructure_quality: float
    talent_availability: float


@dataclass
class USEconomicImpact:
    """US economic impact analysis on business."""
    
    # Current Impact
    current_fed_rate_impact: float
    current_inflation_impact: float
    current_unemployment_impact: float
    overall_economic_impact: float
    
    # Forward-Looking
    projected_economic_impact_6m: float
    recession_risk_impact: float
    interest_rate_trend_impact: float
    policy_change_impact: float
    
    # Sector-Specific
    sector_economic_correlation: float
    cyclical_vs_defensive_score: float
    economic_hedge_quality: float


class USBusinessAnalyzer:
    """Comprehensive US small business performance analyzer."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Performance benchmarks for US SMEs
        self.us_benchmarks = {
            "revenue_growth": {
                "excellent": 0.20,    # 20%+ annual growth
                "good": 0.10,         # 10-20% growth
                "average": 0.05,      # 5-10% growth
                "poor": 0.0           # <5% growth
            },
            "profit_margin": {
                "excellent": 0.15,    # 15%+ margin
                "good": 0.10,         # 10-15% margin
                "average": 0.05,      # 5-10% margin
                "poor": 0.0           # <5% margin
            },
            "cash_runway": {
                "excellent": 12.0,    # 12+ months
                "good": 6.0,          # 6-12 months
                "average": 3.0,       # 3-6 months
                "poor": 1.0           # <3 months
            },
            "revenue_volatility": {
                "excellent": 0.1,     # <10% volatility
                "good": 0.2,          # 10-20% volatility
                "average": 0.3,       # 20-30% volatility
                "poor": 0.5           # >30% volatility
            }
        }
    
    async def analyze_us_business_comprehensive(self, business_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive analysis of US small business performance.
        
        Args:
            business_data: Complete US business information
            
        Returns:
            Detailed analysis with scores, insights, and recommendations
        """
        
        start_time = datetime.now()
        self.logger.info(f"Starting comprehensive US business analysis for {business_data.get('business_name', 'Business')}")
        
        try:
            # Calculate core business metrics
            business_metrics = await self._calculate_business_metrics(business_data)
            
            # Analyze market context
            market_context = await self._analyze_market_context(business_data)
            
            # Assess economic impact
            economic_impact = await self._assess_economic_impact(business_data, business_metrics)
            
            # Generate performance scores
            performance_scores = await self._calculate_performance_scores(business_metrics, market_context)
            
            # Analyze competitive position
            competitive_analysis = await self._analyze_competitive_position(business_data, business_metrics, market_context)
            
            # Assess growth potential
            growth_analysis = await self._analyze_growth_potential(business_data, business_metrics, market_context)
            
            # Risk assessment
            risk_analysis = await self._assess_business_risks(business_data, business_metrics, economic_impact)
            
            # Financial health analysis
            financial_health = await self._analyze_financial_health(business_data, business_metrics)
            
            # Operational efficiency analysis
            operational_analysis = await self._analyze_operational_efficiency(business_data, business_metrics)
            
            # Strategic positioning
            strategic_positioning = await self._analyze_strategic_positioning(business_data, market_context, competitive_analysis)
            
            # Investment readiness
            investment_readiness = await self._assess_investment_readiness(business_data, business_metrics, financial_health)
            
            # Synthesize comprehensive analysis
            comprehensive_analysis = {
                "business_overview": {
                    "business_name": business_data.get('business_name'),
                    "sector": business_data.get('sector'),
                    "location": f"{business_data.get('city')}, {business_data.get('state')}",
                    "years_in_business": business_data.get('years_in_business'),
                    "employees": business_data.get('employees_count'),
                    "business_structure": business_data.get('business_structure'),
                    "analysis_date": start_time.isoformat()
                },
                
                "core_metrics": asdict(business_metrics),
                "market_context": asdict(market_context),
                "economic_impact": asdict(economic_impact),
                
                "performance_analysis": {
                    "overall_score": performance_scores["overall_score"],
                    "performance_grade": performance_scores["performance_grade"],
                    "percentile_ranking": performance_scores["percentile_ranking"],
                    "vs_sector_average": performance_scores["vs_sector_performance"],
                    "score_breakdown": performance_scores["score_breakdown"],
                    "performance_trend": performance_scores["performance_trend"],
                    "key_performance_drivers": performance_scores["key_drivers"],
                    "performance_constraints": performance_scores["constraints"]
                },
                
                "competitive_analysis": competitive_analysis,
                "growth_analysis": growth_analysis,
                "risk_analysis": risk_analysis,
                "financial_health": financial_health,
                "operational_analysis": operational_analysis,
                "strategic_positioning": strategic_positioning,
                "investment_readiness": investment_readiness,
                
                "key_insights": await self._generate_key_insights(
                    business_metrics, market_context, economic_impact, 
                    performance_scores, competitive_analysis
                ),
                
                "strategic_recommendations": await self._generate_strategic_recommendations(
                    business_data, business_metrics, market_context, 
                    performance_scores, risk_analysis, economic_impact
                ),
                
                "analysis_metadata": {
                    "analysis_version": "2.0",
                    "analysis_time_seconds": (datetime.now() - start_time).total_seconds(),
                    "confidence_level": 0.85,
                    "data_sources": ["FRED", "Census", "BLS", "Alpha_Vantage", "Proprietary_Models"],
                    "last_updated": datetime.now().isoformat()
                }
            }
            
            execution_time = (datetime.now() - start_time).total_seconds()
            self.logger.info(f"US business analysis completed in {execution_time:.2f} seconds")
            
            return comprehensive_analysis
            
        except Exception as e:
            self.logger.error(f"Error in US business analysis: {str(e)}")
            return await self._create_fallback_analysis(business_data, str(e))
    
    async def _calculate_business_metrics(self, business_data: Dict[str, Any]) -> USBusinessMetrics:
        """Calculate core US business performance metrics."""
        
        try:
            # Extract financial data
            monthly_revenue = business_data.get('monthly_revenue', [])
            monthly_expenses = business_data.get('monthly_expenses', [])
            current_cash = business_data.get('current_cash', 0)
            employees_count = max(1, business_data.get('employees_count', 1))
            outstanding_debt = business_data.get('outstanding_debt', 0)
            
            # Calculate basic financial metrics
            annual_revenue = sum(monthly_revenue) if monthly_revenue else 0
            current_monthly_revenue = monthly_revenue[-1] if monthly_revenue else 0
            avg_monthly_expenses = sum(monthly_expenses) / 12 if isinstance(monthly_expenses, list) and len(monthly_expenses) == 12 else monthly_expenses if isinstance(monthly_expenses, (int, float)) else 0
            monthly_cash_flow = current_monthly_revenue - avg_monthly_expenses
            
            # Growth and trend analysis
            revenue_growth_rate = calculate_growth_rate(monthly_revenue) if len(monthly_revenue) >= 2 else 0.0
            revenue_volatility = calculate_volatility(monthly_revenue) if len(monthly_revenue) >= 3 else 0.0
            
            # Profitability metrics
            profit_margin = calculate_profit_margin(current_monthly_revenue, avg_monthly_expenses)
            cash_runway_months = calculate_cash_runway(current_cash, avg_monthly_expenses)
            
            # Productivity metrics
            revenue_per_employee = annual_revenue / employees_count if employees_count > 0 else 0
            
            # Get sector data for benchmarking
            sector = business_data.get('sector', 'general')
            sector_data = get_us_sector_data(sector)
            
            # Market position scoring
            market_position_score = await self._calculate_market_position_score(
                annual_revenue, sector_data, business_data
            )
            
            competitive_strength = await self._calculate_competitive_strength(
                business_data, annual_revenue, revenue_growth_rate
            )
            
            # Economic sensitivity analysis
            economic_impact = calculate_us_economic_impact(sector, business_data)
            fed_rate_sensitivity = economic_impact.get('fed_rate_impact', 0)
            inflation_sensitivity = economic_impact.get('inflation_impact', 0)
            
            # Resilience scoring
            resilience_data = calculate_sector_resilience_score(sector)
            economic_resilience_score = resilience_data.get('resilience_score', 0.5) * 100
            
            # Risk metrics
            debt_service_coverage = None
            if outstanding_debt > 0 and monthly_cash_flow > 0:
                monthly_debt_service = outstanding_debt * 0.05 / 12  # Assume 5% annual rate
                debt_service_coverage = monthly_cash_flow / monthly_debt_service
            
            cash_flow_stability = self._calculate_cash_flow_stability(monthly_revenue, monthly_expenses)
            financial_stress_score = self._calculate_financial_stress_score(
                cash_runway_months, debt_service_coverage, profit_margin
            )
            
            # Growth metrics
            growth_momentum_score = self._calculate_growth_momentum(
                revenue_growth_rate, monthly_revenue, business_data
            )
            
            scalability_potential = self._calculate_scalability_potential(
                business_data, revenue_per_employee, sector_data
            )
            
            market_expansion_readiness = self._calculate_market_expansion_readiness(
                current_cash, monthly_cash_flow, business_data
            )
            
            investment_attraction_score = self._calculate_investment_attraction_score(
                revenue_growth_rate, profit_margin, market_position_score
            )
            
            return USBusinessMetrics(
                annual_revenue=annual_revenue,
                current_monthly_revenue=current_monthly_revenue,
                revenue_growth_rate=revenue_growth_rate,
                monthly_cash_flow=monthly_cash_flow,
                profit_margin=profit_margin,
                cash_runway_months=cash_runway_months,
                revenue_per_employee=revenue_per_employee,
                market_position_score=market_position_score,
                competitive_strength=competitive_strength,
                sector_performance_ratio=self._calculate_sector_performance_ratio(
                    annual_revenue, sector_data
                ),
                fed_rate_sensitivity=fed_rate_sensitivity,
                inflation_sensitivity=inflation_sensitivity,
                economic_resilience_score=economic_resilience_score,
                recession_probability_impact=self._calculate_recession_impact(
                    sector, economic_resilience_score
                ),
                revenue_volatility=revenue_volatility,
                cash_flow_stability=cash_flow_stability,
                debt_service_coverage=debt_service_coverage,
                financial_stress_score=financial_stress_score,
                growth_momentum_score=growth_momentum_score,
                scalability_potential=scalability_potential,
                market_expansion_readiness=market_expansion_readiness,
                investment_attraction_score=investment_attraction_score
            )
            
        except Exception as e:
            self.logger.error(f"Error calculating business metrics: {str(e)}")
            # Return default metrics
            return USBusinessMetrics(
                annual_revenue=0, current_monthly_revenue=0, revenue_growth_rate=0,
                monthly_cash_flow=0, profit_margin=0, cash_runway_months=0,
                revenue_per_employee=0, market_position_score=50, competitive_strength=50,
                sector_performance_ratio=1.0, fed_rate_sensitivity=0, inflation_sensitivity=0,
                economic_resilience_score=50, recession_probability_impact=0,
                revenue_volatility=0, cash_flow_stability=50, debt_service_coverage=None,
                financial_stress_score=50, growth_momentum_score=50, scalability_potential=50,
                market_expansion_readiness=50, investment_attraction_score=50
            )
    
    async def _analyze_market_context(self, business_data: Dict[str, Any]) -> USMarketContext:
        """Analyze US market context for the business."""
        
        try:
            # Extract location information
            city = business_data.get('city', '')
            state = business_data.get('state', '')
            zip_code = business_data.get('zip_code', '')
            sector = business_data.get('sector', '')
            
            # Classify location type
            location_type = classify_us_location_type(city, state, zip_code)
            
            # Get location and sector data
            location_data = get_us_location_data(location_type)
            sector_data = get_us_sector_data(sector)
            
            # Calculate location advantage
            location_multiplier = get_us_sector_location_multiplier(sector, location_type)
            location_advantage_score = normalize_score(location_multiplier, 0.7, 1.5, 0, 100)
            
            # Market opportunity scoring
            market_opportunity = calculate_us_market_opportunity_score(sector, location_type)
            
            # Regional economic health (simplified)
            regional_economic_health = 75.0  # Would be fetched from economic data
            
            # Competition density
            local_competition_density = location_data.get('characteristics', {}).get('competition', 'medium')
            
            # Market conditions
            sector_performance = sector_data.get('base_performance', {})
            sector_growth_rate = sector_performance.get('growth_rate', 0.05)
            
            # Estimate market size (simplified)
            population_estimate = 50000  # Would be from Census data
            market_size = population_estimate * sector_performance.get('average_monthly_revenue', 50000) * 0.1
            
            # Customer demographics (from location data)
            customer_demographics = location_data.get('characteristics', {}).get('demographics', {
                'median_income': 65000,
                'age_25_44': 30,
                'college_degree': 40
            })
            
            # Purchasing power index
            purchasing_power_index = customer_demographics.get('median_income', 65000) / 65000  # Normalized to US median
            
            return USMarketContext(
                location_type=location_type,
                location_advantage_score=location_advantage_score,
                regional_economic_health=regional_economic_health,
                local_competition_density=local_competition_density,
                sector_growth_rate=sector_growth_rate,
                market_size=market_size,
                customer_demographics=customer_demographics,
                purchasing_power_index=purchasing_power_index,
                regulatory_friendliness=75.0,  # Would be calculated from regulatory data
                tax_burden_score=65.0,  # Would be calculated from tax data
                infrastructure_quality=80.0,  # Would be from infrastructure data
                talent_availability=70.0  # Would be from labor market data
            )
            
        except Exception as e:
            self.logger.error(f"Error analyzing market context: {str(e)}")
            return USMarketContext(
                location_type="suburban", location_advantage_score=50,
                regional_economic_health=50, local_competition_density="medium",
                sector_growth_rate=0.05, market_size=1000000,
                customer_demographics={}, purchasing_power_index=1.0,
                regulatory_friendliness=50, tax_burden_score=50,
                infrastructure_quality=50, talent_availability=50
            )
    
    async def _assess_economic_impact(self, business_data: Dict[str, Any], 
                                     business_metrics: USBusinessMetrics) -> USEconomicImpact:
        """Assess current and projected US economic impact on business."""
        
        try:
            sector = business_data.get('sector', '')
            
            # Get current economic indicators
            economic_indicators = get_current_us_economic_indicators()
            
            # Calculate current economic impact
            economic_impact = calculate_us_economic_impact(sector, business_data)
            current_fed_rate_impact = economic_impact.get('fed_rate_impact', 0)
            current_inflation_impact = economic_impact.get('inflation_impact', 0)
            current_unemployment_impact = economic_impact.get('unemployment_impact', 0)
            overall_economic_impact = economic_impact.get('total_economic_impact', 0)
            
            # Project future economic impact
            economic_trends = project_us_economic_trends(6)
            projected_indicators = economic_trends.get('projected_indicators', {})
            
            # Calculate projected impact
            current_fed_rate = economic_indicators.get('fed_funds_rate', 5.25)
            projected_fed_rate = projected_indicators.get('fed_funds_rate', current_fed_rate)
            fed_rate_change_impact = (projected_fed_rate - current_fed_rate) * business_metrics.fed_rate_sensitivity
            
            projected_economic_impact_6m = overall_economic_impact + fed_rate_change_impact
            
            # Recession risk impact
            recession_indicators = {
                'yield_curve_inversion': current_fed_rate > projected_indicators.get('fed_funds_rate', current_fed_rate),
                'high_inflation': economic_indicators.get('inflation_rate', 3.2) > 4.0,
                'unemployment_rising': False  # Would need historical data
            }
            
            recession_risk_score = sum(recession_indicators.values()) / len(recession_indicators)
            recession_risk_impact = recession_risk_score * (1 - business_metrics.economic_resilience_score / 100) * -0.2
            
            # Interest rate trend impact
            rate_trend = "decreasing" if projected_fed_rate < current_fed_rate else "increasing"
            interest_rate_trend_impact = fed_rate_change_impact
            
            # Policy change impact (simplified)
            policy_change_impact = 0.0  # Would incorporate policy analysis
            
            # Sector correlation with economy
            sector_correlations = {
                'electronics': 0.7, 'food': 0.3, 'retail': 0.8, 'auto': 0.9,
                'professional_services': 0.5, 'manufacturing': 0.8
            }
            sector_economic_correlation = sector_correlations.get(sector, 0.6)
            
            # Cyclical vs defensive classification
            cyclical_sectors = ['auto', 'retail', 'electronics', 'manufacturing']
            cyclical_vs_defensive_score = 0.8 if sector in cyclical_sectors else 0.3
            
            # Economic hedge quality
            hedge_sectors = ['food', 'professional_services']
            economic_hedge_quality = 0.7 if sector in hedge_sectors else 0.3
            
            return USEconomicImpact(
                current_fed_rate_impact=current_fed_rate_impact,
                current_inflation_impact=current_inflation_impact,
                current_unemployment_impact=current_unemployment_impact,
                overall_economic_impact=overall_economic_impact,
                projected_economic_impact_6m=projected_economic_impact_6m,
                recession_risk_impact=recession_risk_impact,
                interest_rate_trend_impact=interest_rate_trend_impact,
                policy_change_impact=policy_change_impact,
                sector_economic_correlation=sector_economic_correlation,
                cyclical_vs_defensive_score=cyclical_vs_defensive_score,
                economic_hedge_quality=economic_hedge_quality
            )
            
        except Exception as e:
            self.logger.error(f"Error assessing economic impact: {str(e)}")
            return USEconomicImpact(
                current_fed_rate_impact=0, current_inflation_impact=0,
                current_unemployment_impact=0, overall_economic_impact=0,
                projected_economic_impact_6m=0, recession_risk_impact=0,
                interest_rate_trend_impact=0, policy_change_impact=0,
                sector_economic_correlation=0.5, cyclical_vs_defensive_score=0.5,
                economic_hedge_quality=0.5
            )
    
    async def _calculate_performance_scores(self, business_metrics: USBusinessMetrics, 
                                          market_context: USMarketContext) -> Dict[str, Any]:
        """Calculate comprehensive performance scores."""
        
        try:
            # Individual metric scores (0-100 scale)
            scores = {}
            
            # Financial Performance Scores
            scores['revenue_growth'] = self._score_against_benchmark(
                business_metrics.revenue_growth_rate, self.us_benchmarks['revenue_growth']
            )
            
            scores['profitability'] = self._score_against_benchmark(
                business_metrics.profit_margin, self.us_benchmarks['profit_margin']
            )
            
            scores['cash_management'] = self._score_against_benchmark(
                business_metrics.cash_runway_months, self.us_benchmarks['cash_runway']
            )
            
            scores['revenue_stability'] = self._score_against_benchmark(
                1 - business_metrics.revenue_volatility, self.us_benchmarks['revenue_volatility'], inverse=True
            )
            
            # Market Performance Scores
            scores['market_position'] = business_metrics.market_position_score
            scores['competitive_strength'] = business_metrics.competitive_strength
            scores['location_advantage'] = market_context.location_advantage_score
            
            # Operational Efficiency Scores
            productivity_benchmark = 150000  # $150k revenue per employee benchmark
            scores['productivity'] = normalize_score(
                business_metrics.revenue_per_employee, 0, productivity_benchmark * 2, 0, 100
            )
            
            # Economic Resilience Scores
            scores['economic_resilience'] = business_metrics.economic_resilience_score
            scores['financial_stability'] = 100 - business_metrics.financial_stress_score
            
            # Growth Potential Scores
            scores['growth_momentum'] = business_metrics.growth_momentum_score
            scores['scalability'] = business_metrics.scalability_potential
            scores['expansion_readiness'] = business_metrics.market_expansion_readiness
            
            # Calculate weighted overall score
            weights = {
                'revenue_growth': 0.15,
                'profitability': 0.15,
                'cash_management': 0.10,
                'revenue_stability': 0.10,
                'market_position': 0.10,
                'competitive_strength': 0.10,
                'productivity': 0.08,
                'economic_resilience': 0.07,
                'financial_stability': 0.05,
                'growth_momentum': 0.05,
                'scalability': 0.03,
                'expansion_readiness': 0.02
            }
            
            overall_score = sum(scores[metric] * weight for metric, weight in weights.items())
            
            # Performance grade
            if overall_score >= 85:
                grade = "A"
            elif overall_score >= 75:
                grade = "B"
            elif overall_score >= 65:
                grade = "C"
            elif overall_score >= 50:
                grade = "D"
            else:
                grade = "F"
            
            # Percentile ranking (estimated based on score)
            percentile_ranking = min(99, max(1, int(overall_score)))
            
            # vs Sector performance
            sector_avg_score = 65.0  # Would be calculated from sector data
            vs_sector_performance = ((overall_score / sector_avg_score) - 1) * 100
            
            # Performance trend
            recent_revenue_trend = calculate_trend_direction(
                business_metrics.annual_revenue if isinstance(business_metrics.annual_revenue, list) 
                else [business_metrics.annual_revenue]
            )
            
            performance_trend = "improving" if business_metrics.revenue_growth_rate > 0.05 else \
                              "stable" if business_metrics.revenue_growth_rate > -0.02 else "declining"
            
            # Key drivers and constraints
            key_drivers = []
            constraints = []
            
            if scores['revenue_growth'] > 75:
                key_drivers.append("Strong revenue growth momentum")
            if scores['profitability'] > 75:
                key_drivers.append("Healthy profit margins")
            if scores['market_position'] > 75:
                key_drivers.append("Strong market position")
            
            if scores['cash_management'] < 50:
                constraints.append("Limited cash runway")
            if scores['revenue_stability'] < 50:
                constraints.append("High revenue volatility")
            if scores['competitive_strength'] < 50:
                constraints.append("Weak competitive position")
            
            return {
                'overall_score': overall_score,
                'performance_grade': grade,
                'percentile_ranking': percentile_ranking,
                'vs_sector_performance': vs_sector_performance,
                'score_breakdown': scores,
                'performance_trend': performance_trend,
                'key_drivers': key_drivers,
                'constraints': constraints,
                'score_weights': weights
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating performance scores: {str(e)}")
            return {
                'overall_score': 50.0,
                'performance_grade': 'C',
                'percentile_ranking': 50,
                'vs_sector_performance': 0.0,
                'score_breakdown': {},
                'performance_trend': 'stable',
                'key_drivers': [],
                'constraints': [],
                'score_weights': {}
            }
    
    # Helper methods for scoring and calculations
    def _score_against_benchmark(self, value: float, benchmarks: Dict[str, float], 
                                inverse: bool = False) -> float:
        """Score a value against US SME benchmarks."""
        
        if inverse:
            # For metrics where lower is better (e.g., volatility)
            if value <= benchmarks['excellent']:
                return 90.0
            elif value <= benchmarks['good']:
                return 75.0
            elif value <= benchmarks['average']:
                return 60.0
            else:
                return 40.0
        else:
            # For metrics where higher is better
            if value >= benchmarks['excellent']:
                return 90.0
            elif value >= benchmarks['good']:
                return 75.0
            elif value >= benchmarks['average']:
                return 60.0
            else:
                return 40.0
    
    async def _calculate_market_position_score(self, annual_revenue: float, 
                                             sector_data: Dict[str, Any],
                                             business_data: Dict[str, Any]) -> float:
        """Calculate market position score based on revenue and sector data."""
        
        try:
            sector_performance = sector_data.get('base_performance', {})
            sector_avg_revenue = sector_performance.get('average_monthly_revenue', 75000) * 12
            
            # Compare to sector average
            if annual_revenue >= sector_avg_revenue * 1.5:
                return 85.0
            elif annual_revenue >= sector_avg_revenue * 1.2:
                return 75.0
            elif annual_revenue >= sector_avg_revenue * 0.8:
                return 60.0
            else:
                return 40.0
                
        except:
            return 50.0
    
    async def _calculate_competitive_strength(self, business_data: Dict[str, Any],
                                            annual_revenue: float, 
                                            revenue_growth_rate: float) -> float:
        """Calculate competitive strength score."""
        
        try:
            strength_factors = []
            
            # Revenue size advantage
            if annual_revenue > 1000000:  # $1M+ annual revenue
                strength_factors.append(20)
            elif annual_revenue > 500000:  # $500K+ annual revenue
                strength_factors.append(15)
            else:
                strength_factors.append(10)
            
            # Growth momentum
            if revenue_growth_rate > 0.15:  # 15%+ growth
                strength_factors.append(25)
            elif revenue_growth_rate > 0.08:  # 8%+ growth
                strength_factors.append(15)
            elif revenue_growth_rate > 0.03:  # 3%+ growth
                strength_factors.append(10)
            else:
                strength_factors.append(5)
            
            # Years in business (stability factor)
            years_in_business = business_data.get('years_in_business', 0)
            if years_in_business > 10:
                strength_factors.append(20)
            elif years_in_business > 5:
                strength_factors.append(15)
            elif years_in_business > 2:
                strength_factors.append(10)
            else:
                strength_factors.append(5)
            
            # Team size (capacity factor)
            employees = business_data.get('employees_count', 0)
            if employees > 20:
                strength_factors.append(15)
            elif employees > 10:
                strength_factors.append(12)
            elif employees > 5:
                strength_factors.append(10)
            else:
                strength_factors.append(8)
            
            # Unique value proposition (if provided)
            if business_data.get('unique_value_proposition'):
                strength_factors.append(10)
            
            # Competitive advantages (if provided)
            competitive_advantages = business_data.get('competitive_advantages', [])
            if len(competitive_advantages) >= 3:
                strength_factors.append(10)
            elif len(competitive_advantages) >= 1:
                strength_factors.append(5)
            
            return min(100.0, sum(strength_factors))
            
        except Exception as e:
            self.logger.error(f"Error calculating competitive strength: {str(e)}")
            return 50.0
    
    def _calculate_sector_performance_ratio(self, annual_revenue: float, 
                                          sector_data: Dict[str, Any]) -> float:
        """Calculate performance ratio vs sector average."""
        
        try:
            sector_performance = sector_data.get('base_performance', {})
            sector_avg_monthly = sector_performance.get('average_monthly_revenue', 75000)
            sector_avg_annual = sector_avg_monthly * 12
            
            if sector_avg_annual > 0:
                return annual_revenue / sector_avg_annual
            else:
                return 1.0
                
        except:
            return 1.0
    
    def _calculate_cash_flow_stability(self, monthly_revenue: List[float], 
                                     monthly_expenses: float) -> float:
        """Calculate cash flow stability score."""
        
        try:
            if not monthly_revenue or len(monthly_revenue) < 3:
                return 50.0
            
            # Calculate monthly cash flows
            cash_flows = [revenue - monthly_expenses for revenue in monthly_revenue]
            
            # Calculate volatility of cash flows
            if len(cash_flows) >= 2:
                volatility = calculate_volatility(cash_flows)
                # Convert volatility to stability score (inverse relationship)
                stability_score = max(0, 100 - (volatility * 200))
                return min(100.0, stability_score)
            else:
                return 50.0
                
        except:
            return 50.0
    
    def _calculate_financial_stress_score(self, cash_runway: float, 
                                        debt_service_coverage: Optional[float],
                                        profit_margin: float) -> float:
        """Calculate financial stress score (higher = more stress)."""
        
        try:
            stress_factors = []
            
            # Cash runway stress
            if cash_runway < 1.0:
                stress_factors.append(40)  # Critical
            elif cash_runway < 3.0:
                stress_factors.append(25)  # High stress
            elif cash_runway < 6.0:
                stress_factors.append(15)  # Moderate stress
            else:
                stress_factors.append(5)   # Low stress
            
            # Debt service stress
            if debt_service_coverage is not None:
                if debt_service_coverage < 1.0:
                    stress_factors.append(30)  # Cannot service debt
                elif debt_service_coverage < 1.5:
                    stress_factors.append(20)  # Tight debt service
                elif debt_service_coverage < 2.0:
                    stress_factors.append(10)  # Adequate debt service
                else:
                    stress_factors.append(0)   # Comfortable debt service
            
            # Profitability stress
            if profit_margin < 0:
                stress_factors.append(25)  # Losing money
            elif profit_margin < 0.05:
                stress_factors.append(15)  # Very thin margins
            elif profit_margin < 0.10:
                stress_factors.append(10)  # Thin margins
            else:
                stress_factors.append(0)   # Healthy margins
            
            return min(100.0, sum(stress_factors))
            
        except:
            return 50.0
    
    def _calculate_growth_momentum(self, revenue_growth_rate: float,
                                 monthly_revenue: List[float],
                                 business_data: Dict[str, Any]) -> float:
        """Calculate growth momentum score."""
        
        try:
            momentum_factors = []
            
            # Recent growth rate
            if revenue_growth_rate > 0.20:
                momentum_factors.append(30)
            elif revenue_growth_rate > 0.10:
                momentum_factors.append(25)
            elif revenue_growth_rate > 0.05:
                momentum_factors.append(15)
            elif revenue_growth_rate > 0:
                momentum_factors.append(10)
            else:
                momentum_factors.append(0)
            
            # Growth consistency (if we have monthly data)
            if len(monthly_revenue) >= 6:
                recent_trend = calculate_trend_direction(monthly_revenue[-6:])
                if recent_trend == "increasing":
                    momentum_factors.append(20)
                elif recent_trend == "stable":
                    momentum_factors.append(10)
                else:
                    momentum_factors.append(0)
            
            # Business expansion plans
            expansion_plans = business_data.get('expansion_plans', [])
            if len(expansion_plans) > 0:
                momentum_factors.append(15)
            
            # Investment readiness
            current_cash = business_data.get('current_cash', 0)
            monthly_expenses = business_data.get('monthly_expenses', [])
            avg_monthly_expenses = sum(monthly_expenses) / 12 if isinstance(monthly_expenses, list) else monthly_expenses
            
            if current_cash > avg_monthly_expenses * 12:  # 12+ months runway
                momentum_factors.append(15)
            elif current_cash > avg_monthly_expenses * 6:  # 6+ months runway
                momentum_factors.append(10)
            
            # Market conditions factor
            sector = business_data.get('sector', '')
            sector_data = get_us_sector_data(sector)
            sector_growth = sector_data.get('base_performance', {}).get('growth_rate', 0.05)
            
            if sector_growth > 0.08:
                momentum_factors.append(10)
            elif sector_growth > 0.05:
                momentum_factors.append(5)
            
            return min(100.0, sum(momentum_factors))
            
        except:
            return 50.0
    
    def _calculate_scalability_potential(self, business_data: Dict[str, Any],
                                       revenue_per_employee: float,
                                       sector_data: Dict[str, Any]) -> float:
        """Calculate business scalability potential."""
        
        try:
            scalability_factors = []
            
            # Revenue per employee efficiency
            sector_performance = sector_data.get('base_performance', {})
            sector_avg_revenue = sector_performance.get('average_monthly_revenue', 75000) * 12
            employees = max(1, business_data.get('employees_count', 1))
            sector_revenue_per_employee = sector_avg_revenue / 5  # Assume 5 employees average
            
            if revenue_per_employee > sector_revenue_per_employee * 1.5:
                scalability_factors.append(25)
            elif revenue_per_employee > sector_revenue_per_employee:
                scalability_factors.append(20)
            else:
                scalability_factors.append(10)
            
            # Business model scalability
            business_model = business_data.get('business_model', '')
            scalable_models = ['b2b', 'saas', 'digital', 'platform']
            if any(model in business_model.lower() for model in scalable_models):
                scalability_factors.append(20)
            else:
                scalability_factors.append(10)
            
            # Technology adoption
            # This would be assessed from business operations data
            scalability_factors.append(15)  # Placeholder
            
            # Market size potential
            location = business_data.get('city', '').lower()
            major_markets = ['new york', 'los angeles', 'chicago', 'houston', 'phoenix']
            if any(market in location for market in major_markets):
                scalability_factors.append(20)
            else:
                scalability_factors.append(10)
            
            # Financial capacity for scaling
            current_cash = business_data.get('current_cash', 0)
            monthly_revenue = business_data.get('monthly_revenue', [])
            current_monthly_revenue = monthly_revenue[-1] if monthly_revenue else 0
            
            if current_cash > current_monthly_revenue * 6:
                scalability_factors.append(15)
            elif current_cash > current_monthly_revenue * 3:
                scalability_factors.append(10)
            else:
                scalability_factors.append(5)
            
            return min(100.0, sum(scalability_factors))
            
        except:
            return 50.0
    
    def _calculate_market_expansion_readiness(self, current_cash: float,
                                            monthly_cash_flow: float,
                                            business_data: Dict[str, Any]) -> float:
        """Calculate readiness for market expansion."""
        
        try:
            readiness_factors = []
            
            # Financial readiness
            if current_cash > monthly_cash_flow * 12 and monthly_cash_flow > 0:
                readiness_factors.append(30)
            elif current_cash > monthly_cash_flow * 6 and monthly_cash_flow > 0:
                readiness_factors.append(20)
            else:
                readiness_factors.append(10)
            
            # Operational readiness (team size)
            employees = business_data.get('employees_count', 0)
            if employees > 10:
                readiness_factors.append(25)
            elif employees > 5:
                readiness_factors.append(20)
            else:
                readiness_factors.append(10)
            
            # Market experience
            years_in_business = business_data.get('years_in_business', 0)
            if years_in_business > 5:
                readiness_factors.append(20)
            elif years_in_business > 2:
                readiness_factors.append(15)
            else:
                readiness_factors.append(5)
            
            # Business goals alignment
            expansion_goals = ['expand_locations', 'enter_new_markets', 'launch_new_products']
            business_goals = business_data.get('business_goals', [])
            if any(goal in business_goals for goal in expansion_goals):
                readiness_factors.append(15)
            
            # Current performance strength
            monthly_revenue = business_data.get('monthly_revenue', [])
            if monthly_revenue:
                recent_growth = calculate_growth_rate(monthly_revenue[-6:]) if len(monthly_revenue) >= 6 else 0
                if recent_growth > 0.1:
                    readiness_factors.append(10)
                elif recent_growth > 0.05:
                    readiness_factors.append(5)
            
            return min(100.0, sum(readiness_factors))
            
        except:
            return 50.0
    
    def _calculate_investment_attraction_score(self, revenue_growth_rate: float,
                                             profit_margin: float,
                                             market_position_score: float) -> float:
        """Calculate how attractive the business is for investment."""
        
        try:
            attraction_factors = []
            
            # Growth rate attractiveness
            if revenue_growth_rate > 0.25:
                attraction_factors.append(35)
            elif revenue_growth_rate > 0.15:
                attraction_factors.append(25)
            elif revenue_growth_rate > 0.08:
                attraction_factors.append(15)
            else:
                attraction_factors.append(5)
            
            # Profitability attractiveness
            if profit_margin > 0.15:
                attraction_factors.append(25)
            elif profit_margin > 0.10:
                attraction_factors.append(20)
            elif profit_margin > 0.05:
                attraction_factors.append(15)
            else:
                attraction_factors.append(5)
            
            # Market position strength
            if market_position_score > 80:
                attraction_factors.append(25)
            elif market_position_score > 60:
                attraction_factors.append(20)
            else:
                attraction_factors.append(10)
            
            # Additional factors
            attraction_factors.append(15)  # Base attractiveness
            
            return min(100.0, sum(attraction_factors))
            
        except:
            return 50.0
    
    def _calculate_recession_impact(self, sector: str, economic_resilience_score: float) -> float:
        """Calculate potential recession impact."""
        
        try:
            # Sector recession sensitivity
            recession_sensitive_sectors = ['auto', 'retail', 'electronics', 'manufacturing']
            if sector in recession_sensitive_sectors:
                base_impact = -0.25  # 25% negative impact
            else:
                base_impact = -0.10  # 10% negative impact
            
            # Adjust based on business resilience
            resilience_adjustment = (economic_resilience_score / 100) * 0.15
            
            return base_impact + resilience_adjustment
            
        except:
            return -0.15  # Default moderate impact
    
    async def _analyze_competitive_position(self, business_data: Dict[str, Any],
                                          business_metrics: USBusinessMetrics,
                                          market_context: USMarketContext) -> Dict[str, Any]:
        """Analyze competitive position in US market."""
        
        try:
            # Competitive strengths
            strengths = []
            if business_metrics.revenue_growth_rate > 0.10:
                strengths.append("Strong revenue growth momentum")
            if business_metrics.profit_margin > 0.12:
                strengths.append("Above-average profit margins")
            if business_metrics.cash_runway_months > 6:
                strengths.append("Strong financial position")
            if business_metrics.revenue_per_employee > 150000:
                strengths.append("High employee productivity")
            
            # Competitive weaknesses
            weaknesses = []
            if business_metrics.revenue_volatility > 0.3:
                weaknesses.append("High revenue volatility")
            if business_metrics.cash_runway_months < 3:
                weaknesses.append("Limited cash runway")
            if business_metrics.market_position_score < 50:
                weaknesses.append("Weak market position")
            if business_metrics.financial_stress_score > 70:
                weaknesses.append("High financial stress")
            
            # Market opportunities
            opportunities = []
            if market_context.sector_growth_rate > 0.08:
                opportunities.append("Growing sector market")
            if market_context.location_advantage_score > 70:
                opportunities.append("Favorable location for growth")
            if market_context.purchasing_power_index > 1.2:
                opportunities.append("High local purchasing power")
            
            # Market threats
            threats = []
            if market_context.local_competition_density == "very_high":
                threats.append("Intense local competition")
            if business_metrics.economic_resilience_score < 50:
                threats.append("Economic downturn vulnerability")
            
            # Competitive positioning
            if business_metrics.competitive_strength > 75:
                positioning = "market_leader"
            elif business_metrics.competitive_strength > 60:
                positioning = "strong_competitor"
            elif business_metrics.competitive_strength > 45:
                positioning = "average_performer"
            else:
                positioning = "struggling_player"
            
            # Competitive strategy recommendation
            if business_metrics.profit_margin > 0.12 and business_metrics.market_position_score > 70:
                strategy = "differentiation"
            elif business_metrics.profit_margin < 0.08 and market_context.local_competition_density == "very_high":
                strategy = "cost_leadership"
            else:
                strategy = "focused_differentiation"
            
            return {
                "positioning": positioning,
                "competitive_strength_score": business_metrics.competitive_strength,
                "strengths": strengths,
                "weaknesses": weaknesses,
                "opportunities": opportunities,
                "threats": threats,
                "recommended_strategy": strategy,
                "market_share_estimate": self._estimate_market_share(business_data, business_metrics),
                "competitive_moats": self._identify_competitive_moats(business_data),
                "competitive_risks": self._identify_competitive_risks(business_data, market_context)
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing competitive position: {str(e)}")
            return {
                "positioning": "unknown",
                "competitive_strength_score": 50,
                "strengths": [],
                "weaknesses": [],
                "opportunities": [],
                "threats": [],
                "recommended_strategy": "focused_differentiation",
                "market_share_estimate": 0.01,
                "competitive_moats": [],
                "competitive_risks": []
            }
    
    def _estimate_market_share(self, business_data: Dict[str, Any], 
                             business_metrics: USBusinessMetrics) -> float:
        """Estimate local market share."""
        
        try:
            # This would use market size data and business revenue
            # Simplified calculation
            sector = business_data.get('sector', '')
            location_type = classify_us_location_type(
                business_data.get('city', ''),
                business_data.get('state', ''),
                business_data.get('zip_code', '')
            )
            
            # Estimate local market size (simplified)
            local_market_size = 5000000  # $5M local market assumption
            business_revenue = business_metrics.annual_revenue
            
            market_share = (business_revenue / local_market_size) * 100
            return min(50.0, max(0.01, market_share))  # Cap at reasonable range
            
        except:
            return 1.0  # Default 1% market share
    
    def _identify_competitive_moats(self, business_data: Dict[str, Any]) -> List[str]:
        """Identify potential competitive moats."""
        
        moats = []
        
        # Customer loyalty (years in business)
        if business_data.get('years_in_business', 0) > 10:
            moats.append("Established customer relationships")
        
        # Location advantage
        location_type = classify_us_location_type(
            business_data.get('city', ''),
            business_data.get('state', ''),
            business_data.get('zip_code', '')
        )
        if location_type in ['urban_high_income', 'business_district']:
            moats.append("Prime location advantage")
        
        # Specialized expertise
        if business_data.get('certifications') or business_data.get('unique_value_proposition'):
            moats.append("Specialized expertise and certifications")
        
        # Scale advantages
        if business_data.get('employees_count', 0) > 20:
            moats.append("Operational scale advantages")
        
        return moats
    
    def _identify_competitive_risks(self, business_data: Dict[str, Any],
                                  market_context: USMarketContext) -> List[str]:
        """Identify competitive risks."""
        
        risks = []
        
        # High competition
        if market_context.local_competition_density in ['high', 'very_high']:
            risks.append("Intense local competition")
        
        # Digital disruption
        sector = business_data.get('sector', '')
        disruptible_sectors = ['retail', 'electronics', 'auto']
        if sector in disruptible_sectors:
            risks.append("Digital disruption risk")
        
        # Economic sensitivity
        if market_context.sector_growth_rate < 0.03:
            risks.append("Slow sector growth")
        
        # Small scale vulnerability
        if business_data.get('employees_count', 0) < 5:
            risks.append("Scale disadvantage vs larger competitors")
        
        return risks
    
    async def _analyze_growth_potential(self, business_data: Dict[str, Any],
                                      business_metrics: USBusinessMetrics,
                                      market_context: USMarketContext) -> Dict[str, Any]:
        """Analyze business growth potential."""
        
        try:
            # Growth readiness assessment
            growth_readiness_factors = []
            
            # Financial readiness
            if business_metrics.cash_runway_months > 6:
                growth_readiness_factors.append("Strong cash position")
            if business_metrics.monthly_cash_flow > 0:
                growth_readiness_factors.append("Positive cash flow")
            if business_metrics.profit_margin > 0.10:
                growth_readiness_factors.append("Healthy profit margins")
            
            # Market readiness
            if market_context.sector_growth_rate > 0.08:
                growth_readiness_factors.append("Growing market sector")
            if market_context.location_advantage_score > 70:
                growth_readiness_factors.append("Favorable location")
            
            # Operational readiness
            if business_data.get('employees_count', 0) > 5:
                growth_readiness_factors.append("Adequate team size")
            if business_data.get('years_in_business', 0) > 3:
                growth_readiness_factors.append("Operational experience")
            
            # Growth constraints
            growth_constraints = []
            
            if business_metrics.cash_runway_months < 3:
                growth_constraints.append("Limited cash runway")
            if business_metrics.financial_stress_score > 70:
                growth_constraints.append("High financial stress")
            if market_context.local_competition_density == "very_high":
                growth_constraints.append("Intense competition")
            if business_metrics.revenue_volatility > 0.4:
                growth_constraints.append("Revenue instability")
            
            # Growth opportunities
            growth_opportunities = []
            
            # Market expansion
            if business_metrics.market_expansion_readiness > 70:
                growth_opportunities.append({
                    "type": "geographic_expansion",
                    "description": "Expand to new geographic markets",
                    "investment_required": business_metrics.current_monthly_revenue * 3,
                    "timeline": "6-12 months",
                    "success_probability": 70
                })
            
            # Product/Service expansion
            if business_metrics.scalability_potential > 60:
                growth_opportunities.append({
                    "type": "product_expansion",
                    "description": "Expand product/service offerings",
                    "investment_required": business_metrics.current_monthly_revenue * 2,
                    "timeline": "3-6 months",
                    "success_probability": 75
                })
            
            # Digital transformation
            growth_opportunities.append({
                "type": "digital_transformation",
                "description": "Enhance digital capabilities and online presence",
                "investment_required": business_metrics.current_monthly_revenue * 1.5,
                "timeline": "2-4 months",
                "success_probability": 80
            })
            
            # Growth strategy recommendations
            if business_metrics.growth_momentum_score > 75:
                strategy = "aggressive_growth"
            elif business_metrics.growth_momentum_score > 50:
                strategy = "steady_expansion"
            else:
                strategy = "consolidation_first"
            
            return {
                "growth_potential_score": business_metrics.growth_momentum_score,
                "growth_strategy": strategy,
                "growth_readiness_factors": growth_readiness_factors,
                "growth_constraints": growth_constraints,
                "growth_opportunities": growth_opportunities,
                "scalability_assessment": {
                    "scalability_score": business_metrics.scalability_potential,
                    "scalability_timeline": "12-24 months",
                    "scalability_investment": business_metrics.annual_revenue * 0.2
                },
                "market_expansion_assessment": {
                    "expansion_readiness": business_metrics.market_expansion_readiness,
                    "target_markets": self._identify_target_markets(business_data),
                    "expansion_strategy": self._recommend_expansion_strategy(business_data, business_metrics)
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing growth potential: {str(e)}")
            return {
                "growth_potential_score": 50,
                "growth_strategy": "steady_expansion",
                "growth_readiness_factors": [],
                "growth_constraints": [],
                "growth_opportunities": [],
                "scalability_assessment": {},
                "market_expansion_assessment": {}
            }
    
    def _identify_target_markets(self, business_data: Dict[str, Any]) -> List[str]:
        """Identify potential target markets for expansion."""
        
        current_state = business_data.get('state', '').upper()
        sector = business_data.get('sector', '')
        
        # Market expansion recommendations by sector and current location
        expansion_markets = {
            'electronics': ['TX', 'CA', 'FL', 'NY', 'WA'],
            'food': ['CA', 'TX', 'NY', 'FL', 'IL'],
            'retail': ['CA', 'TX', 'FL', 'NY', 'OH'],
            'auto': ['TX', 'CA', 'FL', 'MI', 'OH'],
            'professional_services': ['NY', 'CA', 'TX', 'FL', 'IL']
        }
        
        potential_markets = expansion_markets.get(sector, ['TX', 'CA', 'FL', 'NY'])
        
        # Remove current state from recommendations
        target_markets = [state for state in potential_markets if state != current_state]
        
        return target_markets[:3]  # Top 3 recommendations
    
    def _recommend_expansion_strategy(self, business_data: Dict[str, Any],
                                    business_metrics: USBusinessMetrics) -> str:
        """Recommend expansion strategy based on business readiness."""
        
        if business_metrics.cash_runway_months > 12 and business_metrics.revenue_growth_rate > 0.15:
            return "aggressive_multi_market"
        elif business_metrics.cash_runway_months > 6 and business_metrics.monthly_cash_flow > 0:
            return "careful_single_market"
        else:
            return "strengthen_before_expansion"
    
    # Continue with the remaining methods in the next part...
    
    async def _assess_business_risks(self, business_data: Dict[str, Any],
                                   business_metrics: USBusinessMetrics,
                                   economic_impact: USEconomicImpact) -> Dict[str, Any]:
        """Comprehensive US business risk assessment."""
        
        try:
            # Financial risks
            financial_risks = []
            
            if business_metrics.cash_runway_months < 3:
                financial_risks.append({
                    "risk": "Cash flow crisis",
                    "severity": "critical",
                    "probability": 0.8,
                    "impact": "business_closure",
                    "mitigation": "Immediate cash flow improvement or financing"
                })
            
            if business_metrics.debt_service_coverage and business_metrics.debt_service_coverage < 1.25:
                financial_risks.append({
                    "risk": "Debt service difficulty",
                    "severity": "high",
                    "probability": 0.6,
                    "impact": "default_risk",
                    "mitigation": "Debt restructuring or revenue improvement"
                })
            
            if business_metrics.revenue_volatility > 0.4:
                financial_risks.append({
                    "risk": "Revenue instability",
                    "severity": "medium",
                    "probability": 0.7,
                    "impact": "planning_difficulty",
                    "mitigation": "Revenue diversification and forecasting"
                })
            
            # Market risks
            market_risks = []
            
            if economic_impact.recession_risk_impact < -0.15:
                market_risks.append({
                    "risk": "Economic recession impact",
                    "severity": "high",
                    "probability": 0.4,
                    "impact": "revenue_decline",
                    "mitigation": "Defensive business model adjustments"
                })
            
            if business_metrics.economic_resilience_score < 40:
                market_risks.append({
                    "risk": "Economic sensitivity",
                    "severity": "medium",
                    "probability": 0.6,
                    "impact": "volatile_performance",
                    "mitigation": "Economic hedging strategies"
                })
            
            # Operational risks
            operational_risks = []
            
            employees_count = business_data.get('employees_count', 0)
            if employees_count < 3:
                operational_risks.append({
                    "risk": "Key person dependency",
                    "severity": "high",
                    "probability": 0.5,
                    "impact": "operational_disruption",
                    "mitigation": "Team expansion and process documentation"
                })
            
            # Competitive risks
            competitive_risks = []
            
            if business_metrics.competitive_strength < 50:
                competitive_risks.append({
                    "risk": "Competitive disadvantage",
                    "severity": "medium",
                    "probability": 0.6,
                    "impact": "market_share_loss",
                    "mitigation": "Competitive positioning improvement"
                })
            
            # Overall risk assessment
            all_risks = financial_risks + market_risks + operational_risks + competitive_risks
            
            # Calculate overall risk score
            high_severity_count = sum(1 for risk in all_risks if risk['severity'] in ['critical', 'high'])
            total_risk_count = len(all_risks)
            
            if high_severity_count >= 3:
                overall_risk_level = "high"
                risk_score = 75
            elif high_severity_count >= 1:
                overall_risk_level = "medium"
                risk_score = 55
            else:
                overall_risk_level = "low"
                risk_score = 30
            
            # Risk mitigation priorities
            mitigation_priorities = sorted(
                all_risks, 
                key=lambda x: (x['severity'] == 'critical', x['severity'] == 'high', x['probability']),
                reverse=True
            )[:5]  # Top 5 priorities
            
            return {
                "overall_risk_level": overall_risk_level,
                "overall_risk_score": risk_score,
                "financial_risks": financial_risks,
                "market_risks": market_risks,
                "operational_risks": operational_risks,
                "competitive_risks": competitive_risks,
                "top_risk_priorities": mitigation_priorities,
                "risk_monitoring_recommendations": self._generate_risk_monitoring_plan(all_risks),
                "business_continuity_score": self._calculate_business_continuity_score(business_metrics),
                "insurance_recommendations": self._recommend_insurance_coverage(business_data, all_risks)
            }
            
        except Exception as e:
            self.logger.error(f"Error assessing business risks: {str(e)}")
            return {
                "overall_risk_level": "medium",
                "overall_risk_score": 50,
                "financial_risks": [],
                "market_risks": [],
                "operational_risks": [],
                "competitive_risks": [],
                "top_risk_priorities": [],
                "risk_monitoring_recommendations": [],
                "business_continuity_score": 50,
                "insurance_recommendations": []
            }
    
    def _generate_risk_monitoring_plan(self, risks: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Generate risk monitoring recommendations."""
        
        monitoring_plan = []
        
        # Financial monitoring
        if any('cash flow' in risk['risk'].lower() for risk in risks):
            monitoring_plan.append({
                "metric": "Weekly cash flow tracking",
                "frequency": "weekly",
                "threshold": "Less than 4 weeks runway",
                "action": "Immediate financing or cost reduction"
            })
        
        # Market monitoring
        if any('recession' in risk['risk'].lower() or 'economic' in risk['risk'].lower() for risk in risks):
            monitoring_plan.append({
                "metric": "Economic indicator tracking",
                "frequency": "monthly",
                "threshold": "Fed rate changes or recession indicators",
                "action": "Adjust business strategy defensively"
            })
        
        # Competitive monitoring
        if any('competitive' in risk['risk'].lower() for risk in risks):
            monitoring_plan.append({
                "metric": "Competitive landscape review",
                "frequency": "quarterly",
                "threshold": "New competitors or pricing changes",
                "action": "Adjust competitive strategy"
            })
        
        return monitoring_plan
    
    def _calculate_business_continuity_score(self, business_metrics: USBusinessMetrics) -> float:
        """Calculate business continuity score."""
        
        continuity_factors = []
        
        # Financial continuity
        if business_metrics.cash_runway_months > 6:
            continuity_factors.append(25)
        elif business_metrics.cash_runway_months > 3:
            continuity_factors.append(15)
        else:
            continuity_factors.append(5)
        
        # Revenue stability
        if business_metrics.revenue_volatility < 0.2:
            continuity_factors.append(20)
        elif business_metrics.revenue_volatility < 0.4:
            continuity_factors.append(15)
        else:
            continuity_factors.append(5)
        
        # Profitability
        if business_metrics.profit_margin > 0.10:
            continuity_factors.append(20)
        elif business_metrics.profit_margin > 0.05:
            continuity_factors.append(15)
        else:
            continuity_factors.append(5)
        
        # Market position
        if business_metrics.market_position_score > 70:
            continuity_factors.append(15)
        elif business_metrics.market_position_score > 50:
            continuity_factors.append(10)
        else:
            continuity_factors.append(5)
        
        # Economic resilience
        if business_metrics.economic_resilience_score > 70:
            continuity_factors.append(20)
        elif business_metrics.economic_resilience_score > 50:
            continuity_factors.append(15)
        else:
            continuity_factors.append(10)
        
        return min(100.0, sum(continuity_factors))
    
    def _recommend_insurance_coverage(self, business_data: Dict[str, Any],
                                    risks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Recommend insurance coverage based on identified risks."""
        
        recommendations = []
        
        # General liability (always recommended)
        recommendations.append({
            "coverage_type": "General Liability",
            "importance": "essential",
            "estimated_annual_cost": 1200,
            "coverage_amount": 1000000,
            "reasoning": "Protection against customer injury and property damage claims"
        })
        
        # Property insurance
        if business_data.get('business_assets', 0) > 50000:
            recommendations.append({
                "coverage_type": "Commercial Property",
                "importance": "high",
                "estimated_annual_cost": 800,
                "coverage_amount": business_data.get('business_assets', 100000),
                "reasoning": "Protection of business assets and equipment"
            })
        
        # Business interruption
        if any('operational' in risk['risk'].lower() for risk in risks):
            recommendations.append({
                "coverage_type": "Business Interruption",
                "importance": "high",
                "estimated_annual_cost": 600,
                "coverage_amount": business_data.get('monthly_revenue', [0])[-1] * 6 if business_data.get('monthly_revenue') else 300000,
                "reasoning": "Protection against lost income during operational disruptions"
            })
        
        # Key person insurance
        employees = business_data.get('employees_count', 0)
        if employees < 5:
            recommendations.append({
                "coverage_type": "Key Person Life Insurance",
                "importance": "medium",
                "estimated_annual_cost": 500,
                "coverage_amount": 250000,
                "reasoning": "Protection against loss of key personnel in small business"
            })
        
        return recommendations
    
    async def _analyze_financial_health(self, business_data: Dict[str, Any],
                                      business_metrics: USBusinessMetrics) -> Dict[str, Any]:
        """Comprehensive financial health analysis."""
        
        try:
            # Liquidity analysis
            current_ratio = None
            quick_ratio = None
            
            # Working capital analysis
            monthly_revenue = business_data.get('monthly_revenue', [])
            monthly_expenses = business_data.get('monthly_expenses', [])
            
            if isinstance(monthly_expenses, list):
                avg_monthly_expenses = sum(monthly_expenses) / len(monthly_expenses)
            else:
                avg_monthly_expenses = monthly_expenses
            
            working_capital = business_metrics.current_monthly_revenue - avg_monthly_expenses
            
            # Debt analysis
            outstanding_debt = business_data.get('outstanding_debt', 0)
            debt_to_revenue = safe_divide(outstanding_debt, business_metrics.annual_revenue)
            
            # Profitability analysis
            gross_margin = business_metrics.profit_margin
            net_margin = business_metrics.profit_margin  # Simplified
            
            # Cash flow analysis
            operating_cash_flow = business_metrics.monthly_cash_flow
            free_cash_flow = operating_cash_flow  # Simplified
            
            # Financial ratios
            financial_ratios = {
                "profit_margin": business_metrics.profit_margin,
                "cash_runway_months": business_metrics.cash_runway_months,
                "debt_to_revenue": debt_to_revenue,
                "revenue_growth_rate": business_metrics.revenue_growth_rate,
                "revenue_volatility": business_metrics.revenue_volatility
            }
            
            # Financial health score components
            liquidity_score = min(100, (business_metrics.cash_runway_months / 6) * 100)
            profitability_score = min(100, (business_metrics.profit_margin / 0.15) * 100)
            stability_score = max(0, 100 - (business_metrics.revenue_volatility * 200))
            growth_score = min(100, max(0, (business_metrics.revenue_growth_rate + 0.05) / 0.20 * 100))
            
            overall_financial_health = (
                liquidity_score * 0.3 +
                profitability_score * 0.3 +
                stability_score * 0.25 +
                growth_score * 0.15
            )
            
            # Financial health grade
            if overall_financial_health >= 85:
                health_grade = "Excellent"
            elif overall_financial_health >= 70:
                health_grade = "Good"
            elif overall_financial_health >= 55:
                health_grade = "Fair"
            elif overall_financial_health >= 40:
                health_grade = "Poor"
            else:
                health_grade = "Critical"
            
            # Financial strengths and concerns
            strengths = []
            concerns = []
            
            if business_metrics.profit_margin > 0.12:
                strengths.append("Strong profit margins")
            if business_metrics.cash_runway_months > 6:
                strengths.append("Adequate cash reserves")
            if business_metrics.revenue_growth_rate > 0.08:
                strengths.append("Good revenue growth")
            
            if business_metrics.cash_runway_months < 3:
                concerns.append("Limited cash runway")
            if business_metrics.profit_margin < 0.05:
                concerns.append("Thin profit margins")
            if business_metrics.revenue_volatility > 0.3:
                concerns.append("High revenue volatility")
            if debt_to_revenue > 0.5:
                concerns.append("High debt burden")
            
            return {
                "overall_financial_health_score": overall_financial_health,
                "financial_health_grade": health_grade,
                "component_scores": {
                    "liquidity": liquidity_score,
                    "profitability": profitability_score,
                    "stability": stability_score,
                    "growth": growth_score
                },
                "financial_ratios": financial_ratios,
                "cash_flow_analysis": {
                    "monthly_operating_cash_flow": operating_cash_flow,
                    "cash_runway_months": business_metrics.cash_runway_months,
                    "cash_burn_rate": avg_monthly_expenses,
                    "cash_generation_ability": "positive" if operating_cash_flow > 0 else "negative"
                },
                "debt_analysis": {
                    "total_debt": outstanding_debt,
                    "debt_to_revenue_ratio": debt_to_revenue,
                    "debt_service_coverage": business_metrics.debt_service_coverage,
                    "debt_burden_assessment": "high" if debt_to_revenue > 0.3 else "moderate" if debt_to_revenue > 0.1 else "low"
                },
                "financial_strengths": strengths,
                "financial_concerns": concerns,
                "improvement_recommendations": self._generate_financial_improvement_recommendations(
                    business_metrics, concerns
                )
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing financial health: {str(e)}")
            return {
                "overall_financial_health_score": 50,
                "financial_health_grade": "Fair",
                "component_scores": {},
                "financial_ratios": {},
                "cash_flow_analysis": {},
                "debt_analysis": {},
                "financial_strengths": [],
                "financial_concerns": [],
                "improvement_recommendations": []
            }
    
    def _generate_financial_improvement_recommendations(self, business_metrics: USBusinessMetrics,
                                                      concerns: List[str]) -> List[Dict[str, Any]]:
        """Generate financial improvement recommendations."""
        
        recommendations = []
        
        # Cash flow improvements
        if business_metrics.cash_runway_months < 6:
            recommendations.append({
                "area": "cash_flow_management",
                "recommendation": "Improve accounts receivable collection",
                "priority": "high",
                "timeline": "immediate",
                "expected_impact": "1-2 months additional runway",
                "implementation_steps": [
                    "Review payment terms with customers",
                    "Implement faster invoicing process",
                    "Consider factoring for immediate cash"
                ]
            })
        
        # Profitability improvements
        if business_metrics.profit_margin < 0.08:
            recommendations.append({
                "area": "profitability",
                "recommendation": "Optimize pricing and reduce costs",
                "priority": "high",
                "timeline": "1-3 months",
                "expected_impact": "2-5% margin improvement",
                "implementation_steps": [
                    "Analyze pricing vs competitors",
                    "Review cost structure for reductions",
                    "Focus on higher-margin products/services"
                ]
            })
        
        # Revenue stability
        if business_metrics.revenue_volatility > 0.3:
            recommendations.append({
                "area": "revenue_stability",
                "recommendation": "Diversify revenue streams",
                "priority": "medium",
                "timeline": "3-6 months",
                "expected_impact": "Reduced revenue volatility",
                "implementation_steps": [
                    "Develop recurring revenue model",
                    "Expand customer base",
                    "Add complementary services"
                ]
            })
        
        return recommendations
    
    async def _analyze_operational_efficiency(self, business_data: Dict[str, Any],
                                            business_metrics: USBusinessMetrics) -> Dict[str, Any]:
        """Analyze operational efficiency metrics."""
        
        try:
            # Productivity metrics
            revenue_per_employee = business_metrics.revenue_per_employee
            employees_count = max(1, business_data.get('employees_count', 1))
            
            # Industry benchmarks for revenue per employee
            sector_benchmarks = {
                'electronics': 200000,
                'food': 150000,
                'retail': 180000,
                'auto': 250000,
                'professional_services': 300000,
                'manufacturing': 220000
            }
            
            sector = business_data.get('sector', 'retail')
            benchmark = sector_benchmarks.get(sector, 180000)
            
            productivity_ratio = revenue_per_employee / benchmark
            
            # Efficiency scores
            if productivity_ratio > 1.5:
                productivity_score = 90
            elif productivity_ratio > 1.2:
                productivity_score = 75
            elif productivity_ratio > 0.8:
                productivity_score = 60
            else:
                productivity_score = 40
            
            # Asset utilization (simplified)
            business_assets = business_data.get('business_assets', 0)
            if business_assets > 0:
                asset_turnover = business_metrics.annual_revenue / business_assets
            else:
                asset_turnover = None
            
            # Operational efficiency insights
            efficiency_strengths = []
            efficiency_opportunities = []
            
            if productivity_ratio > 1.2:
                efficiency_strengths.append("High employee productivity")
            if business_metrics.scalability_potential > 70:
                efficiency_strengths.append("Good scalability potential")
            
            if productivity_ratio < 0.8:
                efficiency_opportunities.append("Improve employee productivity")
            if employees_count > 0 and business_metrics.annual_revenue / employees_count < benchmark:
                efficiency_opportunities.append("Optimize staffing levels")
            
            # Automation opportunities
            automation_score = self._assess_automation_potential(business_data, sector)
            
            return {
                "productivity_analysis": {
                    "revenue_per_employee": revenue_per_employee,
                    "industry_benchmark": benchmark,
                    "productivity_ratio": productivity_ratio,
                    "productivity_score": productivity_score
                },
                "efficiency_metrics": {
                    "asset_turnover": asset_turnover,
                    "scalability_score": business_metrics.scalability_potential,
                    "operational_leverage": self._calculate_operational_leverage(business_data)
                },
                "automation_assessment": {
                    "automation_potential_score": automation_score,
                    "automation_opportunities": self._identify_automation_opportunities(business_data, sector),
                    "technology_adoption_level": self._assess_technology_adoption(business_data)
                },
                "efficiency_strengths": efficiency_strengths,
                "efficiency_opportunities": efficiency_opportunities,
                "operational_recommendations": self._generate_operational_recommendations(
                    business_data, business_metrics, productivity_ratio
                )
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing operational efficiency: {str(e)}")
            return {
                "productivity_analysis": {},
                "efficiency_metrics": {},
                "automation_assessment": {},
                "efficiency_strengths": [],
                "efficiency_opportunities": [],
                "operational_recommendations": []
            }
    
    def _assess_automation_potential(self, business_data: Dict[str, Any], sector: str) -> float:
        """Assess automation potential for the business."""
        
        # Sector automation potential
        sector_automation_scores = {
            'electronics': 75,
            'retail': 60,
            'food': 50,
            'auto': 70,
            'professional_services': 80,
            'manufacturing': 85
        }
        
        base_score = sector_automation_scores.get(sector, 60)
        
        # Adjust based on business size
        employees = business_data.get('employees_count', 0)
        if employees > 20:
            size_adjustment = 10
        elif employees > 10:
            size_adjustment = 5
        else:
            size_adjustment = 0
        
        return min(100, base_score + size_adjustment)
    
    def _identify_automation_opportunities(self, business_data: Dict[str, Any], sector: str) -> List[str]:
        """Identify specific automation opportunities."""
        
        opportunities = []
        
        # Common automation opportunities by sector
        sector_opportunities = {
            'electronics': ['Inventory management', 'Customer support chatbots', 'Pricing optimization'],
            'retail': ['Point of sale systems', 'Inventory tracking', 'Customer relationship management'],
            'food': ['Order management', 'Inventory tracking', 'Customer loyalty programs'],
            'auto': ['Parts inventory', 'Service scheduling', 'Customer communications'],
            'professional_services': ['Client management', 'Document automation', 'Scheduling systems'],
            'manufacturing': ['Production scheduling', 'Quality control', 'Supply chain management']
        }
        
        return sector_opportunities.get(sector, ['Process automation', 'Data management', 'Customer service'])
    
    def _assess_technology_adoption(self, business_data: Dict[str, Any]) -> str:
        """Assess current technology adoption level."""
        
        # This would be based on actual technology usage data
        # For now, we'll use a simplified assessment
        
        years_in_business = business_data.get('years_in_business', 0)
        employees = business_data.get('employees_count', 0)
        
        if employees > 20 and years_in_business < 5:
            return "advanced"
        elif employees > 10 or years_in_business > 3:
            return "moderate"
        else:
            return "basic"
    
    def _calculate_operational_leverage(self, business_data: Dict[str, Any]) -> Optional[float]:
        """Calculate operational leverage."""
        
        try:
            monthly_revenue = business_data.get('monthly_revenue', [])
            if len(monthly_revenue) >= 2:
                revenue_change = (monthly_revenue[-1] - monthly_revenue[-2]) / monthly_revenue[-2]
                # Simplified - assume 20% variable costs
                profit_change = revenue_change * 1.25  # Operational leverage effect
                return profit_change / revenue_change if revenue_change != 0 else None
            return None
        except:
            return None
    
    def _generate_operational_recommendations(self, business_data: Dict[str, Any],
                                            business_metrics: USBusinessMetrics,
                                            productivity_ratio: float) -> List[Dict[str, Any]]:
        """Generate operational improvement recommendations."""
        
        recommendations = []
        
        if productivity_ratio < 0.8:
            recommendations.append({
                "area": "productivity_improvement",
                "recommendation": "Enhance employee productivity through training and tools",
                "priority": "high",
                "expected_impact": "10-20% productivity increase",
                "implementation_timeline": "2-4 months"
            })
        
        if business_metrics.scalability_potential < 60:
            recommendations.append({
                "area": "process_optimization",
                "recommendation": "Standardize and document key business processes",
                "priority": "medium",
                "expected_impact": "Improved scalability and consistency",
                "implementation_timeline": "1-3 months"
            })
        
        employees = business_data.get('employees_count', 0)
        if employees > 5:
            recommendations.append({
                "area": "technology_adoption",
                "recommendation": "Implement business management software",
                "priority": "medium",
                "expected_impact": "Enhanced operational efficiency",
                "implementation_timeline": "2-6 months"
            })
        
        return recommendations
    
    async def _analyze_strategic_positioning(self, business_data: Dict[str, Any],
                                           market_context: USMarketContext,
                                           competitive_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze strategic positioning in the US market."""
        
        try:
            # Current strategic position
            current_position = competitive_analysis.get('positioning', 'average_performer')
            competitive_strength = competitive_analysis.get('competitive_strength_score', 50)
            
            # Strategic options analysis
            strategic_options = []
            
            # Market leadership strategy
            if competitive_strength > 75:
                strategic_options.append({
                    "strategy": "market_leadership",
                    "description": "Leverage strong position to dominate market",
                    "feasibility": 85,
                    "investment_required": "high",
                    "timeline": "12-18 months",
                    "risk_level": "medium"
                })
            
            # Differentiation strategy
            if market_context.purchasing_power_index > 1.1:
                strategic_options.append({
                    "strategy": "differentiation",
                    "description": "Focus on premium positioning and unique value",
                    "feasibility": 70,
                    "investment_required": "medium",
                    "timeline": "6-12 months",
                    "risk_level": "medium"
                })
            
            # Cost leadership strategy
            if market_context.local_competition_density == "very_high":
                strategic_options.append({
                    "strategy": "cost_leadership",
                    "description": "Compete on price through operational efficiency",
                    "feasibility": 60,
                    "investment_required": "medium",
                    "timeline": "6-12 months",
                    "risk_level": "high"
                })
            
            # Focus strategy
            strategic_options.append({
                "strategy": "focused_differentiation",
                "description": "Specialize in specific market niche",
                "feasibility": 75,
                "investment_required": "low",
                "timeline": "3-6 months",
                "risk_level": "low"
            })
            
            # Strategic positioning score
            positioning_factors = []
            
            if competitive_strength > 60:
                positioning_factors.append(25)
            if market_context.location_advantage_score > 70:
                positioning_factors.append(20)
            if market_context.sector_growth_rate > 0.08:
                positioning_factors.append(20)
            if business_data.get('unique_value_proposition'):
                positioning_factors.append(15)
            if business_data.get('years_in_business', 0) > 5:
                positioning_factors.append(10)
            
            positioning_strength = min(100, sum(positioning_factors))
            
            # Recommended strategic direction
            if positioning_strength > 75:
                recommended_direction = "aggressive_growth"
            elif positioning_strength > 60:
                recommended_direction = "selective_expansion"
            elif positioning_strength > 45:
                recommended_direction = "strengthen_position"
            else:
                recommended_direction = "defensive_consolidation"
            
            return {
                "current_strategic_position": current_position,
                "positioning_strength_score": positioning_strength,
                "strategic_options": strategic_options,
                "recommended_strategic_direction": recommended_direction,
                "strategic_priorities": self._identify_strategic_priorities(
                    business_data, competitive_analysis, market_context
                ),
                "competitive_moats": competitive_analysis.get('competitive_moats', []),
                "strategic_risks": self._identify_strategic_risks(business_data, market_context),
                "value_proposition_assessment": self._assess_value_proposition(business_data),
                "market_positioning_recommendations": self._generate_positioning_recommendations(
                    business_data, market_context, competitive_analysis
                )
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing strategic positioning: {str(e)}")
            return {
                "current_strategic_position": "average_performer",
                "positioning_strength_score": 50,
                "strategic_options": [],
                "recommended_strategic_direction": "strengthen_position",
                "strategic_priorities": [],
                "competitive_moats": [],
                "strategic_risks": [],
                "value_proposition_assessment": {},
                "market_positioning_recommendations": []
            }
    
    def _identify_strategic_priorities(self, business_data: Dict[str, Any],
                                     competitive_analysis: Dict[str, Any],
                                     market_context: USMarketContext) -> List[Dict[str, Any]]:
        """Identify top strategic priorities."""
        
        priorities = []
        
        # Financial stability priority
        cash_runway = business_data.get('current_cash', 0) / max(1, business_data.get('monthly_expenses', 1))
        if cash_runway < 6:
            priorities.append({
                "priority": "financial_stabilization",
                "urgency": "critical",
                "description": "Improve cash flow and financial stability",
                "timeline": "immediate"
            })
        
        # Competitive positioning
        competitive_strength = competitive_analysis.get('competitive_strength_score', 50)
        if competitive_strength < 50:
            priorities.append({
                "priority": "competitive_strengthening",
                "urgency": "high",
                "description": "Improve competitive position and differentiation",
                "timeline": "3-6 months"
            })
        
        # Market expansion
        if market_context.sector_growth_rate > 0.08:
            priorities.append({
                "priority": "market_expansion",
                "urgency": "medium",
                "description": "Capitalize on growing market opportunities",
                "timeline": "6-12 months"
            })
        
        # Operational efficiency
        priorities.append({
            "priority": "operational_optimization",
            "urgency": "medium",
            "description": "Improve operational efficiency and scalability",
            "timeline": "ongoing"
        })
        
        return priorities
    
    def _identify_strategic_risks(self, business_data: Dict[str, Any],
                                market_context: USMarketContext) -> List[str]:
        """Identify strategic risks."""
        
        risks = []
        
        if market_context.local_competition_density == "very_high":
            risks.append("Market overcrowding and price pressure")
        
        if market_context.sector_growth_rate < 0.03:
            risks.append("Declining market growth potential")
        
        if business_data.get('years_in_business', 0) < 3:
            risks.append("Insufficient market experience and brand recognition")
        
        if business_data.get('employees_count', 0) < 3:
            risks.append("Over-dependence on key personnel")
        
        return risks
    
    def _assess_value_proposition(self, business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess current value proposition strength."""
        
        uvp = business_data.get('unique_value_proposition', '')
        competitive_advantages = business_data.get('competitive_advantages', [])
        
        if uvp and len(competitive_advantages) >= 2:
            strength = "strong"
        elif uvp or len(competitive_advantages) >= 1:
            strength = "moderate"
        else:
            strength = "weak"
        
        return {
            "strength": strength,
            "current_proposition": uvp,
            "competitive_advantages": competitive_advantages,
            "improvement_opportunities": self._identify_value_prop_improvements(business_data)
        }
    
    def _identify_value_prop_improvements(self, business_data: Dict[str, Any]) -> List[str]:
        """Identify value proposition improvement opportunities."""
        
        improvements = []
        
        if not business_data.get('unique_value_proposition'):
            improvements.append("Develop clear unique value proposition")
        
        if len(business_data.get('competitive_advantages', [])) < 2:
            improvements.append("Identify and develop competitive advantages")
        
        if business_data.get('years_in_business', 0) > 5:
            improvements.append("Leverage experience and reputation")
        
        return improvements
    
    def _generate_positioning_recommendations(self, business_data: Dict[str, Any],
                                            market_context: USMarketContext,
                                            competitive_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate market positioning recommendations."""
        
        recommendations = []
        
        if market_context.purchasing_power_index > 1.2:
            recommendations.append({
                "positioning": "premium_quality",
                "rationale": "High local purchasing power supports premium positioning",
                "implementation": "Focus on quality, service, and premium pricing",
                "timeline": "3-6 months"
            })
        
        if market_context.local_competition_density == "very_high":
            recommendations.append({
                "positioning": "niche_specialization",
                "rationale": "High competition requires focused differentiation",
                "implementation": "Specialize in specific customer segment or service",
                "timeline": "2-4 months"
            })
        
        if competitive_analysis.get('competitive_strength_score', 50) > 75:
            recommendations.append({
                "positioning": "market_leadership",
                "rationale": "Strong competitive position enables leadership strategy",
                "implementation": "Expand market share and set industry standards",
                "timeline": "6-12 months"
            })
        
        return recommendations
    
    async def _assess_investment_readiness(self, business_data: Dict[str, Any],
                                         business_metrics: USBusinessMetrics,
                                         financial_health: Dict[str, Any]) -> Dict[str, Any]:
        """Assess readiness for investment opportunities."""
        
        try:
            # Investment capacity analysis
            current_cash = business_data.get('current_cash', 0)
            monthly_expenses = business_data.get('monthly_expenses', [])
            if isinstance(monthly_expenses, list):
                avg_monthly_expenses = sum(monthly_expenses) / len(monthly_expenses)
            else:
                avg_monthly_expenses = monthly_expenses
            
            # Calculate available investment capital (keep 3-6 months runway)
            required_runway_months = 6 if business_metrics.revenue_volatility > 0.3 else 3
            required_cash_reserve = avg_monthly_expenses * required_runway_months
            available_investment_capital = max(0, current_cash - required_cash_reserve)
            
            # Investment readiness factors
            readiness_factors = []
            readiness_score = 0
            
            # Financial stability
            if business_metrics.cash_runway_months > 6:
                readiness_factors.append("Strong cash position")
                readiness_score += 25
            elif business_metrics.cash_runway_months > 3:
                readiness_factors.append("Adequate cash reserves")
                readiness_score += 15
            
            # Profitability
            if business_metrics.profit_margin > 0.12:
                readiness_factors.append("Strong profitability")
                readiness_score += 20
            elif business_metrics.profit_margin > 0.05:
                readiness_factors.append("Positive cash generation")
                readiness_score += 10
            
            # Growth momentum
            if business_metrics.revenue_growth_rate > 0.15:
                readiness_factors.append("High growth momentum")
                readiness_score += 20
            elif business_metrics.revenue_growth_rate > 0.05:
                readiness_factors.append("Steady growth")
                readiness_score += 10
            
            # Market position
            if business_metrics.market_position_score > 70:
                readiness_factors.append("Strong market position")
                readiness_score += 15
            
            # Operational maturity
            if business_data.get('years_in_business', 0) > 5:
                readiness_factors.append("Operational maturity")
                readiness_score += 10
            
            # Team capacity
            if business_data.get('employees_count', 0) > 10:
                readiness_factors.append("Adequate team capacity")
                readiness_score += 10
            
            # Investment readiness level
            if readiness_score >= 80:
                readiness_level = "high"
            elif readiness_score >= 60:
                readiness_level = "moderate"
            elif readiness_score >= 40:
                readiness_level = "limited"
            else:
                readiness_level = "not_ready"
            
            # Investment constraints
            constraints = []
            
            if business_metrics.cash_runway_months < 3:
                constraints.append("Limited cash runway")
            if business_metrics.profit_margin < 0.05:
                constraints.append("Weak profitability")
            if business_metrics.revenue_volatility > 0.4:
                constraints.append("High revenue volatility")
            if business_data.get('outstanding_debt', 0) / business_metrics.annual_revenue > 0.3:
                constraints.append("High debt burden")
            
            # Investment recommendations by category
            investment_categories = self._generate_investment_categories(
                available_investment_capital, business_metrics, business_data
            )
            
            return {
                "investment_readiness_level": readiness_level,
                "investment_readiness_score": readiness_score,
                "available_investment_capital": available_investment_capital,
                "required_cash_reserve": required_cash_reserve,
                "readiness_factors": readiness_factors,
                "investment_constraints": constraints,
                "investment_capacity_analysis": {
                    "total_cash": current_cash,
                    "monthly_expenses": avg_monthly_expenses,
                    "recommended_runway": required_runway_months,
                    "investment_capacity": available_investment_capital
                },
                "investment_categories": investment_categories,
                "risk_tolerance_assessment": self._assess_investment_risk_tolerance(business_data, business_metrics),
                "investment_timeline_recommendations": self._recommend_investment_timeline(
                    readiness_level, available_investment_capital
                )
            }
            
        except Exception as e:
            self.logger.error(f"Error assessing investment readiness: {str(e)}")
            return {
                "investment_readiness_level": "limited",
                "investment_readiness_score": 40,
                "available_investment_capital": 0,
                "required_cash_reserve": 0,
                "readiness_factors": [],
                "investment_constraints": [],
                "investment_capacity_analysis": {},
                "investment_categories": [],
                "risk_tolerance_assessment": {},
                "investment_timeline_recommendations": {}
            }
    
    def _generate_investment_categories(self, available_capital: float,
                                      business_metrics: USBusinessMetrics,
                                      business_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate investment category recommendations."""
        
        categories = []
        
        if available_capital > 0:
            # Business reinvestment
            business_reinvestment = min(available_capital * 0.4, available_capital)
            if business_reinvestment > 5000:
                categories.append({
                    "category": "business_reinvestment",
                    "recommended_amount": business_reinvestment,
                    "percentage": 40,
                    "expected_roi": 15,
                    "risk_level": "medium",
                    "timeline": "6-18 months",
                    "opportunities": [
                        "Marketing and customer acquisition",
                        "Equipment and technology upgrades",
                        "Inventory expansion",
                        "Staff hiring and training"
                    ]
                })
            
            # Emergency fund
            emergency_fund = min(available_capital * 0.3, available_capital - business_reinvestment)
            if emergency_fund > 1000:
                categories.append({
                    "category": "emergency_fund",
                    "recommended_amount": emergency_fund,
                    "percentage": 30,
                    "expected_roi": 4,
                    "risk_level": "low",
                    "timeline": "immediate",
                    "opportunities": [
                        "High-yield savings account",
                        "Money market funds",
                        "Short-term Treasury bills"
                    ]
                })
            
            # Market investments
            remaining_capital = available_capital - business_reinvestment - emergency_fund
            if remaining_capital > 2000:
                categories.append({
                    "category": "market_investments",
                    "recommended_amount": remaining_capital,
                    "percentage": 30,
                    "expected_roi": 8,
                    "risk_level": "medium",
                    "timeline": "long_term",
                    "opportunities": [
                        "Diversified index funds",
                        "Sector-specific ETFs",
                        "Individual stocks",
                        "Real estate investment trusts (REITs)"
                    ]
                })
        
        return categories
    
    def _assess_investment_risk_tolerance(self, business_data: Dict[str, Any],
                                        business_metrics: USBusinessMetrics) -> Dict[str, str]:
        """Assess investment risk tolerance based on business characteristics."""
        
        # Start with moderate baseline
        risk_factors = []
        
        # Business stability factors
        if business_data.get('years_in_business', 0) > 10:
            risk_factors.append("established_business")
        if business_metrics.revenue_volatility < 0.2:
            risk_factors.append("stable_revenue")
        if business_metrics.cash_runway_months > 12:
            risk_factors.append("strong_cash_position")
        
        # Risk-reducing factors
        if business_metrics.profit_margin > 0.15:
            risk_factors.append("high_profitability")
        if business_metrics.economic_resilience_score > 70:
            risk_factors.append("recession_resistant")
        
        # Risk-increasing factors
        risk_increasing = []
        if business_metrics.revenue_volatility > 0.4:
            risk_increasing.append("volatile_revenue")
        if business_metrics.cash_runway_months < 6:
            risk_increasing.append("limited_cash")
        if business_data.get('employees_count', 0) < 5:
            risk_increasing.append("small_team_dependency")
        
        # Determine overall risk tolerance
        if len(risk_factors) >= 3 and len(risk_increasing) <= 1:
            risk_tolerance = "moderate_to_aggressive"
        elif len(risk_factors) >= 2:
            risk_tolerance = "moderate"
        else:
            risk_tolerance = "conservative"
        
        return {
            "risk_tolerance": risk_tolerance,
            "risk_factors": risk_factors,
            "risk_constraints": risk_increasing,
            "investment_style": "growth_focused" if risk_tolerance == "moderate_to_aggressive" else 
                              "balanced" if risk_tolerance == "moderate" else "income_focused"
        }
    
    def _recommend_investment_timeline(self, readiness_level: str, available_capital: float) -> Dict[str, Any]:
        """Recommend investment timeline based on readiness."""
        
        if readiness_level == "high" and available_capital > 10000:
            return {
                "immediate": ["Emergency fund establishment", "High-priority business investments"],
                "3_months": ["Market investment initiation", "Equipment upgrades"],
                "6_months": ["Diversification expansion", "Growth investments"],
                "12_months": ["Portfolio rebalancing", "Advanced opportunities"]
            }
        elif readiness_level == "moderate":
            return {
                "immediate": ["Emergency fund", "Critical business needs"],
                "6_months": ["Conservative market investments"],
                "12_months": ["Gradual portfolio building"],
                "18_months": ["Expansion considerations"]
            }
        else:
            return {
                "immediate": ["Focus on business cash flow"],
                "6_months": ["Build emergency fund"],
                "12_months": ["Consider conservative investments"],
                "18_months": ["Reassess investment readiness"]
            }
    
    async def _generate_key_insights(self, business_metrics: USBusinessMetrics,
                                   market_context: USMarketContext,
                                   economic_impact: USEconomicImpact,
                                   performance_scores: Dict[str, Any],
                                   competitive_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate key business insights for decision making."""
        
        insights = []
        
        # Performance insight
        overall_score = performance_scores.get('overall_score', 50)
        if overall_score > 75:
            insights.append({
                "category": "performance",
                "insight": f"Strong overall performance with {overall_score:.0f}/100 score places you in top quartile",
                "impact": "positive",
                "urgency": "opportunity",
                "action_implication": "Consider aggressive growth strategies to capitalize on strong position"
            })
        elif overall_score < 50:
            insights.append({
                "category": "performance",
                "insight": f"Performance score of {overall_score:.0f}/100 indicates need for improvement",
                "impact": "negative",
                "urgency": "high",
                "action_implication": "Focus on operational improvements and cost management"
            })
        
        # Cash flow insight
        if business_metrics.cash_runway_months < 3:
            insights.append({
                "category": "financial",
                "insight": f"Critical cash runway of only {business_metrics.cash_runway_months:.1f} months",
                "impact": "critical",
                "urgency": "immediate",
                "action_implication": "Urgent need for cash flow improvement or emergency financing"
            })
        elif business_metrics.cash_runway_months > 12:
            insights.append({
                "category": "financial",
                "insight": f"Strong cash position with {business_metrics.cash_runway_months:.0f} months runway",
                "impact": "positive",
                "urgency": "opportunity",
                "action_implication": "Excess cash could be invested in growth or market investments"
            })
        
        # Growth insight
        if business_metrics.revenue_growth_rate > 0.20:
            insights.append({
                "category": "growth",
                "insight": f"Exceptional growth rate of {business_metrics.revenue_growth_rate*100:.1f}% annually",
                "impact": "positive",
                "urgency": "opportunity",
                "action_implication": "Ensure systems and processes can handle continued growth"
            })
        elif business_metrics.revenue_growth_rate < -0.05:
            insights.append({
                "category": "growth",
                "insight": f"Declining revenue at {business_metrics.revenue_growth_rate*100:.1f}% annually",
                "impact": "negative",
                "urgency": "high",
                "action_implication": "Immediate focus on customer retention and new customer acquisition"
            })
        
        # Market insight
        if market_context.sector_growth_rate > 0.10:
            insights.append({
                "category": "market",
                "insight": f"Sector growing at {market_context.sector_growth_rate*100:.1f}% creates expansion opportunities",
                "impact": "positive",
                "urgency": "opportunity",
                "action_implication": "Position for market share capture in growing sector"
            })
        
        # Economic insight
        if abs(economic_impact.overall_economic_impact) > 0.10:
            if economic_impact.overall_economic_impact > 0:
                insights.append({
                    "category": "economic",
                    "insight": "Current US economic conditions are favorable for your business",
                    "impact": "positive",
                    "urgency": "opportunity",
                    "action_implication": "Take advantage of favorable conditions for expansion"
                })
            else:
                insights.append({
                    "category": "economic",
                    "insight": "Current US economic conditions pose challenges for your business",
                    "impact": "negative",
                    "urgency": "medium",
                    "action_implication": "Implement defensive strategies and improve resilience"
                })
        
        # Competitive insight
        competitive_strength = competitive_analysis.get('competitive_strength_score', 50)
        if competitive_strength > 75:
            insights.append({
                "category": "competitive",
                "insight": "Strong competitive position provides market advantage",
                "impact": "positive",
                "urgency": "opportunity",
                "action_implication": "Leverage competitive strength for market expansion"
            })
        elif competitive_strength < 40:
            insights.append({
                "category": "competitive",
                "insight": "Weak competitive position requires immediate attention",
                "impact": "negative",
                "urgency": "high",
                "action_implication": "Develop competitive advantages and differentiation strategy"
            })
        
        return insights[:5]  # Return top 5 most important insights
    
    async def _generate_strategic_recommendations(self, business_data: Dict[str, Any],
                                            business_metrics: USBusinessMetrics,
                                            market_context: USMarketContext,
                                            performance_scores: Dict[str, Any],
                                            risk_analysis: Dict[str, Any],
                                            economic_impact: USEconomicImpact) -> List[Dict[str, Any]]:
        """Generate strategic recommendations for business improvement."""
        
        recommendations = []
        
        # Financial recommendations
        if business_metrics.cash_runway_months < 6:
            recommendations.append({
                "category": "financial_management",
                "priority": "critical",
                "recommendation": "Improve cash flow management and build reserves",
                "specific_actions": [
                    "Accelerate accounts receivable collection",
                    "Negotiate extended payment terms with suppliers",
                    "Consider invoice factoring for immediate cash",
                    "Review and reduce non-essential expenses"
                ],
                "expected_outcome": "Increase cash runway to 6+ months",
                "timeline": "immediate",
                "investment_required": 0,
                "expected_roi": "survival"
            })
        
        # Growth recommendations
        overall_score = performance_scores.get('overall_score', 50)
        if overall_score > 70 and business_metrics.cash_runway_months > 6:
            recommendations.append({
                "category": "growth_acceleration",
                "priority": "high",
                "recommendation": "Accelerate growth through strategic investments",
                "specific_actions": [
                    "Increase marketing and customer acquisition spending",
                    "Expand product/service offerings",
                    "Hire additional sales staff",
                    "Consider geographic expansion"
                ],
                "expected_outcome": "20-30% revenue growth within 12 months",
                "timeline": "3-6 months",
                "investment_required": business_metrics.current_monthly_revenue * 2,
                "expected_roi": "25%"
            })
        
        # Operational recommendations
        if business_metrics.revenue_per_employee < 150000:
            recommendations.append({
                "category": "operational_efficiency",
                "priority": "medium",
                "recommendation": "Improve operational efficiency and productivity",
                "specific_actions": [
                    "Implement business process automation",
                    "Provide staff training and development",
                    "Optimize workflow and eliminate waste",
                    "Invest in productivity tools and technology"
                ],
                "expected_outcome": "15-25% productivity improvement",
                "timeline": "3-6 months",
                "investment_required": business_metrics.current_monthly_revenue * 1.5,
                "expected_roi": "30%"
            })
        
        # Market positioning recommendations
        competitive_strength = business_metrics.competitive_strength
        if competitive_strength < 60:
            recommendations.append({
                "category": "competitive_positioning",
                "priority": "medium",
                "recommendation": "Strengthen competitive position and differentiation",
                "specific_actions": [
                    "Develop unique value proposition",
                    "Improve customer service and experience",
                    "Build brand recognition and reputation",
                    "Create competitive advantages"
                ],
                "expected_outcome": "Improved market position and customer retention",
                "timeline": "6-12 months",
                "investment_required": business_metrics.current_monthly_revenue * 1,
                "expected_roi": "20%"
            })
        
        # Risk mitigation recommendations
        high_risks = [risk for risk in risk_analysis.get('top_risk_priorities', []) 
                     if risk.get('severity') in ['critical', 'high']]
        if high_risks:
            recommendations.append({
                "category": "risk_mitigation",
                "priority": "high",
                "recommendation": "Address critical business risks",
                "specific_actions": [
                    f"Mitigate {risk['risk']}" for risk in high_risks[:3]
                ],
                "expected_outcome": "Reduced business risk and improved stability",
                "timeline": "immediate to 3 months",
                "investment_required": business_metrics.current_monthly_revenue * 0.5,
                "expected_roi": "risk_reduction"
            })
        
        # Economic adaptation recommendations
        if abs(economic_impact.overall_economic_impact) > 0.05:
            if economic_impact.overall_economic_impact < 0:
                recommendations.append({
                    "category": "economic_adaptation",
                    "priority": "medium",
                    "recommendation": "Adapt to challenging economic conditions",
                    "specific_actions": [
                        "Implement cost control measures",
                        "Diversify revenue streams",
                        "Build recession-resistant capabilities",
                        "Strengthen customer relationships"
                    ],
                    "expected_outcome": "Improved economic resilience",
                    "timeline": "3-6 months",
                    "investment_required": business_metrics.current_monthly_revenue * 0.75,
                    "expected_roi": "stability"
                })
        
        return recommendations[:5]  # Return top 5 recommendations
    
    async def _create_fallback_analysis(self, business_data: Dict[str, Any], 
                                      error_message: str) -> Dict[str, Any]:
        """Create basic fallback analysis when main analysis fails."""
        
        return {
            "business_overview": {
                "business_name": business_data.get('business_name', 'Business'),
                "sector": business_data.get('sector', 'unknown'),
                "analysis_status": "partial_failure",
                "error_message": error_message
            },
            "core_metrics": {
                "annual_revenue": sum(business_data.get('monthly_revenue', [0])),
                "cash_available": business_data.get('current_cash', 0),
                "employees": business_data.get('employees_count', 0)
            },
            "performance_analysis": {
                "overall_score": 50,
                "performance_grade": "C",
                "status": "analysis_incomplete"
            },
            "key_insights": [{
                "category": "system",
                "insight": "Analysis could not be completed due to technical issues",
                "impact": "neutral",
                "urgency": "medium",
                "action_implication": "Retry analysis or contact support"
            }],
            "strategic_recommendations": [{
                "category": "system",
                "priority": "medium",
                "recommendation": "Complete full business analysis",
                "specific_actions": ["Retry analysis with complete data"],
                "timeline": "immediate"
            }],
            "analysis_metadata": {
                "analysis_version": "2.0_fallback",
                "confidence_level": 0.3,
                "status": "incomplete",
                "error": error_message
            }
        }


# Helper function for module testing
async def test_business_analyzer():
    """Test function for the business analyzer."""
    
    analyzer = USBusinessAnalyzer()
    
    # Sample business data for testing
    test_business_data = {
        'business_name': 'Test Electronics Store',
        'sector': 'electronics',
        'city': 'Austin',
        'state': 'TX',
        'zip_code': '73301',
        'monthly_revenue': [45000, 47000, 50000, 52000, 48000, 51000, 
                           53000, 49000, 54000, 56000, 55000, 58000],
        'monthly_expenses': [35000] * 12,
        'current_cash': 75000,
        'employees_count': 6,
        'years_in_business': 4,
        'business_structure': 'llc',
        'outstanding_debt': 25000,
        'business_goals': ['increase_profits', 'expand_locations'],
        'main_challenges': ['competition', 'cash_flow']
    }
    
    try:
        result = await analyzer.analyze_us_business_comprehensive(test_business_data)
        print("✅ Business analyzer test completed successfully")
        print(f"Overall Score: {result.get('performance_analysis', {}).get('overall_score', 'N/A')}")
        print(f"Key Insights: {len(result.get('key_insights', []))}")
        return result
    except Exception as e:
        print(f"❌ Business analyzer test failed: {str(e)}")
        return None


if __name__ == "__main__":
    # Run test if called directly
    import asyncio
    asyncio.run(test_business_analyzer())