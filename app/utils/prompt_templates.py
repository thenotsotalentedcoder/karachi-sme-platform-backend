"""Optimized prompt templates for US small business AI analysis."""

from typing import Dict, Any, Optional
import json


class InsightPromptTemplates:
    """Specialized prompt templates for generating business insights."""
    
    def get_main_insight_prompt(self, critical_area: str, analysis_result: Dict[str, Any],
                               business_data: Dict[str, Any], economic_data: Dict[str, Any] = None,
                               market_data: Dict[str, Any] = None) -> str:
        """Generate prompt for main business insight."""
        
        current_revenue = business_data.get('monthly_revenue', [0])[-1] if business_data.get('monthly_revenue') else 0
        
        prompt = f"""
        EXPERT US SMALL BUSINESS ADVISOR ROLE:
        
        Generate the single most critical insight for this US small business based on comprehensive analysis.
        
        BUSINESS PROFILE:
        - Business: {business_data.get('business_name', 'US Small Business')}
        - Sector: {business_data.get('sector', 'N/A')}
        - Location: {business_data.get('location', 'N/A')}
        - Current Monthly Revenue: ${current_revenue:,.0f}
        - Monthly Expenses: ${business_data.get('monthly_expenses', 0):,.0f}
        - Cash Position: ${business_data.get('current_cash', 0):,.0f}
        - Years Operating: {business_data.get('years_in_business', 0)}
        
        CRITICAL AREA IDENTIFIED: {critical_area}
        
        ANALYSIS SUMMARY:
        {self._format_analysis_summary(analysis_result)}
        
        {self._add_economic_context_to_prompt(economic_data) if economic_data else ""}
        
        GENERATE THE MOST IMPORTANT INSIGHT IN JSON FORMAT:
        {{
            "title": "<compelling, specific insight title>",
            "main_message": "<clear, actionable main message in 2-3 sentences>",
            "supporting_facts": [
                "<specific fact with numbers>",
                "<relevant trend or comparison>",
                "<economic or market context>"
            ],
            "recommended_actions": [
                "<immediate action with timeline>",
                "<strategic action with expected outcome>",
                "<monitoring action with metrics>"
            ],
            "potential_impact": {{
                "revenue_impact": "<potential $ impact or % improvement>",
                "timeframe": "<timeline for impact>",
                "probability": <0-100 success probability>
                }},
           "confidence_level": <80-95 confidence score>
       }}
       
       Focus on the highest-impact, most actionable insight that addresses the critical area.
       Include specific dollar amounts and percentages where possible.
       """

        return prompt
   
    def get_problem_insight_prompt(self, problem: Dict[str, Any], analysis_result: Dict[str, Any],
                                  business_data: Dict[str, Any], economic_data: Dict[str, Any] = None) -> str:
        """Generate prompt for problem-specific insights."""

        prompt = f"""
        EXPERT BUSINESS PROBLEM SOLVER ROLE:

        Analyze this specific business problem and provide detailed insights for resolution.

        PROBLEM IDENTIFIED: {problem['type']}
        Problem Urgency: {problem.get('urgency', 'medium')}
        Problem Severity: {problem.get('severity', 'medium')}

        BUSINESS CONTEXT:
        - Sector: {business_data.get('sector', 'N/A')}
        - Years Operating: {business_data.get('years_in_business', 0)}
        - Current Financial State: {self._format_financial_summary(business_data, analysis_result)}

        PROBLEM DATA:
        {json.dumps(problem.get('data', {}), indent=2)}

        {self._add_economic_context_to_prompt(economic_data) if economic_data else ""}

        PROVIDE PROBLEM ANALYSIS IN JSON FORMAT:
        {{
            "title": "<specific problem statement>",
            "problem_description": "<detailed description of the problem and its manifestations>",
            "root_causes": [
                "<primary root cause with explanation>",
                "<secondary root cause>",
                "<systemic or external cause>"
            ],
            "impact_analysis": {{
                "current_impact": "<quantified current impact on business>",
                "potential_future_impact": "<what happens if unaddressed>",
                "affected_areas": ["<area 1>", "<area 2>", "<area 3>"]
            }},
            "solution_approaches": [
                {{
                    "approach": "<solution name>",
                    "description": "<how to implement>",
                    "investment_required": <dollar amount>,
                    "timeline": "<implementation timeline>",
                    "success_probability": <percentage>
                }}
            ],
            "prevention_strategies": [
                "<strategy to prevent recurrence>",
                "<monitoring system to implement>",
                "<early warning indicators>"
            ],
            "confidence_level": <75-90 confidence score>
        }}

        Focus on practical, implementable solutions with specific costs and timelines.
        """

        return prompt
    
    def get_opportunity_insight_prompt(self, opportunity: Dict[str, Any], analysis_result: Dict[str, Any],
                                     business_data: Dict[str, Any], economic_data: Dict[str, Any] = None,
                                     market_data: Dict[str, Any] = None) -> str:
        """Generate prompt for opportunity-specific insights."""

        prompt = f"""
        EXPERT GROWTH STRATEGIST ROLE:

        Analyze this growth opportunity and provide detailed insights for capitalization.

        OPPORTUNITY IDENTIFIED: {opportunity['type']}
        Opportunity Priority: {opportunity.get('priority', 'medium')}
        Growth Potential: {opportunity.get('potential', 'medium')}

        BUSINESS STRENGTHS TO LEVERAGE:
        {self._format_business_strengths(analysis_result)}

        MARKET CONDITIONS:
        {self._format_market_conditions(market_data) if market_data else 'Limited market data available'}

        OPPORTUNITY DATA:
        {json.dumps(opportunity.get('data', {}), indent=2)}

        {self._add_economic_context_to_prompt(economic_data) if economic_data else ""}

        PROVIDE OPPORTUNITY ANALYSIS IN JSON FORMAT:
        {{
            "title": "<compelling opportunity title>",
            "opportunity_description": "<detailed description of the opportunity and why it's viable>",
            "market_potential": {{
                "market_size": "<estimated market size or customer base>",
                "growth_rate": "<market growth rate or trend>",
                "competitive_intensity": "<competition level>",
                "timing_favorability": "<why now is the right time>"
            }},
            "implementation_strategy": [
                {{
                    "phase": "<phase name>",
                    "actions": ["<action 1>", "<action 2>"],
                    "timeline": "<duration>",
                    "investment": <dollar amount>,
                    "expected_outcome": "<measurable outcome>"
                }}
            ],
            "resource_requirements": {{
                "financial_investment": <total dollar amount>,
                "human_resources": "<staffing needs>",
                "operational_changes": "<required changes>",
                "technology_needs": "<tech requirements>"
            }},
            "timeline_to_value": "<time to see positive returns>",
            "success_probability": <percentage based on business strengths>,
            "competitive_advantages": [
                "<advantage 1 that supports this opportunity>",
                "<advantage 2>",
                "<advantage 3>"
            ],
            "confidence_level": <75-90 confidence score>
        }}

        Focus on realistic opportunities that align with business capabilities and market conditions.
        """

        return prompt
    
    def get_market_position_insight_prompt(self, business_data: Dict[str, Any],
                                         market_data: Dict[str, Any],
                                         economic_data: Dict[str, Any] = None) -> str:
        """Generate prompt for market position insights."""

        current_revenue = business_data.get('monthly_revenue', [0])[-1] if business_data.get('monthly_revenue') else 0

        prompt = f"""
        EXPERT MARKET ANALYST ROLE:

        Analyze this US small business market position and provide strategic positioning insights.

        BUSINESS MARKET PROFILE:
        - Sector: {business_data.get('sector', 'N/A')}
        - Location: {business_data.get('location', 'N/A')}
        - Current Revenue: ${current_revenue:,.0f}/month
        - Business Model: {business_data.get('business_type', 'N/A')}
        - Market Experience: {business_data.get('years_in_business', 0)} years

        MARKET DATA:
        {json.dumps(market_data, indent=2) if market_data else 'Limited market data available'}

        {self._add_economic_context_to_prompt(economic_data) if economic_data else ""}

        PROVIDE MARKET POSITION ANALYSIS IN JSON FORMAT:
        {{
            "title": "<market position summary>",
            "position_analysis": {{
                "current_position": "<where business stands in market>",
                "market_share_estimate": "<estimated market share>",
                "competitive_ranking": "<ranking among competitors>",
                "differentiation_level": "<how differentiated from competitors>"
            }},
            "competitive_dynamics": [
                "<key competitive force 1>",
                "<key competitive force 2>",
                "<market entry/exit dynamics>",
                "<pricing dynamics>"
            ],
            "market_trends": [
                "<trend 1 affecting market>",
                "<trend 2 affecting market>",
                "<customer behavior changes>",
                "<technology/regulatory changes>"
            ],
            "positioning_recommendations": [
                {{
                    "strategy": "<positioning strategy>",
                    "rationale": "<why this positioning works>",
                    "implementation": "<how to achieve this positioning>",
                    "timeline": "<timeline for positioning shift>"
                }}
            ],
            "confidence_level": <80-90 confidence score>
        }}

        Focus on actionable positioning strategies that leverage business strengths.
        """

        return prompt
    
    def get_economic_impact_insight_prompt(self, business_data: Dict[str, Any],
                                         economic_data: Dict[str, Any]) -> str:
        """Generate prompt for economic impact insights."""

        prompt = f"""
        EXPERT ECONOMIC ANALYST ROLE:

        Analyze how current US economic conditions specifically impact this small business.

        BUSINESS PROFILE:
        - Sector: {business_data.get('sector', 'N/A')}
        - Business Model: {business_data.get('business_type', 'N/A')}
        - Customer Base: {business_data.get('primary_customers', 'N/A')}
        - Location: {business_data.get('location', 'N/A')}

        CURRENT US ECONOMIC CONDITIONS:
        - Fed Funds Rate: {economic_data.get('fed_funds_rate', 'N/A')}%
        - Inflation Rate: {economic_data.get('inflation_cpi', 'N/A')}
        - Unemployment Rate: {economic_data.get('unemployment_rate', 'N/A')}%
        - Consumer Confidence: {economic_data.get('consumer_confidence', 'N/A')}
        - Small Business Optimism: {economic_data.get('small_business_optimism', 'N/A')}
        - Economic Health Score: {economic_data.get('economic_health_score', 'N/A')}/100

        PROVIDE ECONOMIC IMPACT ANALYSIS IN JSON FORMAT:
        {{
            "title": "<economic impact summary>",
            "impact_analysis": {{
                "overall_impact": "<positive/negative/mixed/neutral>",
                "impact_magnitude": "<high/medium/low>",
                "primary_impact_channels": ["<channel 1>", "<channel 2>", "<channel 3>"],
                "quantified_impact": "<estimated $ or % impact>"
            }},
            "sector_implications": [
                "<how Fed rates affect this sector>",
                "<how inflation affects costs/pricing>",
                "<how employment affects demand>",
                "<consumer confidence impact on purchases>"
            ],
            "adaptation_strategies": [
                {{
                    "strategy": "<adaptation approach>",
                    "economic_scenario": "<which conditions this addresses>",
                    "implementation_cost": <dollar amount>,
                    "expected_benefit": "<quantified benefit>"
                }}
            ],
            "timing_considerations": {{
                "immediate_actions": ["<action 1>", "<action 2>"],
                "if_conditions_worsen": ["<defensive action 1>", "<defensive action 2>"],
                "if_conditions_improve": ["<growth action 1>", "<growth action 2>"],
                "monitoring_indicators": ["<indicator 1>", "<indicator 2>"]
            }},
            "confidence_level": <85-95 confidence score>
        }}

        Focus on specific, actionable adaptations to current economic conditions.
        """

        return prompt
    
    def get_growth_strategy_insight_prompt(self, analysis_result: Dict[str, Any],
                                         business_data: Dict[str, Any],
                                         economic_data: Dict[str, Any] = None) -> str:
        """Generate prompt for growth strategy insights."""

        prompt = f"""
        EXPERT GROWTH STRATEGIST ROLE:

        Develop comprehensive growth strategy insights for this US small business.

        BUSINESS GROWTH PROFILE:
        - Current Performance: {self._format_performance_summary(analysis_result)}
        - Growth Potential Score: {analysis_result.get('growth_analysis', {}).get('growth_score', 'N/A')}/100
        - Market Position: {analysis_result.get('market_position', {}).get('performance_category', 'N/A')}
        - Financial Capacity: {analysis_result.get('financial_health', {}).get('status', 'N/A')}

        BUSINESS CAPABILITIES:
        - Years Experience: {business_data.get('years_in_business', 0)}
        - Team Size: {business_data.get('employees_count', 0)}
        - Sector Expertise: {business_data.get('sector', 'N/A')}

        {self._add_economic_context_to_prompt(economic_data) if economic_data else ""}

        PROVIDE GROWTH STRATEGY ANALYSIS IN JSON FORMAT:
        {{
            "title": "<growth strategy direction>",
            "strategy_analysis": {{
                "growth_readiness": "<ready/partially_ready/not_ready>",
                "optimal_growth_vector": "<organic/acquisition/partnership/expansion>",
                "growth_timing": "<immediate/short_term/medium_term>",
                "growth_constraints": ["<constraint 1>", "<constraint 2>"]
            }},
            "growth_vectors": [
                {{
                    "vector": "<growth approach>",
                    "potential_impact": "<revenue/market impact>",
                    "resource_requirement": <dollar amount>,
                    "timeline": "<implementation timeline>",
                    "success_probability": <percentage>
                }}
            ],
            "resource_allocation": {{
                "current_operations": <percentage>,
                "growth_investments": <percentage>,
                "market_expansion": <percentage>,
                "capability_building": <percentage>
            }},
            "milestone_framework": [
                {{
                    "milestone": "<specific milestone>",
                    "timeline": "<when to achieve>",
                    "success_metric": "<how to measure>",
                    "investment_required": <dollar amount>
                }}
            ],
            "risk_considerations": [
                "<growth risk 1>",
                "<growth risk 2>",
                "<mitigation approach>"
            ],
            "confidence_level": <80-90 confidence score>
        }}

        Focus on realistic, fundable growth strategies aligned with business capabilities.
        """

        return prompt
    
    def get_competitive_strategy_insight_prompt(self, analysis_result: Dict[str, Any],
                                              business_data: Dict[str, Any]) -> str:
        """Generate prompt for competitive strategy insights."""

        prompt = f"""
        EXPERT COMPETITIVE STRATEGIST ROLE:

        Develop competitive strategy insights for this US small business.

        COMPETITIVE POSITION:
        - Market Performance: {analysis_result.get('market_position', {}).get('performance_category', 'N/A')}
        - Competitive Strengths: {analysis_result.get('competitive_analysis', {}).get('competitive_strengths', [])}
        - Competitive Weaknesses: {analysis_result.get('competitive_analysis', {}).get('competitive_weaknesses', [])}
        - Market Share: {analysis_result.get('competitive_analysis', {}).get('estimated_market_share', 'N/A')}%

        BUSINESS ASSETS:
        - Experience: {business_data.get('years_in_business', 0)} years in market
        - Sector: {business_data.get('sector', 'N/A')}
        - Customer Base: {business_data.get('primary_customers', 'N/A')}

        PROVIDE COMPETITIVE STRATEGY ANALYSIS IN JSON FORMAT:
        {{
            "title": "<competitive strategy framework>",
            "competitive_analysis": {{
                "competitive_position": "<leader/challenger/follower/niche>",
                "key_differentiators": ["<differentiator 1>", "<differentiator 2>"],
                "competitive_gaps": ["<gap 1>", "<gap 2>"],
                "sustainable_advantages": ["<advantage 1>", "<advantage 2>"]
            }},
            "differentiation_opportunities": [
                {{
                    "opportunity": "<differentiation approach>",
                    "implementation": "<how to achieve>",
                    "investment": <dollar amount>,
                    "competitive_moat": "<how sustainable>"
                }}
            ],
            "competitive_moves": [
                {{
                    "move": "<strategic move>",
                    "objective": "<what this achieves>",
                    "execution": "<how to execute>",
                    "expected_response": "<competitor likely response>"
                }}
            ],
            "defensive_strategies": [
                "<defensive strategy 1>",
                "<defensive strategy 2>",
                "<customer retention approach>"
            ],
            "confidence_level": <75-85 confidence score>
        }}

        Focus on practical competitive strategies that small businesses can execute effectively.
        """

        return prompt
    
    def _format_analysis_summary(self, analysis_result: Dict[str, Any]) -> str:
        """Format analysis results into readable summary."""

        summary_parts = []

        # Overall score
        overall_score = analysis_result.get("overall_score", {}).get("overall_score", "N/A")
        summary_parts.append(f"Overall Business Score: {overall_score}/100")

        # Financial health
        financial_health = analysis_result.get("financial_health", {})
        if financial_health:
            cash_runway = financial_health.get("cash_runway_months", "N/A")
            monthly_cash_flow = financial_health.get("monthly_cash_flow", "N/A")
            summary_parts.append(f"Financial Health: {financial_health.get('status', 'N/A')} (Cash runway: {cash_runway} months)")

        # Market position
        market_position = analysis_result.get("market_position", {})
        if market_position:
            performance_ratio = market_position.get("performance_ratio", "N/A")
            summary_parts.append(f"Market Performance: {performance_ratio:.1f}x industry average" if isinstance(performance_ratio, (int, float)) else f"Market Performance: {performance_ratio}")

        # Growth analysis
        growth_analysis = analysis_result.get("growth_analysis", {})
        if growth_analysis:
            growth_score = growth_analysis.get("growth_score", "N/A")
            summary_parts.append(f"Growth Potential: {growth_score}/100")

        return "\n".join(summary_parts)
    
    def _format_financial_summary(self, business_data: Dict[str, Any], analysis_result: Dict[str, Any]) -> str:
        """Format financial summary for prompts."""

        current_revenue = business_data.get('monthly_revenue', [0])[-1] if business_data.get('monthly_revenue') else 0
        monthly_expenses = business_data.get('monthly_expenses', 0)
        current_cash = business_data.get('current_cash', 0)

        financial_health = analysis_result.get("financial_health", {})

        return (f"Revenue: ${current_revenue:,.0f}/month, "
                f"Expenses: ${monthly_expenses:,.0f}/month, "
                f"Cash: ${current_cash:,.0f}, "
                f"Health: {financial_health.get('status', 'N/A')}")
    
    def _format_business_strengths(self, analysis_result: Dict[str, Any]) -> str:
        """Format business strengths for prompts."""

        overall_score = analysis_result.get("overall_score", {})
        strengths = overall_score.get("strengths", [])

        if strengths:
            return "Key Strengths:\n" + "\n".join(f"- {strength}" for strength in strengths)

        return "Strengths analysis in progress"
    
    def _format_market_conditions(self, market_data: Dict[str, Any]) -> str:
        """Format market conditions for prompts."""

        if not market_data:
            return "Limited market data available"

        conditions = []

        if "sector_growth_rate" in market_data:
            conditions.append(f"Sector Growth: {market_data['sector_growth_rate']*100:.1f}%")

        if "competition_level" in market_data:
            conditions.append(f"Competition: {market_data['competition_level']}")

        if "market_sentiment" in market_data:
            conditions.append(f"Market Sentiment: {market_data['market_sentiment']}")

        return "Market Conditions:\n" + "\n".join(f"- {condition}" for condition in conditions)
    
    def _format_performance_summary(self, analysis_result: Dict[str, Any]) -> str:
        """Format performance summary for prompts."""

        performance_metrics = analysis_result.get("performance_metrics", {})

        parts = []

        if "revenue_growth_rate" in performance_metrics:
            growth_rate = performance_metrics["revenue_growth_rate"]
            parts.append(f"Revenue Growth: {growth_rate*100:.1f}%")

        if "profit_margin" in performance_metrics:
            profit_margin = performance_metrics["profit_margin"]
            parts.append(f"Profit Margin: {profit_margin*100:.1f}%")

        if "financial_efficiency_score" in performance_metrics:
            efficiency = performance_metrics["financial_efficiency_score"]
            parts.append(f"Efficiency Score: {efficiency}/100")

        return ", ".join(parts) if parts else "Performance data being analyzed"
    
    def _add_economic_context_to_prompt(self, economic_data: Dict[str, Any]) -> str:
        """Add economic context section to prompts."""

        if not economic_data:
            return ""

        context = f"""
        CURRENT US ECONOMIC ENVIRONMENT:
        - Federal Funds Rate: {economic_data.get('fed_funds_rate', 'N/A')}%
        - Inflation (CPI): {economic_data.get('inflation_cpi', 'N/A')}
        - Unemployment Rate: {economic_data.get('unemployment_rate', 'N/A')}%
        - Consumer Confidence: {economic_data.get('consumer_confidence', 'N/A')}
        - Economic Health Score: {economic_data.get('economic_health_score', 'N/A')}/100
        - Small Business Climate: {economic_data.get('small_business_impact', {}).get('overall_impact', 'N/A')}
        """

        return context


