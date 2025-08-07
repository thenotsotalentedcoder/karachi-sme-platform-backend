"""US Investment Advisory Engine for Small Business Owners."""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import json
from dataclasses import dataclass
from enum import Enum

from app.core.multi_gemini_engine import MultiGeminiEngine
from app.services.fred_service import FREDService
from app.services.alpha_vantage_service import AlphaVantageService
from app.data.us_economic_factors import (
    get_current_us_economic_indicators,
    calculate_us_economic_impact,
    project_us_economic_trends,
    calculate_sector_resilience_score,
    get_regional_adjustment_factors
)
from app.config import settings

logger = logging.getLogger(__name__)


class RiskProfile(Enum):
    """Investment risk profiles for US small business owners."""
    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"


class InvestmentCategory(Enum):
    """Investment categories for portfolio allocation."""
    BUSINESS_REINVESTMENT = "business_reinvestment"
    EMERGENCY_FUND = "emergency_fund"
    MARKET_INVESTMENTS = "market_investments"
    RETIREMENT_ACCOUNTS = "retirement_accounts"
    TAX_OPTIMIZATION = "tax_optimization"
    ALTERNATIVE_INVESTMENTS = "alternative_investments"


@dataclass
class InvestmentCapacity:
    """Investment capacity analysis for business owner."""
    total_available_capital: float
    emergency_fund_requirement: float
    investment_ready_capital: float
    monthly_investment_capacity: float
    debt_capacity: float
    risk_profile: RiskProfile
    liquidity_needs: Dict[str, float]


@dataclass
class AssetAllocation:
    """Recommended asset allocation strategy."""
    business_reinvestment: float
    emergency_cash: float
    growth_investments: float
    income_investments: float
    alternative_investments: float
    international_exposure: float
    sector_specific: float


@dataclass
class InvestmentRecommendation:
    """Individual investment recommendation."""
    investment_type: str
    specific_recommendation: str
    allocation_amount: float
    expected_annual_return: float
    risk_level: str
    time_horizon: str
    liquidity: str
    tax_efficiency: float
    correlation_with_business: float
    implementation_steps: List[str]
    rationale: str


