"""AI-powered insight generation engine for US small business intelligence."""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

from app.services.multi_gemini_service import MultiGeminiEngine
from app.utils.prompt_templates import InsightPromptTemplates

logger = logging.getLogger(__name__)


class USInsightGenerator:
    """Advanced AI insight generation for US small businesses."""
    
    def __init__(self):
        self.ai_engine = MultiGeminiEngine()
        self.prompt_templates = InsightPromptTemplates()
        
        # Insight categories and their weights
        self.insight_categories = {
            "financial_performance": 0.25,
            "market_opportunity": 0.20,
            "operational_efficiency": 0.20,
            "economic_impact": 0.15,
            "competitive_advantage": 0.10,
            "risk_mitigation": 0.10
        }
    
    async def generate_main_insight(self, analysis_result: Dict[str, Any], 
                                  business_data: Dict[str, Any],
                                  economic_data: Dict[str, Any] = None,
                                  market_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate the primary business insight with highest impact."""
        
        logger.info("Generating main business insight")
        
        try:
            # Identify the most critical area needing attention
            critical_area = self._identify_critical_area(analysis_result, business_data)
            
            # Generate targeted insight for the critical area
            insight_prompt = self.prompt_templates.get_main_insight_prompt(
                critical_area, analysis_result, business_data, economic_data, market_data
            )
            
            insight_response = await self.ai_engine._make_gemini_request(
                self.ai_engine.get_optimal_key("business_analysis"),
                insight_prompt,
                "main_insight"
            )
            
            # Structure the main insight
            main_insight = {
                "insight_id": f"main_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "insight_type": "primary",
                "category": critical_area,
                "urgency": self._calculate_urgency(analysis_result, critical_area),
                "title": insight_response.get("title", "Key Business Insight"),
                "main_message": insight_response.get("main_message", ""),
                "supporting_facts": insight_response.get("supporting_facts", []),
                "recommended_actions": insight_response.get("recommended_actions", []),
                "potential_impact": insight_response.get("potential_impact", {}),
                "confidence_level": insight_response.get("confidence_level", 80),
                "economic_context": self._add_economic_context(economic_data),
                "generated_at": datetime.now().isoformat()
            }
            
            logger.info(f"Generated main insight: {main_insight['title']}")
            return main_insight
            
        except Exception as e:
            logger.error(f"Failed to generate main insight: {str(e)}")
            return self._create_fallback_insight("main", str(e))
    
    async def generate_problem_insights(self, analysis_result: Dict[str, Any],
                                      business_data: Dict[str, Any],
                                      economic_data: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Generate insights about current business problems and challenges."""
        
        logger.info("Generating problem insights")
        
        try:
            # Identify key problems
            problems = self._identify_key_problems(analysis_result, business_data)
            
            problem_insights = []
            
            for problem in problems[:3]:  # Top 3 problems
                insight_prompt = self.prompt_templates.get_problem_insight_prompt(
                    problem, analysis_result, business_data, economic_data
                )
                
                insight_response = await self.ai_engine._make_gemini_request(
                    self.ai_engine.get_optimal_key("business_analysis"),
                    insight_prompt,
                    "problem_insight"
                )
                
                problem_insight = {
                    "insight_id": f"problem_{problem['type']}_{datetime.now().strftime('%H%M%S')}",
                    "insight_type": "problem",
                    "category": problem["type"],
                    "urgency": problem.get("urgency", "medium"),
                    "title": insight_response.get("title", f"{problem['type'].title()} Challenge"),
                    "problem_description": insight_response.get("problem_description", ""),
                    "root_causes": insight_response.get("root_causes", []),
                    "impact_analysis": insight_response.get("impact_analysis", {}),
                    "solution_approaches": insight_response.get("solution_approaches", []),
                    "prevention_strategies": insight_response.get("prevention_strategies", []),
                    "confidence_level": insight_response.get("confidence_level", 75),
                    "generated_at": datetime.now().isoformat()
                }
                
                problem_insights.append(problem_insight)
            
            logger.info(f"Generated {len(problem_insights)} problem insights")
            return problem_insights
            
        except Exception as e:
            logger.error(f"Failed to generate problem insights: {str(e)}")
            return [self._create_fallback_insight("problem", str(e))]
    
    async def generate_opportunity_insights(self, analysis_result: Dict[str, Any],
                                          business_data: Dict[str, Any],
                                          economic_data: Dict[str, Any] = None,
                                          market_data: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Generate insights about business opportunities and growth potential."""
        
        logger.info("Generating opportunity insights")
        
        try:
            # Identify growth opportunities
            opportunities = self._identify_growth_opportunities(
                analysis_result, business_data, economic_data, market_data
            )
            
            opportunity_insights = []
            
            for opportunity in opportunities[:3]:  # Top 3 opportunities
                insight_prompt = self.prompt_templates.get_opportunity_insight_prompt(
                    opportunity, analysis_result, business_data, economic_data, market_data
                )
                
                insight_response = await self.ai_engine._make_gemini_request(
                    self.ai_engine.get_optimal_key("market_intelligence"),
                    insight_prompt,
                    "opportunity_insight"
                )
                
                opportunity_insight = {
                    "insight_id": f"opportunity_{opportunity['type']}_{datetime.now().strftime('%H%M%S')}",
                    "insight_type": "opportunity",
                    "category": opportunity["type"],
                    "priority": opportunity.get("priority", "medium"),
                    "title": insight_response.get("title", f"{opportunity['type'].title()} Opportunity"),
                    "opportunity_description": insight_response.get("opportunity_description", ""),
                    "market_potential": insight_response.get("market_potential", {}),
                    "implementation_strategy": insight_response.get("implementation_strategy", []),
                    "resource_requirements": insight_response.get("resource_requirements", {}),
                    "timeline_to_value": insight_response.get("timeline_to_value", ""),
                    "success_probability": insight_response.get("success_probability", 0),
                    "competitive_advantages": insight_response.get("competitive_advantages", []),
                    "confidence_level": insight_response.get("confidence_level", 75),
                    "generated_at": datetime.now().isoformat()
                }
                
                opportunity_insights.append(opportunity_insight)
            
            logger.info(f"Generated {len(opportunity_insights)} opportunity insights")
            return opportunity_insights
            
        except Exception as e:
            logger.error(f"Failed to generate opportunity insights: {str(e)}")
            return [self._create_fallback_insight("opportunity", str(e))]
    
    async def generate_market_insights(self, business_data: Dict[str, Any],
                                     market_data: Dict[str, Any],
                                     economic_data: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Generate insights about market conditions and competitive landscape."""
        
        logger.info("Generating market insights")
        
        try:
            market_insights = []
            
            # Market position insight
            position_prompt = self.prompt_templates.get_market_position_insight_prompt(
                business_data, market_data, economic_data
            )
            
            position_response = await self.ai_engine._make_gemini_request(
                self.ai_engine.get_optimal_key("market_intelligence"),
                position_prompt,
                "market_position"
            )
            
            position_insight = {
                "insight_id": f"market_position_{datetime.now().strftime('%H%M%S')}",
                "insight_type": "market",
                "category": "market_position",
                "urgency": "medium",
                "title": position_response.get("title", "Market Position Analysis"),
                "position_analysis": position_response.get("position_analysis", {}),
                "competitive_dynamics": position_response.get("competitive_dynamics", []),
                "market_trends": position_response.get("market_trends", []),
                "positioning_recommendations": position_response.get("positioning_recommendations", []),
                "confidence_level": position_response.get("confidence_level", 80),
                "generated_at": datetime.now().isoformat()
            }
            
            market_insights.append(position_insight)
            
            # Economic impact insight
            if economic_data:
                economic_prompt = self.prompt_templates.get_economic_impact_insight_prompt(
                    business_data, economic_data
                )
                
                economic_response = await self.ai_engine._make_gemini_request(
                    self.ai_engine.get_optimal_key("business_analysis"),
                    economic_prompt,
                    "economic_impact"
                )
                
                economic_insight = {
                    "insight_id": f"economic_impact_{datetime.now().strftime('%H%M%S')}",
                    "insight_type": "market",
                    "category": "economic_impact",
                    "urgency": "high",
                    "title": economic_response.get("title", "Economic Environment Impact"),
                    "impact_analysis": economic_response.get("impact_analysis", {}),
                    "sector_implications": economic_response.get("sector_implications", []),
                    "adaptation_strategies": economic_response.get("adaptation_strategies", []),
                    "timing_considerations": economic_response.get("timing_considerations", {}),
                    "confidence_level": economic_response.get("confidence_level", 85),
                    "generated_at": datetime.now().isoformat()
                }
                
                market_insights.append(economic_insight)
            
            logger.info(f"Generated {len(market_insights)} market insights")
            return market_insights
            
        except Exception as e:
            logger.error(f"Failed to generate market insights: {str(e)}")
            return [self._create_fallback_insight("market", str(e))]
    
    async def generate_strategic_insights(self, analysis_result: Dict[str, Any],
                                        business_data: Dict[str, Any],
                                        economic_data: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Generate strategic insights for long-term business success."""
        
        logger.info("Generating strategic insights")
        
        try:
            strategic_insights = []
            
            # Growth strategy insight
            growth_prompt = self.prompt_templates.get_growth_strategy_insight_prompt(
                analysis_result, business_data, economic_data
            )
            
            growth_response = await self.ai_engine._make_gemini_request(
                self.ai_engine.get_optimal_key("recommendations"),
                growth_prompt,
                "growth_strategy"
            )
            
            growth_insight = {
                "insight_id": f"growth_strategy_{datetime.now().strftime('%H%M%S')}",
                "insight_type": "strategic",
                "category": "growth_strategy",
                "priority": "high",
                "title": growth_response.get("title", "Growth Strategy Direction"),
                "strategy_analysis": growth_response.get("strategy_analysis", {}),
                "growth_vectors": growth_response.get("growth_vectors", []),
                "resource_allocation": growth_response.get("resource_allocation", {}),
                "milestone_framework": growth_response.get("milestone_framework", []),
                "risk_considerations": growth_response.get("risk_considerations", []),
                "confidence_level": growth_response.get("confidence_level", 80),
                "generated_at": datetime.now().isoformat()
            }
            
            strategic_insights.append(growth_insight)
            
            # Competitive strategy insight
            competitive_prompt = self.prompt_templates.get_competitive_strategy_insight_prompt(
                analysis_result, business_data
            )
            
            competitive_response = await self.ai_engine._make_gemini_request(
                self.ai_engine.get_optimal_key("market_intelligence"),
                competitive_prompt,
                "competitive_strategy"
            )
            
            competitive_insight = {
                "insight_id": f"competitive_strategy_{datetime.now().strftime('%H%M%S')}",
                "insight_type": "strategic",
                "category": "competitive_strategy",
                "priority": "medium",
                "title": competitive_response.get("title", "Competitive Strategy Framework"),
                "competitive_analysis": competitive_response.get("competitive_analysis", {}),
                "differentiation_opportunities": competitive_response.get("differentiation_opportunities", []),
                "competitive_moves": competitive_response.get("competitive_moves", []),
                "defensive_strategies": competitive_response.get("defensive_strategies", []),
                "confidence_level": competitive_response.get("confidence_level", 75),
                "generated_at": datetime.now().isoformat()
            }
            
            strategic_insights.append(competitive_insight)
            
            logger.info(f"Generated {len(strategic_insights)} strategic insights")
            return strategic_insights
            
        except Exception as e:
            logger.error(f"Failed to generate strategic insights: {str(e)}")
            return [self._create_fallback_insight("strategic", str(e))]
    
    def _identify_critical_area(self, analysis_result: Dict[str, Any], 
                               business_data: Dict[str, Any]) -> str:
        """Identify the most critical area requiring immediate attention."""
        
        # Calculate scores for different areas
        area_scores = {}
        
        # Financial health score
        financial_health = analysis_result.get("financial_health", {})
        health_score = financial_health.get("health_score", 50)
        area_scores["financial_performance"] = 100 - health_score  # Lower health = higher urgency
        
        # Cash flow urgency
        cash_runway = financial_health.get("cash_runway_months", 6)
        if cash_runway < 3:
            area_scores["financial_performance"] += 30
        
        # Market position concerns
        market_position = analysis_result.get("market_position", {})
        performance_ratio = market_position.get("performance_ratio", 1.0)
        if performance_ratio < 0.7:
            area_scores["market_opportunity"] = 80
        
        # Growth stagnation
        performance_metrics = analysis_result.get("performance_metrics", {})
        growth_rate = performance_metrics.get("revenue_growth_rate", 0)
        if growth_rate < 0:
            area_scores["operational_efficiency"] = 85
        
        # Risk assessment
        risk_assessment = analysis_result.get("risk_assessment", {})
        overall_risk = risk_assessment.get("overall_risk_score", 50)
        if overall_risk > 70:
            area_scores["risk_mitigation"] = overall_risk
        
        # Economic impact
        economic_impact = analysis_result.get("economic_impact", {})
        if economic_impact.get("economic_environment") in ["strong_headwinds", "moderate_headwinds"]:
            area_scores["economic_impact"] = 70
        
        # Return the area with highest score (most urgent)
        if area_scores:
            return max(area_scores, key=area_scores.get)
        
        return "financial_performance"  # Default
    
    def _calculate_urgency(self, analysis_result: Dict[str, Any], critical_area: str) -> str:
        """Calculate urgency level for the critical area."""
        
        urgency_factors = {
            "financial_performance": self._assess_financial_urgency(analysis_result),
            "market_opportunity": self._assess_market_urgency(analysis_result),
            "operational_efficiency": self._assess_operational_urgency(analysis_result),
            "economic_impact": self._assess_economic_urgency(analysis_result),
            "risk_mitigation": self._assess_risk_urgency(analysis_result),
            "competitive_advantage": self._assess_competitive_urgency(analysis_result)
        }
        
        urgency_score = urgency_factors.get(critical_area, 50)
        
        if urgency_score >= 80:
            return "critical"
        elif urgency_score >= 60:
            return "high"
        elif urgency_score >= 40:
            return "medium"
        else:
            return "low"
    
    def _assess_financial_urgency(self, analysis_result: Dict[str, Any]) -> int:
        """Assess financial urgency score."""
        urgency = 0
        
        financial_health = analysis_result.get("financial_health", {})
        
        # Cash runway assessment
        cash_runway = financial_health.get("cash_runway_months", 6)
        if cash_runway < 1:
            urgency += 40
        elif cash_runway < 3:
            urgency += 25
        elif cash_runway < 6:
            urgency += 10
        
        # Cash flow assessment
        monthly_cash_flow = financial_health.get("monthly_cash_flow", 0)
        if monthly_cash_flow < 0:
            urgency += 30
        
        # Stress indicators
        stress_indicators = financial_health.get("stress_indicators", [])
        urgency += len(stress_indicators) * 5
        
        return min(100, urgency)
    
    def _assess_market_urgency(self, analysis_result: Dict[str, Any]) -> int:
        """Assess market urgency score."""
        urgency = 0
        
        market_position = analysis_result.get("market_position", {})
        
        # Performance ratio
        performance_ratio = market_position.get("performance_ratio", 1.0)
        if performance_ratio < 0.5:
            urgency += 40
        elif performance_ratio < 0.7:
            urgency += 25
        elif performance_ratio < 0.9:
            urgency += 10
        
        # Market context
        market_context = market_position.get("market_context", {})
        competitive_intensity = market_context.get("competitive_intensity", 0.5)
        urgency += competitive_intensity * 30
        
        return min(100, urgency)
    
    def _assess_operational_urgency(self, analysis_result: Dict[str, Any]) -> int:
        """Assess operational urgency score."""
        urgency = 0
        
        performance_metrics = analysis_result.get("performance_metrics", {})
        
        # Revenue trend
        revenue_growth = performance_metrics.get("revenue_growth_rate", 0)
        if revenue_growth < -0.1:  # 10% decline
            urgency += 35
        elif revenue_growth < 0:
            urgency += 20
        
        # Efficiency score
        efficiency_score = performance_metrics.get("financial_efficiency_score", 50)
        if efficiency_score < 30:
            urgency += 25
        elif efficiency_score < 50:
            urgency += 15
        
        return min(100, urgency)
    
    def _assess_economic_urgency(self, analysis_result: Dict[str, Any]) -> int:
        """Assess economic environment urgency score."""
        urgency = 0
        
        economic_impact = analysis_result.get("economic_impact", {})
        
        # Economic environment
        environment = economic_impact.get("economic_environment", "neutral")
        if environment == "strong_headwinds":
            urgency += 40
        elif environment == "moderate_headwinds":
            urgency += 25
        
        # Economic impact score
        impact_score = economic_impact.get("overall_impact_score", 0)
        if impact_score < -20:
            urgency += 30
        elif impact_score < 0:
            urgency += 15
        
        return min(100, urgency)
    
    def _assess_risk_urgency(self, analysis_result: Dict[str, Any]) -> int:
        """Assess risk urgency score."""
        urgency = 0
        
        risk_assessment = analysis_result.get("risk_assessment", {})
        
        # Overall risk score
        overall_risk = risk_assessment.get("overall_risk_score", 50)
        if overall_risk > 80:
            urgency += 40
        elif overall_risk > 60:
            urgency += 25
        
        # Key vulnerabilities
        vulnerabilities = risk_assessment.get("key_vulnerabilities", [])
        urgency += len(vulnerabilities) * 10
        
        return min(100, urgency)
    
    def _assess_competitive_urgency(self, analysis_result: Dict[str, Any]) -> int:
        """Assess competitive urgency score."""
        urgency = 0
        
        competitive_analysis = analysis_result.get("competitive_analysis", {})
        
        # Competitive weaknesses
        weaknesses = competitive_analysis.get("competitive_weaknesses", [])
        urgency += len(weaknesses) * 10
        
        # Market share
        market_share = competitive_analysis.get("estimated_market_share", 5)
        if market_share < 1:
            urgency += 30
        elif market_share < 3:
            urgency += 15
        
        return min(100, urgency)
    
    def _identify_key_problems(self, analysis_result: Dict[str, Any],
                              business_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify key business problems requiring attention."""
        
        problems = []
        
        # Financial problems
        financial_health = analysis_result.get("financial_health", {})
        if financial_health.get("cash_runway_months", 6) < 3:
            problems.append({
                "type": "cash_flow",
                "urgency": "critical",
                "severity": "high",
                "data": financial_health
            })
        
        if financial_health.get("monthly_cash_flow", 0) < 0:
            problems.append({
                "type": "profitability",
                "urgency": "high",
                "severity": "high",
                "data": financial_health
            })
        
        # Market problems
        market_position = analysis_result.get("market_position", {})
        if market_position.get("performance_ratio", 1.0) < 0.7:
            problems.append({
                "type": "market_underperformance",
                "urgency": "medium",
                "severity": "medium",
                "data": market_position
            })
        
        # Operational problems
        performance_metrics = analysis_result.get("performance_metrics", {})
        if performance_metrics.get("revenue_growth_rate", 0) < -0.05:
            problems.append({
                "type": "revenue_decline",
                "urgency": "high",
                "severity": "high",
                "data": performance_metrics
            })
        
        # Risk problems
        risk_assessment = analysis_result.get("risk_assessment", {})
        if risk_assessment.get("overall_risk_score", 50) > 70:
            problems.append({
                "type": "high_risk_exposure",
                "urgency": "medium",
                "severity": "medium",
                "data": risk_assessment
            })
        
        # Sort by urgency and severity
        urgency_order = {"critical": 4, "high": 3, "medium": 2, "low": 1}
        problems.sort(key=lambda x: urgency_order.get(x["urgency"], 1), reverse=True)
        
        return problems
    
    def _identify_growth_opportunities(self, analysis_result: Dict[str, Any],
                                     business_data: Dict[str, Any],
                                     economic_data: Dict[str, Any] = None,
                                     market_data: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Identify growth opportunities for the business."""
        
        opportunities = []
        
        # Market expansion opportunities
        market_position = analysis_result.get("market_position", {})
        if market_position.get("performance_ratio", 1.0) > 1.2:
            opportunities.append({
                "type": "market_expansion",
                "priority": "high",
                "potential": "high",
                "data": market_position
            })
        
        # Operational efficiency opportunities
        performance_metrics = analysis_result.get("performance_metrics", {})
        efficiency_score = performance_metrics.get("financial_efficiency_score", 50)
        if efficiency_score < 70:
            opportunities.append({
                "type": "operational_efficiency",
                "priority": "medium",
                "potential": "medium",
                "data": performance_metrics
            })
        
        # Technology adoption opportunities
        sector = business_data.get("sector", "")
        if sector in ["retail", "food", "electronics"]:
            opportunities.append({
                "type": "digital_transformation",
                "priority": "medium",
                "potential": "high",
                "data": {"sector": sector}
            })
        
        # Economic tailwind opportunities
        if economic_data:
            economic_impact = analysis_result.get("economic_impact", {})
            if economic_impact.get("overall_impact_score", 0) > 10:
                opportunities.append({
                    "type": "economic_timing",
                    "priority": "high",
                    "potential": "medium",
                    "data": economic_impact
                })
        
        # Investment opportunities
        financial_health = analysis_result.get("financial_health", {})
        if financial_health.get("cash_runway_months", 6) > 6:
            opportunities.append({
                "type": "strategic_investment",
                "priority": "medium",
                "potential": "high",
                "data": financial_health
            })
        
        # Sort by priority and potential
        priority_order = {"high": 3, "medium": 2, "low": 1}
        opportunities.sort(
            key=lambda x: (priority_order.get(x["priority"], 1), 
                          priority_order.get(x["potential"], 1)), 
            reverse=True
        )
        
        return opportunities
    
    def _add_economic_context(self, economic_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add relevant economic context to insights."""
        
        if not economic_data:
            return {}
        
        return {
            "fed_funds_rate": economic_data.get("fed_funds_rate"),
            "inflation_rate": economic_data.get("inflation_cpi"),
            "unemployment_rate": economic_data.get("unemployment_rate"),
            "economic_health_score": economic_data.get("economic_health_score"),
            "small_business_impact": economic_data.get("small_business_impact", {}).get("overall_impact"),
            "context_summary": f"Current Fed rate at {economic_data.get('fed_funds_rate', 'N/A')}%, "
                             f"inflation at {economic_data.get('inflation_cpi', 'N/A')}, "
                             f"unemployment at {economic_data.get('unemployment_rate', 'N/A')}%"
        }
    
    def _create_fallback_insight(self, insight_type: str, error_message: str) -> Dict[str, Any]:
        """Create a fallback insight when AI generation fails."""
        
        return {
            "insight_id": f"fallback_{insight_type}_{datetime.now().strftime('%H%M%S')}",
            "insight_type": insight_type,
            "category": "system_generated",
            "urgency": "low",
            "title": f"Analysis {insight_type.title()} Summary",
            "main_message": "Automated analysis completed. Manual review recommended for detailed insights.",
            "supporting_facts": ["Analysis engine completed primary calculations"],
            "recommended_actions": ["Review detailed analysis results", "Consider consulting with business advisor"],
            "confidence_level": 50,
            "error_context": error_message,
            "generated_at": datetime.now().isoformat()
        }