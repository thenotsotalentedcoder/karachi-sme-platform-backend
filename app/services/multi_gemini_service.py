"""Multi-Gemini AI analysis engine with intelligent routing and fallback."""

import asyncio
import httpx
import json
import logging
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import random
from functools import wraps

from app.config import GEMINI_KEYS, OPENROUTER_KEYS, settings

logger = logging.getLogger(__name__)


class MultiGeminiEngine:
    """Advanced multi-Gemini AI analysis engine with intelligent routing."""
    
    def __init__(self):
        self.gemini_keys = GEMINI_KEYS
        self.openrouter_keys = OPENROUTER_KEYS
        self.current_gemini_index = 0
        self.current_openrouter_index = 0
        
        # Request tracking for rate limiting
        self.request_counts = {key: 0 for key in self.gemini_keys}
        self.last_reset_time = datetime.now()
        
        # Task-specific key assignment
        self.task_key_mapping = {
            "business_analysis": 0,      # Gemini key 1
            "market_intelligence": 1,    # Gemini key 2  
            "recommendations": 2,        # Gemini key 3
            "investment_advice": 3,      # Gemini key 4
            "report_generation": 4,      # Gemini key 5
            "real_time_processing": 5,   # Gemini key 6
            "backup_overflow": 6         # Gemini key 7
        }
    
    def rate_limit_check(func):
        """Decorator to check and manage rate limits."""
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            # Reset counters every minute
            current_time = datetime.now()
            if (current_time - self.last_reset_time).seconds >= 60:
                self.request_counts = {key: 0 for key in self.gemini_keys}
                self.last_reset_time = current_time
            
            return await func(self, *args, **kwargs)
        return wrapper
    
    def get_optimal_key(self, task_type: str = "general", priority: str = "normal") -> str:
        """Get optimal Gemini key based on task type and current load."""
        
        # High priority tasks get dedicated keys
        if priority == "high":
            return self.gemini_keys[self.task_key_mapping["real_time_processing"]]
        
        # Task-specific routing
        if task_type in self.task_key_mapping:
            key_index = self.task_key_mapping[task_type]
            key = self.gemini_keys[key_index]
            
            # Check if this key has capacity (under 15 requests this minute)
            if self.request_counts[key] < 15:
                return key
        
        # Round-robin through available keys
        for _ in range(len(self.gemini_keys)):
            key = self.gemini_keys[self.current_gemini_index]
            self.current_gemini_index = (self.current_gemini_index + 1) % len(self.gemini_keys)
            
            if self.request_counts[key] < 15:
                return key
        
        # All keys at capacity, use overflow key
        return self.gemini_keys[self.task_key_mapping["backup_overflow"]]
    
    @rate_limit_check
    async def analyze_business_comprehensive(self, business_data: Dict[str, Any], 
                                           economic_data: Dict[str, Any],
                                           market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive business analysis using multiple Gemini instances."""
        
        logger.info("Starting comprehensive business analysis with multi-Gemini engine")
        
        # Parallel analysis tasks with different Gemini keys
        analysis_tasks = [
            self._analyze_business_performance(business_data, economic_data),
            self._analyze_market_position(business_data, market_data, economic_data),
            self._generate_strategic_recommendations(business_data, economic_data, market_data),
            self._analyze_investment_opportunities(business_data, economic_data),
            self._assess_risk_factors(business_data, economic_data, market_data)
        ]
        
        # Execute all analyses in parallel
        results = await asyncio.gather(*analysis_tasks, return_exceptions=True)
        
        # Process results and handle any failures
        analysis_result = {}
        task_names = ["performance", "market_position", "recommendations", "investment", "risk_assessment"]
        
        for i, result in enumerate(results):
            task_name = task_names[i]
            if isinstance(result, Exception):
                logger.error(f"Analysis task {task_name} failed: {str(result)}")
                analysis_result[task_name] = {"error": str(result), "status": "failed"}
            else:
                analysis_result[task_name] = result
        
        # Synthesize final analysis
        final_analysis = await self._synthesize_analysis_results(analysis_result, business_data)
        
        logger.info("Comprehensive business analysis completed")
        return final_analysis
    
    async def _analyze_business_performance(self, business_data: Dict[str, Any], 
                                          economic_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze business performance metrics using dedicated Gemini key."""
        
        key = self.get_optimal_key("business_analysis")
        
        prompt = f"""
        EXPERT BUSINESS ANALYST ROLE:
        
        Analyze this US small business performance in detail with current economic context.
        
        BUSINESS PROFILE:
        - Industry: {business_data.get('sector', 'N/A')}
        - Location: {business_data.get('location', 'N/A')}
        - Revenue (Last 6 months): ${business_data.get('monthly_revenue', [])}
        - Monthly Expenses: ${business_data.get('monthly_expenses', 0):,.0f}
        - Current Cash: ${business_data.get('current_cash', 0):,.0f}
        - Years Operating: {business_data.get('years_in_business', 0)}
        - Employees: {business_data.get('employees_count', 0)}
        
        CURRENT US ECONOMIC CONTEXT:
        - Fed Funds Rate: {economic_data.get('fed_funds_rate', 'N/A')}%
        - Inflation (CPI): {economic_data.get('inflation_cpi', 'N/A')}
        - Unemployment Rate: {economic_data.get('unemployment_rate', 'N/A')}%
        - Consumer Confidence: {economic_data.get('consumer_confidence', 'N/A')}
        - Small Business Optimism: {economic_data.get('small_business_optimism', 'N/A')}
        
        PROVIDE DETAILED ANALYSIS IN JSON FORMAT:
        {{
            "performance_score": <0-100 score>,
            "revenue_analysis": {{
                "trend": "<increasing/declining/stable>",
                "growth_rate": <monthly growth rate>,
                "stability_score": <0-100>,
                "seasonal_patterns": "<description>"
            }},
            "financial_health": {{
                "profit_margin": <percentage>,
                "cash_runway_months": <number>,
                "debt_to_revenue_ratio": <percentage>,
                "liquidity_score": <0-100>
            }},
            "economic_impact": {{
                "fed_rate_impact": "<positive/negative/neutral>",
                "inflation_impact": "<positive/negative/neutral>",
                "overall_economic_tailwind": <-100 to +100>
            }},
            "key_strengths": ["<strength 1>", "<strength 2>", "<strength 3>"],
            "key_weaknesses": ["<weakness 1>", "<weakness 2>", "<weakness 3>"],
            "immediate_concerns": ["<concern 1>", "<concern 2>"],
            "performance_vs_industry": "<above_average/average/below_average>",
            "confidence_level": <0-100>
        }}
        
        Be specific with dollar amounts, percentages, and timeframes.
        """
        
        return await self._make_gemini_request(key, prompt, "business_analysis")
    
    async def _analyze_market_position(self, business_data: Dict[str, Any],
                                     market_data: Dict[str, Any], 
                                     economic_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze market position using dedicated Gemini key."""
        
        key = self.get_optimal_key("market_intelligence")
        
        prompt = f"""
        EXPERT MARKET ANALYST ROLE:
        
        Analyze this US small business market position and competitive landscape.
        
        BUSINESS DETAILS:
        - Sector: {business_data.get('sector', 'N/A')}
        - Location: {business_data.get('location', 'N/A')}
        - Current Monthly Revenue: ${business_data.get('monthly_revenue', [0])[-1]:,.0f}
        - Business Type: {business_data.get('business_type', 'N/A')}
        
        ECONOMIC ENVIRONMENT:
        - Sector Growth Rate: {market_data.get('sector_growth_rate', 'N/A')}%
        - Market Size: ${market_data.get('total_market_size', 'N/A'):,.0f}
        - Competition Level: {market_data.get('competition_level', 'N/A')}
        - Economic Health Score: {economic_data.get('economic_health_score', 'N/A')}/100
        
        PROVIDE MARKET ANALYSIS IN JSON FORMAT:
        {{
            "market_position": {{
                "percentile_rank": <0-100>,
                "market_share_estimate": <percentage>,
                "competitive_advantage": "<strong/moderate/weak>",
                "market_positioning": "<leader/follower/niche/struggling>"
            }},
            "competitive_landscape": {{
                "competition_intensity": <1-10 scale>,
                "barriers_to_entry": "<high/medium/low>",
                "competitive_threats": ["<threat 1>", "<threat 2>"],
                "competitive_opportunities": ["<opportunity 1>", "<opportunity 2>"]
            }},
            "market_trends": {{
                "sector_outlook": "<growing/stable/declining>",
                "technology_disruption_risk": <1-10 scale>,
                "demographic_trends_impact": "<positive/negative/neutral>",
                "regulatory_environment": "<supportive/neutral/challenging>"
            }},
            "growth_potential": {{
                "organic_growth_potential": <1-10 scale>,
                "market_expansion_opportunities": ["<opportunity 1>", "<opportunity 2>"],
                "acquisition_opportunities": <true/false>,
                "new_market_segments": ["<segment 1>", "<segment 2>"]
            }},
            "location_analysis": {{
                "location_advantage": <1-10 scale>,
                "foot_traffic_potential": "<high/medium/low>",
                "rent_to_revenue_ratio": <percentage>,
                "expansion_locations": ["<location 1>", "<location 2>"]
            }},
            "strategic_positioning": {{
                "recommended_strategy": "<differentiation/cost_leadership/focus>",
                "pricing_power": <1-10 scale>,
                "brand_strength": <1-10 scale>,
                "customer_loyalty": <1-10 scale>
            }},
            "confidence_level": <0-100>
        }}
       
        Focus on actionable insights specific to US small business market dynamics.
        """

        return await self._make_gemini_request(key, prompt, "market_intelligence")
   
    async def _generate_strategic_recommendations(self, business_data: Dict[str, Any],
                                                economic_data: Dict[str, Any],
                                                market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate strategic recommendations using dedicated Gemini key."""
        
        key = self.get_optimal_key("recommendations")
        
        current_revenue = business_data.get('monthly_revenue', [0])[-1] if business_data.get('monthly_revenue') else 0
        
        prompt = f"""
        EXPERT BUSINESS STRATEGIST ROLE:
        
        Generate specific, actionable strategic recommendations for this US small business.
        
        BUSINESS SITUATION:
        - Sector: {business_data.get('sector', 'N/A')}
        - Monthly Revenue: ${current_revenue:,.0f}
        - Monthly Expenses: ${business_data.get('monthly_expenses', 0):,.0f}
        - Cash Position: ${business_data.get('current_cash', 0):,.0f}
        - Team Size: {business_data.get('employees_count', 0)} employees
        
        ECONOMIC CONDITIONS:
        - Fed Funds Rate: {economic_data.get('fed_funds_rate', 'N/A')}%
        - Business Climate Score: {economic_data.get('business_climate_score', 'N/A')}/100
        - Small Business Impact: {economic_data.get('small_business_impact', {}).get('overall_impact', 'N/A')}
        
        PROVIDE STRATEGIC RECOMMENDATIONS IN JSON FORMAT:
        {{
            "immediate_actions": [
                {{
                    "action": "<specific action>",
                    "timeframe": "<this week/this month>",
                    "expected_impact": "<revenue/cost/efficiency gain>",
                    "investment_required": <dollar amount>,
                    "roi_timeline": "<weeks/months>",
                    "implementation_steps": ["<step 1>", "<step 2>", "<step 3>"]
                }}
            ],
            "short_term_strategies": [
                {{
                    "strategy": "<strategic initiative>",
                    "timeframe": "<1-3 months>",
                    "expected_outcome": "<specific measurable outcome>",
                    "investment_required": <dollar amount>,
                    "risk_level": "<low/medium/high>",
                    "success_probability": <percentage>
                }}
            ],
            "long_term_vision": [
                {{
                    "initiative": "<major initiative>",
                    "timeframe": "<6-12 months>",
                    "transformational_impact": "<description>",
                    "capital_requirement": <dollar amount>,
                    "strategic_value": <1-10 scale>
                }}
            ],
            "operational_improvements": [
                {{
                    "area": "<operations/marketing/finance/technology>",
                    "improvement": "<specific improvement>",
                    "cost_savings": <annual dollar amount>,
                    "implementation_complexity": "<low/medium/high>"
                }}
            ],
            "risk_mitigation": [
                {{
                    "risk": "<specific risk>",
                    "mitigation_strategy": "<strategy>",
                    "cost_of_inaction": <dollar amount>,
                    "implementation_priority": "<high/medium/low>"
                }}
            ],
            "growth_acceleration": {{
                "revenue_optimization": ["<tactic 1>", "<tactic 2>"],
                "market_expansion": ["<approach 1>", "<approach 2>"],
                "efficiency_gains": ["<improvement 1>", "<improvement 2>"],
                "competitive_advantages": ["<advantage 1>", "<advantage 2>"]
            }},
            "confidence_level": <0-100>
        }}
        
        All recommendations must be specific, measurable, and include dollar amounts where applicable.
        """
        
        return await self._make_gemini_request(key, prompt, "recommendations")
    
    async def _analyze_investment_opportunities(self, business_data: Dict[str, Any],
                                              economic_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze investment opportunities using dedicated Gemini key."""
        
        key = self.get_optimal_key("investment_advice")
        
        current_cash = business_data.get('current_cash', 0)
        monthly_expenses = business_data.get('monthly_expenses', 0)
        available_capital = max(0, current_cash - (monthly_expenses * 3))  # Keep 3 months runway
        
        prompt = f"""
        EXPERT INVESTMENT ADVISOR ROLE:
        
        Analyze investment opportunities for this US small business owner.
        
        FINANCIAL PROFILE:
        - Available Investment Capital: ${available_capital:,.0f}
        - Monthly Cash Flow: ${(business_data.get('monthly_revenue', [0])[-1] if business_data.get('monthly_revenue') else 0) - business_data.get('monthly_expenses', 0):,.0f}
        - Sector: {business_data.get('sector', 'N/A')}
        - Business Maturity: {business_data.get('years_in_business', 0)} years
        
        ECONOMIC ENVIRONMENT:
        - Fed Funds Rate: {economic_data.get('fed_funds_rate', 'N/A')}%
        - Economic Health: {economic_data.get('economic_health_score', 'N/A')}/100
        - Market Conditions: {economic_data.get('small_business_impact', {}).get('overall_impact', 'N/A')}
        
        PROVIDE INVESTMENT ANALYSIS IN JSON FORMAT:
        {{
            "investment_capacity": {{
                "available_capital": <dollar amount>,
                "recommended_allocation": {{
                    "business_reinvestment": <percentage>,
                    "emergency_fund": <percentage>,
                    "growth_investments": <percentage>,
                    "market_investments": <percentage>
                }},
                "risk_tolerance": "<conservative/moderate/aggressive>"
            }},
            "business_reinvestment": [
                {{
                    "investment_type": "<equipment/inventory/marketing/technology>",
                    "amount": <dollar amount>,
                    "expected_roi": <percentage>,
                    "payback_period": "<months>",
                    "strategic_value": <1-10 scale>
                }}
            ],
            "market_investments": [
                {{
                    "investment_vehicle": "<stocks/bonds/etfs/real_estate>",
                    "sector_focus": "<technology/healthcare/finance/diversified>",
                    "amount": <dollar amount>,
                    "expected_annual_return": <percentage>,
                    "risk_level": "<low/medium/high>",
                    "time_horizon": "<short/medium/long>"
                }}
            ],
            "sector_specific_opportunities": [
                {{
                    "opportunity": "<specific to business sector>",
                    "investment_amount": <dollar amount>,
                    "strategic_alignment": <1-10 scale>,
                    "market_timing": "<excellent/good/fair/poor>"
                }}
            ],
            "tax_optimization": [
                {{
                    "strategy": "<tax strategy>",
                    "annual_savings": <dollar amount>,
                    "implementation_complexity": "<low/medium/high>"
                }}
            ],
            "exit_strategy_planning": {{
                "business_valuation_estimate": <dollar amount>,
                "value_enhancement_opportunities": ["<opportunity 1>", "<opportunity 2>"],
                "optimal_exit_timeline": "<years>",
                "preparation_steps": ["<step 1>", "<step 2>"]
            }},
            "confidence_level": <0-100>
        }}
        
        Focus on practical, implementable investment strategies for small business owners.
        """
        
        return await self._make_gemini_request(key, prompt, "investment_advice")
    
    async def _assess_risk_factors(self, business_data: Dict[str, Any],
                                 economic_data: Dict[str, Any],
                                 market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess business risk factors using dedicated Gemini key."""
        
        key = self.get_optimal_key("business_analysis")
        
        prompt = f"""
        EXPERT RISK ANALYST ROLE:
        
        Conduct comprehensive risk assessment for this US small business.
        
        BUSINESS PROFILE:
        - Sector: {business_data.get('sector', 'N/A')}
        - Revenue Volatility: {self._calculate_revenue_volatility(business_data.get('monthly_revenue', []))}
        - Cash Runway: {self._calculate_cash_runway(business_data)} months
        - Market Position: {market_data.get('competitive_position', 'N/A')}
        
        ECONOMIC RISKS:
        - Interest Rate Environment: {economic_data.get('fed_funds_rate', 'N/A')}%
        - Economic Health: {economic_data.get('economic_health_score', 'N/A')}/100
        - Sector Outlook: {market_data.get('sector_outlook', 'N/A')}
        
        PROVIDE RISK ASSESSMENT IN JSON FORMAT:
        {{
            "overall_risk_score": <0-100>,
            "risk_categories": {{
                "financial_risk": {{
                    "score": <0-100>,
                    "key_factors": ["<factor 1>", "<factor 2>"],
                    "mitigation_strategies": ["<strategy 1>", "<strategy 2>"]
                }},
                "operational_risk": {{
                    "score": <0-100>,
                    "key_factors": ["<factor 1>", "<factor 2>"],
                    "mitigation_strategies": ["<strategy 1>", "<strategy 2>"]
                }},
                "market_risk": {{
                    "score": <0-100>,
                    "key_factors": ["<factor 1>", "<factor 2>"],
                    "mitigation_strategies": ["<strategy 1>", "<strategy 2>"]
                }},
                "economic_risk": {{
                    "score": <0-100>,
                    "key_factors": ["<factor 1>", "<factor 2>"],
                    "mitigation_strategies": ["<strategy 1>", "<strategy 2>"]
                }},
                "regulatory_risk": {{
                    "score": <0-100>,
                    "key_factors": ["<factor 1>", "<factor 2>"],
                    "mitigation_strategies": ["<strategy 1>", "<strategy 2>"]
                }}
            }},
            "critical_vulnerabilities": [
                {{
                    "vulnerability": "<specific vulnerability>",
                    "impact_severity": "<low/medium/high/critical>",
                    "probability": <percentage>,
                    "time_to_impact": "<immediate/short/medium/long>",
                    "mitigation_cost": <dollar amount>
                }}
            ],
            "scenario_analysis": {{
                "best_case": {{
                    "probability": <percentage>,
                    "revenue_impact": <percentage change>,
                    "key_drivers": ["<driver 1>", "<driver 2>"]
                }},
                "most_likely": {{
                    "probability": <percentage>,
                    "revenue_impact": <percentage change>,
                    "key_drivers": ["<driver 1>", "<driver 2>"]
                }},
                "worst_case": {{
                    "probability": <percentage>,
                    "revenue_impact": <percentage change>,
                    "key_drivers": ["<driver 1>", "<driver 2>"]
                }}
            }},
            "insurance_recommendations": [
                {{
                    "coverage_type": "<coverage type>",
                    "coverage_amount": <dollar amount>,
                    "annual_premium_estimate": <dollar amount>,
                    "priority": "<high/medium/low>"
                }}
            ],
            "contingency_planning": [
                {{
                    "scenario": "<risk scenario>",
                    "response_plan": "<plan description>",
                    "resource_requirements": <dollar amount>,
                    "preparation_timeline": "<timeframe>"
                }}
            ],
            "confidence_level": <0-100>
        }}
        
        Be specific about dollar amounts for mitigation costs and potential impacts.
        """
        
        return await self._make_gemini_request(key, prompt, "risk_assessment")
    
    async def _synthesize_analysis_results(self, analysis_results: Dict[str, Any],
                                         business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize all analysis results into final comprehensive report."""
        
        key = self.get_optimal_key("report_generation")
        
        # Prepare synthesis prompt with all analysis results
        analysis_summary = json.dumps(analysis_results, indent=2)
        
        prompt = f"""
        EXPERT BUSINESS INTELLIGENCE SYNTHESIZER ROLE:
        
        Synthesize all analysis results into a comprehensive business intelligence report.
        
        BUSINESS: {business_data.get('business_name', 'Business')}
        SECTOR: {business_data.get('sector', 'N/A')}
        
        ANALYSIS RESULTS:
        {analysis_summary}
        
        PROVIDE SYNTHESIZED INTELLIGENCE IN JSON FORMAT:
        {{
            "executive_summary": {{
                "overall_health_score": <0-100>,
                "business_stage": "<startup/growth/mature/declining>",
                "competitive_position": "<leader/strong/average/weak>",
                "financial_stability": "<excellent/good/fair/poor>",
                "growth_trajectory": "<accelerating/steady/slowing/declining>",
                "key_message": "<one sentence summary>",
                "confidence_level": <0-100>
            }},
            "critical_insights": [
                {{
                    "insight": "<critical insight>",
                    "impact": "<high/medium/low>",
                    "urgency": "<immediate/short_term/long_term>",
                    "action_required": "<specific action>"
                }}
            ],
            "performance_dashboard": {{
                "revenue_score": <0-100>,
                "profitability_score": <0-100>,
                "growth_score": <0-100>,
                "efficiency_score": <0-100>,
                "market_position_score": <0-100>,
                "risk_score": <0-100>
            }},
            "priority_recommendations": [
                {{
                    "priority": <1-5>,
                    "recommendation": "<specific recommendation>",
                    "expected_impact": "<quantified impact>",
                    "investment_required": <dollar amount>,
                    "implementation_timeline": "<timeframe>",
                    "roi_estimate": <percentage>
                }}
            ],
            "investment_allocation": {{
                "immediate_needs": <dollar amount>,
                "growth_investments": <dollar amount>,
                "risk_mitigation": <dollar amount>,
                "market_opportunities": <dollar amount>,
                "total_recommended": <dollar amount>
            }},
            "performance_projections": {{
                "3_month_revenue_projection": <dollar amount>,
                "6_month_revenue_projection": <dollar amount>,
                "12_month_revenue_projection": <dollar amount>,
                "break_even_timeline": "<months>",
                "growth_rate_projection": <percentage>
            }},
            "competitive_advantages": [
                {{
                    "advantage": "<specific advantage>",
                    "strength": <1-10 scale>,
                    "sustainability": "<high/medium/low>",
                    "leverage_strategy": "<how to leverage>"
                }}
            ],
            "risk_mitigation_plan": [
                {{
                    "risk": "<top risk>",
                    "mitigation_action": "<specific action>",
                    "cost": <dollar amount>,
                    "timeline": "<implementation timeframe>",
                    "success_probability": <percentage>
                }}
            ],
            "next_review_date": "<date>",
            "confidence_level": <0-100>
        }}
        
        Ensure all dollar amounts and percentages are realistic and actionable.
        """
        
        synthesis_result = await self._make_gemini_request(key, prompt, "synthesis")
        
        # Add metadata
        synthesis_result["analysis_metadata"] = {
            "analysis_date": datetime.now().isoformat(),
            "analysis_components": list(analysis_results.keys()),
            "total_analysis_time": "estimated_time",
            "confidence_scores": {
                component: result.get("confidence_level", 0) 
                for component, result in analysis_results.items() 
                if isinstance(result, dict)
            }
        }
        
        return synthesis_result
    
    async def _make_gemini_request(self, api_key: str, prompt: str, task_type: str) -> Dict[str, Any]:
        """Make request to Gemini API with error handling and retries."""
        
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
            }
        }
        
        url = f"{settings.GEMINI_BASE_URL}/models/{settings.GEMINI_MODEL}:generateContent?key={api_key}"
        
        # Track request
        self.request_counts[api_key] += 1
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                async with httpx.AsyncClient(timeout=60.0) as client:
                    response = await client.post(url, headers=headers, json=payload)
                    
                    if response.status_code == 429:  # Rate limited
                        wait_time = 2 ** attempt
                        logger.warning(f"Rate limited for {task_type}, waiting {wait_time}s")
                        await asyncio.sleep(wait_time)
                        continue
                       
                    response.raise_for_status()
                    data = response.json()
                    
                    # Extract content from Gemini response
                    if "candidates" in data and len(data["candidates"]) > 0:
                        content = data["candidates"][0]["content"]["parts"][0]["text"]
                        
                        # Try to parse as JSON
                        try:
                            return json.loads(content)
                        except json.JSONDecodeError:
                            # If not valid JSON, return as text
                            return {"analysis": content, "format": "text"}
                    
                    raise Exception(f"Unexpected Gemini response format: {data}")
                    
            except httpx.TimeoutException:
                logger.error(f"Timeout for {task_type} on attempt {attempt + 1}")
                if attempt == max_retries - 1:
                    return await self._fallback_to_openrouter(prompt, task_type)
                await asyncio.sleep(2 ** attempt)
                
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error for {task_type}: {e.response.status_code}")
                if e.response.status_code >= 500 and attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                    continue
                return await self._fallback_to_openrouter(prompt, task_type)
                
            except Exception as e:
                logger.error(f"Error for {task_type}: {str(e)}")
                if attempt == max_retries - 1:
                    return await self._fallback_to_openrouter(prompt, task_type)
                await asyncio.sleep(2 ** attempt)
        
        return await self._fallback_to_openrouter(prompt, task_type)
    
    async def _fallback_to_openrouter(self, prompt: str, task_type: str) -> Dict[str, Any]:
        """Fallback to OpenRouter when Gemini fails."""
        
        logger.warning(f"Falling back to OpenRouter for {task_type}")
        
        key = self.openrouter_keys[self.current_openrouter_index]
        self.current_openrouter_index = (self.current_openrouter_index + 1) % len(self.openrouter_keys)
        
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "model": settings.OPENROUTER_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,
            "max_tokens": 4096
        }
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
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
                    return json.loads(content)
                except json.JSONDecodeError:
                    return {"analysis": content, "format": "text", "source": "openrouter_fallback"}
                    
        except Exception as e:
            logger.error(f"OpenRouter fallback failed for {task_type}: {str(e)}")
            return {
                "error": f"Analysis failed for {task_type}",
                "details": str(e),
                "status": "failed",
                "fallback_attempted": True
            }
    
    def _calculate_revenue_volatility(self, revenue_data: List[float]) -> float:
        """Calculate revenue volatility score."""
        if not revenue_data or len(revenue_data) < 2:
            return 0.0
        
        mean_revenue = sum(revenue_data) / len(revenue_data)
        if mean_revenue == 0:
            return 0.0
        
        variance = sum((x - mean_revenue) ** 2 for x in revenue_data) / len(revenue_data)
        std_dev = variance ** 0.5
        cv = std_dev / mean_revenue
        
        return cv
    
    def _calculate_cash_runway(self, business_data: Dict[str, Any]) -> float:
        """Calculate cash runway in months."""
        current_cash = business_data.get('current_cash', 0)
        monthly_expenses = business_data.get('monthly_expenses', 0)
        
        if monthly_expenses <= 0:
            return float('inf')
        
        return current_cash / monthly_expenses