class BusinessAnalysisPromptTemplates:
   """Prompt templates for comprehensive business analysis."""
   
   @staticmethod
   def get_comprehensive_analysis_prompt(business_data: Dict[str, Any], 
                                       economic_data: Dict[str, Any],
                                       market_data: Dict[str, Any]) -> str:
       """Generate comprehensive business analysis prompt."""
       
       current_revenue = business_data.get('monthly_revenue', [0])[-1] if business_data.get('monthly_revenue') else 0
       
       return f"""
       EXPERT US SMALL BUSINESS ANALYST ROLE:
       
       Conduct comprehensive analysis of this US small business with current economic and market context.
       
       BUSINESS PROFILE:
       - Business Name: {business_data.get('business_name', 'US Small Business')}
       - Industry Sector: {business_data.get('sector', 'N/A')}
       - Location: {business_data.get('location', 'N/A')}
       - Business Type: {business_data.get('business_type', 'N/A')}
       - Years in Operation: {business_data.get('years_in_business', 0)}
       - Employee Count: {business_data.get('employees_count', 0)}
       
       FINANCIAL DATA (Last 6 Months):
       - Monthly Revenue: {business_data.get('monthly_revenue', [])}
       - Monthly Expenses: ${business_data.get('monthly_expenses', 0):,.0f}
       - Current Cash Position: ${business_data.get('current_cash', 0):,.0f}
       - Current Monthly Revenue: ${current_revenue:,.0f}
       
       OPERATIONAL CONTEXT:
       - Primary Customer Type: {business_data.get('primary_customers', 'N/A')}
       - Main Business Challenges: {business_data.get('main_challenges', [])}
       - Business Goals: {business_data.get('business_goals', [])}
       
       CURRENT US ECONOMIC ENVIRONMENT:
       - Fed Funds Rate: {economic_data.get('fed_funds_rate', 'N/A')}%
       - Inflation Rate (CPI): {economic_data.get('inflation_cpi', 'N/A')}
       - Unemployment Rate: {economic_data.get('unemployment_rate', 'N/A')}%
       - Consumer Confidence Index: {economic_data.get('consumer_confidence', 'N/A')}
       - Small Business Optimism Index: {economic_data.get('small_business_optimism', 'N/A')}
       - GDP Growth Rate: {economic_data.get('gdp_growth', 'N/A')}%
       - Economic Health Score: {economic_data.get('economic_health_score', 'N/A')}/100
       
       MARKET CONDITIONS:
       {json.dumps(market_data, indent=2) if market_data else 'Market data being analyzed'}
       
       PROVIDE COMPREHENSIVE ANALYSIS IN JSON FORMAT:
       {{
           "executive_summary": {{
               "overall_health_score": <0-100>,
               "business_stage": "<startup/growth/mature/declining>",
               "competitive_position": "<leader/strong/average/weak>",
               "financial_stability": "<excellent/good/fair/poor/critical>",
               "growth_trajectory": "<accelerating/steady/slowing/declining>",
               "economic_sensitivity": "<low/medium/high>",
               "key_message": "<one sentence executive summary>"
           }},
           "financial_analysis": {{
               "revenue_trend": "<increasing/stable/declining>",
               "revenue_growth_rate": <monthly growth rate as decimal>,
               "profit_margin": <percentage as decimal>,
               "cash_runway_months": <number of months>,
               "liquidity_score": <0-100>,
               "financial_health_grade": "<A/B/C/D/F>",
               "burn_rate": <monthly cash burn>,
               "break_even_analysis": {{
                   "current_break_even": <monthly revenue needed>,
                   "break_even_gap": <difference from current>
               }}
           }},
           "market_position": {{
               "market_performance_ratio": <ratio vs industry average>,
               "percentile_rank": <0-100 percentile>,
               "competitive_advantages": ["<advantage 1>", "<advantage 2>"],
               "competitive_disadvantages": ["<disadvantage 1>", "<disadvantage 2>"],
               "market_share_estimate": <percentage>,
               "differentiation_level": "<high/medium/low>"
           }},
           "economic_impact_assessment": {{
               "interest_rate_sensitivity": "<high/medium/low>",
               "inflation_impact": "<positive/negative/neutral>",
               "consumer_confidence_correlation": "<strong/moderate/weak>",
               "recession_resilience": "<high/medium/low>",
               "economic_tailwinds": ["<tailwind 1>", "<tailwind 2>"],
               "economic_headwinds": ["<headwind 1>", "<headwind 2>"]
           }},
           "growth_analysis": {{
               "organic_growth_potential": <0-100 score>,
               "scalability_assessment": "<high/medium/low>",
               "growth_constraints": ["<constraint 1>", "<constraint 2>"],
               "expansion_readiness": "<ready/partial/not_ready>",
               "recommended_growth_strategy": "<strategy name>",
               "growth_investment_needed": <dollar amount>
           }},
           "risk_assessment": {{
               "overall_risk_score": <0-100>,
               "financial_risk": <0-100>,
               "market_risk": <0-100>,
               "operational_risk": <0-100>,
               "economic_risk": <0-100>,
               "top_risks": ["<risk 1>", "<risk 2>", "<risk 3>"],
               "risk_mitigation_priority": "<high/medium/low>"
           }},
           "strategic_recommendations": [
               {{
                   "category": "<financial/operational/marketing/strategic>",
                   "recommendation": "<specific recommendation>",
                   "priority": "<high/medium/low>",
                   "timeline": "<immediate/short_term/long_term>",
                   "investment_required": <dollar amount>,
                   "expected_roi": <percentage or dollar amount>,
                   "implementation_difficulty": "<low/medium/high>"
               }}
           ],
           "performance_projections": {{
               "3_month_revenue_forecast": <dollar amount>,
               "6_month_revenue_forecast": <dollar amount>,
               "12_month_revenue_forecast": <dollar amount>,
               "confidence_intervals": {{
                   "best_case": <percentage above forecast>,
                   "worst_case": <percentage below forecast>
               }}
           }},
           "investment_recommendations": {{
               "available_investment_capital": <dollar amount>,
               "recommended_allocation": {{
                   "business_reinvestment": <percentage>,
                   "emergency_fund": <percentage>,
                   "market_investments": <percentage>,
                   "growth_opportunities": <percentage>
               }},
               "specific_investment_opportunities": [
                   {{
                       "opportunity": "<investment opportunity>",
                       "amount": <dollar amount>,
                       "expected_return": <percentage>,
                       "risk_level": "<low/medium/high>"
                   }}
               ]
           }},
           "next_steps": {{
               "immediate_actions": ["<action 1>", "<action 2>", "<action 3>"],
               "30_day_goals": ["<goal 1>", "<goal 2>"],
               "90_day_objectives": ["<objective 1>", "<objective 2>"],
               "monitoring_metrics": ["<metric 1>", "<metric 2>", "<metric 3>"]
           }},
           "confidence_level": <80-95 overall confidence in analysis>
       }}
       
       Ensure all financial figures are realistic and all recommendations are specific and actionable.
       Focus on practical strategies appropriate for US small businesses in the current economic environment.
       """


