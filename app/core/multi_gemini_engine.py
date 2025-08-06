"""Multi-Gemini AI analysis engine with intelligent routing and fallback for US SME Intelligence."""

import asyncio
import httpx
import json
import logging
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime, timedelta
import random
from functools import wraps
import time

from app.config import GEMINI_KEYS, OPENROUTER_KEYS, settings

logger = logging.getLogger(__name__)


class RateLimitTracker:
    """Track rate limits for each API key."""
    
    def __init__(self):
        self.request_counts = {key: 0 for key in GEMINI_KEYS}
        self.last_reset_time = datetime.now()
        self.request_timestamps = {key: [] for key in GEMINI_KEYS}
    
    def can_make_request(self, api_key: str) -> bool:
        """Check if we can make a request with this key."""
        now = datetime.now()
        
        # Reset counters every minute
        if (now - self.last_reset_time).total_seconds() >= 60:
            self.request_counts = {key: 0 for key in GEMINI_KEYS}
            self.request_timestamps = {key: [] for key in GEMINI_KEYS}
            self.last_reset_time = now
        
        # Clean old timestamps (older than 1 minute)
        cutoff_time = now - timedelta(minutes=1)
        self.request_timestamps[api_key] = [
            ts for ts in self.request_timestamps[api_key] if ts > cutoff_time
        ]
        
        return len(self.request_timestamps[api_key]) < settings.GEMINI_RATE_LIMIT_PER_KEY
    
    def record_request(self, api_key: str):
        """Record a request for rate limiting."""
        now = datetime.now()
        self.request_counts[api_key] += 1
        self.request_timestamps[api_key].append(now)