class USInvestmentAdvisor:
    """Comprehensive US investment advisory engine for small business owners."""
    
    def __init__(self):
        self.gemini_engine = MultiGeminiEngine()
        self.fred_service = FREDService()
        self.alpha_vantage_service = AlphaVantageService()
        
        # US investment universe
        self.investment_options = {
            "equity_etfs": {
                "SPY": {"name": "S&P 500", "expense_ratio": 0.0945, "risk": "moderate"},
                "VTI": {"name": "Total Stock Market", "expense_ratio": 0.03, "risk": "moderate"},
                "QQQ": {"name": "NASDAQ 100", "expense_ratio": 0.20, "risk": "aggressive"},
                "IWM": {"name": "Russell 2000 Small Cap", "expense_ratio": 0.19, "risk": "aggressive"},
                "VEA": {"name": "Developed International", "expense_ratio": 0.05, "risk": "moderate"},
                "VWO": {"name": "Emerging Markets", "expense_ratio": 0.10, "risk": "aggressive"}
            },
            "bond_etfs": {
                "BND": {"name": "Total Bond Market", "expense_ratio": 0.03, "risk": "conservative"},
                "TLT": {"name": "20+ Year Treasury", "expense_ratio": 0.15, "risk": "moderate"},
                "TIPS": {"name": "Inflation-Protected Securities", "expense_ratio": 0.19, "risk": "conservative"},
                "HYG": {"name": "High Yield Corporate", "expense_ratio": 0.49, "risk": "moderate"}
            },
            "sector_etfs": {
                "XLK": {"name": "Technology", "expense_ratio": 0.10, "risk": "aggressive"},
                "XLV": {"name": "Healthcare", "expense_ratio": 0.10, "risk": "moderate"},
                "XLF": {"name": "Financial", "expense_ratio": 0.10, "risk": "moderate"},
                "XLE": {"name": "Energy", "expense_ratio": 0.10, "risk": "aggressive"},
                "XLRE": {"name": "Real Estate", "expense_ratio": 0.10, "risk": "moderate"}
            },
            "retirement_accounts": {
                "SEP_IRA": {"contribution_limit": 66000, "tax_benefit": "deductible"},
                "Solo_401k": {"contribution_limit": 66000, "tax_benefit": "deductible"},
                "Traditional_IRA": {"contribution_limit": 6500, "tax_benefit": "deductible"},
                "Roth_IRA": {"contribution_limit": 6500, "tax_benefit": "tax_free_growth"},
                "Simple_IRA": {"contribution_limit": 16000, "tax_benefit": "deductible"}
            }
        }
        
        # US tax brackets and considerations
        self.tax_considerations = {
            "federal_brackets": {
                "10%": (0, 11000),
                "12%": (11001, 44725),
                "22%": (44726, 95375),
                "24%": (95376, 182050),
                "32%": (182051, 231250),
                "35%": (231251, 578125),
                "37%": (578126, float('inf'))
            },
            "capital_gains": {
                "short_term": "ordinary_income",
                "long_term_0%": (0, 44625),
                "long_term_15%": (44626, 492300),
                "long_term_20%": (492301, float('inf'))
            }
        }
    
    async def analyze_investment_opportunities(self, business_data: Dict[str, Any],
                                             economic_data: Dict[str, Any] = None,
                                             market_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Comprehensive investment analysis for US small business owner.
        
        Args:
            business_data: US business financial and operational data
            economic_data: Current US economic conditions
            market_data: US market conditions and performance
            
        Returns:
            Complete investment advisory report
        """
        
        logger.info(f"Starting investment analysis for {business_data.get('business_name', 'US Business')}")
        
        # Get current market data if not provided
        if economic_data is None:
            economic_data = get_current_us_economic_indicators()
            
        if market_data is None:
            market_data = await self._get_current_market_data()
        
        # Parallel analysis tasks
        analysis_tasks = [
            self._analyze_investment_capacity(business_data, economic_data),
            self._determine_risk_profile(business_data, economic_data),
            self._generate_asset_allocation(business_data, economic_data, market_data),
            self._analyze_business_reinvestment_opportunities(business_data, economic_data),
            self._analyze_market_investment_opportunities(business_data, economic_data, market_data),
            self._analyze_retirement_planning(business_data, economic_data),
            self._analyze_tax_optimization_strategies(business_data, economic_data),
            self._analyze_risk_hedging_strategies(business_data, economic_data, market_data)
        ]
        
        # Execute all analyses
        results = await asyncio.gather(*analysis_tasks, return_exceptions=True)
        
        # Process results
        analysis_components = {}
        component_names = [
            "investment_capacity", "risk_profile", "asset_allocation", 
            "business_reinvestment", "market_investments", "retirement_planning",
            "tax_optimization", "risk_hedging"
        ]
        
        for i, result in enumerate(results):
            component_name = component_names[i]
            if isinstance(result, Exception):
                logger.error(f"Investment analysis component {component_name} failed: {str(result)}")
                analysis_components[component_name] = {"error": str(result), "status": "failed"}
            else:
                analysis_components[component_name] = result
        
        # Generate comprehensive investment recommendations using AI
        investment_recommendations = await self._generate_ai_investment_recommendations(
            business_data, economic_data, market_data, analysis_components
        )
        
        # Create final investment advisory report
        investment_report = {
            "investment_capacity_analysis": analysis_components.get("investment_capacity", {}),
            "risk_profile_assessment": analysis_components.get("risk_profile", {}),
            "recommended_asset_allocation": analysis_components.get("asset_allocation", {}),
            "business_reinvestment_opportunities": analysis_components.get("business_reinvestment", {}),
            "market_investment_recommendations": analysis_components.get("market_investments", {}),
            "retirement_wealth_building": analysis_components.get("retirement_planning", {}),
            "tax_optimization_strategies": analysis_components.get("tax_optimization", {}),
            "risk_hedging_strategies": analysis_components.get("risk_hedging", {}),
            "ai_investment_recommendations": investment_recommendations,
            "implementation_roadmap": self._create_implementation_roadmap(analysis_components),
            "monitoring_framework": self._create_monitoring_framework(business_data, analysis_components),
            "analysis_metadata": {
                "analysis_timestamp": datetime.now().isoformat(),
                "economic_context": self._summarize_economic_context(economic_data),
                "market_context": self._summarize_market_context(market_data),
                "confidence_level": self._calculate_overall_confidence(analysis_components)
            }
        }
        
        logger.info("Investment analysis completed successfully")
        return investment_report
    
    async def _analyze_investment_capacity(self, business_data: Dict[str, Any],
                                         economic_data: Dict[str, Any]) -> InvestmentCapacity:
        """Analyze business owner's investment capacity."""
        
        # Financial metrics
        monthly_revenue = business_data.get('monthly_revenue', [])
        current_revenue = monthly_revenue[-1] if monthly_revenue else 0
        monthly_expenses = business_data.get('monthly_expenses', 0)
        current_cash = business_data.get('current_cash', 0)
        outstanding_debt = business_data.get('outstanding_debt', 0)
        business_assets = business_data.get('business_assets', 0)
        
        # Calculate monthly cash flow
        monthly_cash_flow = current_revenue - monthly_expenses
        annual_cash_flow = monthly_cash_flow * 12
        
        # Emergency fund requirement (3-6 months expenses)
        emergency_fund_requirement = monthly_expenses * 4  # 4 months conservative
        
        # Available investment capital
        available_cash = max(0, current_cash - emergency_fund_requirement)
        monthly_investment_capacity = max(0, monthly_cash_flow * 0.2)  # 20% of cash flow
        
        # Total investable assets (including business equity)
        business_equity = max(0, business_assets - outstanding_debt)
        total_investable_assets = available_cash + business_equity * 0.1  # 10% of business equity
        
        # Debt capacity analysis
        debt_to_income_ratio = outstanding_debt / max(1, annual_cash_flow)
        additional_debt_capacity = 0
        if debt_to_income_ratio < 0.3:  # Conservative 30% debt-to-income
            additional_debt_capacity = (annual_cash_flow * 0.3) - outstanding_debt
        
        # Risk profile assessment
        years_in_business = business_data.get('years_in_business', 0)
        revenue_volatility = self._calculate_revenue_volatility(monthly_revenue)
        
        if years_in_business < 3 or revenue_volatility > 0.3 or monthly_cash_flow < 0:
            risk_profile = RiskProfile.CONSERVATIVE
        elif years_in_business > 10 and revenue_volatility < 0.15 and monthly_cash_flow > monthly_expenses * 0.2:
            risk_profile = RiskProfile.AGGRESSIVE
        else:
            risk_profile = RiskProfile.MODERATE
        
        # Liquidity needs analysis
        liquidity_needs = {
            "immediate_access": emergency_fund_requirement,
            "short_term_needs": monthly_expenses * 2,
            "seasonal_adjustments": self._calculate_seasonal_liquidity_needs(business_data),
            "growth_capital_reserve": monthly_expenses * 1
        }
        
        return InvestmentCapacity(
            total_available_capital=total_investable_assets,
            emergency_fund_requirement=emergency_fund_requirement,
            investment_ready_capital=available_cash,
            monthly_investment_capacity=monthly_investment_capacity,
            debt_capacity=max(0, additional_debt_capacity),
            risk_profile=risk_profile,
            liquidity_needs=liquidity_needs
        )
    
    async def _determine_risk_profile(self, business_data: Dict[str, Any],
                                    economic_data: Dict[str, Any]) -> Dict[str, Any]:
        """Determine comprehensive risk profile for investment strategy."""
        
        # Business stability factors
        years_in_business = business_data.get('years_in_business', 0)
        revenue_data = business_data.get('monthly_revenue', [])
        revenue_volatility = self._calculate_revenue_volatility(revenue_data)
        monthly_cash_flow = (revenue_data[-1] if revenue_data else 0) - business_data.get('monthly_expenses', 0)
        
        # Sector resilience
        sector = business_data.get('sector', 'professional_services')
        sector_resilience = calculate_sector_resilience_score(sector)
        
        # Economic environment assessment
        fed_rate = economic_data.get('fed_funds_rate', 5.0)
        economic_uncertainty = self._assess_economic_uncertainty(economic_data)
        
        # Risk scoring (0-100, higher = more risk tolerance)
        risk_score = 50  # Baseline
        
        # Business maturity factor (+/-20)
        if years_in_business >= 10:
            risk_score += 20
        elif years_in_business >= 5:
            risk_score += 10
        elif years_in_business < 3:
            risk_score -= 15
        
        # Cash flow stability factor (+/-25)
        if monthly_cash_flow > business_data.get('monthly_expenses', 0) * 0.3:
            risk_score += 25
        elif monthly_cash_flow > 0:
            risk_score += 10
        else:
            risk_score -= 25
        
        # Revenue volatility factor (+/-20)
        if revenue_volatility < 0.10:
            risk_score += 20
        elif revenue_volatility < 0.20:
            risk_score += 10
        elif revenue_volatility > 0.40:
            risk_score -= 20
        
        # Sector resilience factor (+/-15)
        risk_score += (sector_resilience['resilience_score'] - 0.5) * 30
        
        # Economic uncertainty factor (+/-10)
        risk_score -= economic_uncertainty * 10
        
        # Determine final risk profile
        risk_score = max(0, min(100, risk_score))
        
        if risk_score >= 75:
            risk_profile = RiskProfile.AGGRESSIVE
            risk_description = "High risk tolerance suitable for growth-focused investments"
        elif risk_score >= 45:
            risk_profile = RiskProfile.MODERATE
            risk_description = "Balanced approach mixing growth and stability"
        else:
            risk_profile = RiskProfile.CONSERVATIVE
            risk_description = "Conservative approach prioritizing capital preservation"
        
        return {
            "risk_profile": risk_profile.value,
            "risk_score": risk_score,
            "risk_description": risk_description,
            "risk_factors": {
                "business_maturity": years_in_business,
                "cash_flow_stability": monthly_cash_flow,
                "revenue_volatility": revenue_volatility,
                "sector_resilience": sector_resilience['resilience_score'],
                "economic_uncertainty": economic_uncertainty
            },
            "investment_constraints": {
                "liquidity_requirements": "high" if monthly_cash_flow < 0 else "moderate",
                "time_horizon": "long" if years_in_business > 5 else "medium",
                "loss_tolerance": risk_profile.value,
                "complexity_tolerance": "high" if years_in_business > 10 else "medium"
            }
        }
    
    async def _generate_asset_allocation(self, business_data: Dict[str, Any],
                                       economic_data: Dict[str, Any],
                                       market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate optimal asset allocation strategy."""
        
        # Get investment capacity and risk profile
        capacity = await self._analyze_investment_capacity(business_data, economic_data)
        risk_analysis = await self._determine_risk_profile(business_data, economic_data)
        risk_profile = RiskProfile(risk_analysis['risk_profile'])
        
        # Base allocation templates by risk profile
        allocation_templates = {
            RiskProfile.CONSERVATIVE: {
                "business_reinvestment": 0.30,
                "emergency_cash": 0.25,
                "growth_investments": 0.20,
                "income_investments": 0.20,
                "alternative_investments": 0.05,
                "international_exposure": 0.00
            },
            RiskProfile.MODERATE: {
                "business_reinvestment": 0.35,
                "emergency_cash": 0.15,
                "growth_investments": 0.30,
                "income_investments": 0.15,
                "alternative_investments": 0.05,
                "international_exposure": 0.00
            },
            RiskProfile.AGGRESSIVE: {
                "business_reinvestment": 0.40,
                "emergency_cash": 0.10,
                "growth_investments": 0.35,
                "income_investments": 0.05,
                "alternative_investments": 0.10,
                "international_exposure": 0.00
            }
        }
        
        base_allocation = allocation_templates[risk_profile]
        
        # Adjust allocation based on economic environment
        fed_rate = economic_data.get('fed_funds_rate', 5.0)
        inflation_rate = economic_data.get('inflation_rate', 3.0)
        
        # High interest rate environment - increase income investments
        if fed_rate > 5.5:
            base_allocation["income_investments"] += 0.05
            base_allocation["growth_investments"] -= 0.05
        
        # High inflation environment - increase real assets
        if inflation_rate > 4.0:
            base_allocation["alternative_investments"] += 0.05
            base_allocation["income_investments"] -= 0.05
        
        # Sector-specific adjustments
        sector = business_data.get('sector', 'professional_services')
        sector_correlation = self._get_sector_correlation(sector)
        
        # Reduce correlation with business sector
        if sector_correlation > 0.7:
            base_allocation["international_exposure"] += 0.05
            base_allocation["growth_investments"] -= 0.05
        
        # Calculate dollar allocations
        total_investment_capital = capacity.investment_ready_capital
        
        dollar_allocation = {}
        for category, percentage in base_allocation.items():
            dollar_allocation[category] = total_investment_capital * percentage
        
        # Generate specific allocation recommendations
        specific_allocations = await self._generate_specific_allocations(
            dollar_allocation, risk_profile, economic_data, market_data
        )
        
        return {
            "recommended_allocation": {
                "percentages": base_allocation,
                "dollar_amounts": dollar_allocation,
                "total_investment_capital": total_investment_capital
            },
            "specific_allocations": specific_allocations,
            "allocation_rationale": self._generate_allocation_rationale(
                risk_profile, economic_data, base_allocation
            ),
            "rebalancing_strategy": {
                "frequency": "quarterly",
                "threshold": 5.0,  # Rebalance when allocation drifts >5%
                "tax_considerations": "prioritize_tax_advantaged_accounts",
                "monitoring_metrics": ["asset_drift", "correlation_changes", "economic_shifts"]
            },
            "risk_metrics": {
                "expected_annual_return": self._calculate_expected_return(base_allocation, market_data),
                "expected_volatility": self._calculate_expected_volatility(base_allocation),
                "maximum_drawdown_estimate": self._calculate_max_drawdown(base_allocation, risk_profile),
                "correlation_with_business": sector_correlation
            }
        }
    
    async def _analyze_business_reinvestment_opportunities(self, business_data: Dict[str, Any],
                                                         economic_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze business reinvestment opportunities."""
        
        sector = business_data.get('sector', 'professional_services')
        current_revenue = business_data.get('monthly_revenue', [0])[-1] * 12  # Annualized
        employees = business_data.get('employees_count', 0)
        years_in_business = business_data.get('years_in_business', 0)
        
        # Generate AI-powered business reinvestment analysis
        prompt = f"""
        EXPERT US BUSINESS INVESTMENT ADVISOR:
        
        Analyze business reinvestment opportunities for this US small business.
        
        BUSINESS PROFILE:
        - Sector: {sector}
        - Annual Revenue: ${current_revenue:,.0f}
        - Employees: {employees}
        - Years Operating: {years_in_business}
        - Current Economic Environment: Fed Rate {economic_data.get('fed_funds_rate', 5.0)}%
        
        PROVIDE BUSINESS REINVESTMENT ANALYSIS IN JSON:
        {{
            "high_roi_opportunities": [
                {{
                    "investment_type": "<equipment/technology/marketing/expansion/inventory>",
                    "specific_opportunity": "<detailed description>",
                    "investment_amount": <dollar amount>,
                    "expected_annual_roi": <percentage>,
                    "payback_period_months": <months>,
                    "strategic_value_score": <1-10>,
                    "implementation_complexity": "<low/medium/high>",
                    "competitive_advantage": "<advantage gained>",
                    "scalability_impact": "<how this enables scaling>",
                    "rationale": "<why this investment makes sense now>"
                }}
            ],
            "technology_investments": [
                {{
                    "technology_type": "<automation/software/equipment/systems>",
                    "investment_amount": <dollar amount>,
                    "efficiency_gain": <percentage>,
                    "cost_savings": <annual dollar savings>,
                    "revenue_impact": <annual revenue increase>,
                    "implementation_timeline": "<months>"
                }}
            ],
            "marketing_investments": [
                {{
                    "marketing_channel": "<digital/traditional/content/social>",
                    "investment_amount": <dollar amount>,
                    "expected_customer_acquisition": <number of new customers>,
                    "customer_acquisition_cost": <cost per customer>,
                    "lifetime_value_impact": <dollar amount>,
                    "brand_building_value": <1-10 score>
                }}
            ],
            "operational_improvements": [
                {{
                    "improvement_area": "<processes/systems/facilities/supply_chain>",
                    "investment_amount": <dollar amount>,
                    "efficiency_improvement": <percentage>,
                    "cost_reduction": <annual dollar savings>,
                    "quality_improvement": <1-10 score>,
                    "employee_satisfaction_impact": "<positive/neutral/negative>"
                }}
            ],
            "expansion_opportunities": [
                {{
                    "expansion_type": "<geographic/product_line/service_offering/market_segment>",
                    "investment_amount": <dollar amount>,
                    "market_size_opportunity": <dollar amount>,
                    "timeline_to_profitability": "<months>",
                    "risk_level": "<low/medium/high>",
                    "cannibalization_risk": <percentage>
                }}
            ],
            "overall_reinvestment_strategy": {{
                "recommended_annual_reinvestment": <dollar amount>,
                "reinvestment_rate": <percentage of revenue>,
                "priority_sequence": ["<priority 1>", "<priority 2>", "<priority 3>"],
                "funding_strategy": "<cash/financing/phased>",
                "success_metrics": ["<metric 1>", "<metric 2>", "<metric 3>"]
            }}
        }}
        
        Focus on specific, implementable opportunities with clear ROI calculations.
        """
        
        return await self.gemini_engine._make_gemini_request(
            self.gemini_engine.get_optimal_key("investment_advice"), 
            prompt, 
            "business_reinvestment"
        )
    
    async def _analyze_market_investment_opportunities(self, business_data: Dict[str, Any],
                                                     economic_data: Dict[str, Any],
                                                     market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze market investment opportunities."""
        
        # Get current market conditions
        market_sentiment = market_data.get('market_sentiment', 'neutral')
        sp500_performance = market_data.get('sp500', {})
        sector_performance = market_data.get('sector_performance', {})
        
        # Business context
        sector = business_data.get('sector', 'professional_services')
        investment_capacity = (await self._analyze_investment_capacity(business_data, economic_data)).investment_ready_capital
        risk_profile = (await self._determine_risk_profile(business_data, economic_data))['risk_profile']
        
        # Generate AI-powered market investment analysis
        prompt = f"""
        EXPERT US MARKET INVESTMENT ADVISOR:
        
        Analyze market investment opportunities for this US small business owner.
        
        INVESTOR PROFILE:
        - Available Investment Capital: ${investment_capacity:,.0f}
        - Risk Profile: {risk_profile}
        - Business Sector: {sector}
        - Investment Time Horizon: Medium to Long-term (5+ years)
        
        CURRENT MARKET CONDITIONS:
        - Market Sentiment: {market_sentiment}
        - S&P 500 Recent Performance: {sp500_performance.get('change_percent', 'N/A')}
        - Federal Funds Rate: {economic_data.get('fed_funds_rate', 'N/A')}%
        - Inflation Rate: {economic_data.get('inflation_rate', 'N/A')}%
        
        PROVIDE MARKET INVESTMENT RECOMMENDATIONS IN JSON:
        {{
            "equity_investments": [
                {{
                    "investment_vehicle": "<ETF/mutual_fund/individual_stocks>",
                    "specific_recommendation": "<ticker symbol and name>",
                    "allocation_amount": <dollar amount>,
                    "expected_annual_return": <percentage>,
                    "risk_level": "<low/medium/high>",
                    "expense_ratio": <percentage>,
                    "diversification_benefit": <1-10 score>,
                    "correlation_with_business": <-1 to 1>,
                    "dividend_yield": <percentage>,
                    "rationale": "<investment thesis>"
                }}
            ],
            "fixed_income_investments": [
                {{
                    "bond_type": "<treasury/corporate/municipal/tips>",
                    "specific_recommendation": "<bond fund or security>",
                    "allocation_amount": <dollar amount>,
                    "current_yield": <percentage>,
                    "duration": <years>,
                    "credit_quality": "<AAA/AA/A/BBB>",
                    "interest_rate_sensitivity": "<high/medium/low>",
                    "tax_efficiency": "<taxable/tax_free/tax_deferred>",
                    "inflation_protection": <true/false>
                }}
            ],
            "sector_rotation_strategy": [
                {{
                    "sector": "<technology/healthcare/finance/energy/utilities>",
                    "allocation_percentage": <percentage>,
                    "current_outlook": "<positive/neutral/negative>",
                    "economic_drivers": ["<driver 1>", "<driver 2>"],
                    "recommended_etf": "<ticker symbol>",
                    "timing_consideration": "<buy/hold/avoid>"
                }}
            ],
            "international_diversification": [
                {{
                    "geographic_exposure": "<developed_international/emerging_markets/specific_country>",
                    "allocation_amount": <dollar amount>,
                    "currency_hedge": <true/false>,
                    "regional_advantages": ["<advantage 1>", "<advantage 2>"],
                    "correlation_benefit": <correlation coefficient>,
                    "recommended_vehicle": "<ETF ticker and name>"
                }}
            ],
            "alternative_investments": [
                {{
                    "asset_class": "<REITs/commodities/precious_metals/crypto>",
                    "allocation_amount": <dollar amount>,
                    "portfolio_role": "<diversification/inflation_hedge/growth>",
                    "liquidity_profile": "<high/medium/low>",
                    "minimum_investment": <dollar amount>,
                    "expected_correlation": <correlation with traditional assets>,
                    "risk_considerations": ["<risk 1>", "<risk 2>"]
                }}
            ],
            "tax_advantaged_strategies": [
                {{
                    "strategy_type": "<401k/IRA/HSA/529>",
                    "contribution_recommendation": <dollar amount>,
                    "tax_benefit": "<deduction/tax_free_growth/both>",
                    "investment_options": ["<option 1>", "<option 2>"],
                    "employer_match_opportunity": <dollar amount if applicable>,
                    "age_based_considerations": "<strategy adjustments>"
                }}
            ],
            "market_timing_considerations": {{
                "current_market_phase": "<bull/bear/sideways/volatile>",
                "dollar_cost_averaging_strategy": "<lump_sum/monthly/quarterly>",
                "entry_point_analysis": "<good_time/wait/start_small>",
                "volatility_opportunity": "<high_volatility_advantage>",
                "fed_policy_impact": "<positive/negative/neutral>",
                "seasonal_considerations": ["<factor 1>", "<factor 2>"]
            }},
            "portfolio_construction": {{
                "core_holdings": ["<holding 1>", "<holding 2>", "<holding 3>"],
                "satellite_holdings": ["<holding 1>", "<holding 2>"],
                "rebalancing_frequency": "<monthly/quarterly/semi_annual>",
                "tax_loss_harvesting": <true/false>,
                "asset_location_optimization": "<tax_efficient_placement>"
            }}
        }}
        
        Provide specific, actionable investment recommendations with ticker symbols where appropriate.
        """
        
        return await self.gemini_engine._make_gemini_request(
            self.gemini_engine.get_optimal_key("investment_advice"), 
            prompt, 
            "market_investments"
        )
    
    async def _analyze_retirement_planning(self, business_data: Dict[str, Any],
                                        economic_data: Dict[str, Any]) -> Dict[str, Any]:
       """Analyze retirement planning strategies for business owner."""
       
       annual_revenue = sum(business_data.get('monthly_revenue', [0] * 12))
       monthly_expenses = business_data.get('monthly_expenses', 0)
       annual_expenses = monthly_expenses * 12
       net_income = annual_revenue - annual_expenses
       years_in_business = business_data.get('years_in_business', 0)
       employees = business_data.get('employees_count', 0)
       
       # Estimate business owner's age (rough estimate based on business years)
       estimated_age = min(65, 30 + years_in_business)
       years_to_retirement = max(0, 65 - estimated_age)
       
       prompt = f"""
       EXPERT US RETIREMENT PLANNING ADVISOR:
       
       Create comprehensive retirement strategy for this US small business owner.
       
       OWNER PROFILE:
       - Estimated Age: {estimated_age} years
       - Years to Retirement: {years_to_retirement}
       - Annual Business Income: ${net_income:,.0f}
       - Employees: {employees}
       - Business Sector: {business_data.get('sector', 'N/A')}
       
       CURRENT ECONOMIC ENVIRONMENT:
       - Fed Funds Rate: {economic_data.get('fed_funds_rate', 5.0)}%
       - Inflation Rate: {economic_data.get('inflation_rate', 3.0)}%
       - Social Security Future: Uncertain funding
       
       PROVIDE RETIREMENT PLANNING ANALYSIS IN JSON:
       {{
           "retirement_account_recommendations": [
               {{
                   "account_type": "<SEP_IRA/Solo_401k/Simple_IRA/Traditional_IRA/Roth_IRA>",
                   "annual_contribution_limit": <2024 limit>,
                   "recommended_annual_contribution": <dollar amount>,
                   "tax_benefit": "<immediate_deduction/tax_free_growth/both>",
                   "catch_up_contributions": <additional amount if over 50>,
                   "investment_strategy": "<aggressive/moderate/conservative>",
                   "employer_match_potential": <dollar amount if applicable>,
                   "administrative_complexity": "<low/medium/high>",
                   "rationale": "<why this account type>"
               }}
           ],
           "retirement_savings_targets": {{
               "target_retirement_savings": <total amount needed>,
               "monthly_savings_required": <monthly contribution needed>,
               "replacement_income_ratio": <percentage of current income>,
               "retirement_lifestyle_assumption": "<maintain_current/modest/luxury>",
               "healthcare_cost_estimate": <annual healthcare costs>,
               "longevity_planning": <years of retirement funding>
           }},
           "business_succession_planning": {{
               "business_value_estimate": <current business value>,
               "succession_strategy": "<family/employee/third_party_sale>",
               "timeline_preparation": "<years needed to prepare>",
               "value_enhancement_opportunities": ["<opportunity 1>", "<opportunity 2>"],
               "tax_optimization_strategies": ["<strategy 1>", "<strategy 2>"],
               "professional_help_needed": ["<advisor_type 1>", "<advisor_type 2>"]
           }},
           "social_security_optimization": {{
               "estimated_social_security_benefit": <monthly benefit>,
               "optimal_claiming_strategy": "<age_62/full_retirement_age/age_70>",
               "spousal_benefits_consideration": <if applicable>,
               "tax_implications": "<percentage_taxable>",
               "integration_with_savings": "<strategy>"
           }},
           "healthcare_retirement_planning": {{
               "medicare_preparation": {{
                   "parts_coverage": ["<Part A/B/C/D>"],
                   "supplemental_insurance": "<medigap/advantage>",
                   "estimated_monthly_cost": <dollar amount>
               }},
               "health_savings_account": {{
                   "hsa_eligibility": <true/false>,
                   "contribution_strategy": "<max_out/moderate/minimal>",
                   "triple_tax_advantage": "<explanation>",
                   "retirement_healthcare_fund": <target amount>
               }}
           }},
           "estate_planning_integration": {{
               "estate_tax_considerations": <estimated estate value>,
               "wealth_transfer_strategies": ["<strategy 1>", "<strategy 2>"],
               "business_asset_protection": "<trust/LLC/other_structure>",
               "charitable_giving_opportunities": ["<opportunity 1>", "<opportunity 2>"],
               "document_updates_needed": ["<document 1>", "<document 2>"]
           }},
           "retirement_income_strategies": {{
               "withdrawal_strategy": "<4_percent_rule/bucket_strategy/bond_ladder>",
               "tax_efficient_withdrawals": "<account_sequencing>",
               "required_minimum_distributions": "<RMD_planning>",
               "inflation_adjustment_mechanism": "<strategy>",
               "contingency_planning": ["<scenario 1>", "<scenario 2>"]
           }},
           "catch_up_strategies": {{
               "behind_on_savings": <true/false>,
               "accelerated_savings_options": ["<option 1>", "<option 2>"],
               "late_career_optimization": ["<strategy 1>", "<strategy 2>"],
               "working_in_retirement": "<part_time/consulting/passive_income>"
           }}
       }}
       
       Focus on practical, implementable retirement strategies for US small business owners.
       """
       
       return await self.gemini_engine._make_gemini_request(
           self.gemini_engine.get_optimal_key("investment_advice"), 
           prompt, 
           "retirement_planning"
       )
   
    async def _analyze_tax_optimization_strategies(self, business_data: Dict[str, Any],
                                                 economic_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze tax optimization investment strategies."""

        annual_revenue = sum(business_data.get('monthly_revenue', [0] * 12))
        business_structure = business_data.get('business_structure', 'llc')
        sector = business_data.get('sector', 'professional_services')
        state = business_data.get('state', 'TX')

        prompt = f"""
        EXPERT US TAX OPTIMIZATION ADVISOR:

        Analyze tax-efficient investment strategies for this US small business.

        BUSINESS TAX PROFILE:
        - Annual Revenue: ${annual_revenue:,.0f}
        - Business Structure: {business_structure}
        - Sector: {sector}
        - State: {state}
        - Current Tax Environment: 2024 US tax code

        PROVIDE TAX OPTIMIZATION ANALYSIS IN JSON:
        {{
            "business_tax_strategies": [
                {{
                    "strategy": "<specific tax strategy>",
                    "description": "<detailed implementation>",
                    "annual_tax_savings": <dollar amount>,
                    "implementation_complexity": "<low/medium/high>",
                    "audit_risk_level": "<low/medium/high>",
                    "professional_help_required": "<CPA/tax_attorney/financial_planner>",
                    "timing_considerations": "<year_end/quarterly/ongoing>",
                    "eligibility_requirements": ["<requirement 1>", "<requirement 2>"]
                }}
            ],
            "retirement_account_tax_benefits": [
                {{
                    "account_type": "<SEP_IRA/Solo_401k/etc>",
                    "current_year_deduction": <dollar amount>,
                    "lifetime_tax_savings": <estimated amount>,
                    "tax_deferral_value": <present value of deferral>,
                    "roth_conversion_opportunities": <dollar amount>,
                    "required_minimum_distribution_impact": "<strategy>"
                }}
            ],
            "investment_tax_efficiency": [
                {{
                    "investment_type": "<municipal_bonds/index_funds/tax_managed_funds>",
                    "tax_advantage": "<tax_free/tax_deferred/tax_efficient>",
                    "after_tax_return_improvement": <percentage points>,
                    "tax_drag_reduction": <percentage>,
                    "asset_location_optimization": "<taxable/tax_deferred/tax_free_account>",
                    "suitability_score": <1-10>
                }}
            ],
            "business_investment_deductions": [
                {{
                    "deduction_category": "<equipment/software/training/marketing>",
                    "section_179_eligibility": <dollar amount>,
                    "bonus_depreciation": <percentage and dollar amount>,
                    "timing_strategy": "<current_year/future_year>",
                    "documentation_requirements": ["<requirement 1>", "<requirement 2>"],
                    "tax_savings": <dollar amount>
                }}
            ],
            "estate_tax_planning": [
                {{
                    "strategy": "<gifting/trust/valuation_discount>",
                    "current_exemption_usage": <dollar amount>,
                    "lifetime_exemption_remaining": <dollar amount>,
                    "generation_skipping_considerations": <true/false>,
                    "state_estate_tax_impact": "<strategy>",
                    "implementation_timeline": "<immediate/1_year/2_years>"
                }}
            ],
            "charitable_giving_strategies": [
                {{
                    "giving_vehicle": "<donor_advised_fund/charitable_remainder_trust/direct_giving>",
                    "tax_deduction_value": <dollar amount>,
                    "income_tax_savings": <annual savings>,
                    "estate_tax_savings": <estimated savings>,
                    "control_and_flexibility": "<high/medium/low>",
                    "minimum_gift_amount": <dollar amount>
                }}
            ],
            "state_tax_considerations": {{
                "state_income_tax_rate": <percentage>,
                "state_specific_strategies": ["<strategy 1>", "<strategy 2>"],
                "multi_state_planning": <true/false>,
                "relocating_tax_benefits": "<potential_savings>",
                "state_retirement_account_treatment": "<favorable/neutral/unfavorable>"
            }},
            "tax_loss_harvesting": {{
                "annual_opportunity": <estimated dollar benefit>,
                "wash_sale_rule_compliance": "<strategy>",
                "asset_replacement_strategy": "<specific_approach>",
                "carryforward_optimization": "<multi_year_strategy>",
                "automated_vs_manual": "<recommendation>"
            }},
            "alternative_minimum_tax": {{
                "amt_risk_assessment": "<low/medium/high>",
                "planning_strategies": ["<strategy 1>", "<strategy 2>"],
                "iso_stock_option_considerations": <if_applicable>,
                "preference_item_management": "<approach>"
            }}
        }}

        Provide specific, actionable tax strategies with quantified benefits.
        """

        return await self.gemini_engine._make_gemini_request(
            self.gemini_engine.get_optimal_key("investment_advice"), 
            prompt, 
            "tax_optimization"
        )
    
    async def _analyze_risk_hedging_strategies(self, business_data: Dict[str, Any],
                                             economic_data: Dict[str, Any],
                                             market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze risk hedging and portfolio protection strategies."""

        sector = business_data.get('sector', 'professional_services')
        annual_revenue = sum(business_data.get('monthly_revenue', [0] * 12))
        investment_capacity = (await self._analyze_investment_capacity(business_data, economic_data)).investment_ready_capital

        prompt = f"""
        EXPERT INVESTMENT RISK MANAGEMENT ADVISOR:

        Develop comprehensive risk hedging strategies for this US small business owner's portfolio.

        RISK PROFILE:
        - Business Sector: {sector}
        - Annual Revenue: ${annual_revenue:,.0f}
        - Investment Portfolio Size: ${investment_capacity:,.0f}
        - Economic Environment: Fed Rate {economic_data.get('fed_funds_rate', 5.0)}%, Inflation {economic_data.get('inflation_rate', 3.0)}%

        PROVIDE RISK HEDGING ANALYSIS IN JSON:
        {{
            "portfolio_risk_assessment": {{
                "primary_risk_factors": ["<risk_1>", "<risk_2>", "<risk_3>"],
                "correlation_with_business": <-1_to_1>,
                "concentration_risk_level": "<low/medium/high>",
                "liquidity_risk": "<low/medium/high>",
                "interest_rate_sensitivity": "<low/medium/high>",
                "inflation_sensitivity": "<low/medium/high>"
            }},
            "economic_hedging_strategies": [
                {{
                    "economic_risk": "<inflation/recession/interest_rate_spike/dollar_devaluation>",
                    "hedge_investment": "<TIPS/commodities/international_stocks/real_estate>",
                    "allocation_amount": <dollar_amount>,
                    "hedge_effectiveness": <0-100_percentage>,
                    "cost_of_hedge": <annual_cost_percentage>,
                    "correlation_coefficient": <-1_to_1>,
                    "implementation_method": "<ETF/mutual_fund/individual_securities>",
                    "rebalancing_frequency": "<monthly/quarterly/annual>"
                }}
            ],
            "sector_diversification": [
                {{
                    "diversification_benefit": "<reducing_correlation_with_business>",
                    "recommended_sectors": ["<sector_1>", "<sector_2>", "<sector_3>"],
                    "allocation_percentages": [<percentage_1>, <percentage_2>, <percentage_3>],
                    "correlation_reduction": <percentage_improvement>,
                    "geographic_diversification": ["<US_regions>", "<international_markets>"],
                    "implementation_vehicles": ["<ETF_1>", "<ETF_2>", "<ETF_3>"]
                }}
            ],
            "downside_protection_strategies": [
                {{
                    "strategy_type": "<put_options/stop_losses/defensive_assets/volatility_hedging>",
                    "protection_level": <percentage_downside_protection>,
                    "cost_of_protection": <annual_percentage_cost>,
                    "trigger_conditions": ["<condition_1>", "<condition_2>"],
                    "implementation_complexity": "<low/medium/high>",
                    "suitable_market_conditions": "<bear/volatile/uncertain>"
                }}
            ],
            "currency_risk_management": [
                {{
                    "currency_exposure": "<international_investments/business_operations>",
                    "hedging_strategy": "<currency_hedged_funds/forex_contracts/natural_hedge>",
                    "hedge_ratio": <percentage_to_hedge>,
                    "cost_benefit_analysis": "<cost_vs_risk_reduction>",
                    "dynamic_vs_static_hedging": "<recommendation>"
                }}
            ],
            "alternative_investments_for_diversification": [
                {{
                    "asset_class": "<REITs/commodities/private_equity/hedge_funds>",
                    "diversification_benefit": <correlation_improvement>,
                    "allocation_recommendation": <percentage_of_portfolio>,
                    "liquidity_profile": "<daily/monthly/quarterly/annual>",
                    "minimum_investment": <dollar_amount>,
                    "expected_return": <annual_percentage>,
                    "risk_level": "<low/medium/high>"
                }}
            ],
            "insurance_as_risk_management": [
                {{
                    "insurance_type": "<life/disability/umbrella/business_interruption>",
                    "coverage_amount": <dollar_amount>,
                    "annual_premium": <dollar_amount>,
                    "portfolio_protection_value": "<wealth_preservation_benefit>",
                    "tax_advantages": "<deductible/tax_free_benefits>",
                    "integration_with_investments": "<coordination_strategy>"
                }}
            ],
            "scenario_analysis": [
                {{
                    "scenario": "<2008_financial_crisis/COVID_pandemic/stagflation/tech_bubble>",
                    "portfolio_impact_without_hedging": <percentage_loss>,
                    "portfolio_impact_with_hedging": <percentage_loss_with_protection>,
                    "hedge_effectiveness": <percentage_protection_provided>,
                    "lessons_learned": ["<lesson_1>", "<lesson_2>"],
                    "preparation_strategies": ["<strategy_1>", "<strategy_2>"]
                }}
            ],
            "dynamic_hedging_framework": {{
                "market_indicators_to_monitor": ["<indicator_1>", "<indicator_2>", "<indicator_3>"],
                "hedge_adjustment_triggers": ["<trigger_1>", "<trigger_2>"],
                "rebalancing_rules": "<systematic_approach>",
                "stress_testing_frequency": "<monthly/quarterly>",
                "emergency_protocols": ["<protocol_1>", "<protocol_2>"]
            }}
        }}

        Focus on practical, cost-effective hedging strategies appropriate for small business owner portfolios.
        """

        return await self.gemini_engine._make_gemini_request(
            self.gemini_engine.get_optimal_key("investment_advice"), 
            prompt, 
            "risk_hedging"
        )
    
    async def _generate_ai_investment_recommendations(self, business_data: Dict[str, Any],
                                                   economic_data: Dict[str, Any],
                                                   market_data: Dict[str, Any],
                                                   analysis_components: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive AI-powered investment recommendations."""

        # Summarize all analysis components
        analysis_summary = json.dumps({k: v for k, v in analysis_components.items() if not isinstance(v, dict) or "error" not in v}, indent=2)

        business_name = business_data.get('business_name', 'US Small Business')
        sector = business_data.get('sector', 'professional_services')
        annual_revenue = sum(business_data.get('monthly_revenue', [0] * 12))

        prompt = f"""
        EXPERT US INVESTMENT ADVISOR - COMPREHENSIVE SYNTHESIS:

        Create final investment recommendations by synthesizing all analysis components.

        BUSINESS: {business_name}
        SECTOR: {sector}
        ANNUAL REVENUE: ${annual_revenue:,.0f}

        COMPLETE ANALYSIS RESULTS:
        {analysis_summary}

        CURRENT US MARKET CONDITIONS:
        - Fed Funds Rate: {economic_data.get('fed_funds_rate', 5.0)}%
        - Market Sentiment: {market_data.get('market_sentiment', 'neutral')}
        - Economic Health Score: {economic_data.get('economic_health_score', 50)}/100

        PROVIDE SYNTHESIZED INVESTMENT RECOMMENDATIONS IN JSON:
        {{
            "executive_investment_summary": {{
                "total_recommended_investment": <dollar_amount>,
                "investment_strategy_theme": "<conservative_growth/balanced_diversification/aggressive_growth>",
                "primary_investment_objective": "<wealth_preservation/income_generation/growth/tax_optimization>",
                "time_horizon": "<short_term/medium_term/long_term>",
                "key_success_factors": ["<factor_1>", "<factor_2>", "<factor_3>"],
                "overall_expected_return": <annual_percentage>,
                "risk_adjusted_return": <sharpe_ratio_estimate>
            }},
            "top_priority_investments": [
                {{
                    "priority_rank": <1-5>,
                    "investment_recommendation": "<specific_investment>",
                    "allocation_amount": <dollar_amount>,
                    "investment_vehicle": "<ETF/mutual_fund/individual_stock/bond>",
                    "ticker_symbol": "<if_applicable>",
                    "expected_annual_return": <percentage>,
                    "risk_level": "<low/medium/high>",
                    "strategic_rationale": "<why_this_is_priority>",
                    "implementation_timeline": "<immediate/1_month/3_months>",
                    "monitoring_frequency": "<weekly/monthly/quarterly>",
                    "exit_strategy": "<conditions_for_selling>"
                }}
            ],
            "portfolio_architecture": {{
                "core_holdings": [
                    {{
                        "holding_type": "<broad_market_etf/bond_fund/sector_fund>",
                        "specific_fund": "<fund_name_and_ticker>",
                        "allocation_percentage": <percentage>,
                        "role_in_portfolio": "<foundation/growth_engine/stability/diversification>",
                        "rebalancing_frequency": "<monthly/quarterly/annual>"
                    }}
                ],
                "satellite_holdings": [
                    {{
                        "holding_type": "<sector_rotation/international/alternatives>",
                        "specific_investment": "<investment_name>",
                        "allocation_percentage": <percentage>,
                        "tactical_purpose": "<opportunity/hedge/speculation>",
                        "review_frequency": "<monthly/quarterly>"
                    }}
                ],
                "tactical_opportunities": [
                    {{
                        "opportunity": "<specific_market_opportunity>",
                        "allocation_amount": <dollar_amount>,
                        "opportunity_window": "<months>",
                        "success_probability": <percentage>,
                        "risk_reward_ratio": <ratio>
                    }}
                ]
            }},
            "implementation_roadmap": {{
                "phase_1_immediate": {{
                    "timeline": "<first_30_days>",
                    "actions": ["<action_1>", "<action_2>", "<action_3>"],
                    "investment_amount": <dollar_amount>,
                    "expected_completion": "<date>"
                }},
                "phase_2_buildup": {{
                    "timeline": "<months_2_6>",
                    "actions": ["<action_1>", "<action_2>"],
                    "investment_amount": <dollar_amount>,
                    "milestones": ["<milestone_1>", "<milestone_2>"]
                }},
                "phase_3_optimization": {{
                    "timeline": "<months_6_12>",
                    "actions": ["<action_1>", "<action_2>"],
                    "investment_amount": <dollar_amount>,
                    "performance_targets": ["<target_1>", "<target_2>"]
                }}
            }},
            "risk_management_protocol": {{
                "maximum_acceptable_loss": <percentage>,
                "stop_loss_levels": ["<level_1>", "<level_2>"],
                "diversification_requirements": "<minimum_holdings_across_sectors>",
                "correlation_limits": "<maximum_correlation_between_holdings>",
                "liquidity_requirements": "<percentage_in_liquid_investments>",
                "stress_testing_scenarios": ["<scenario_1>", "<scenario_2>"]
            }},
            "tax_optimization_integration": {{
                "asset_location_strategy": "<which_investments_in_which_accounts>",
                "tax_loss_harvesting_plan": "<systematic_approach>",
                "tax_efficient_fund_selection": ["<fund_1>", "<fund_2>"],
                "retirement_account_optimization": "<contribution_and_investment_strategy>",
                "charitable_giving_integration": "<donor_advised_fund_strategy>"
            }},
            "economic_scenario_adaptations": {{
                "rising_interest_rate_strategy": "<portfolio_adjustments>",
                "recession_protection_plan": "<defensive_measures>",
                "inflation_hedge_activation": "<inflation_protection_investments>",
                "market_crash_response": "<systematic_response_plan>",
                "economic_boom_opportunity": "<growth_acceleration_strategy>"
            }},
            "performance_monitoring_framework": {{
                "key_performance_indicators": ["<kpi_1>", "<kpi_2>", "<kpi_3>"],
                "benchmark_comparisons": ["<benchmark_1>", "<benchmark_2>"],
                "review_schedule": {{
                    "daily_monitoring": ["<metric_1>", "<metric_2>"],
                    "weekly_review": ["<item_1>", "<item_2>"],
                    "monthly_analysis": ["<analysis_1>", "<analysis_2>"],
                    "quarterly_rebalancing": "<systematic_approach>"
                }},
                "decision_triggers": ["<trigger_1>", "<trigger_2>"],
                "performance_reporting": "<dashboard_and_reports>"
            }},
            "continuous_improvement_plan": {{
                "learning_objectives": ["<objective_1>", "<objective_2>"],
                "skill_development_areas": ["<area_1>", "<area_2>"],
                "professional_development": ["<resource_1>", "<resource_2>"],
                "advisory_relationships": ["<advisor_type_1>", "<advisor_type_2>"],
                "technology_tools": ["<tool_1>", "<tool_2>"]
            }}
        }}

        Ensure all recommendations are specific, actionable, and include exact dollar amounts and ticker symbols where applicable.
        """

        return await self.gemini_engine._make_gemini_request(
            self.gemini_engine.get_optimal_key("synthesis_reporting"), 
            prompt, 
            "investment_synthesis"
        )
    
    # Helper methods
    
    async def _get_current_market_data(self) -> Dict[str, Any]:
        """Get current market data from Alpha Vantage."""
        try:
            market_overview = await self.alpha_vantage_service.get_market_overview()
            return market_overview
        except Exception as e:
            logger.error(f"Failed to get market data: {str(e)}")
            return {"error": str(e), "market_sentiment": "neutral"}
    
    def _calculate_revenue_volatility(self, revenue_data: List[float]) -> float:
        """Calculate revenue volatility coefficient."""
        if not revenue_data or len(revenue_data) < 2:
            return 0.0

        mean_revenue = sum(revenue_data) / len(revenue_data)
        if mean_revenue == 0:
            return 0.0

        variance = sum((x - mean_revenue) ** 2 for x in revenue_data) / len(revenue_data)
        std_dev = variance ** 0.5
        return std_dev / mean_revenue
    
    def _calculate_seasonal_liquidity_needs(self, business_data: Dict[str, Any]) -> float:
        """Calculate seasonal liquidity adjustment."""
        sector = business_data.get('sector', 'professional_services')
        monthly_expenses = business_data.get('monthly_expenses', 0)

        # Seasonal multipliers by sector
        seasonal_multipliers = {
            "retail": 1.5,      # Holiday seasons require more inventory
            "food": 1.2,        # Seasonal menu changes, events
            "auto": 1.3,        # Weather-related demand changes
            "electronics": 1.4, # Holiday and back-to-school seasons
            "professional_services": 1.1  # Generally less seasonal
        }

        multiplier = seasonal_multipliers.get(sector, 1.2)
        return monthly_expenses * multiplier
    
    def _assess_economic_uncertainty(self, economic_data: Dict[str, Any]) -> float:
        """Assess current economic uncertainty level (0-1 scale)."""
        uncertainty = 0.5  # Baseline

        # Fed rate volatility
        fed_rate = economic_data.get('fed_funds_rate', 5.0)
        if fed_rate > 6.0 or fed_rate < 2.0:
            uncertainty += 0.2

        # Inflation concerns
        inflation = economic_data.get('inflation_rate', 3.0)
        if inflation > 4.0:
            uncertainty += 0.2
        elif inflation < 1.0:
            uncertainty += 0.1

        # Economic health
        economic_health = economic_data.get('economic_health_score', 50)
        if economic_health < 40:
            uncertainty += 0.3
        elif economic_health < 60:
            uncertainty += 0.1

        return min(1.0, max(0.0, uncertainty))
    
    def _get_sector_correlation(self, sector: str) -> float:
        """Get correlation between business sector and broad market."""
        correlations = {
            "technology": 0.85,
            "electronics": 0.80,
            "healthcare": 0.60,
            "food": 0.45,
            "retail": 0.75,
            "auto": 0.85,
            "professional_services": 0.65,
            "manufacturing": 0.80,
            "construction": 0.85
        }
        return correlations.get(sector.lower(), 0.70)
    
    async def _generate_specific_allocations(self, dollar_allocation: Dict[str, float],
                                           risk_profile: RiskProfile,
                                           economic_data: Dict[str, Any],
                                           market_data: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """Generate specific investment allocations."""

        allocations = {}

        # Growth investments
        growth_amount = dollar_allocation.get("growth_investments", 0)
        if growth_amount > 0:
            if risk_profile == RiskProfile.AGGRESSIVE:
                allocations["growth_investments"] = [
                    {"investment": "VTI (Total Stock Market ETF)", "amount": growth_amount * 0.4, "ticker": "VTI"},
                    {"investment": "QQQ (NASDAQ 100 ETF)", "amount": growth_amount * 0.3, "ticker": "QQQ"},
                    {"investment": "VEA (International Developed)", "amount": growth_amount * 0.2, "ticker": "VEA"},
                    {"investment": "VWO (Emerging Markets)", "amount": growth_amount * 0.1, "ticker": "VWO"}
                ]
            elif risk_profile == RiskProfile.MODERATE:
                allocations["growth_investments"] = [
                    {"investment": "SPY (S&P 500 ETF)", "amount": growth_amount * 0.5, "ticker": "SPY"},
                    {"investment": "VTI (Total Stock Market ETF)", "amount": growth_amount * 0.3, "ticker": "VTI"},
                    {"investment": "VEA (International Developed)", "amount": growth_amount * 0.2, "ticker": "VEA"}
                ]
            else:  # Conservative
                allocations["growth_investments"] = [
                    {"investment": "SPY (S&P 500 ETF)", "amount": growth_amount * 0.6, "ticker": "SPY"},
                    {"investment": "VTI (Total Stock Market ETF)", "amount": growth_amount * 0.4, "ticker": "VTI"}
                ]

        # Income investments
        income_amount = dollar_allocation.get("income_investments", 0)
        if income_amount > 0:
            fed_rate = economic_data.get('fed_funds_rate', 5.0)
            if fed_rate > 5.0:  # High rate environment - favor shorter duration
                allocations["income_investments"] = [
                    {"investment": "SHY (1-3 Year Treasury ETF)", "amount": income_amount * 0.4, "ticker": "SHY"},
                    {"investment": "BND (Total Bond Market ETF)", "amount": income_amount * 0.3, "ticker": "BND"},
                    {"investment": "TIPS (Inflation Protected)", "amount": income_amount * 0.3, "ticker": "SCHP"}
                ]
            else:  # Lower rate environment
                allocations["income_investments"] = [
                    {"investment": "BND (Total Bond Market ETF)", "amount": income_amount * 0.5, "ticker": "BND"},
                   {"investment": "TLT (20+ Year Treasury ETF)", "amount": income_amount * 0.3, "ticker": "TLT"},
                   {"investment": "TIPS (Inflation Protected)", "amount": income_amount * 0.2, "ticker": "SCHP"}
               ]
       
       # Alternative investments
        alternative_amount = dollar_allocation.get("alternative_investments", 0)
        if alternative_amount > 0:
            allocations["alternative_investments"] = [
                {"investment": "VNQ (Real Estate ETF)", "amount": alternative_amount * 0.6, "ticker": "VNQ"},
                {"investment": "DBC (Commodities ETF)", "amount": alternative_amount * 0.25, "ticker": "DBC"},
                {"investment": "GLD (Gold ETF)", "amount": alternative_amount * 0.15, "ticker": "GLD"}
            ]

        return allocations
    
    def _generate_allocation_rationale(self, risk_profile: RiskProfile, 
                                     economic_data: Dict[str, Any],
                                     allocation: Dict[str, float]) -> str:
        """Generate rationale for asset allocation."""
        
        fed_rate = economic_data.get('fed_funds_rate', 5.0)
        inflation = economic_data.get('inflation_rate', 3.0)
        
        rationale = f"Asset allocation designed for {risk_profile.value} investor profile. "
        
        if allocation["business_reinvestment"] > 0.3:
            rationale += "High business reinvestment allocation reflects strong ROI opportunities. "
        
        if fed_rate > 5.0:
            rationale += f"Current {fed_rate}% Fed rate supports income investments for yield. "
        
        if inflation > 3.5:
            rationale += f"Inflation at {inflation}% justifies inflation-protected securities and real assets. "
        
        if allocation["growth_investments"] > 0.3:
            rationale += "Growth emphasis capitalizes on long-term equity market outperformance. "
        
        return rationale
    
    def _calculate_expected_return(self, allocation: Dict[str, float], market_data: Dict[str, Any]) -> float:
        """Calculate expected portfolio return."""
        
        # Expected returns by asset class (annualized)
        expected_returns = {
            "business_reinvestment": 0.15,   # 15% typical small business ROI
            "emergency_cash": 0.05,          # 5% high-yield savings
            "growth_investments": 0.10,      # 10% long-term equity return
            "income_investments": 0.04,      # 4% bond return
            "alternative_investments": 0.08, # 8% alternatives return
            "international_exposure": 0.09   # 9% international equity return
        }
        
        weighted_return = 0.0
        for asset_class, weight in allocation.items():
            if asset_class in expected_returns:
                weighted_return += weight * expected_returns[asset_class]
        
        return weighted_return
    
    def _calculate_expected_volatility(self, allocation: Dict[str, float]) -> float:
        """Calculate expected portfolio volatility."""
        
        # Expected volatilities by asset class (annualized)
        volatilities = {
            "business_reinvestment": 0.25,   # 25% business volatility
            "emergency_cash": 0.01,          # 1% cash volatility
            "growth_investments": 0.16,      # 16% equity volatility
            "income_investments": 0.04,      # 4% bond volatility
            "alternative_investments": 0.18, # 18% alternatives volatility
            "international_exposure": 0.18   # 18% international volatility
        }
        
        # Simplified volatility calculation (assuming some correlation)
        weighted_volatility = 0.0
        for asset_class, weight in allocation.items():
            if asset_class in volatilities:
                weighted_volatility += (weight ** 2) * (volatilities[asset_class] ** 2)
        
        return weighted_volatility ** 0.5
    
    def _calculate_max_drawdown(self, allocation: Dict[str, float], risk_profile: RiskProfile) -> float:
        """Estimate maximum drawdown for portfolio."""
        
        base_drawdown = {
            RiskProfile.CONSERVATIVE: 0.08,   # 8% max drawdown
            RiskProfile.MODERATE: 0.15,       # 15% max drawdown
            RiskProfile.AGGRESSIVE: 0.25      # 25% max drawdown
        }
        
        # Adjust based on allocation
        growth_weight = allocation.get("growth_investments", 0) + allocation.get("alternative_investments", 0)
        adjustment = growth_weight * 0.1  # Higher growth allocation increases drawdown risk
        
        return min(0.40, base_drawdown[risk_profile] + adjustment)
    
    def _create_implementation_roadmap(self, analysis_components: Dict[str, Any]) -> Dict[str, Any]:
        """Create implementation roadmap for investment strategy."""
        
        return {
            "phase_1_foundation": {
                "timeline": "Days 1-30",
                "priority_actions": [
                    "Open necessary investment accounts (brokerage, retirement)",
                    "Establish emergency fund in high-yield savings",
                    "Implement core portfolio holdings",
                    "Set up automatic investment plan"
                ],
                "completion_criteria": [
                    "All accounts opened and funded",
                    "Emergency fund fully established",
                    "Core investments purchased",
                    "Automation systems active"
                ]
            },
            "phase_2_optimization": {
                "timeline": "Days 31-90",
                "priority_actions": [
                    "Add satellite holdings and sector allocations",
                    "Implement tax-loss harvesting system",
                    "Optimize asset location across accounts",
                    "Establish rebalancing schedule"
                ],
                "completion_criteria": [
                    "Full portfolio allocation achieved",
                    "Tax optimization systems in place",
                    "Monitoring systems established"
                ]
            },
            "phase_3_enhancement": {
                "timeline": "Days 91-365",
                "priority_actions": [
                    "Fine-tune allocation based on performance",
                    "Add advanced strategies (covered calls, etc.)",
                    "Optimize for changing economic conditions",
                    "Plan for increased contribution capacity"
                ],
                "completion_criteria": [
                    "Portfolio performing to expectations",
                    "Advanced strategies implemented",
                    "Continuous improvement process established"
                ]
            }
        }
    
    def _create_monitoring_framework(self, business_data: Dict[str, Any], 
                                   analysis_components: Dict[str, Any]) -> Dict[str, Any]:
        """Create monitoring and review framework."""
        
        return {
            "daily_monitoring": {
                "automated_alerts": [
                    "Portfolio value changes > 2%",
                    "Individual position changes > 5%",
                    "Economic indicator releases",
                    "Fed policy announcements"
                ],
                "dashboard_metrics": [
                    "Total portfolio value",
                    "Asset allocation drift",
                    "Cash position",
                    "Top movers"
                ]
            },
            "weekly_review": {
                "performance_analysis": [
                    "Portfolio vs benchmark comparison",
                    "Individual position performance",
                    "Sector allocation review",
                    "Risk metrics assessment"
                ],
                "rebalancing_check": [
                    "Allocation drift beyond thresholds",
                    "New investment opportunities",
                    "Tax-loss harvesting opportunities"
                ]
            },
            "monthly_analysis": {
                "comprehensive_review": [
                    "Full portfolio performance attribution",
                    "Economic environment impact assessment",
                    "Business correlation analysis",
                    "Strategy effectiveness evaluation"
                ],
                "adjustment_decisions": [
                    "Tactical allocation changes",
                    "New investment additions",
                    "Underperformer elimination",
                    "Risk level adjustments"
                ]
            },
            "quarterly_strategy_review": {
                "strategic_assessment": [
                    "Investment thesis validation",
                    "Economic assumption updates",
                    "Long-term goal progress",
                    "Risk tolerance reassessment"
                ],
                "portfolio_optimization": [
                    "Full rebalancing if needed",
                    "Asset location optimization",
                    "Tax strategy updates",
                    "Fee and expense analysis"
                ]
            },
            "annual_comprehensive_review": {
                "complete_strategy_evaluation": [
                    "Full investment policy review",
                    "Goal and timeline updates",
                    "Risk profile reassessment",
                    "Tax situation changes"
                ],
                "strategic_planning": [
                    "Next year investment plan",
                    "Retirement timeline updates",
                    "Estate planning coordination",
                    "Professional advisor consultation"
                ]
            }
        }
    
    def _summarize_economic_context(self, economic_data: Dict[str, Any]) -> Dict[str, Any]:
        """Summarize economic context for investment decisions."""
        
        return {
            "monetary_policy": {
                "fed_funds_rate": economic_data.get('fed_funds_rate', 5.0),
                "policy_direction": "neutral",  # Would be determined by recent Fed actions
                "impact_on_investments": "Moderate headwind for growth, tailwind for income"
            },
            "inflation_environment": {
                "current_rate": economic_data.get('inflation_rate', 3.0),
                "trend": "moderating",
                "investment_implications": "Favor real assets and TIPS"
            },
            "economic_growth": {
                "gdp_trend": economic_data.get('gdp_growth', 2.4),
                "business_cycle_stage": "mid-cycle",
                "sector_implications": "Favor defensive sectors with growth opportunities"
            },
            "market_conditions": {
                "equity_valuations": "fair_to_elevated",
                "bond_yields": "attractive",
                "dollar_strength": "strong",
                "overall_assessment": "Balanced approach warranted"
            }
        }
    
    def _summarize_market_context(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Summarize market context for investment decisions."""
        
        return {
            "equity_markets": {
                "sentiment": market_data.get('market_sentiment', 'neutral'),
                "volatility_level": "moderate",
                "sector_rotation": "Technology to defensive sectors",
                "international_relative_value": "US markets premium valuation"
            },
            "fixed_income": {
                "yield_curve_shape": "normal",
                "credit_spreads": "tight",
                "duration_risk": "elevated",
                "opportunity_assessment": "Attractive yields available"
            },
            "alternatives": {
                "real_estate": "Regional variations, generally stable",
                "commodities": "Mixed signals, inflation hedge value",
                "private_markets": "Limited access for individual investors"
            },
            "investment_environment": {
                "opportunity_level": "moderate",
                "risk_level": "moderate",
                "diversification_importance": "high",
                "active_vs_passive": "Favor low-cost passive with tactical active"
            }
        }
    
    def _calculate_overall_confidence(self, analysis_components: Dict[str, Any]) -> float:
        """Calculate overall confidence in investment recommendations."""
        
        confidence_scores = []
        
        for component, result in analysis_components.items():
            if isinstance(result, dict) and "error" not in result:
                # Extract confidence if available, otherwise assume moderate confidence
                if "confidence_level" in result:
                    confidence_scores.append(result["confidence_level"])
                else:
                    confidence_scores.append(75)  # Default moderate confidence
            else:
                confidence_scores.append(30)  # Low confidence for failed components
        
        if confidence_scores:
            return sum(confidence_scores) / len(confidence_scores)
        else:
            return 50  # Baseline confidence