class RecommendationPromptTemplates:
   """Prompt templates for generating business recommendations."""
   
   @staticmethod
   def get_immediate_actions_prompt(analysis_result: Dict[str, Any],
                                  business_data: Dict[str, Any],
                                  economic_data: Dict[str, Any]) -> str:
       """Generate prompt for immediate action recommendations."""
       
       return f"""
       EXPERT BUSINESS ADVISOR ROLE:
       
       Based on comprehensive business analysis, generate immediate action recommendations for this US small business.
       
       CRITICAL SITUATION SUMMARY:
       - Overall Business Score: {analysis_result.get('overall_score', {}).get('overall_score', 'N/A')}/100
       - Financial Health: {analysis_result.get('financial_health', {}).get('status', 'N/A')}
       - Cash Runway: {analysis_result.get('financial_health', {}).get('cash_runway_months', 'N/A')} months
       - Market Performance: {analysis_result.get('market_position', {}).get('performance_category', 'N/A')}
       - Risk Level: {analysis_result.get('risk_assessment', {}).get('risk_level', 'N/A')}
       
       BUSINESS CONSTRAINTS:
       - Available Cash: ${business_data.get('current_cash', 0):,.0f}
       - Monthly Expenses: ${business_data.get('monthly_expenses', 0):,.0f}
       - Team Size: {business_data.get('employees_count', 0)} employees
       
       ECONOMIC URGENCY FACTORS:
       - Fed Rate Impact: {economic_data.get('small_business_impact', {}).get('financing_cost_impact', 'N/A')}
       - Economic Environment: {economic_data.get('small_business_impact', {}).get('overall_impact', 'N/A')}
       
       GENERATE IMMEDIATE ACTION PLAN (NEXT 30 DAYS) IN JSON FORMAT:
       {{
           "critical_actions": [
               {{
                   "action": "<specific action to take>",
                   "urgency": "<critical/high/medium>",
                   "timeline": "<specific deadline>",
                   "cost": <dollar amount or 0>,
                   "expected_outcome": "<measurable result>",
                   "implementation_steps": ["<step 1>", "<step 2>", "<step"step 3>"],
                  "success_metric": "<how to measure success>"
              }}
          ],
          "financial_stabilization": [
              {{
                  "action": "<cash flow improvement action>",
                  "impact": <dollar amount improvement>,
                  "timeline": "<implementation time>",
                  "difficulty": "<easy/medium/hard>",
                  "resources_needed": ["<resource 1>", "<resource 2>"]
              }}
          ],
          "operational_improvements": [
              {{
                  "improvement": "<specific operational change>",
                  "cost_savings": <annual dollar savings>,
                  "implementation_cost": <upfront cost>,
                  "payback_period": "<time to break even>",
                  "priority": "<high/medium/low>"
              }}
          ],
          "risk_mitigation": [
              {{
                  "risk": "<specific risk to address>",
                  "mitigation_action": "<action to take>",
                  "cost": <implementation cost>,
                  "risk_reduction": "<percentage risk reduction>"
              }}
          ],
          "quick_wins": [
              {{
                  "action": "<easy to implement action>",
                  "benefit": "<specific benefit>",
                  "timeline": "<days to complete>",
                  "effort_required": "<low/medium/high>"
              }}
          ],
          "monitoring_checklist": [
              "<daily metric to track>",
              "<weekly review item>",
              "<monthly assessment>"
          ]
      }}
      
      Focus on actions that can be implemented immediately with available resources.
      Prioritize cash flow improvement and risk reduction given current economic conditions.
      """

   @staticmethod
   def get_strategic_actions_prompt(analysis_result: Dict[str, Any],
                                  business_data: Dict[str, Any],
                                  economic_data: Dict[str, Any]) -> str:
       """Generate prompt for strategic action recommendations."""
       
       return f"""
       EXPERT STRATEGIC BUSINESS CONSULTANT ROLE:
       
       Develop strategic action recommendations (3-12 month horizon) for this US small business.
       
       STRATEGIC CONTEXT:
       - Business Maturity: {business_data.get('years_in_business', 0)} years in operation
       - Growth Potential: {analysis_result.get('growth_analysis', {}).get('growth_score', 'N/A')}/100
       - Market Position: {analysis_result.get('market_position', {}).get('performance_category', 'N/A')}
       - Expansion Readiness: {analysis_result.get('growth_analysis', {}).get('expansion_readiness', {}).get('readiness_level', 'N/A')}
       
       INVESTMENT CAPACITY:
       - Available Capital: ${business_data.get('current_cash', 0):,.0f}
       - Monthly Cash Generation: ${analysis_result.get('financial_health', {}).get('monthly_cash_flow', 0):,.0f}
       - Debt Capacity: ${analysis_result.get('financial_health', {}).get('debt_capacity', 0):,.0f}
       
       ECONOMIC STRATEGIC FACTORS:
       - Economic Environment: {economic_data.get('small_business_impact', {}).get('overall_impact', 'N/A')}
       - Interest Rate Environment: {economic_data.get('fed_funds_rate', 'N/A')}%
       - Business Climate Score: {economic_data.get('business_climate_score', 'N/A')}/100
       
       GENERATE STRATEGIC ACTION PLAN IN JSON FORMAT:
       {{
           "growth_initiatives": [
               {{
                   "initiative": "<specific growth strategy>",
                   "objective": "<measurable goal>",
                   "timeline": "<3-12 months>",
                   "investment_required": <total dollar amount>,
                   "expected_roi": <percentage return>,
                   "success_probability": <percentage>,
                   "market_timing": "<excellent/good/fair/poor>",
                   "implementation_phases": [
                       {{
                           "phase": "<phase name>",
                           "duration": "<months>",
                           "investment": <dollar amount>,
                           "milestones": ["<milestone 1>", "<milestone 2>"]
                       }}
                   ]
               }}
           ],
           "market_positioning": [
               {{
                   "strategy": "<positioning strategy>",
                   "target_market": "<specific target>",
                   "competitive_advantage": "<key differentiator>",
                   "marketing_investment": <dollar amount>,
                   "timeline_to_impact": "<months>",
                   "success_metrics": ["<metric 1>", "<metric 2>"]
               }}
           ],
           "operational_scaling": [
               {{
                   "area": "<operations/technology/people/processes>",
                   "improvement": "<specific enhancement>",
                   "capacity_increase": "<percentage improvement>",
                   "investment": <dollar amount>,
                   "roi_timeline": "<months to payback>",
                   "implementation_complexity": "<low/medium/high>"
               }}
           ],
           "financial_optimization": [
               {{
                   "strategy": "<financial strategy>",
                   "objective": "<specific financial goal>",
                   "annual_impact": <dollar amount>,
                   "implementation_cost": <dollar amount>,
                   "risk_level": "<low/medium/high>",
                   "regulatory_considerations": ["<consideration 1>", "<consideration 2>"]
               }}
           ],
           "technology_investments": [
               {{
                   "technology": "<specific technology>",
                   "business_benefit": "<operational improvement>",
                   "cost": <implementation cost>,
                   "annual_savings": <dollar savings>,
                   "competitive_advantage": "<advantage gained>",
                   "implementation_timeline": "<months>"
               }}
           ],
           "strategic_partnerships": [
               {{
                   "partnership_type": "<supplier/distributor/strategic>",
                   "objective": "<partnership goal>",
                   "potential_partners": ["<partner type 1>", "<partner type 2>"],
                   "expected_benefit": "<quantified benefit>",
                   "timeline_to_establish": "<months>"
               }}
           ],
           "risk_management": [
               {{
                   "strategic_risk": "<long-term risk>",
                   "mitigation_strategy": "<comprehensive strategy>",
                   "investment_required": <dollar amount>,
                   "timeline": "<implementation period>",
                   "risk_reduction": "<percentage reduction>"
               }}
           ],
           "success_framework": {{
               "quarterly_milestones": ["<Q1 milestone>", "<Q2 milestone>", "<Q3 milestone>", "<Q4 milestone>"],
               "key_performance_indicators": ["<KPI 1>", "<KPI 2>", "<KPI 3>"],
               "review_schedule": "<monthly/quarterly review process>",
               "adjustment_triggers": ["<trigger 1>", "<trigger 2>"]
           }}
       }}
       
       Focus on strategies that build sustainable competitive advantages and long-term value.
       Consider current economic conditions and their impact on strategy timing and execution.
       """

   @staticmethod
   def get_investment_recommendations_prompt(analysis_result: Dict[str, Any],
                                           business_data: Dict[str, Any],
                                           economic_data: Dict[str, Any]) -> str:
       """Generate prompt for investment recommendations."""
       
       available_capital = max(0, business_data.get('current_cash', 0) - (business_data.get('monthly_expenses', 0) * 3))
       
       return f"""
       EXPERT SMALL BUSINESS INVESTMENT ADVISOR ROLE:
       
       Provide comprehensive investment recommendations for this US small business owner.
       
       INVESTOR PROFILE:
       - Business Owner with {business_data.get('years_in_business', 0)} years experience
       - Sector Expertise: {business_data.get('sector', 'N/A')}
       - Available Investment Capital: ${available_capital:,.0f}
       - Monthly Business Cash Flow: ${analysis_result.get('financial_health', {}).get('monthly_cash_flow', 0):,.0f}
       - Risk Tolerance: {RecommendationPromptTemplates._assess_risk_tolerance(analysis_result, business_data)}
       
       BUSINESS INVESTMENT CAPACITY:
       - Cash Position: ${business_data.get('current_cash', 0):,.0f}
       - Debt Capacity: ${analysis_result.get('financial_health', {}).get('debt_capacity', 0):,.0f}
       - Business Health Score: {analysis_result.get('financial_health', {}).get('health_score', 'N/A')}/100
       
       CURRENT ECONOMIC ENVIRONMENT:
       - Fed Funds Rate: {economic_data.get('fed_funds_rate', 'N/A')}%
       - Inflation Rate: {economic_data.get('inflation_cpi', 'N/A')}
       - Market Conditions: {economic_data.get('small_business_impact', {}).get('overall_impact', 'N/A')}
       - Bond Yields: Estimated {(economic_data.get('fed_funds_rate', 5) + 1):.1f}% for 10-year Treasury
       
       PROVIDE INVESTMENT RECOMMENDATIONS IN JSON FORMAT:
       {{
           "investment_strategy": {{
               "overall_approach": "<conservative/balanced/growth/aggressive>",
               "time_horizon": "<short/medium/long term focus>",
               "diversification_principle": "<strategy description>",
               "risk_management": "<risk management approach>"
           }},
           "asset_allocation": {{
               "business_reinvestment": {{
                   "percentage": <percentage of available capital>,
                   "amount": <dollar amount>,
                   "rationale": "<why this allocation>",
                   "expected_return": <percentage annual return>
               }},
               "emergency_reserve": {{
                   "percentage": <percentage>,
                   "amount": <dollar amount>,
                   "vehicle": "<high-yield savings/money market>",
                   "target_months_coverage": <months of expenses>
               }},
               "market_investments": {{
                   "percentage": <percentage>,
                   "amount": <dollar amount>,
                   "risk_level": "<conservative/moderate/aggressive>",
                   "expected_annual_return": <percentage>
               }},
               "alternative_investments": {{
                   "percentage": <percentage>,
                   "amount": <dollar amount>,
                   "types": ["<investment type 1>", "<investment type 2>"]
               }}
           }},
           "specific_recommendations": [
               {{
                   "investment_type": "<stocks/bonds/ETFs/business_expansion/real_estate>",
                   "allocation_amount": <dollar amount>,
                   "specific_vehicles": ["<specific investment 1>", "<specific investment 2>"],
                   "rationale": "<why this investment fits>",
                   "expected_return": <annual percentage return>,
                   "risk_level": "<low/medium/high>",
                   "liquidity": "<high/medium/low>",
                   "tax_implications": "<tax considerations>"
               }}
           ],
           "sector_specific_investments": [
               {{
                   "investment": "<sector-related investment opportunity>",
                   "amount": <dollar amount>,
                   "strategic_value": "<how it complements business>",
                   "risk_correlation": "<correlation with business risk>",
                   "expected_return": <percentage>
               }}
           ],
           "retirement_planning": {{
               "recommended_contribution": <annual dollar amount>,
               "vehicle": "<SEP-IRA/Solo 401k/Simple IRA>",
               "tax_benefit": <annual tax savings>,
               "catch_up_potential": <additional if age 50+>
           }},
           "tax_optimization": [
               {{
                   "strategy": "<tax strategy>",
                   "annual_savings": <dollar amount>,
                   "implementation": "<how to implement>",
                   "compliance_requirements": ["<requirement 1>", "<requirement 2>"]
               }}
           ],
           "economic_hedging": [
               {{
                   "economic_risk": "<inflation/recession/interest_rate>",
                   "hedge_strategy": "<specific hedging approach>",
                   "allocation": <dollar amount>,
                   "effectiveness": "<hedge effectiveness>"
               }}
           ],
           "monitoring_framework": {{
               "review_frequency": "<monthly/quarterly/annual>",
               "rebalancing_triggers": ["<trigger 1>", "<trigger 2>"],
               "performance_benchmarks": ["<benchmark 1>", "<benchmark 2>"],
               "adjustment_criteria": ["<criteria 1>", "<criteria 2>"]
           }},
           "implementation_timeline": [
               {{
                   "phase": "<immediate/30_days/90_days>",
                   "actions": ["<action 1>", "<action 2>"],
                   "investment_amount": <dollar amount>,
                   "priority": "<high/medium/low>"
               }}
           ]
       }}
       
       Ensure all recommendations are appropriate for small business owners and current economic conditions.
       Consider the correlation between business risk and investment risk for proper diversification.
       """

   @staticmethod
   def _assess_risk_tolerance(analysis_result: Dict[str, Any], business_data: Dict[str, Any]) -> str:
       """Assess risk tolerance based on business situation."""
       
       # Conservative factors
       conservative_factors = 0
       
       # Cash runway
       cash_runway = analysis_result.get('financial_health', {}).get('cash_runway_months', 6)
       if cash_runway < 6:
           conservative_factors += 2
       elif cash_runway < 3:
           conservative_factors += 3
       
       # Years in business
       years = business_data.get('years_in_business', 0)
       if years < 3:
           conservative_factors += 1
       elif years > 10:
           conservative_factors -= 1
       
       # Financial health
       health_score = analysis_result.get('financial_health', {}).get('health_score', 50)
       if health_score < 50:
           conservative_factors += 2
       elif health_score > 80:
           conservative_factors -= 1
       
       # Risk assessment
       risk_score = analysis_result.get('risk_assessment', {}).get('overall_risk_score', 50)
       if risk_score > 70:
           conservative_factors += 2
       elif risk_score < 30:
           conservative_factors -= 1
       
       # Determine risk tolerance
       if conservative_factors >= 5:
           return "very_conservative"
       elif conservative_factors >= 3:
           return "conservative"
       elif conservative_factors >= 1:
           return "moderate"
       elif conservative_factors <= -2:
           return "aggressive"
       else:
           return "balanced"