class MultiGeminiEngine:
    """Advanced multi-Gemini AI analysis engine with intelligent routing for US SME analysis."""
    
    def __init__(self):
        self.gemini_keys = GEMINI_KEYS
        self.openrouter_keys = OPENROUTER_KEYS
        self.rate_limiter = RateLimitTracker()
        
        # Task-specific key assignment for optimal performance
        self.task_key_mapping = {
            "business_performance": 0,    # Gemini key 1 - Core business analysis
            "market_intelligence": 1,     # Gemini key 2 - Market analysis
            "strategic_recommendations": 2, # Gemini key 3 - Strategy recommendations
            "investment_analysis": 3,     # Gemini key 4 - Investment advice
            "risk_assessment": 4,         # Gemini key 5 - Risk analysis
            "real_time_processing": 5,    # Gemini key 6 - High priority/real-time
            "synthesis_reporting": 6      # Gemini key 7 - Final synthesis
        }
        
        self.current_openrouter_index = 0
        
        # Performance tracking
        self.analysis_metrics = {
            "total_analyses": 0,
            "successful_analyses": 0,
            "failed_analyses": 0,
            "average_response_time": 0.0,
            "gemini_usage": {key: 0 for key in self.gemini_keys},
            "openrouter_fallbacks": 0
        }
    
    async def analyze_us_business_comprehensive(self, business_data: Dict[str, Any], 
                                              economic_data: Dict[str, Any],
                                              market_data: Dict[str, Any],
                                              analysis_options: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Comprehensive US small business analysis using multi-Gemini intelligence.
        
        Args:
            business_data: US business information (EIN, NAICS, financials, etc.)
            economic_data: Current US economic indicators
            market_data: US market conditions and benchmarks
            analysis_options: Analysis configuration options
        
        Returns:
            Comprehensive analysis results with insights, recommendations, and investment advice
        """
        
        start_time = time.time()
        self.analysis_metrics["total_analyses"] += 1
        
        logger.info(f"Starting comprehensive US business analysis for {business_data.get('business_name', 'Business')}")
        
        try:
            # Parallel analysis tasks using different Gemini keys
            analysis_tasks = await self._create_analysis_tasks(business_data, economic_data, market_data, analysis_options)
            
            # Execute all analyses in parallel with timeout
            results = await asyncio.wait_for(
                asyncio.gather(*analysis_tasks, return_exceptions=True),
                timeout=180.0  # 3 minute timeout
            )
            
            # Process results and handle any failures
            processed_results = await self._process_analysis_results(results, business_data)
            
            # Synthesize final comprehensive analysis
            final_analysis = await self._synthesize_comprehensive_analysis(
                processed_results, business_data, economic_data, market_data
            )
            
            # Add metadata and performance metrics
            analysis_time = time.time() - start_time
            final_analysis["analysis_metadata"] = self._create_analysis_metadata(analysis_time, processed_results)
            
            self.analysis_metrics["successful_analyses"] += 1
            self._update_performance_metrics(analysis_time)
            
            logger.info(f"Comprehensive analysis completed in {analysis_time:.2f} seconds")
            return final_analysis
            
        except asyncio.TimeoutError:
            logger.error("Analysis timeout - taking too long to complete")
            self.analysis_metrics["failed_analyses"] += 1
            return await self._create_timeout_fallback_analysis(business_data, economic_data)
            
        except Exception as e:
            logger.error(f"Analysis failed with error: {str(e)}")
            self.analysis_metrics["failed_analyses"] += 1
            return await self._create_error_fallback_analysis(business_data, str(e))
    
    async def _create_analysis_tasks(self, business_data: Dict[str, Any], 
                                   economic_data: Dict[str, Any],
                                   market_data: Dict[str, Any],
                                   analysis_options: Dict[str, Any] = None) -> List[asyncio.Task]:
        """Create parallel analysis tasks for different aspects."""
        
        options = analysis_options or {}
        tasks = []
        
        # Core business performance analysis (always included)
        tasks.append(asyncio.create_task(
            self._analyze_business_performance(business_data, economic_data),
            name="business_performance"
        ))
        
        # Market intelligence analysis
        if options.get("include_market_comparison", True):
            tasks.append(asyncio.create_task(
                self._analyze_market_intelligence(business_data, market_data, economic_data),
                name="market_intelligence"
            ))
        
        # Strategic recommendations
        tasks.append(asyncio.create_task(
            self._generate_strategic_recommendations(business_data, economic_data, market_data),
            name="strategic_recommendations"
        ))
        
        # Investment analysis
        if options.get("include_investment_advice", True):
            tasks.append(asyncio.create_task(
                self._analyze_investment_opportunities(business_data, economic_data, market_data),
                name="investment_analysis"
            ))
        
        # Risk assessment
        if options.get("include_risk_assessment", True):
            tasks.append(asyncio.create_task(
                self._assess_business_risks(business_data, economic_data, market_data),
                name="risk_assessment"
            ))
        
        return tasks
    
    async def _analyze_business_performance(self, business_data: Dict[str, Any], 
                                          economic_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze US business performance metrics using dedicated Gemini key."""
        
        key = self._get_optimal_key("business_performance")
        
        # Calculate key metrics
        monthly_revenue = business_data.get('monthly_revenue', [])
        current_revenue = monthly_revenue[-1] if monthly_revenue else 0
        revenue_trend = self._calculate_revenue_trend(monthly_revenue)
        cash_runway = self._calculate_cash_runway(business_data)
        
        prompt = f"""
        EXPERT US SMALL BUSINESS PERFORMANCE ANALYST:
        
        Analyze this US small business performance with current economic context.
        
        BUSINESS PROFILE:
        - Business: {business_data.get('business_name', 'US Small Business')}
        - Sector: {business_data.get('sector', 'N/A')}
        - Location: {business_data.get('city', 'N/A')}, {business_data.get('state', 'N/A')} {business_data.get('zip_code', '')}
        - NAICS Code: {business_data.get('naics_code', 'N/A')}
        - Structure: {business_data.get('business_structure', 'N/A')}
        - Years Operating: {business_data.get('years_in_business', 0)}
        - Employees: {business_data.get('employees_count', 0)}
        
        FINANCIAL PERFORMANCE (Last 12 Months):
        - Monthly Revenue: {monthly_revenue}
        - Current Monthly Revenue: ${current_revenue:,.0f}
        - Monthly Expenses: ${business_data.get('monthly_expenses', 0):,.0f}
        - Current Cash: ${business_data.get('current_cash', 0):,.0f}
        - Outstanding Debt: ${business_data.get('outstanding_debt', 0):,.0f}
        - Revenue Trend: {revenue_trend}
        - Cash Runway: {cash_runway:.1f} months
        
        US ECONOMIC CONTEXT:
        - Fed Funds Rate: {economic_data.get('fed_funds_rate', 'N/A')}%
        - Inflation (CPI): {economic_data.get('inflation_rate', 'N/A')}%
        - Unemployment: {economic_data.get('unemployment_rate', 'N/A')}%
        - Consumer Confidence: {economic_data.get('consumer_confidence', 'N/A')}
        - Small Business Optimism: {economic_data.get('small_business_optimism', 'N/A')}
        - GDP Growth: {economic_data.get('gdp_growth', 'N/A')}%
        
        PROVIDE DETAILED US BUSINESS PERFORMANCE ANALYSIS IN JSON:
        {{
            "overall_performance_score": <0-100>,
            "financial_health": {{
                "revenue_analysis": {{
                    "trend": "<increasing/stable/declining>",
                    "growth_rate": <monthly growth rate as decimal>,
                    "stability_score": <0-100>,
                    "seasonality_impact": <0-100>,
                    "revenue_predictability": <0-100>
                }},
                "profitability": {{
                    "gross_margin": <percentage as decimal>,
                    "net_margin": <percentage as decimal>,
                    "profit_trend": "<improving/stable/declining>",
                    "margin_sustainability": <0-100>
                }},
                "cash_flow": {{
                    "monthly_cash_flow": <average monthly cash flow>,
                    "cash_runway_months": <{cash_runway:.1f}>,
                    "cash_conversion_cycle": <days>,
                    "liquidity_score": <0-100>
                }},
                "financial_efficiency": {{
                    "asset_turnover": <ratio>,
                    "working_capital_management": <0-100>,
                    "cost_control_effectiveness": <0-100>,
                    "financial_leverage": <debt_to_equity_ratio>
                }}
            }},
            "operational_performance": {{
                "productivity_metrics": {{
                    "revenue_per_employee": <annual revenue per employee>,
                    "productivity_trend": "<improving/stable/declining>",
                    "operational_efficiency": <0-100>
                }},
                "market_performance": {{
                    "market_share_estimate": <percentage>,
                    "customer_acquisition_rate": <monthly new customers>,
                    "customer_retention_rate": <percentage>,
                    "brand_strength": <0-100>
                }}
            }},
            "us_economic_impact": {{
                "interest_rate_sensitivity": <-100 to 100>,
                "inflation_impact_score": <-100 to 100>,
                "economic_cycle_correlation": <-1 to 1>,
                "recession_resilience": <0-100>,
                "economic_tailwinds": ["<factor 1>", "<factor 2>"],
                "economic_headwinds": ["<factor 1>", "<factor 2>"]
            }},
            "competitive_position": {{
                "industry_percentile": <0-100>,
                "competitive_advantages": ["<advantage 1>", "<advantage 2>"],
                "competitive_threats": ["<threat 1>", "<threat 2>"],
                "differentiation_strength": <0-100>
            }},
            "performance_drivers": {{
                "top_growth_drivers": ["<driver 1>", "<driver 2>", "<driver 3>"],
                "performance_constraints": ["<constraint 1>", "<constraint 2>"],
                "efficiency_opportunities": ["<opportunity 1>", "<opportunity 2>"]
            }},
            "sector_context": {{
                "sector_growth_alignment": <-100 to 100>,
                "sector_disruption_risk": <0-100>,
                "technology_adoption_level": <0-100>,
                "regulatory_compliance_score": <0-100>
            }},
            "key_insights": [
                {{
                    "insight": "<critical performance insight>",
                    "impact": "<high/medium/low>",
                    "data_support": "<supporting data point>",
                    "action_implication": "<what this means for actions>"
                }}
            ],
            "performance_trajectory": {{
                "3_month_outlook": "<positive/stable/concerning>",
                "6_month_projection": "<growth/stable/decline>",
                "annual_performance_forecast": "<strong/moderate/weak>",
                "key_monitoring_metrics": ["<metric 1>", "<metric 2>", "<metric 3>"]
            }},
            "confidence_level": <80-95>
        }}
        
        Focus on specific, quantifiable insights with US market context.
        Include economic sensitivity analysis for Fed policy impacts.
        """
        
        return await self._make_gemini_request(key, prompt, "business_performance")
    
    async def _analyze_market_intelligence(self, business_data: Dict[str, Any],
                                         market_data: Dict[str, Any], 
                                         economic_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze US market position and competitive intelligence."""
        
        key = self._get_optimal_key("market_intelligence")
        
        current_revenue = business_data.get('monthly_revenue', [0])[-1] if business_data.get('monthly_revenue') else 0
        annual_revenue = sum(business_data.get('monthly_revenue', [0] * 12))
        
        prompt = f"""
        EXPERT US MARKET INTELLIGENCE ANALYST:
        
        Analyze this US small business market position and competitive landscape.
        
        BUSINESS MARKET PROFILE:
        - Sector: {business_data.get('sector', 'N/A')}
        - NAICS: {business_data.get('naics_code', 'N/A')}
        - Location: {business_data.get('city', 'N/A')}, {business_data.get('state', 'N/A')}
        - Annual Revenue: ${annual_revenue:,.0f}
        - Monthly Revenue: ${current_revenue:,.0f}
        - Market Experience: {business_data.get('years_in_business', 0)} years
        - Business Model: {business_data.get('business_model', 'N/A')}
        
        US MARKET CONDITIONS:
        - Market Size: {market_data.get('total_market_size', 'Analyzing...')}
        - Sector Growth: {market_data.get('sector_growth_rate', 'Analyzing...')}
        - Competition Level: {market_data.get('competition_density', 'Analyzing...')}
        - Market Maturity: {market_data.get('market_maturity', 'Analyzing...')}
        
        US ECONOMIC ENVIRONMENT:
        - Fed Policy Impact: {economic_data.get('fed_funds_rate', 'N/A')}% rate affecting sector
        - Consumer Spending: {economic_data.get('consumer_confidence', 'N/A')} confidence level
        - Business Investment Climate: {economic_data.get('small_business_optimism', 'N/A')} optimism
        - Economic Growth: {economic_data.get('gdp_growth', 'N/A')}% GDP growth
        
        PROVIDE US MARKET INTELLIGENCE ANALYSIS IN JSON:
        {{
            "market_position_analysis": {{
                "overall_market_position": "<leader/strong_competitor/average_performer/struggling>",
                "market_share_estimate": <percentage of local/regional market>,
                "revenue_percentile": <0-100 percentile in sector>,
                "competitive_ranking": "<top_10_percent/top_25_percent/average/below_average>",
                "market_presence_strength": <0-100>
            }},
            "competitive_landscape": {{
                "competition_intensity": <1-10 scale>,
                "market_concentration": "<fragmented/moderate/concentrated>",
                "barrier_to_entry": "<low/medium/high>",
                "competitive_moats": ["<moat 1>", "<moat 2>"],
                "competitive_vulnerabilities": ["<vulnerability 1>", "<vulnerability 2>"],
                "pricing_power": <0-100>,
                "customer_switching_costs": "<low/medium/high>"
            }},
            "market_dynamics": {{
                "sector_growth_trajectory": "<rapid_growth/steady_growth/mature/declining>",
                "market_size_trend": "<expanding/stable/contracting>",
                "customer_demand_patterns": ["<pattern 1>", "<pattern 2>"],
                "technology_disruption_level": <0-100>,
                "regulatory_environment": "<supportive/neutral/challenging>",
                "supply_chain_stability": <0-100>
            }},
            "customer_market_analysis": {{
                "target_market_size": <addressable market size>,
                "customer_acquisition_cost": <estimated CAC>,
                "customer_lifetime_value": <estimated CLV>,
                "market_penetration": <percentage of addressable market>,
                "customer_segment_growth": ["<growing_segment 1>", "<growing_segment 2>"],
                "underserved_segments": ["<opportunity 1>", "<opportunity 2>"]
            }},
            "us_regional_factors": {{
                "location_advantage": <-100 to 100>,
                "regional_market_health": <0-100>,
                "local_economic_indicators": {{
                    "unemployment_vs_national": <percentage difference>,
                    "income_levels": "<above_average/average/below_average>",
                    "population_growth": <percentage>,
                    "business_formation_rate": <percentage>
                }},
                "infrastructure_quality": <0-100>,
                "talent_availability": <0-100>
            }},
            "growth_opportunities": [
                {{
                    "opportunity": "<specific market opportunity>",
                    "market_size": <dollar value>,
                    "growth_potential": <0-100>,
                    "time_to_market": "<months>",
                    "investment_required": <dollar amount>,
                    "success_probability": <percentage>,
                    "competitive_advantage": "<advantage for this opportunity>"
                }}
            ],
            "market_threats": [
                {{
                    "threat": "<specific market threat>",
                    "probability": <percentage>,
                    "potential_impact": "<high/medium/low>",
                    "timeline": "<immediate/short_term/medium_term>",
                    "mitigation_strategies": ["<strategy 1>", "<strategy 2>"]
                }}
            ],
            "strategic_positioning": {{
                "current_positioning": "<how market perceives business>",
                "optimal_positioning": "<recommended market position>",
                "positioning_gap": ["<gap 1>", "<gap 2>"],
                "repositioning_strategy": "<strategic approach>",
                "brand_differentiation": <0-100>,
                "value_proposition_strength": <0-100>
            }},
            "market_entry_exit_dynamics": {{
                "new_entrant_threat": <0-100>,
                "exit_barrier_height": "<low/medium/high>",
                "market_consolidation_trend": "<increasing/stable/decreasing>",
                "acquisition_opportunities": ["<potential_target_type 1>", "<potential_target_type 2>"]
            }},
            "economic_sector_correlation": {{
                "economic_sensitivity": <-100 to 100>,
                "cyclical_vs_defensive": "<cyclical/defensive/neutral>",
                "interest_rate_impact": "<positive/negative/neutral>",
                "inflation_hedge_quality": <0-100>,
                "recession_performance": "<outperform/inline/underperform>"
            }},
            "actionable_intelligence": [
                {{
                    "intelligence": "<specific market insight>",
                    "action_implication": "<what business should do>",
                    "timing_consideration": "<when to act>",
                    "resource_requirement": "<what's needed>"
                }}
            ],
            "confidence_level": <85-95>
        }}
        
        Focus on US market-specific insights with economic context.
        Include specific competitive intelligence and positioning recommendations.
        """
        
        return await self._make_gemini_request(key, prompt, "market_intelligence")
    
    async def _generate_strategic_recommendations(self, business_data: Dict[str, Any],
                                                economic_data: Dict[str, Any],
                                                market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate strategic recommendations using dedicated Gemini key."""
        
        key = self._get_optimal_key("strategic_recommendations")
        
        current_cash = business_data.get('current_cash', 0)
        monthly_expenses = business_data.get('monthly_expenses', 0)
        available_capital = max(0, current_cash - (monthly_expenses * 3))  # Keep 3 months runway
        
        prompt = f"""
        EXPERT US SMALL BUSINESS STRATEGIST:
        
        Generate comprehensive strategic recommendations for this US small business.
        
        BUSINESS STRATEGIC CONTEXT:
        - Business: {business_data.get('business_name', 'US Business')}
        - Sector: {business_data.get('sector', 'N/A')}
        - Location: {business_data.get('city', 'N/A')}, {business_data.get('state', 'N/A')}
        - Maturity: {business_data.get('years_in_business', 0)} years
        - Scale: {business_data.get('employees_count', 0)} employees
        - Available Capital: ${available_capital:,.0f}
        
        FINANCIAL RESOURCES:
        - Current Cash: ${current_cash:,.0f}
        - Monthly Expenses: ${monthly_expenses:,.0f}
        - Revenue Stream: {business_data.get('revenue_streams', [])}
        - Business Goals: {business_data.get('business_goals', [])}
        - Main Challenges: {business_data.get('main_challenges', [])}
        
        US ECONOMIC STRATEGIC ENVIRONMENT:
        - Fed Policy: {economic_data.get('fed_funds_rate', 'N/A')}% - affecting borrowing costs
        - Economic Growth: {economic_data.get('gdp_growth', 'N/A')}% - affecting demand
        - Inflation: {economic_data.get('inflation_rate', 'N/A')}% - affecting costs
        - Business Climate: {economic_data.get('small_business_optimism', 'N/A')} optimism index
        
        PROVIDE STRATEGIC RECOMMENDATIONS IN JSON:
        {{
            "strategic_framework": {{
                "primary_strategic_objective": "<main 12-month goal>",
                "strategic_positioning": "<how to compete and win>",
                "resource_allocation_strategy": "<how to deploy resources>",
                "growth_vector": "<organic/acquisition/partnership/expansion>",
                "competitive_strategy": "<differentiation/cost_leadership/focus>"
            }},
            "immediate_actions": [
                {{
                    "action": "<specific action for next 30 days>",
                    "category": "<financial/operational/marketing/strategic>",
                    "urgency": "<critical/high/medium>",
                    "investment_required": <dollar amount>,
                    "expected_outcome": "<measurable result>",
                    "timeline": "<specific deadline>",
                    "roi_estimate": <percentage or dollar return>,
                    "implementation_steps": ["<step 1>", "<step 2>", "<step 3>"],
                    "success_metrics": ["<metric 1>", "<metric 2>"],
                    "risk_level": "<low/medium/high>"
                }}
            ],
            "growth_strategies": [
                {{
                    "strategy": "<specific growth approach>",
                    "target_outcome": "<measurable growth goal>",
                    "investment_requirement": <total dollar amount>,
                    "timeline": "<3-12 months>",
                    "market_opportunity": <market size or percentage>,
                    "competitive_advantage": "<how this creates advantage>",
                    "implementation_phases": [
                        {{
                            "phase": "<phase name>",
                            "duration": "<months>",
                            "investment": <dollar amount>,
                            "key_activities": ["<activity 1>", "<activity 2>"],
                            "milestones": ["<milestone 1>", "<milestone 2>"]
                        }}
                    ],
                    "success_probability": <percentage>,
                    "scalability_factor": <1-10 scale>
                }}
            ],
            "operational_excellence": [
                {{
                    "improvement_area": "<operations/technology/processes/people>",
                    "specific_improvement": "<detailed improvement>",
                    "efficiency_gain": <percentage improvement>,
                    "cost_savings": <annual dollar savings>,
                    "implementation_cost": <upfront investment>,
                    "payback_period": "<months>",
                    "competitive_impact": "<how this improves competitiveness>"
                }}
            ],
            "market_expansion": [
                {{
                    "expansion_type": "<geographic/demographic/product/channel>",
                    "target_market": "<specific new market>",
                    "market_size": <addressable market value>,
                    "entry_strategy": "<how to enter market>",
                    "investment_required": <dollar amount>,
                    "timeline_to_revenue": "<months>",
                    "cannibalization_risk": <percentage>,
                    "success_indicators": ["<indicator 1>", "<indicator 2>"]
                }}
            ],
            "financial_optimization": [
                {{
                    "optimization_area": "<cash_flow/pricing/costs/capital_structure>",
                    "specific_strategy": "<detailed strategy>",
                    "financial_impact": <annual dollar impact>,
                    "implementation_timeline": "<months>",
                    "complexity_level": "<low/medium/high>",
                    "us_tax_implications": "<tax considerations>",
                    "regulatory_considerations": ["<consideration 1>", "<consideration 2>"]
                }}
            ],
            "risk_mitigation_strategies": [
                {{
                    "risk_category": "<financial/operational/market/economic>",
                    "specific_risk": "<detailed risk>",
                    "mitigation_approach": "<comprehensive mitigation strategy>",
                    "cost_of_mitigation": <dollar amount>,
                    "cost_of_inaction": <potential loss amount>,
                    "implementation_priority": "<high/medium/low>",
                    "monitoring_approach": "<how to monitor this risk>"
                }}
            ],
            "technology_digital_strategy": [
                {{
                    "technology_area": "<automation/analytics/customer_experience/operations>",
                    "strategic_initiative": "<specific tech initiative>",
                    "business_value": "<operational/competitive benefit>",
                    "investment_cost": <dollar amount>,
                    "roi_timeline": "<months to positive return>",
                    "implementation_complexity": "<low/medium/high>",
                    "competitive_necessity": "<must_have/advantage/nice_to_have>"
                }}
            ],
            "strategic_partnerships": [
                {{
                    "partnership_type": "<supplier/distributor/technology/strategic>",
                    "strategic_objective": "<what partnership achieves>",
                    "ideal_partner_profile": "<characteristics of ideal partner>",
                    "value_proposition": "<what we offer partner>",
                    "expected_benefits": ["<benefit 1>", "<benefit 2>"],
                    "timeline_to_establish": "<months>",
                    "success_metrics": ["<metric 1>", "<metric 2>"]
                }}
            ],
            "us_economic_adaptations": [
                {{
                    "economic_factor": "<interest_rates/inflation/recession_risk>",
                    "adaptation_strategy": "<how to adapt to this factor>",
                    "proactive_measures": ["<measure 1>", "<measure 2>"],
                    "defensive_measures": ["<measure 1>", "<measure 2>"],
                    "opportunistic_measures": ["<opportunity 1>", "<opportunity 2>"],
                    "monitoring_indicators": ["<indicator 1>", "<indicator 2>"]
                }}
            ],
            "implementation_roadmap": {{
                "30_day_priorities": ["<priority 1>", "<priority 2>", "<priority 3>"],
                "90_day_objectives": ["<objective 1>", "<objective 2>"],
                "6_month_milestones": ["<milestone 1>", "<milestone 2>"],
                "12_month_vision": "<where business should be in 1 year>",
                "resource_sequencing": "<how to sequence resource allocation>",
                "decision_checkpoints": ["<checkpoint 1>", "<checkpoint 2>"]
            }},
            "success_measurement": {{
                "primary_kpis": ["<kpi 1>", "<kpi 2>", "<kpi 3>"],
                "financial_targets": {{
                    "revenue_growth": <percentage>,
                    "profit_margin_improvement": <percentage points>,
                    "cash_flow_target": <monthly cash flow goal>
                }},
                "operational_targets": {{
                    "efficiency_improvement": <percentage>,
                    "customer_satisfaction": <score target>,
                    "market_share_growth": <percentage points>
                }},
                "review_schedule": "<monthly/quarterly review process>"
            }},
            "confidence_level": <85-95>
        }}
        
        Focus on actionable, specific strategies with clear implementation paths.
        Include US-specific economic considerations and regulatory factors.
        Ensure all recommendations are properly sized for SME capabilities.
        """
        
        return await self._make_gemini_request(key, prompt, "strategic_recommendations")
    
    async def _analyze_investment_opportunities(self, business_data: Dict[str, Any],
                                              economic_data: Dict[str, Any],
                                              market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze investment opportunities using dedicated Gemini key."""
        
        key = self._get_optimal_key("investment_analysis")
        
        current_cash = business_data.get('current_cash', 0)
        monthly_expenses = business_data.get('monthly_expenses', 0)
        monthly_revenue = business_data.get('monthly_revenue', [])
        current_monthly_revenue = monthly_revenue[-1] if monthly_revenue else 0
        monthly_cash_flow = current_monthly_revenue - monthly_expenses
        available_capital = max(0, current_cash - (monthly_expenses * 3))  # Keep 3 months runway

        prompt = f"""
        EXPERT US SMALL BUSINESS INVESTMENT ADVISOR:

        Analyze investment opportunities and provide recommendations for this US small business owner.

        INVESTMENT PROFILE:
        - Business Owner with {business_data.get('years_in_business', 0)} years experience in {business_data.get('sector', 'N/A')}
        - Monthly Revenue: ${current_monthly_revenue:,.0f}
        - Monthly Expenses: ${monthly_expenses:,.0f}
        - Monthly Cash Flow: ${monthly_cash_flow:,.0f}
        - Current Cash Position: ${current_cash:,.0f}
        - Available Investment Capital: ${available_capital:,.0f}
        - Outstanding Debt: ${business_data.get('outstanding_debt', 0):,.0f}
        - Business Assets: ${business_data.get('business_assets', 0):,.0f}

        US INVESTMENT ENVIRONMENT:
        - Federal Funds Rate: {economic_data.get('fed_funds_rate', 'N/A')}%
        - 10-Year Treasury Yield: ~{economic_data.get('fed_funds_rate', 5) + 1:.1f}%
        - Inflation Rate: {economic_data.get('inflation_rate', 'N/A')}%
        - S&P 500 Performance: {economic_data.get('stock_market_sp500', 'N/A')}
        - Small Business Credit: {economic_data.get('small_business_lending', 'Available')}
        - Economic Outlook: {economic_data.get('gdp_growth', 'N/A')}% GDP growth

        BUSINESS CONTEXT:
        - Risk Tolerance: Based on {business_data.get('years_in_business', 0)} years experience and cash position
        - Investment Goals: {business_data.get('investment_interests', [])}
        - Sector Correlation: Consider correlation between business sector and investments

        PROVIDE US INVESTMENT ANALYSIS IN JSON:
        {{
            "investment_capacity_analysis": {{
                "total_investable_assets": <current cash + business equity estimate>,
                "available_liquid_capital": <{available_capital:,.0f}>,
                "emergency_fund_recommendation": <3-6 months expenses>,
                "investment_ready_capital": <capital available for investment>,
                "debt_capacity": <additional borrowing capacity>,
                "risk_tolerance_assessment": "<conservative/moderate/aggressive>",
                "investment_timeline_preference": "<short_term/medium_term/long_term>"
            }},
            "asset_allocation_strategy": {{
                "recommended_allocation": {{
                    "business_reinvestment": {{
                        "percentage": <percentage of investment capital>,
                        "amount": <dollar amount>,
                        "rationale": "<why this allocation>",
                        "expected_roi": <percentage annual return>
                    }},
                    "emergency_cash_reserve": {{
                        "percentage": <percentage>,
                        "amount": <dollar amount>,
                        "vehicle": "<high_yield_savings/money_market/treasury_bills>",
                        "yield_expectation": <percentage yield>
                    }},
                    "diversified_market_investments": {{
                        "percentage": <percentage>,
                        "amount": <dollar amount>,
                        "risk_level": "<conservative/moderate/aggressive>",
                        "expected_annual_return": <percentage>
                    }},
                    "sector_specific_investments": {{
                        "percentage": <percentage>,
                        "amount": <dollar amount>,
                        "correlation_consideration": "<how it relates to business sector>"
                    }},
                    "alternative_investments": {{
                        "percentage": <percentage>,
                        "amount": <dollar amount>,
                        "types": ["<real_estate/commodities/private_equity>"]
                    }}
                }}
            }},
            "specific_investment_recommendations": [
                {{
                    "investment_category": "<business_reinvestment/stocks/bonds/etfs/real_estate>",
                    "specific_recommendation": "<detailed investment recommendation>",
                    "allocation_amount": <dollar amount>,
                    "expected_annual_return": <percentage>,
                    "risk_level": "<low/medium/high>",
                    "time_horizon": "<1_year/3_years/5_years/10_years>",
                    "liquidity": "<high/medium/low>",
                    "tax_efficiency": <tax considerations score 0-100>,
                    "correlation_with_business": "<low/medium/high correlation>",
                    "rationale": "<why this investment fits profile>",
                    "implementation_steps": ["<step 1>", "<step 2>", "<step 3>"]
                }}
            ],
            "business_reinvestment_opportunities": [
                {{
                    "investment_type": "<equipment/technology/marketing/expansion/inventory>",
                    "specific_opportunity": "<detailed business investment>",
                    "investment_amount": <dollar amount>,
                    "expected_roi": <percentage annual return>,
                    "payback_period": "<months>",
                    "strategic_value": <0-100 strategic importance>,
                    "risk_assessment": "<low/medium/high>",
                    "implementation_timeline": "<months>",
                    "competitive_advantage": "<advantage gained>",
                    "scalability_impact": "<how this enables scaling>"
                }}
            ],
            "retirement_wealth_building": {{
                "retirement_account_recommendations": [
                    {{
                        "account_type": "<SEP_IRA/Solo_401k/Simple_IRA>",
                        "annual_contribution_limit": <dollar amount>,
                        "recommended_contribution": <dollar amount>,
                        "tax_benefit": <annual tax savings>,
                        "investment_options": ["<option 1>", "<option 2>"],
                        "employer_match_opportunity": <if applicable>
                    }}
                ],
                "wealth_building_strategy": "<long_term_approach>",
                "target_retirement_savings": <recommended total>,
                "catch_up_contributions": <if over 50>
            }},
            "tax_optimization_strategies": [
                {{
                    "strategy": "<specific tax strategy>",
                    "investment_vehicle": "<vehicle that provides tax benefit>",
                    "annual_tax_savings": <dollar amount>,
                    "implementation_complexity": "<low/medium/high>",
                    "regulatory_compliance": ["<requirement 1>", "<requirement 2>"],
                    "professional_assistance_needed": "<tax_advisor/financial_planner/attorney>"
                }}
            ],
            "economic_hedging_strategies": [
                {{
                    "economic_risk": "<inflation/recession/interest_rate_risk>",
                    "hedge_investment": "<specific hedging investment>",
                    "allocation_amount": <dollar amount>,
                    "hedge_effectiveness": <0-100>,
                    "correlation_coefficient": <-1 to 1>,
                    "implementation_approach": "<how to implement hedge>"
                }}
            ],
            "sector_specific_considerations": {{
                "business_sector_outlook": "<positive/neutral/negative>",
                "sector_investment_opportunities": ["<opportunity 1>", "<opportunity 2>"],
                "diversification_imperative": "<how important to diversify away from sector>",
                "sector_correlation_investments": ["<correlated investment 1>", "<correlated investment 2>"],
                "counter_cyclical_investments": ["<counter investment 1>", "<counter investment 2>"]
            }},
            "risk_management": {{
                "portfolio_risk_level": "<conservative/moderate/aggressive>",
                "diversification_strategy": "<geographic/sector/asset_class diversification>",
                "downside_protection": ["<protection strategy 1>", "<protection strategy 2>"],
                "volatility_management": "<approach to managing investment volatility>",
                "liquidity_management": "<ensuring adequate liquidity>",
                "insurance_considerations": ["<insurance need 1>", "<insurance need 2>"]
            }},
            "implementation_timeline": [
                {{
                    "phase": "<immediate/30_days/90_days/6_months>",
                    "actions": ["<specific action 1>", "<specific action 2>"],
                    "investment_amount": <dollar amount for this phase>,
                    "expected_setup_time": "<time to implement>",
                    "professional_assistance": "<type of help needed>",
                    "priority_level": "<high/medium/low>"
                }}
            ],
            "monitoring_rebalancing": {{
                "review_frequency": "<monthly/quarterly/semi_annual>",
                "rebalancing_triggers": ["<trigger 1>", "<trigger 2>"],
                "performance_benchmarks": ["<benchmark 1>", "<benchmark 2>"],
                "adjustment_criteria": ["<criteria 1>", "<criteria 2>"],
                "professional_review_schedule": "<when to consult advisor>"
            }},
            "economic_scenario_planning": {{
                "recession_scenario": {{
                    "probability": <percentage>,
                    "portfolio_impact": "<expected impact>",
                    "defensive_adjustments": ["<adjustment 1>", "<adjustment 2>"],
                    "opportunity_investments": ["<opportunity 1>", "<opportunity 2>"]
                }},
                "inflation_scenario": {{
                    "probability": <percentage>,
                    "inflation_hedges": ["<hedge 1>", "<hedge 2>"],
                    "asset_rotation_strategy": "<how to rotate assets>"
                }},
                "growth_scenario": {{
                    "probability": <percentage>,
                    "growth_positioning": ["<growth investment 1>", "<growth investment 2>"],
                    "leverage_opportunities": ["<opportunity 1>", "<opportunity 2>"]
                }}
            }},
            "confidence_level": <85-95>
        }}

        Focus on practical investment strategies appropriate for US small business owners.
        Consider tax implications, liquidity needs, and correlation with business risk.
        Provide specific, implementable recommendations with clear rationale.
        """

        return await self._make_gemini_request(key, prompt, "investment_analysis")
   
    async def _assess_business_risks(self, business_data: Dict[str, Any],
                                   economic_data: Dict[str, Any],
                                   market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess comprehensive business risks using dedicated Gemini key."""
        
        key = self._get_optimal_key("risk_assessment")
        
        cash_runway = self._calculate_cash_runway(business_data)
        revenue_volatility = self._calculate_revenue_volatility(business_data.get('monthly_revenue', []))
        debt_to_revenue = (business_data.get('outstanding_debt', 0) / 
                          (sum(business_data.get('monthly_revenue', [0])) or 1))
        
        prompt = f"""
        EXPERT US SMALL BUSINESS RISK ANALYST:
        
        Conduct comprehensive risk assessment for this US small business.
        
        BUSINESS RISK PROFILE:
        - Business: {business_data.get('business_name', 'US Business')}
        - Sector: {business_data.get('sector', 'N/A')} (NAICS: {business_data.get('naics_code', 'N/A')})
        - Location: {business_data.get('city', 'N/A')}, {business_data.get('state', 'N/A')}
        - Maturity: {business_data.get('years_in_business', 0)} years
        - Scale: {business_data.get('employees_count', 0)} employees
        - Financial Metrics:
          * Cash Runway: {cash_runway:.1f} months
          * Revenue Volatility: {revenue_volatility:.2f}
          * Debt-to-Revenue Ratio: {debt_to_revenue:.2f}
          * Current Cash: ${business_data.get('current_cash', 0):,.0f}
        
        US RISK ENVIRONMENT:
        - Economic Cycle: {economic_data.get('gdp_growth', 'N/A')}% growth
        - Interest Rate Environment: {economic_data.get('fed_funds_rate', 'N/A')}%
        - Inflation Pressure: {economic_data.get('inflation_rate', 'N/A')}%
        - Credit Conditions: {economic_data.get('bank_lending_standards', 'N/A')}
        - Small Business Climate: {economic_data.get('small_business_optimism', 'N/A')}
        
        MARKET RISK FACTORS:
        - Competition Level: {market_data.get('competition_density', 'Analyzing...')}
        - Market Growth: {market_data.get('sector_growth_rate', 'Analyzing...')}
        - Industry Disruption: {market_data.get('technology_disruption', 'Analyzing...')}
        
        PROVIDE COMPREHENSIVE US BUSINESS RISK ASSESSMENT IN JSON:
        {{
            "overall_risk_assessment": {{
                "total_risk_score": <0-100 where 100 is highest risk>,
                "risk_category": "<low_risk/moderate_risk/high_risk/critical_risk>",
                "risk_trend": "<increasing/stable/decreasing>",
                "business_resilience_score": <0-100>,
                "survival_probability": {{
                    "1_year": <percentage probability>,
                    "3_years": <percentage probability>,
                    "5_years": <percentage probability>
                }}
            }},
            "financial_risks": {{
                "cash_flow_risk": {{
                    "risk_score": <0-100>,
                    "cash_runway_months": <{cash_runway:.1f}>,
                    "seasonal_cash_flow_variation": <percentage>,
                    "payment_delay_risk": <0-100>,
                    "revenue_concentration_risk": <0-100>,
                    "key_risk_factors": ["<factor 1>", "<factor 2>"],
                    "mitigation_strategies": ["<strategy 1>", "<strategy 2>"]
                }},
                "credit_liquidity_risk": {{
                    "risk_score": <0-100>,
                    "debt_service_coverage": <ratio>,
                    "credit_availability": "<abundant/adequate/tight/unavailable>",
                    "interest_rate_sensitivity": <-100 to 100>,
                    "refinancing_risk": <0-100>,
                    "banking_relationship_strength": <0-100>
                }},
                "profitability_risk": {{
                    "risk_score": <0-100>,
                    "margin_volatility": <percentage>,
                    "cost_inflation_exposure": <0-100>,
                    "pricing_power": <0-100>,
                    "competitive_pricing_pressure": <0-100>
                }}
            }},
            "operational_risks": {{
                "supply_chain_risk": {{
                    "risk_score": <0-100>,
                    "supplier_concentration": <0-100>,
                    "supply_chain_disruption_probability": <percentage>,
                    "inventory_risk": <0-100>,
                    "logistics_vulnerability": <0-100>,
                    "mitigation_measures": ["<measure 1>", "<measure 2>"]
                }},
                "human_capital_risk": {{
                    "risk_score": <0-100>,
                    "key_person_dependency": <0-100>,
                    "talent_retention_risk": <0-100>,
                    "skills_gap_risk": <0-100>,
                    "labor_cost_inflation": <0-100>,
                    "workforce_availability": "<abundant/adequate/tight/scarce>"
                }},
                "technology_operational_risk": {{
                    "risk_score": <0-100>,
                    "technology_obsolescence": <0-100>,
                    "cybersecurity_vulnerability": <0-100>,
                    "system_reliability_risk": <0-100>,
                    "digital_transformation_lag": <0-100>
                }}
            }},
            "market_competitive_risks": {{
                "competitive_risk": {{
                    "risk_score": <0-100>,
                    "new_entrant_threat": <0-100>,
                    "competitive_intensity_trend": "<increasing/stable/decreasing>",
                    "market_share_erosion_risk": <0-100>,
                    "price_war_probability": <percentage>,
                    "competitive_response_capability": <0-100>
                }},
                "market_demand_risk": {{
                    "risk_score": <0-100>,
                    "demand_volatility": <0-100>,
                    "customer_concentration_risk": <0-100>,
                    "market_maturity_risk": <0-100>,
                    "substitute_product_threat": <0-100>,
                    "economic_sensitivity": <0-100>
                }},
                "industry_disruption_risk": {{
                    "risk_score": <0-100>,
                    "technology_disruption_probability": <percentage>,
                    "business_model_disruption": <0-100>,
                    "regulatory_disruption": <0-100>,
                    "adaptation_capability": <0-100>
                }}
            }},
            "economic_external_risks": {{
                "macroeconomic_risk": {{
                    "risk_score": <0-100>,
                    "recession_vulnerability": <0-100>,
                    "interest_rate_risk": <-100 to 100>,
                    "inflation_impact_risk": <0-100>,
                    "currency_risk": <0-100 if applicable>,
                    "economic_cycle_correlation": <-1 to 1>
                }},
                "regulatory_compliance_risk": {{
                    "risk_score": <0-100>,
                    "regulatory_change_impact": <0-100>,
                    "compliance_cost_burden": <0-100>,
                    "regulatory_enforcement_risk": <0-100>,
                    "licensing_permit_risk": <0-100>
                }},
                "environmental_social_risk": {{
                    "risk_score": <0-100>,
                    "climate_change_impact": <0-100>,
                    "social_trend_misalignment": <0-100>,
                    "reputation_risk": <0-100>,
                    "stakeholder_expectation_risk": <0-100>
                }}
            }},
            "strategic_risks": {{
                "growth_execution_risk": {{
                    "risk_score": <0-100>,
                    "growth_strategy_feasibility": <0-100>,
                    "execution_capability": <0-100>,
                    "resource_allocation_risk": <0-100>,
                    "timing_risk": <0-100>
                }},
                "innovation_adaptation_risk": {{
                    "risk_score": <0-100>,
                    "innovation_capability": <0-100>,
                    "market_adaptation_speed": <0-100>,
                    "competitive_response_time": <0-100>
                }}
            }},
            "critical_risk_scenarios": [
                {{
                    "scenario": "<specific risk scenario>",
                    "probability": <percentage>,
                    "potential_impact": "<revenue/operational/strategic impact>",
                    "time_to_impact": "<immediate/months/years>",
                    "business_continuity_threat": "<low/medium/high/critical>",
                    "early_warning_indicators": ["<indicator 1>", "<indicator 2>"],
                    "contingency_plan": "<high-level response plan>",
                    "mitigation_cost": <dollar amount>
                }}
            ],
            "risk_mitigation_priorities": [
                {{
                    "risk": "<highest priority risk>",
                    "priority_ranking": <1-5>,
                    "mitigation_strategy": "<comprehensive mitigation approach>",
                    "investment_required": <dollar amount>,
                    "timeline_to_implement": "<months>",
                    "risk_reduction_potential": <percentage reduction>,
                    "return_on_mitigation": <roi of risk mitigation>,
                    "implementation_complexity": "<low/medium/high>"
                }}
            ],
            "insurance_risk_transfer": [
                {{
                    "risk_category": "<liability/property/business_interruption/key_person>",
                    "coverage_recommendation": "<specific coverage type>",
                    "coverage_amount": <dollar amount>,
                    "estimated_premium": <annual premium>,
                    "priority": "<high/medium/low>",
                    "coverage_gaps": ["<gap 1>", "<gap 2>"]
                }}
            ],
            "monitoring_early_warning": {{
                "risk_dashboard_metrics": ["<metric 1>", "<metric 2>", "<metric 3>"],
                "monitoring_frequency": {{
                    "daily_metrics": ["<daily metric 1>", "<daily metric 2>"],
                    "weekly_reviews": ["<weekly review 1>", "<weekly review 2>"],
                    "monthly_assessments": ["<monthly assessment 1>", "<monthly assessment 2>"],
                    "quarterly_evaluations": ["<quarterly evaluation 1>", "<quarterly evaluation 2>"]
                }},
                "trigger_thresholds": [
                    {{
                        "metric": "<specific metric>",
                        "warning_threshold": "<yellow alert level>",
                        "critical_threshold": "<red alert level>",
                        "response_action": "<action to take>"
                    }}
                ]
            }},
            "business_continuity_planning": {{
                "continuity_score": <0-100>,
                "critical_processes": ["<process 1>", "<process 2>"],
                "single_points_of_failure": ["<failure point 1>", "<failure point 2>"],
                "backup_redundancy": <0-100>,
                "recovery_time_objective": "<hours/days to resume operations>",
                "recovery_point_objective": "<acceptable data/transaction loss>"
            }},
            "confidence_level": <85-95>
        }}
        
        Focus on quantifiable, actionable risk insights with specific mitigation strategies.
        Consider US regulatory environment, economic conditions, and sector-specific risks.
        Provide clear prioritization of risks based on impact and probability.
        """
        
        return await self._make_gemini_request(key, prompt, "risk_assessment")
    
    async def _synthesize_comprehensive_analysis(self, analysis_results: Dict[str, Any],
                                               business_data: Dict[str, Any],
                                               economic_data: Dict[str, Any],
                                               market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize all analysis results into final comprehensive intelligence report."""
        
        key = self._get_optimal_key("synthesis_reporting")
        
        # Prepare comprehensive synthesis prompt
        synthesis_data = {
            "business_profile": {
                "name": business_data.get('business_name', 'US Small Business'),
                "sector": business_data.get('sector', 'N/A'),
                "location": f"{business_data.get('city', 'N/A')}, {business_data.get('state', 'N/A')}",
                "years_operating": business_data.get('years_in_business', 0),
                "employees": business_data.get('employees_count', 0),
                "current_revenue": business_data.get('monthly_revenue', [0])[-1] if business_data.get('monthly_revenue') else 0
            },
            "analysis_components": {}
        }
        
        # Extract key insights from each analysis component
        for component, result in analysis_results.items():
            if isinstance(result, dict) and "error" not in result:
                if component == "business_performance":
                    synthesis_data["analysis_components"]["performance"] = {
                        "overall_score": result.get("overall_performance_score", "N/A"),
                        "financial_health": result.get("financial_health", {}),
                        "key_insights": result.get("key_insights", [])
                    }
                elif component == "market_intelligence":
                    synthesis_data["analysis_components"]["market"] = {
                        "market_position": result.get("market_position_analysis", {}),
                        "competitive_landscape": result.get("competitive_landscape", {}),
                        "opportunities": result.get("growth_opportunities", [])
                    }
                elif component == "strategic_recommendations":
                    synthesis_data["analysis_components"]["strategy"] = {
                        "framework": result.get("strategic_framework", {}),
                        "immediate_actions": result.get("immediate_actions", []),
                        "growth_strategies": result.get("growth_strategies", [])
                    }
                elif component == "investment_analysis":
                    synthesis_data["analysis_components"]["investment"] = {
                        "capacity": result.get("investment_capacity_analysis", {}),
                        "recommendations": result.get("specific_investment_recommendations", []),
                        "allocation": result.get("asset_allocation_strategy", {})
                    }
                elif component == "risk_assessment":
                    synthesis_data["analysis_components"]["risk"] = {
                        "overall_risk": result.get("overall_risk_assessment", {}),
                        "critical_scenarios": result.get("critical_risk_scenarios", []),
                        "mitigation_priorities": result.get("risk_mitigation_priorities", [])
                    }
        
        prompt = f"""
        EXPERT US SMALL BUSINESS INTELLIGENCE SYNTHESIZER:
        
        Create a comprehensive intelligence report by synthesizing all analysis components.
        
        BUSINESS: {synthesis_data["business_profile"]["name"]}
        SECTOR: {synthesis_data["business_profile"]["sector"]}
        LOCATION: {synthesis_data["business_profile"]["location"]}
        
        ANALYSIS COMPONENTS COMPLETED:
        {json.dumps(synthesis_data["analysis_components"], indent=2)}
        
        CURRENT US ECONOMIC CONTEXT:
        - Fed Funds Rate: {economic_data.get('fed_funds_rate', 'N/A')}%
        - Economic Growth: {economic_data.get('gdp_growth', 'N/A')}%
        - Small Business Climate: {economic_data.get('small_business_optimism', 'N/A')}
        
        SYNTHESIZE INTO COMPREHENSIVE US SME INTELLIGENCE REPORT IN JSON:
        {{
            "executive_summary": {{
                "overall_business_health_score": <0-100 weighted composite score>,
                "business_life_stage": "<startup/growth/mature/transition/declining>",
                "competitive_position": "<market_leader/strong_competitor/average_performer/struggling>",
                "financial_stability": "<excellent/good/fair/poor/critical>",
                "growth_trajectory": "<rapid_growth/steady_growth/stable/slow_decline/rapid_decline>",
                "economic_resilience": "<high/medium/low>",
                "investment_attractiveness": "<very_attractive/attractive/moderate/poor>",
                "primary_strategic_message": "<one compelling sentence summary>",
                "confidence_in_assessment": <overall confidence 80-95>
            }},
            "critical_business_insights": [
                {{
                    "insight_category": "<performance/market/financial/strategic/risk>",
                    "critical_insight": "<most important insight for this category>",
                    "business_impact": "<high/medium/low>",
                    "urgency": "<immediate/short_term/medium_term/long_term>",
                    "supporting_data": "<key data supporting this insight>",
                    "action_implication": "<what business owner should do>",
                    "confidence_level": <70-95>
                }}
            ],
            "performance_scorecard": {{
                "financial_performance": {{
                    "score": <0-100>,
                    "trend": "<improving/stable/declining>",
                    "vs_industry": "<above_average/average/below_average>",
                    "key_drivers": ["<driver 1>", "<driver 2>"]
                }},
                "market_position": {{
                    "score": <0-100>,
                    "competitive_strength": "<strong/moderate/weak>",
                    "market_share_trend": "<growing/stable/declining>",
                    "differentiation": "<high/medium/low>"
                }},
                "operational_efficiency": {{
                    "score": <0-100>,
                    "productivity_trend": "<improving/stable/declining>",
                    "scalability": "<high/medium/low>",
                    "automation_level": "<advanced/moderate/basic>"
                }},
                "growth_potential": {{
                    "score": <0-100>,
                    "growth_readiness": "<ready/partial/not_ready>",
                    "market_opportunity": "<large/medium/small>",
                    "resource_adequacy": "<adequate/partial/insufficient>"
                }},
                "risk_management": {{
                    "score": <0-100>,
                    "risk_exposure": "<low/medium/high/critical>",
                    "mitigation_effectiveness": "<strong/moderate/weak>",
                    "business_continuity": "<robust/adequate/vulnerable>"
                }}
            }},
            "strategic_priorities": [
                {{
                    "priority_rank": <1-5>,
                    "strategic_priority": "<specific strategic priority>",
                    "business_impact": "<transformational/significant/moderate>",
                    "investment_required": <total dollar investment>,
                    "timeline": "<immediate/3_months/6_months/12_months>",
                    "success_probability": <percentage>,
                    "roi_estimate": "<percentage or dollar return>",
                    "key_success_factors": ["<factor 1>", "<factor 2>"],
                    "implementation_complexity": "<low/medium/high>",
                    "strategic_rationale": "<why this is a top priority>"
                }}
            ],
            "investment_allocation_framework": {{
                "total_recommended_investment": <total dollars to invest>,
                "allocation_strategy": {{
                    "immediate_business_needs": {{
                        "amount": <dollars>,
                        "percentage": <percentage>,
                        "focus": "<cash_flow/operations/compliance>"
                    }},
                    "growth_investments": {{
                        "amount": <dollars>,
                        "percentage": <percentage>,
                        "focus": "<expansion/marketing/technology>"
                    }},
                    "risk_mitigation": {{
                        "amount": <dollars>,
                        "percentage": <percentage>,
                        "focus": "<insurance/diversification/reserves>"
                    }},
                    "market_investments": {{
                        "amount": <dollars>,
                        "percentage": <percentage>,
                        "focus": "<stocks/bonds/real_estate>"
                    }}
                }},
                "expected_portfolio_return": <weighted average return percentage>,
                "risk_adjusted_return": <risk-adjusted return metric>
            }},
            "competitive_advantage_framework": {{
                "current_competitive_moats": [
                    {{
                        "advantage": "<specific competitive advantage>",
                        "strength": <1-10 scale>,
                        "sustainability": "<high/medium/low>",
                        "defendability": "<easily_defendable/moderately_defendable/vulnerable>",
                        "leverage_strategy": "<how to maximize this advantage>"
                    }}
                ],
                "competitive_gap_analysis": [
                    {{
                        "gap": "<competitive disadvantage>",
                        "impact": "<high/medium/low>",
                        "difficulty_to_close": "<easy/medium/hard>",
                        "investment_to_close": <dollar amount>,
                        "timeline_to_close": "<months>"
                    }}
                ]
            }},
            "risk_intelligence_summary": {{
                "overall_risk_profile": "<low_risk/moderate_risk/high_risk/critical_risk>",
                "business_survival_outlook": {{
                    "12_months": "<strong/stable/concerning/critical>",
                    "24_months": "<growth_likely/stable_likely/challenges_likely>",
                    "60_months": "<thriving_likely/surviving_likely/struggling_likely>"
               }},
               "top_risk_priorities": [
                   {{
                       "risk": "<highest priority risk>",
                       "probability": <percentage>,
                       "business_impact": "<catastrophic/severe/moderate/minor>",
                       "time_horizon": "<immediate/short_term/medium_term>",
                       "mitigation_cost": <dollar amount>,
                       "mitigation_roi": "<cost of mitigation vs cost of risk>",
                       "recommended_action": "<specific mitigation action>"
                   }}
               ],
               "insurance_protection_gaps": [
                   "<gap 1>", "<gap 2>", "<gap 3>"
               ],
               "contingency_planning_readiness": <0-100>
           }},
           "economic_adaptation_strategy": {{
               "economic_sensitivity_score": <-100 to 100>,
               "current_economic_impact": "<very_positive/positive/neutral/negative/very_negative>",
               "fed_policy_adaptations": [
                   {{
                       "policy_scenario": "<rate_increase/rate_decrease/rate_hold>",
                       "business_impact": "<positive/neutral/negative>",
                       "recommended_response": "<specific business response>",
                       "timeline_for_action": "<immediate/months>"
                   }}
               ],
               "recession_preparedness": {{
                   "recession_resilience_score": <0-100>,
                   "defensive_strategies": ["<strategy 1>", "<strategy 2>"],
                   "opportunistic_strategies": ["<opportunity 1>", "<opportunity 2>"]
               }},
               "inflation_hedge_strategies": ["<hedge 1>", "<hedge 2>", "<hedge 3>"]
           }},
           "growth_acceleration_roadmap": {{
               "growth_readiness_score": <0-100>,
               "optimal_growth_vector": "<organic/acquisition/partnership/geographic_expansion>",
               "growth_timeline": {{
                   "quick_wins": ["<30_day_win 1>", "<30_day_win 2>"],
                   "short_term_growth": ["<90_day_initiative 1>", "<90_day_initiative 2>"],
                   "medium_term_transformation": ["<6_month_project 1>", "<6_month_project 2>"],
                   "long_term_vision": ["<12_month_goal 1>", "<12_month_goal 2>"]
               }},
               "resource_sequencing": {{
                   "phase_1_investment": <dollars>,
                   "phase_2_investment": <dollars>,
                   "phase_3_investment": <dollars>,
                   "total_growth_investment": <dollars>
               }},
               "growth_success_metrics": [
                   {{
                       "metric": "<specific KPI>",
                       "current_baseline": <current value>,
                       "target_value": <target value>,
                       "timeline": "<months to achieve>",
                       "measurement_frequency": "<daily/weekly/monthly>"
                   }}
               ]
           }},
           "market_opportunity_intelligence": {{
               "primary_market_opportunities": [
                   {{
                       "opportunity": "<specific market opportunity>",
                       "market_size": <addressable market size>,
                       "growth_rate": <market growth percentage>,
                       "competition_level": "<low/medium/high>",
                       "entry_barrier_height": "<low/medium/high>",
                       "investment_to_capture": <dollar investment needed>,
                       "timeline_to_revenue": "<months>",
                       "probability_of_success": <percentage>,
                       "strategic_fit": "<excellent/good/fair/poor>"
                   }}
               ],
               "market_timing_analysis": "<excellent/good/fair/poor>",
               "competitive_response_likelihood": "<low/medium/high>",
               "regulatory_environment_favorability": "<supportive/neutral/challenging>"
           }},
           "financial_optimization_blueprint": {{
               "cash_flow_optimization": {{
                   "current_cash_conversion_cycle": <days>,
                   "target_cash_conversion_cycle": <days>,
                   "working_capital_optimization": <dollar improvement>,
                   "payment_terms_optimization": "<strategy>"
               }},
               "profitability_enhancement": {{
                   "margin_improvement_potential": <percentage points>,
                   "cost_reduction_opportunities": <annual dollar savings>,
                   "revenue_optimization_potential": <percentage increase>,
                   "pricing_power_assessment": <0-100>
               }},
               "capital_efficiency": {{
                   "asset_utilization_improvement": <percentage>,
                   "inventory_optimization": <dollar reduction>,
                   "fixed_asset_efficiency": <revenue per dollar of assets>
               }}
           }},
           "technology_digital_transformation": {{
               "digital_maturity_score": <0-100>,
               "automation_opportunities": [
                   {{
                       "process": "<process to automate>",
                       "automation_cost": <implementation cost>,
                       "annual_savings": <dollar savings>,
                       "payback_period": "<months>",
                       "complexity": "<low/medium/high>"
                   }}
               ],
               "competitive_technology_gaps": ["<gap 1>", "<gap 2>"],
               "recommended_technology_investments": [
                   {{
                       "technology": "<specific technology>",
                       "business_value": "<operational/competitive benefit>",
                       "investment_cost": <dollar amount>,
                       "roi_timeline": "<months>",
                       "strategic_importance": "<critical/important/nice_to_have>"
                   }}
               ]
           }},
           "stakeholder_value_creation": {{
               "customer_value_enhancement": [
                   "<value_enhancement 1>", "<value_enhancement 2>"
               ],
               "employee_value_proposition": [
                   "<value_prop 1>", "<value_prop 2>"
               ],
               "community_economic_impact": "<positive/neutral/negative>",
               "environmental_social_considerations": [
                   "<consideration 1>", "<consideration 2>"
               ]
           }},
           "performance_monitoring_framework": {{
               "executive_dashboard_kpis": [
                   {{
                       "kpi": "<key performance indicator>",
                       "current_value": <current value>,
                       "target_value": <target value>,
                       "monitoring_frequency": "<daily/weekly/monthly>",
                       "alert_thresholds": {{
                           "green": "<good performance threshold>",
                           "yellow": "<warning threshold>",
                           "red": "<critical threshold>"
                       }}
                   }}
               ],
               "review_schedule": {{
                   "daily_operational_review": ["<item 1>", "<item 2>"],
                   "weekly_performance_review": ["<item 1>", "<item 2>"],
                   "monthly_strategic_review": ["<item 1>", "<item 2>"],
                   "quarterly_board_level_review": ["<item 1>", "<item 2>"]
               }}
           }},
           "next_analysis_recommendations": {{
               "recommended_review_frequency": "<monthly/quarterly/semi_annual>",
               "deep_dive_analysis_areas": ["<area 1>", "<area 2>"],
               "additional_data_collection_needs": ["<data_need 1>", "<data_need 2>"],
               "professional_consultation_recommendations": ["<consultant_type 1>", "<consultant_type 2>"]
           }},
           "success_probability_assessment": {{
               "overall_success_probability": <percentage>,
               "key_success_factors": ["<factor 1>", "<factor 2>", "<factor 3>"],
               "critical_failure_points": ["<failure_point 1>", "<failure_point 2>"],
               "contingency_planning_needs": ["<contingency 1>", "<contingency 2>"]
           }},
           "confidence_level": <85-95>
       }}
       
       This is the final synthesis - make it comprehensive, actionable, and strategic.
       Ensure all recommendations are properly prioritized and sequenced.
       Focus on creating a practical roadmap for business success.
       """
       
        return await self._make_gemini_request(key, prompt, "synthesis_reporting")
   
    async def _process_analysis_results(self, results: List[Any], 
                                      business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process parallel analysis results and handle any failures."""

        task_names = ["business_performance", "market_intelligence", "strategic_recommendations", 
                     "investment_analysis", "risk_assessment"]
        processed_results = {}

        for i, result in enumerate(results):
            task_name = task_names[i] if i < len(task_names) else f"task_{i}"

            if isinstance(result, Exception):
                logger.error(f"Analysis task {task_name} failed: {str(result)}")
                processed_results[task_name] = {
                    "error": str(result),
                    "status": "failed",
                    "fallback_analysis": await self._create_fallback_analysis(task_name, business_data)
                }
            elif isinstance(result, dict):
                processed_results[task_name] = result
            else:
                logger.warning(f"Unexpected result type for {task_name}: {type(result)}")
                processed_results[task_name] = {
                    "error": f"Unexpected result type: {type(result)}",
                    "status": "failed",
                    "raw_result": str(result)[:500]  # Truncate for safety
                }

        return processed_results
    
    async def _create_fallback_analysis(self, task_name: str, 
                                      business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create basic fallback analysis when Gemini calls fail."""

        current_revenue = business_data.get('monthly_revenue', [0])[-1] if business_data.get('monthly_revenue') else 0

        fallback_analyses = {
            "business_performance": {
                "overall_performance_score": 50,
                "financial_health": {
                    "revenue_analysis": {"trend": "stable", "growth_rate": 0.0},
                    "cash_flow": {"monthly_cash_flow": current_revenue - business_data.get('monthly_expenses', 0)},
                },
                "key_insights": [{"insight": "Unable to perform detailed analysis", "impact": "medium"}],
                "confidence_level": 30
            },
            "market_intelligence": {
                "market_position_analysis": {"overall_market_position": "average_performer"},
                "competitive_landscape": {"competition_intensity": 5},
                "growth_opportunities": [],
                "confidence_level": 30
            },
            "strategic_recommendations": {
                "strategic_framework": {"primary_strategic_objective": "Maintain current operations"},
                "immediate_actions": [{"action": "Monitor cash flow closely", "investment_required": 0}],
                "confidence_level": 30
            },
            "investment_analysis": {
                "investment_capacity_analysis": {"available_liquid_capital": max(0, business_data.get('current_cash', 0) - business_data.get('monthly_expenses', 0) * 3)},
                "specific_investment_recommendations": [],
                "confidence_level": 30
            },
            "risk_assessment": {
                "overall_risk_assessment": {"total_risk_score": 50, "risk_category": "moderate_risk"},
                "critical_risk_scenarios": [],
                "confidence_level": 30
            }
        }

        return fallback_analyses.get(task_name, {"status": "fallback_unavailable"})
    
    def _get_optimal_key(self, task_type: str) -> str:
        """Get optimal Gemini key based on task type and current load."""

        # Get dedicated key for this task type
        if task_type in self.task_key_mapping:
            key_index = self.task_key_mapping[task_type]
            key = self.gemini_keys[key_index]

            # Check if this key has capacity
            if self.rate_limiter.can_make_request(key):
                self.rate_limiter.record_request(key)
                self.analysis_metrics["gemini_usage"][key] += 1
                return key

        # Round-robin through available keys
        for _ in range(len(self.gemini_keys)):
            key = self.gemini_keys[self.current_gemini_index % len(self.gemini_keys)]
            self.current_gemini_index += 1

            if self.rate_limiter.can_make_request(key):
                self.rate_limiter.record_request(key)
                self.analysis_metrics["gemini_usage"][key] += 1
                return key

        # If all keys are at capacity, use overflow key anyway (will be rate limited by Gemini)
        overflow_key = self.gemini_keys[self.task_key_mapping["synthesis_reporting"]]
        self.rate_limiter.record_request(overflow_key)
        self.analysis_metrics["gemini_usage"][overflow_key] += 1
        return overflow_key
    
    async def _make_gemini_request(self, api_key: str, prompt: str, 
                                 task_type: str, max_retries: int = 3) -> Dict[str, Any]:
        """Make request to Gemini API with comprehensive error handling."""

        headers = {
            "Content-Type": "application/json",
        }

        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.1,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 8192,
                "candidateCount": 1
            },
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH", 
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                }
            ]
        }

        url = f"{settings.GEMINI_BASE_URL}/models/{settings.GEMINI_MODEL}:generateContent?key={api_key}"

        for attempt in range(max_retries):
            try:
                async with httpx.AsyncClient(timeout=120.0) as client:
                    response = await client.post(url, headers=headers, json=payload)

                    if response.status_code == 429:  # Rate limited
                        wait_time = (2 ** attempt) + random.uniform(0, 1)
                        logger.warning(f"Rate limited for {task_type}, waiting {wait_time:.1f}s")
                        await asyncio.sleep(wait_time)
                        continue
                       
                    if response.status_code == 503:  # Service unavailable
                        wait_time = (2 ** attempt) + random.uniform(0, 2)
                        logger.warning(f"Service unavailable for {task_type}, waiting {wait_time:.1f}s")
                        await asyncio.sleep(wait_time)
                        continue
                       
                    response.raise_for_status()
                    data = response.json()

                    # Extract and parse Gemini response
                    if "candidates" in data and len(data["candidates"]) > 0:
                        candidate = data["candidates"][0]

                        # Check if response was blocked
                        if candidate.get("finishReason") == "SAFETY":
                            logger.warning(f"Gemini response blocked by safety filters for {task_type}")
                            return await self._fallback_to_openrouter(prompt, task_type)

                        content = candidate["content"]["parts"][0]["text"]

                        # Try to parse as JSON
                        try:
                            parsed_content = json.loads(content)
                            parsed_content["_source"] = "gemini"
                            parsed_content["_api_key_used"] = api_key[-8:]  # Last 8 chars for identification
                            return parsed_content
                        except json.JSONDecodeError as e:
                            logger.warning(f"Failed to parse JSON for {task_type}: {str(e)}")
                            # Try to extract JSON from the content
                            json_match = self._extract_json_from_text(content)
                            if json_match:
                                try:
                                    parsed_content = json.loads(json_match)
                                    parsed_content["_source"] = "gemini"
                                    parsed_content["_api_key_used"] = api_key[-8:]
                                    return parsed_content
                                except json.JSONDecodeError:
                                    pass
                                   
                            # Return as structured text response
                            return {
                                "analysis": content,
                                "format": "text",
                                "_source": "gemini",
                                "_api_key_used": api_key[-8:],
                                "_parsing_error": str(e)
                            }

                    raise Exception(f"Unexpected Gemini response format: {data}")

            except httpx.TimeoutException:
                logger.error(f"Timeout for {task_type} on attempt {attempt + 1}")
                if attempt == max_retries - 1:
                    return await self._fallback_to_openrouter(prompt, task_type)
                await asyncio.sleep(2 ** attempt)

            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error {e.response.status_code} for {task_type}")
                if e.response.status_code >= 500 and attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                    continue
                elif e.response.status_code == 400:
                    # Bad request - likely prompt issue
                    logger.error(f"Bad request for {task_type} - prompt may be invalid")
                    return {"error": "Invalid request", "status": "failed", "_source": "gemini_error"}
                else:
                    return await self._fallback_to_openrouter(prompt, task_type)

            except Exception as e:
                logger.error(f"Unexpected error for {task_type}: {str(e)}")
                if attempt == max_retries - 1:
                    return await self._fallback_to_openrouter(prompt, task_type)
                await asyncio.sleep(2 ** attempt)

        return await self._fallback_to_openrouter(prompt, task_type)
    
    async def _fallback_to_openrouter(self, prompt: str, task_type: str) -> Dict[str, Any]:
        """Fallback to OpenRouter when all Gemini attempts fail."""

        logger.warning(f"Falling back to OpenRouter for {task_type}")
        self.analysis_metrics["openrouter_fallbacks"] += 1

        key = self.openrouter_keys[self.current_openrouter_index]
        self.current_openrouter_index = (self.current_openrouter_index + 1) % len(self.openrouter_keys)

        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://localhost:8000",
            "X-Title": "US SME Intelligence Platform"
        }

        payload = {
            "model": settings.OPENROUTER_MODEL,
            "messages": [
                {
                    "role": "system", 
                    "content": "You are an expert US small business analyst. Provide detailed, actionable analysis in JSON format."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "temperature": 0.1,
            "max_tokens": 4096,
            "top_p": 0.95
        }

        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    settings.OPENROUTER_BASE_URL + "/chat/completions",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                data = response.json()

                content = data["choices"][0]["message"]["content"]

                # Try to parse as JSON
                try:
                    parsed_content = json.loads(content)
                    parsed_content["_source"] = "openrouter"
                    parsed_content["_fallback"] = True
                    return parsed_content
                except json.JSONDecodeError:
                    # Try to extract JSON from the content
                    json_match = self._extract_json_from_text(content)
                    if json_match:
                        try:
                            parsed_content = json.loads(json_match)
                            parsed_content["_source"] = "openrouter"
                            parsed_content["_fallback"] = True
                            return parsed_content
                        except json.JSONDecodeError:
                            pass
                           
                    return {
                        "analysis": content,
                        "format": "text",
                        "_source": "openrouter",
                        "_fallback": True
                    }

        except Exception as e:
            logger.error(f"OpenRouter fallback failed for {task_type}: {str(e)}")
            return {
                "error": f"All AI analysis failed for {task_type}",
                "details": str(e),
                "status": "failed",
                "fallback_attempted": True,
                "_source": "error"
            }
    
    def _extract_json_from_text(self, text: str) -> Optional[str]:
        """Extract JSON object from text that might have additional content."""

        import re

        # Look for JSON objects in the text
        json_pattern = r'\{(?:[^{}]|{[^{}]*})*\}'
        matches = re.findall(json_pattern, text, re.DOTALL)

        if matches:
            # Return the largest match (likely the main JSON object)
            return max(matches, key=len)

        return None
    
    def _calculate_revenue_trend(self, monthly_revenue: List[float]) -> str:
        """Calculate revenue trend from monthly data."""

        if not monthly_revenue or len(monthly_revenue) < 2:
            return "insufficient_data"

        # Calculate trend over recent months
        recent_months = monthly_revenue[-6:] if len(monthly_revenue) >= 6 else monthly_revenue

        if len(recent_months) < 2:
            return "insufficient_data"

        # Simple linear trend
        growth_rates = []
        for i in range(1, len(recent_months)):
            if recent_months[i-1] > 0:
                growth_rate = (recent_months[i] - recent_months[i-1]) / recent_months[i-1]
                growth_rates.append(growth_rate)

        if not growth_rates:
            return "stable"

        avg_growth = sum(growth_rates) / len(growth_rates)

        if avg_growth > 0.05:  # >5% average monthly growth
            return "strong_growth"
        elif avg_growth > 0.02:  # >2% average monthly growth
            return "moderate_growth"
        elif avg_growth > -0.02:  # -2% to +2%
            return "stable"
        elif avg_growth > -0.05:  # -2% to -5%
            return "declining"
        else:
            return "strong_decline"
    
    def _calculate_cash_runway(self, business_data: Dict[str, Any]) -> float:
        """Calculate cash runway in months."""

        current_cash = business_data.get('current_cash', 0)
        monthly_expenses = business_data.get('monthly_expenses', 0)

        if monthly_expenses <= 0:
            return float('inf')

        return current_cash / monthly_expenses
    
    def _calculate_revenue_volatility(self, revenue_data: List[float]) -> float:
        """Calculate revenue volatility coefficient."""

        if not revenue_data or len(revenue_data) < 2:
            return 0.0

        mean_revenue = sum(revenue_data) / len(revenue_data)
        if mean_revenue == 0:
            return 0.0

        variance = sum((x - mean_revenue) ** 2 for x in revenue_data) / len(revenue_data)
        std_dev = variance ** 0.5
        coefficient_of_variation = std_dev / mean_revenue

        return coefficient_of_variation
    
    def _create_analysis_metadata(self, analysis_time: float, 
                                 processed_results: Dict[str, Any]) -> Dict[str, Any]:
        """Create metadata for the analysis."""

        successful_components = sum(1 for result in processed_results.values() 
                                  if isinstance(result, dict) and "error" not in result)

        confidence_scores = []
        for result in processed_results.values():
            if isinstance(result, dict) and "confidence_level" in result:
                confidence_scores.append(result["confidence_level"])

        return {
            "analysis_timestamp": datetime.now().isoformat(),
            "analysis_duration_seconds": round(analysis_time, 2),
            "components_analyzed": list(processed_results.keys()),
            "successful_components": successful_components,
            "failed_components": len(processed_results) - successful_components,
            "average_confidence": round(sum(confidence_scores) / len(confidence_scores), 1) if confidence_scores else 0,
            "ai_model_usage": {
                "primary_model": settings.GEMINI_MODEL,
                "fallback_model": settings.OPENROUTER_MODEL,
                "total_gemini_requests": sum(self.analysis_metrics["gemini_usage"].values()),
                "openrouter_fallbacks": self.analysis_metrics["openrouter_fallbacks"]
            },
            "analysis_version": "1.0",
            "platform": "US SME Intelligence Platform"
        }
    
    def _update_performance_metrics(self, analysis_time: float):
        """Update internal performance metrics."""

        # Update average response time
        total_time = (self.analysis_metrics["average_response_time"] * 
                     (self.analysis_metrics["successful_analyses"] - 1) + analysis_time)
        self.analysis_metrics["average_response_time"] = (
            total_time / self.analysis_metrics["successful_analyses"]
        )
    
    async def _create_timeout_fallback_analysis(self, business_data: Dict[str, Any],
                                              economic_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create basic analysis when comprehensive analysis times out."""

        current_revenue = business_data.get('monthly_revenue', [0])[-1] if business_data.get('monthly_revenue') else 0
        cash_runway = self._calculate_cash_runway(business_data)

        return {
            "executive_summary": {
                "overall_business_health_score": 50,
                "business_life_stage": "analysis_incomplete",
                "primary_strategic_message": "Analysis timed out - recommend re-running with focused scope",
                "confidence_in_assessment": 25
            },
            "critical_business_insights": [{
                "insight_category": "system",
                "critical_insight": "Comprehensive analysis could not be completed within time limit",
                "business_impact": "medium",
                "urgency": "immediate",
                "action_implication": "Re-run analysis or focus on specific areas"
            }],
            "strategic_priorities": [{
                "priority_rank": 1,
                "strategic_priority": "Complete comprehensive business analysis",
                "timeline": "immediate",
                "strategic_rationale": "Need complete analysis for strategic planning"
            }],
            "performance_scorecard": {
                "financial_performance": {"score": 50, "trend": "unknown"},
                "market_position": {"score": 50, "competitive_strength": "unknown"},
                "operational_efficiency": {"score": 50, "productivity_trend": "unknown"},
                "growth_potential": {"score": 50, "growth_readiness": "unknown"},
                "risk_management": {"score": 50, "risk_exposure": "unknown"}
            },
            "next_analysis_recommendations": {
                "recommended_review_frequency": "immediate",
                "deep_dive_analysis_areas": ["business_performance", "financial_health"],
                "additional_data_collection_needs": ["detailed_financial_data"]
            },
            "analysis_metadata": {
                "analysis_status": "timeout",
                "recommendation": "Re-run with focused scope or increased timeout",
                "partial_results_available": False
            },
            "confidence_level": 25
        }
    
    async def _create_error_fallback_analysis(self, business_data: Dict[str, Any], 
                                            error_message: str) -> Dict[str, Any]:
        """Create basic analysis when comprehensive analysis fails with error."""

        return {
            "executive_summary": {
                "overall_business_health_score": 0,
                "business_life_stage": "analysis_failed",
                "primary_strategic_message": f"Analysis failed due to system error: {error_message[:100]}",
                "confidence_in_assessment": 0
            },
            "critical_business_insights": [{
                "insight_category": "system",
                "critical_insight": "Business analysis could not be completed due to technical issues",
                "business_impact": "high",
                "urgency": "immediate",
                "action_implication": "Contact system administrator or retry analysis"
            }],
            "error_details": {
                "error_message": error_message,
                "recommendation": "Please retry the analysis or contact support",
                "possible_causes": [
                    "Temporary API service disruption",
                    "Invalid business data format", 
                    "Network connectivity issues"
                ]
            },
            "next_analysis_recommendations": {
                "recommended_action": "retry_analysis",
                "data_validation_needed": True,
                "contact_support": True if "API" in error_message else False
            },
            "confidence_level": 0
        }
    
    def get_engine_status(self) -> Dict[str, Any]:
        """Get current status and performance metrics of the engine."""

        return {
            "engine_status": "operational",
            "available_gemini_keys": len([k for k in self.gemini_keys if self.rate_limiter.can_make_request(k)]),
            "total_gemini_keys": len(self.gemini_keys),
            "performance_metrics": self.analysis_metrics.copy(),
            "rate_limit_status": {
                key[-8:]: {
                    "requests_this_minute": len([
                        ts for ts in self.rate_limiter.request_timestamps[key] 
                        if (datetime.now() - ts).total_seconds() < 60
                    ]),
                    "available_requests": max(0, settings.GEMINI_RATE_LIMIT_PER_KEY - len([
                        ts for ts in self.rate_limiter.request_timestamps[key] 
                        if (datetime.now() - ts).total_seconds() < 60
                    ]))
                }
                for key in self.gemini_keys
            },
            "last_analysis_time": getattr(self, '_last_analysis_time', None),
           "uptime_hours": (datetime.now() - getattr(self, '_start_time', datetime.now())).total_seconds() / 3600
       }