class ActionPlanPromptTemplates:
   """Prompt templates for generating action plans."""
   
   @staticmethod
   def get_action_plan_prompt(analysis_result: Dict[str, Any],
                             business_data: Dict[str, Any],
                             economic_data: Dict[str, Any]) -> str:
       """Generate comprehensive action plan prompt."""
       
       return f"""
       EXPERT BUSINESS ACTION PLANNER ROLE:
       
       Create a comprehensive, prioritized action plan for this US small business based on analysis results.
       
       BUSINESS SITUATION SUMMARY:
       - Overall Score: {analysis_result.get('overall_score', {}).get('overall_score', 'N/A')}/100
       - Critical Areas: {', '.join(analysis_result.get('overall_score', {}).get('improvement_areas', []))}
       - Key Strengths: {', '.join(analysis_result.get('overall_score', {}).get('strengths', []))}
       - Available Resources: ${business_data.get('current_cash', 0):,.0f} cash, {business_data.get('employees_count', 0)} employees
       
       ECONOMIC TIMING FACTORS:
       - Economic Environment: {economic_data.get('small_business_impact', {}).get('overall_impact', 'N/A')}
       - Fed Rate: {economic_data.get('fed_funds_rate', 'N/A')}% (affecting borrowing costs)
       - Business Climate: {economic_data.get('business_climate_score', 'N/A')}/100
       
       CREATE COMPREHENSIVE ACTION PLAN IN JSON FORMAT:
       {{
           "action_plan_overview": {{
               "primary_objective": "<main goal for next 12 months>",
               "success_definition": "<how success will be measured>",
               "resource_allocation": "<how resources will be prioritized>",
               "timeline_overview": "<general timeline structure>"
           }},
           "immediate_actions": [
               {{
                   "action_id": "<unique identifier>",
                   "action": "<specific action to take>",
                   "category": "<financial/operational/marketing/strategic>",
                   "priority": "<critical/high/medium/low>",
                   "urgency": "<immediate/this_week/this_month>",
                   "owner": "<who is responsible>",
                   "deadline": "<specific date or timeframe>",
                   "cost": <implementation cost>,
                   "expected_benefit": <dollar amount or percentage improvement>,
                   "success_metric": "<how to measure completion>",
                   "dependencies": ["<dependency 1>", "<dependency 2>"],
                   "implementation_steps": [
                       "<step 1>",
                       "<step 2>",
                       "<step 3>"
                   ]
               }}
           ],
           "short_term_actions": [
               {{
                   "action_id": "<unique identifier>",
                   "action": "<30-90 day action>",
                   "category": "<category>",
                   "priority": "<priority level>",
                   "timeline": "<30/60/90 days>",
                   "investment_required": <dollar amount>,
                   "roi_projection": <return on investment>,
                   "risk_level": "<low/medium/high>",
                   "success_probability": <percentage>,
                   "milestone_checkpoints": ["<checkpoint 1>", "<checkpoint 2>"]
               }}
           ],
           "medium_term_initiatives": [
               {{
                   "initiative": "<3-12 month initiative>",
                   "strategic_objective": "<alignment with business strategy>",
                   "total_investment": <dollar amount>,
                   "expected_return": <dollar amount or percentage>,
                   "timeline": "<months to complete>",
                   "resource_requirements": {{
                       "financial": <dollar amount>,
                       "human": "<staffing needs>",
                       "operational": "<operational changes needed>"
                   }},
                   "phases": [
                       {{
                           "phase": "<phase name>",
                           "duration": "<months>",
                           "key_deliverables": ["<deliverable 1>", "<deliverable 2>"],
                           "investment": <phase cost>
                       }}
                   ]
               }}
           ],
           "performance_tracking": {{
               "daily_metrics": ["<metric 1>", "<metric 2>"],
               "weekly_reviews": ["<review item 1>", "<review item 2>"],
               "monthly_assessments": ["<assessment 1>", "<assessment 2>"],
               "quarterly_evaluations": ["<evaluation 1>", "<evaluation 2>"],
               "annual_goals": ["<goal 1>", "<goal 2>"]
           }},
           "risk_monitoring": [
               {{
                   "risk": "<specific risk to monitor>",
                   "monitoring_frequency": "<daily/weekly/monthly>",
                   "early_warning_indicators": ["<indicator 1>", "<indicator 2>"],
                   "contingency_actions": ["<action 1>", "<action 2>"]
               }}
           ],
           "resource_allocation": {{
               "budget_breakdown": {{
                   "operations": <percentage>,
                   "growth_investments": <percentage>,
                   "emergency_reserves": <percentage>,
                   "marketing": <percentage>,
                   "technology": <percentage>
               }},
               "human_resource_plan": {{
                   "current_capacity": "<assessment of current team>",
                   "hiring_needs": ["<role 1>", "<role 2>"],
                   "training_requirements": ["<training 1>", "<training 2>"],
                   "timeline": "<hiring/training timeline>"
               }}
           }},
           "success_milestones": [
               {{
                   "milestone": "<specific milestone>",
                   "target_date": "<date>",
                   "success_criteria": "<measurable criteria>",
                   "celebration_plan": "<how to acknowledge achievement>"
               }}
           ],
           "contingency_planning": [
               {{
                   "scenario": "<potential challenge scenario>",
                   "probability": <percentage likelihood>,
                   "impact": "<high/medium/low>",
                   "response_plan": ["<response action 1>", "<response action 2>"],
                   "trigger_indicators": ["<trigger 1>", "<trigger 2>"]
               }}
           ],
           "review_and_adjustment": {{
               "review_schedule": "<how often to review plan>",
               "adjustment_criteria": ["<criteria for plan changes>"],
               "stakeholder_communication": "<how to communicate changes>",
               "learning_integration": "<how to incorporate lessons learned>"
           }}
       }}
       
       Ensure the action plan is realistic, properly sequenced, and accounts for business constraints and economic conditions.
       Make all actions specific, measurable, achievable, relevant, and time-bound (SMART).
       """