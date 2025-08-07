"""US Market Intelligence Engine for comprehensive market analysis and insights."""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import statistics
import math

from app.core.data_pipeline import RealTimeDataPipeline
from app.services.multi_gemini_service import MultiGeminiEngine
from app.data.us_economic_factors import (
    get_current_us_economic_indicators,
    calculate_us_economic_impact,
    get_us_market_sentiment,
    project_us_economic_trends,
    get_regional_adjustment_factors,
    calculate_sector_resilience_score
)
from app.data.us_sectors import (
    get_us_sector_data,
    get_us_location_data,
    get_us_sector_location_multiplier,
    get_us_competition_level,
    calculate_us_market_opportunity_score,
    classify_us_location_type
)
from app.config import GEMINI_KEYS

logger = logging.getLogger(__name__)


class USMarketIntelligence:
    """Advanced US market intelligence engine with real-time data and AI analysis."""
    
    def __init__(self):
        self.data_pipeline = RealTimeDataPipeline()
        self.multi_gemini_engine = MultiGeminiEngine()
        
        # Cache for expensive calculations
        self._market_cache = {}
        self._cache_timestamps = {}
        self._cache_duration = 1800  # 30 minutes
    
    async def analyze_complete_market_intelligence(self, business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive US market intelligence report."""
        
        logger.info(f"Starting complete market intelligence analysis for {business_data.get('sector')} in {business_data.get('state')}")
        
        start_time = asyncio.get_event_loop().time()
        
        try:
            # Extract business context
            sector = business_data.get('sector', 'retail')
            state = business_data.get('state', 'CA')
            city = business_data.get('city', 'Los Angeles')
            zip_code = business_data.get('zip_code', '90210')
            location_type = classify_us_location_type(city, state, zip_code)
            
            # Gather all market intelligence data
            market_intelligence_data = await self._gather_market_intelligence_data(
                business_data, sector, location_type, state
            )
            
            # Use MultiGeminiEngine for comprehensive analysis
            comprehensive_analysis = await self.multi_gemini_engine.analyze_business_comprehensive(
                business_data,
                market_intelligence_data["economic_data"],
                market_intelligence_data["market_data"]
            )
            
            # Enhance with market-specific insights
            enhanced_intelligence = await self._enhance_with_market_insights(
                comprehensive_analysis,
                market_intelligence_data,
                business_data
            )
            
            execution_time = asyncio.get_event_loop().time() - start_time
            enhanced_intelligence["analysis_metadata"] = {
                "execution_time_seconds": execution_time,
                "data_sources_used": self._get_data_sources_used(),
                "analysis_completeness": self._assess_analysis_completeness(enhanced_intelligence),
                "confidence_level": comprehensive_analysis.get("confidence_level", 0.8)
            }
            
            logger.info(f"Complete market intelligence analysis completed in {execution_time:.2f}s")
            return enhanced_intelligence
            
        except Exception as e:
            logger.error(f"Error in complete market intelligence analysis: {str(e)}")
            return {
                "error": str(e),
                "analysis_timestamp": datetime.now().isoformat(),
                "execution_time": asyncio.get_event_loop().time() - start_time
            }
    
    async def _gather_market_intelligence_data(self, business_data: Dict[str, Any],
                                             sector: str, location_type: str, state: str) -> Dict[str, Any]:
        """Gather all market intelligence data for analysis."""
        
        try:
            # Parallel data collection
            data_tasks = [
                self._collect_economic_data(sector, state),
                self._collect_market_data(sector, location_type, business_data),
                self._collect_sector_data(sector, business_data),
                self._collect_consumer_data(location_type, state),
                self._collect_competitive_data(sector, location_type)
            ]
            
            # Execute all data collection in parallel
            results = await asyncio.gather(*data_tasks, return_exceptions=True)
            
            # Process results
            intelligence_data = {
                "economic_data": results[0] if not isinstance(results[0], Exception) else {},
                "market_data": results[1] if not isinstance(results[1], Exception) else {},
                "sector_data": results[2] if not isinstance(results[2], Exception) else {},
                "consumer_data": results[3] if not isinstance(results[3], Exception) else {},
                "competitive_data": results[4] if not isinstance(results[4], Exception) else {},
                "business_context": {
                    "sector": sector,
                    "location_type": location_type,
                    "state": state,
                    "analysis_timestamp": datetime.now().isoformat()
                }
            }
            
            # Add any collection errors to metadata
            errors = [str(result) for result in results if isinstance(result, Exception)]
            if errors:
                intelligence_data["collection_errors"] = errors
            
            return intelligence_data
            
        except Exception as e:
            logger.error(f"Error gathering market intelligence data: {str(e)}")
            return {"error": str(e)}
    
    async def _collect_economic_data(self, sector: str, state: str) -> Dict[str, Any]:
        """Collect US economic data relevant to the business."""
        
        try:
            # Get current economic indicators
            economic_indicators = get_current_us_economic_indicators()
            
            # Calculate economic impact on this specific business
            economic_impact = calculate_us_economic_impact(sector, {})
            
            # Get market sentiment for sector
            market_sentiment = get_us_market_sentiment(sector)
            
            # Get regional adjustments
            regional_factors = get_regional_adjustment_factors(state)
            
            # Get sector resilience data
            resilience_data = calculate_sector_resilience_score(sector)
            
            # Project economic trends
            economic_projections = project_us_economic_trends(months_ahead=12)
            
            return {
                "current_indicators": economic_indicators,
                "economic_impact": economic_impact,
                "market_sentiment": market_sentiment,
                "regional_factors": regional_factors,
                "sector_resilience": resilience_data,
                "economic_projections": economic_projections,
                "business_cycle_phase": self._determine_business_cycle_phase(economic_indicators),
                "economic_health_score": self._calculate_economic_health_score(
                    economic_indicators, economic_impact, market_sentiment
                ),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error collecting economic data: {str(e)}")
            return {"error": str(e)}
    
    async def _collect_market_data(self, sector: str, location_type: str, business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Collect market data for sector and location."""
        
        try:
            # Get sector and location data
            sector_data = get_us_sector_data(sector)
            location_data = get_us_location_data(location_type)
            
            # Calculate market opportunity
            opportunity_analysis = calculate_us_market_opportunity_score(sector, location_type, "small")
            
            # Market sizing and positioning
            market_size = self._estimate_total_addressable_market(sector, location_type, business_data)
            competitive_position = self._assess_competitive_position(business_data, sector_data)
            
            # Market trends and dynamics
            market_trends = self._analyze_market_trends(sector, location_type)
            seasonal_patterns = self._analyze_seasonal_patterns(sector)
            
            return {
                "sector_data": sector_data,
                "location_data": location_data,
                "opportunity_analysis": opportunity_analysis,
                "market_size": market_size,
                "competitive_position": competitive_position,
                "market_trends": market_trends,
                "seasonal_patterns": seasonal_patterns,
                "location_multiplier": get_us_sector_location_multiplier(sector, location_type),
                "competition_level": get_us_competition_level(sector, location_type),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error collecting market data: {str(e)}")
            return {"error": str(e)}
    
    async def _collect_sector_data(self, sector: str, business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Collect sector-specific performance data."""
        
        try:
            sector_data = get_us_sector_data(sector)
            
            # Calculate business performance vs sector
            business_revenue = sum(business_data.get('monthly_revenue', [0]))
            sector_average = sector_data["base_performance"]["average_monthly_revenue"] * 12
            performance_ratio = business_revenue / sector_average if sector_average > 0 else 0
            
            # Sector health metrics
            sector_health = self._calculate_sector_health_metrics(sector_data)
            
            # Growth trajectory analysis
            growth_trajectory = self._assess_sector_growth_trajectory(sector_data)
            
            # Disruption and technology risks
            disruption_risks = self._assess_sector_disruption_risks(sector)
            
            return {
                "sector_performance": {
                    "business_vs_sector_ratio": performance_ratio,
                    "sector_average_revenue": sector_average,
                    "market_percentile": min(100, max(0, (performance_ratio - 0.5) * 100 + 50))
                },
                "sector_health": sector_health,
                "growth_trajectory": growth_trajectory,
                "disruption_risks": disruption_risks,
                "sector_benchmarks": sector_data,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error collecting sector data: {str(e)}")
            return {"error": str(e)}
    
    async def _collect_consumer_data(self, location_type: str, state: str) -> Dict[str, Any]:
        """Collect consumer market and demographic data."""
        
        try:
            location_data = get_us_location_data(location_type)
            regional_factors = get_regional_adjustment_factors(state)
            
            # Consumer demographics and behavior
            consumer_profile = self._build_consumer_profile(location_data, regional_factors)
            
            # Spending patterns and preferences
            spending_patterns = self._analyze_consumer_spending_patterns(location_type)
            
            # Market penetration analysis
            market_penetration = self._calculate_market_penetration_potential(location_type, consumer_profile)
            
            # Customer acquisition insights
            acquisition_analysis = self._analyze_customer_acquisition(location_type, consumer_profile)
            
            return {
                "consumer_profile": consumer_profile,
                "spending_patterns": spending_patterns,
                "market_penetration": market_penetration,
                "acquisition_analysis": acquisition_analysis,
                "location_demographics": location_data,
                "regional_economic_factors": regional_factors,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error collecting consumer data: {str(e)}")
            return {"error": str(e)}
    
    async def _collect_competitive_data(self, sector: str, location_type: str) -> Dict[str, Any]:
        """Collect competitive landscape data."""
        
        try:
            # Competition intensity and structure
            competition_analysis = {
                "intensity_level": get_us_competition_level(sector, location_type),
                "market_structure": self._assess_market_structure(sector, location_type),
                "barriers_to_entry": self._assess_barriers_to_entry(sector),
                "competitive_advantages": self._identify_potential_competitive_advantages(sector, location_type)
            }
            
            # Market gaps and opportunities
            market_gaps = self._identify_market_gaps(sector, location_type)
            
            # Competitive threats and opportunities
            competitive_dynamics = self._analyze_competitive_dynamics(sector, location_type)
            
            return {
                "competition_analysis": competition_analysis,
                "market_gaps": market_gaps,
                "competitive_dynamics": competitive_dynamics,
                "differentiation_opportunities": self._identify_differentiation_opportunities(sector, location_type),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error collecting competitive data: {str(e)}")
            return {"error": str(e)}
    
    async def _enhance_with_market_insights(self, comprehensive_analysis: Dict[str, Any],
                                          market_intelligence_data: Dict[str, Any],
                                          business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance the comprehensive analysis with market-specific insights."""
        
        try:
            # Create enhanced analysis structure
            enhanced_analysis = {
                **comprehensive_analysis,
                "market_intelligence": {
                    "market_positioning": self._create_market_positioning_summary(
                        comprehensive_analysis, market_intelligence_data, business_data
                    ),
                    "competitive_landscape": self._create_competitive_landscape_summary(
                        comprehensive_analysis, market_intelligence_data
                    ),
                    "market_opportunities": self._create_market_opportunities_summary(
                        comprehensive_analysis, market_intelligence_data, business_data
                    ),
                    "economic_environment": self._create_economic_environment_summary(
                        comprehensive_analysis, market_intelligence_data
                    ),
                    "consumer_insights": self._create_consumer_insights_summary(
                        market_intelligence_data, business_data
                    ),
                    "sector_analysis": self._create_sector_analysis_summary(
                        comprehensive_analysis, market_intelligence_data
                    )
                },
                "market_scores": self._calculate_market_intelligence_scores(
                    comprehensive_analysis, market_intelligence_data
                ),
                "strategic_market_recommendations": await self._generate_strategic_market_recommendations(
                    comprehensive_analysis, market_intelligence_data, business_data
                )
            }
            
            return enhanced_analysis
            
        except Exception as e:
            logger.error(f"Error enhancing with market insights: {str(e)}")
            # Return original analysis if enhancement fails
            return comprehensive_analysis
    
    async def _generate_strategic_market_recommendations(self, comprehensive_analysis: Dict[str, Any],
                                                       market_intelligence_data: Dict[str, Any],
                                                       business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate strategic market recommendations using MultiGeminiEngine."""
        
        try:
            # Prepare market context for strategic analysis
            market_context = {
                "sector": business_data.get('sector'),
                "location_type": market_intelligence_data["business_context"]["location_type"],
                "market_opportunity_score": market_intelligence_data.get("market_data", {}).get("opportunity_analysis", {}).get("opportunity_score", 50),
                "competition_level": market_intelligence_data.get("market_data", {}).get("competition_level", "medium"),
                "economic_health": market_intelligence_data.get("economic_data", {}).get("economic_health_score", 50),
                "sector_growth": market_intelligence_data.get("sector_data", {}).get("growth_trajectory", "moderate"),
                "consumer_spending_power": market_intelligence_data.get("consumer_data", {}).get("consumer_profile", {}).get("spending_power", 1.0)
            }
            
            # Create strategic market prompt
            strategic_prompt = f"""
            EXPERT STRATEGIC MARKET CONSULTANT:
            
            Based on comprehensive business analysis and market intelligence, provide strategic market recommendations:
            
            BUSINESS ANALYSIS SUMMARY:
            - Overall Health Score: {comprehensive_analysis.get('executive_summary', {}).get('overall_health_score', 'N/A')}/100
            - Competitive Position: {comprehensive_analysis.get('executive_summary', {}).get('competitive_position', 'N/A')}
            - Growth Trajectory: {comprehensive_analysis.get('executive_summary', {}).get('growth_trajectory', 'N/A')}
            
            MARKET INTELLIGENCE:
            - Market Opportunity Score: {market_context['market_opportunity_score']}/100
            - Competition Level: {market_context['competition_level']}
            - Economic Health: {market_context['economic_health']}/100
            - Sector Growth: {market_context['sector_growth']}
            
            PROVIDE STRATEGIC MARKET RECOMMENDATIONS IN JSON FORMAT:
            {{
                "market_positioning_strategy": {{
                    "recommended_position": "<cost_leader/differentiator/niche_focus>",
                    "positioning_rationale": "<specific reasoning>",
                    "competitive_moat": "<sustainable advantage strategy>",
                    "implementation_timeline": "<months>"
                }},
                "market_expansion_opportunities": [
                    {{
                        "opportunity": "<specific expansion opportunity>",
                        "market_size": <estimated dollar amount>,
                        "investment_required": <dollar amount>,
                        "expected_roi": <percentage>,
                        "risk_level": "<low/medium/high>",
                        "timeline": "<months to implementation>"
                    }}
                ],
                "competitive_response_plan": {{
                    "competitive_threats": ["<threat 1>", "<threat 2>"],
                    "defensive_strategies": ["<strategy 1>", "<strategy 2>"],
                    "offensive_opportunities": ["<opportunity 1>", "<opportunity 2>"]
                }},
                "market_timing_insights": {{
                    "current_market_phase": "<expansion/maturity/decline>",
                    "optimal_investment_timing": "<now/6_months/12_months>",
                    "seasonal_optimization": ["<recommendation 1>", "<recommendation 2>"]
                }},
                "customer_acquisition_strategy": {{
                    "primary_target_segments": ["<segment 1>", "<segment 2>"],
                    "acquisition_channels": ["<channel 1>", "<channel 2>"],
                    "customer_lifetime_value_optimization": ["<tactic 1>", "<tactic 2>"]
                }},
                "confidence_level": <0-100>
            }}
            """
            
            # Use MultiGeminiEngine for strategic analysis
            strategic_recommendations = await self.multi_gemini_engine._make_gemini_request(
                self.multi_gemini_engine.get_optimal_key("market_intelligence"),
                strategic_prompt,
                "strategic_market_analysis"
            )
            
            return strategic_recommendations
            
        except Exception as e:
            logger.error(f"Error generating strategic market recommendations: {str(e)}")
            return {"error": str(e)}
    
    # Helper methods for data processing and analysis
    
    def _determine_business_cycle_phase(self, economic_indicators: Dict[str, float]) -> str:
        """Determine current US business cycle phase."""
        
        gdp_growth = economic_indicators.get("gdp_growth", 0.02)
        unemployment = economic_indicators.get("unemployment_rate", 0.04)
        confidence = economic_indicators.get("consumer_confidence", 100)
        
        if gdp_growth > 0.03 and unemployment < 0.04 and confidence > 105:
            return "expansion"
        elif gdp_growth < 0 and unemployment > 0.06:
            return "recession"
        elif gdp_growth > 0 and unemployment > 0.05:
            return "recovery"
        elif gdp_growth < 0.015 and confidence < 95:
            return "contraction"
        else:
            return "stable"
    
    def _calculate_economic_health_score(self, economic_indicators: Dict[str, float],
                                       economic_impact: Dict[str, float],
                                       market_sentiment: Dict[str, Any]) -> float:
        """Calculate overall economic health score."""
        
        base_score = 50
        
        # GDP growth component
        gdp_growth = economic_indicators.get("gdp_growth", 0.02)
        base_score += (gdp_growth - 0.02) * 1000  # Scale GDP growth
        
        # Unemployment component (lower is better)
        unemployment = economic_indicators.get("unemployment_rate", 0.04)
        base_score += (0.04 - unemployment) * 500  # 4% baseline
        
        # Consumer confidence component
        confidence = economic_indicators.get("consumer_confidence", 100)
        base_score += (confidence - 100) * 0.5
        
        # Economic impact component
        total_impact = economic_impact.get("total_economic_impact", 0)
        base_score += total_impact * 100
        
        # Market sentiment component
        sentiment = market_sentiment.get("sentiment", "neutral")
        sentiment_adjustments = {
            "very_positive": 15, "positive": 10, "neutral": 0, "cautious": -10, "negative": -15
        }
        base_score += sentiment_adjustments.get(sentiment, 0)
        
        return min(100, max(0, base_score))
    
    def _estimate_total_addressable_market(self, sector: str, location_type: str, business_data: Dict[str, Any]) -> Dict[str, float]:
        """Estimate total addressable market size."""
        
        sector_data = get_us_sector_data(sector)
        location_data = get_us_location_data(location_type)
        
        if not sector_data or not location_data:
            return {"total_market": 10000000, "serviceable_market": 1000000}
        
        # Base market calculations
        demographics = location_data.get("characteristics", {}).get("demographics", {})
        population_proxy = demographics.get("median_income", 65000) / 1000
        
        sector_average = sector_data["base_performance"]["average_monthly_revenue"] * 12
        location_multiplier = get_us_sector_location_multiplier(sector, location_type)
        
        # Estimate market sizes
        estimated_businesses = max(50, population_proxy / 10)
        total_market = estimated_businesses * sector_average * location_multiplier
        serviceable_market = total_market * 0.1  # 10% serviceable
        
        return {
            "total_market": total_market,
            "serviceable_market": serviceable_market,
            "estimated_competitors": estimated_businesses
        }
    
    def _assess_competitive_position(self, business_data: Dict[str, Any], sector_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess business competitive position."""
        
        business_revenue = sum(business_data.get('monthly_revenue', [0]))
        sector_average = sector_data["base_performance"]["average_monthly_revenue"] * 12
        performance_ratio = business_revenue / sector_average if sector_average > 0 else 0
        
        if performance_ratio >= 1.5:
            position = "market_leader"
            strength = "dominant"
        elif performance_ratio >= 1.2:
            position = "strong_performer"
            strength = "strong"
        elif performance_ratio >= 0.8:
            position = "average_performer"
            strength = "competitive"
        elif performance_ratio >= 0.5:
            position = "below_average"
            strength = "struggling"
        else:
            position = "underperformer"
            strength = "weak"
        
        return {
            "market_position": position,
            "competitive_strength": strength,
            "performance_ratio": performance_ratio,
            "market_percentile": min(100, max(0, (performance_ratio - 0.5) * 100 + 50))
        }
    
    def _analyze_market_trends(self, sector: str, location_type: str) -> Dict[str, Any]:
        """Analyze current market trends."""
        
        trends = {
            "digital_transformation": "accelerating",
            "consumer_behavior_shift": "towards_convenience",
            "sustainability_focus": "increasing",
            "local_business_preference": "growing"
        }
        
        # Sector-specific trend adjustments
        if sector == "food":
            trends.update({
                "delivery_demand": "very_high",
                "health_consciousness": "increasing",
                "ghost_kitchens": "growing_threat"
            })
        elif sector == "retail":
            trends.update({
                "ecommerce_competition": "intensifying",
                "experiential_retail": "growing_importance",
                "omnichannel_expectation": "standard"
            })
        elif sector == "electronics":
            trends.update({
                "online_dominance": "accelerating",
                "service_differentiation": "critical",
                "technical_expertise_value": "increasing"
            })
        
        return trends
    
    def _analyze_seasonal_patterns(self, sector: str) -> Dict[str, Any]:
        """Analyze seasonal demand patterns."""
        
        from app.data.us_economic_factors import get_us_seasonal_factor
        
        seasonal_patterns = {}
        for month in range(1, 13):
            seasonal_patterns[f"month_{month}"] = get_us_seasonal_factor(sector, month)
        
        # Identify peak and low seasons
        max_month = max(seasonal_patterns, key=seasonal_patterns.get)
        min_month = min(seasonal_patterns, key=seasonal_patterns.get)
        
        return {
            "monthly_factors": seasonal_patterns,
            "peak_season": max_month.replace("month_", ""),
            "low_season": min_month.replace("month_", ""),
            "volatility": max(seasonal_patterns.values()) - min(seasonal_patterns.values()),
            "planning_recommendations": self._generate_seasonal_recommendations(sector, seasonal_patterns)
        }
    
    def _generate_seasonal_recommendations(self, sector: str, patterns: Dict[str, float]) -> List[str]:
        """Generate seasonal planning recommendations."""
        
        recommendations = []
        
        peak_months = [month for month, factor in patterns.items() if factor > 1.2]
        low_months = [month for month, factor in patterns.items() if factor < 0.9]
        
        if peak_months:
            recommendations.append(f"Increase inventory and marketing during peak months ({len(peak_months)} months)")
        
        if low_months:
            recommendations.append(f"Focus on cost control during slow months ({len(low_months)} months)")
        
        if sector == "retail":
            recommendations.append("Plan holiday campaigns 2 months in advance")
        elif sector == "food":
            recommendations.append("Develop seasonal menus and promotions")
        
        return recommendations
    
    def _calculate_sector_health_metrics(self, sector_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate sector health metrics."""
        
        base_performance = sector_data.get("base_performance", {})
        market_dynamics = sector_data.get("market_dynamics", {})
        
        return {
            "growth_rate": base_performance.get("growth_rate", 0),
            "profit_margin": base_performance.get("typical_profit_margin", 0),
            "market_volatility": base_performance.get("volatility", 0),
            "competition_intensity": market_dynamics.get("competition_intensity", 0.5),
            "economic_sensitivity": abs(market_dynamics.get("fed_rate_sensitivity", 0)),
            "overall_health_score": self._calculate_overall_sector_health(base_performance, market_dynamics)
        }
    
    def _calculate_overall_sector_health(self, base_performance: Dict[str, float], 
                                       market_dynamics: Dict[str, float]) -> float:
        """Calculate overall sector health score."""
        
        score = 50
        
        # Growth rate component
        growth_rate = base_performance.get("growth_rate", 0)
        score += growth_rate * 200
        
        # Profit margin component
        profit_margin = base_performance.get("typical_profit_margin", 0.15)
        score += (profit_margin - 0.15) * 100
        
        # Volatility component (lower is better)
        volatility = base_performance.get("volatility", 0.15)
        score -= volatility * 100
        
        # Competition component
        competition = market_dynamics.get("competition_intensity", 0.5)
        score -= (competition - 0.5) * 50
        
        return min(100, max(0, score))
    
    def _assess_sector_growth_trajectory(self, sector_data: Dict[str, Any]) -> str:
        """Assess sector growth trajectory."""
        
        growth_rate = sector_data.get("base_performance", {}).get("growth_rate", 0)
        volatility = sector_data.get("base_performance", {}).get("volatility", 0)
        
        if growth_rate > 0.08 and volatility < 0.15:
            return "strong_stable_growth"
        elif growth_rate > 0.05:
            return "moderate_growth"
        elif growth_rate > 0.02:
            return "slow_growth"
        elif growth_rate > -0.02:
            return "stagnant"
        else:
            return "declining"
    
    def _assess_sector_disruption_risks(self, sector: str) -> List[Dict[str, Any]]:
        """Assess disruption risks by sector."""
        
        risks = {
            "retail": [
                {"risk": "E-commerce growth", "impact": "high", "timeline": "ongoing"},
                {"risk": "Changing consumer preferences", "impact": "medium", "timeline": "2-3 years"}
            ],
            "food": [
                {"risk": "Ghost kitchens", "impact": "medium", "timeline": "1-2 years"},
                {"risk": "Automation", "impact": "medium", "timeline": "3-5 years"}
            ],
            "electronics": [
                {"risk": "Online retail dominance", "impact": "very_high", "timeline": "ongoing"},
                {"risk": "Direct-to-consumer brands", "impact": "high", "timeline": "1-2 years"}
            ],
            "auto": [
                {"risk": "Electric vehicle transition", "impact": "high", "timeline": "2-5 years"},
                {"risk": "Online parts sales", "impact": "medium", "timeline": "ongoing"}
            ]
        }
        
        return risks.get(sector, [{"risk": "Technology disruption", "impact": "medium", "timeline": "2-5 years"}])
    
    def _build_consumer_profile(self, location_data: Dict[str, Any], regional_factors: Dict[str, Any]) -> Dict[str, Any]:
        """Build consumer profile for location."""
        
        characteristics = location_data.get("characteristics", {})
        demographics = characteristics.get("demographics", {})
        
        return {
            "median_income": demographics.get("median_income", 65000),
            "spending_power": demographics.get("median_income", 65000) / 65000,
            "age_distribution": {
                "millennials_gen_z": demographics.get("age_25_44", 30),
                "gen_x": 25,
                "boomers": 30,
                "other": 15
            },
            "education_level": demographics.get("college_degree", 40),
            "lifestyle_preferences": {
               "convenience_focused": 0.8,
               "value_conscious": 0.6,
               "technology_adoption": 0.7,
               "sustainability_minded": 0.5
           },
           "shopping_behavior": {
               "online_preference": 0.6,
               "local_loyalty": 0.4,
               "brand_switching": 0.3,
               "impulse_buying": 0.4
           },
           "economic_factors": regional_factors
       }
   
    def _analyze_consumer_spending_patterns(self, location_type: str) -> Dict[str, Any]:
        """Analyze consumer spending patterns by location type."""
        
        if location_type == "urban_high_income":
            return {
                "discretionary_spending": 0.4,
                "convenience_premium": 0.2,
                "brand_preference": 0.7,
                "price_sensitivity": 0.3,
                "seasonal_variation": 0.2
            }
        elif location_type == "suburban":
            return {
                "discretionary_spending": 0.3,
                "convenience_premium": 0.15,
                "brand_preference": 0.5,
                "price_sensitivity": 0.5,
                "seasonal_variation": 0.3
            }
        elif location_type == "small_town":
            return {
                "discretionary_spending": 0.25,
                "convenience_premium": 0.1,
                "brand_preference": 0.3,
                "price_sensitivity": 0.7,
                "seasonal_variation": 0.4
            }
        else:
            return {
                "discretionary_spending": 0.3,
                "convenience_premium": 0.15,
                "brand_preference": 0.5,
                "price_sensitivity": 0.5,
                "seasonal_variation": 0.3
            }
    
    def _calculate_market_penetration_potential(self, location_type: str, consumer_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate market penetration potential."""
        
        spending_power = consumer_profile.get("spending_power", 1.0)
        
        base_penetration = {
            "urban_high_income": 0.15,
            "suburban": 0.12,
            "small_town": 0.20,
            "business_district": 0.10
        }
        
        potential = base_penetration.get(location_type, 0.12) * spending_power
        
        return {
            "market_penetration_rate": potential,
            "growth_potential": max(0, 0.25 - potential),
            "saturation_level": "low" if potential < 0.1 else "medium" if potential < 0.2 else "high",
            "expansion_opportunity": potential < 0.15
        }
    
    def _analyze_customer_acquisition(self, location_type: str, consumer_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze customer acquisition opportunities."""
        
        base_costs = {
            "urban_high_income": 150,
            "suburban": 75,
            "small_town": 25,
            "business_district": 100
        }
        
        acquisition_cost = base_costs.get(location_type, 75)
        
        # Adjust for spending power
        spending_power = consumer_profile.get("spending_power", 1.0)
        adjusted_cost = acquisition_cost / spending_power
        
        return {
            "estimated_acquisition_cost": adjusted_cost,
            "primary_channels": self._identify_primary_channels(location_type),
            "conversion_rates": self._estimate_conversion_rates(location_type),
            "customer_lifetime_value": self._estimate_customer_lifetime_value(location_type, consumer_profile),
            "acquisition_recommendations": self._generate_acquisition_recommendations(location_type)
        }
    
    def _identify_primary_channels(self, location_type: str) -> List[Dict[str, Any]]:
        """Identify primary marketing channels by location."""
        
        if location_type == "urban_high_income":
            return [
                {"channel": "Digital Advertising", "effectiveness": 0.8, "cost": "medium"},
                {"channel": "Social Media", "effectiveness": 0.7, "cost": "low"},
                {"channel": "Professional Networks", "effectiveness": 0.6, "cost": "low"}
            ]
        elif location_type == "suburban":
            return [
                {"channel": "Local SEO", "effectiveness": 0.9, "cost": "low"},
                {"channel": "Community Events", "effectiveness": 0.7, "cost": "medium"},
                {"channel": "Social Media", "effectiveness": 0.8, "cost": "low"}
            ]
        elif location_type == "small_town":
            return [
                {"channel": "Word of Mouth", "effectiveness": 0.9, "cost": "very_low"},
                {"channel": "Local Partnerships", "effectiveness": 0.8, "cost": "low"},
                {"channel": "Community Involvement", "effectiveness": 0.7, "cost": "low"}
            ]
        else:
            return [
                {"channel": "Digital Marketing", "effectiveness": 0.7, "cost": "medium"},
                {"channel": "Local Advertising", "effectiveness": 0.6, "cost": "medium"},
                {"channel": "Referral Programs", "effectiveness": 0.5, "cost": "low"}
            ]
    
    def _estimate_conversion_rates(self, location_type: str) -> Dict[str, float]:
        """Estimate conversion rates by channel and location."""
        
        if location_type == "urban_high_income":
            return {
                "walk_in": 0.25,
                "digital": 0.05,
                "referral": 0.40,
                "social_media": 0.08
            }
        elif location_type == "small_town":
            return {
                "walk_in": 0.45,
                "digital": 0.15,
                "referral": 0.60,
                "social_media": 0.20
            }
        else:
            return {
                "walk_in": 0.35,
                "digital": 0.08,
                "referral": 0.50,
                "social_media": 0.12
            }
    
    def _estimate_customer_lifetime_value(self, location_type: str, consumer_profile: Dict[str, Any]) -> float:
        """Estimate customer lifetime value."""
        
        base_values = {
            "urban_high_income": 2500,
            "suburban": 1500,
            "small_town": 1000,
            "business_district": 2000
        }
        
        base_clv = base_values.get(location_type, 1500)
        spending_power = consumer_profile.get("spending_power", 1.0)
        
        return base_clv * spending_power
    
    def _generate_acquisition_recommendations(self, location_type: str) -> List[str]:
        """Generate customer acquisition recommendations."""
        
        recommendations = {
            "urban_high_income": [
                "Focus on convenience and premium service",
                "Leverage digital channels and apps",
                "Build professional network referrals"
            ],
            "suburban": [
                "Establish strong local presence",
                "Engage in community events",
                "Optimize for local search"
            ],
            "small_town": [
                "Focus on personal relationships",
                "Participate in community activities",
                "Build word-of-mouth referral system"
            ]
        }
        
        return recommendations.get(location_type, [
            "Balance digital and traditional marketing",
            "Focus on customer service excellence",
            "Build referral program"
        ])
    
    def _assess_market_structure(self, sector: str, location_type: str) -> str:
        """Assess market structure (fragmented/concentrated)."""
        
        competition_level = get_us_competition_level(sector, location_type)
        
        if competition_level in ["very_high", "high"]:
            return "fragmented"
        elif competition_level == "medium":
            return "moderately_concentrated"
        else:
            return "concentrated"
    
    def _assess_barriers_to_entry(self, sector: str) -> str:
        """Assess barriers to entry for sector."""
        
        barrier_levels = {
            "food": "low",
            "retail": "low",
            "electronics": "medium",
            "auto": "medium",
            "professional_services": "medium",
            "manufacturing": "high",
            "healthcare": "high",
            "construction": "medium"
        }
        
        return barrier_levels.get(sector, "medium")
    
    def _identify_potential_competitive_advantages(self, sector: str, location_type: str) -> List[str]:
        """Identify potential competitive advantages."""
        
        sector_data = get_us_sector_data(sector)
        success_factors = sector_data.get("business_insights", {}).get("success_factors", [])
        
        location_advantages = {
            "urban_high_income": ["premium_service", "convenience", "brand_prestige"],
            "suburban": ["family_focus", "community_connection", "value_proposition"],
            "small_town": ["personal_relationships", "local_knowledge", "trust"],
            "business_district": ["professional_focus", "speed", "reliability"]
        }
        
        location_specific = location_advantages.get(location_type, [])
        
        return success_factors[:3] + location_specific[:2]
    
    def _identify_market_gaps(self, sector: str, location_type: str) -> List[Dict[str, Any]]:
        """Identify market gaps and opportunities."""
        
        gaps = []
        
        if sector == "food" and location_type in ["suburban", "small_town"]:
            gaps.append({
                "gap": "Healthy Fast Food Options",
                "market_size": 500000,
                "competition_level": "low",
                "implementation_difficulty": "medium"
            })
        elif sector == "retail" and location_type == "urban_high_income":
            gaps.append({
                "gap": "Personalized Shopping Experience",
                "market_size": 1000000,
                "competition_level": "medium",
                "implementation_difficulty": "high"
            })
        elif sector == "electronics":
            gaps.append({
                "gap": "Technical Support and Education",
                "market_size": 750000,
                "competition_level": "low",
                "implementation_difficulty": "medium"
            })
        
        return gaps
    
    def _analyze_competitive_dynamics(self, sector: str, location_type: str) -> Dict[str, Any]:
        """Analyze competitive dynamics."""
        
        return {
            "price_competition_intensity": "high" if get_us_competition_level(sector, location_type) in ["very_high", "high"] else "medium",
            "innovation_pace": "fast" if sector in ["electronics", "professional_services"] else "moderate",
            "customer_switching_costs": "low" if sector in ["retail", "food"] else "medium",
            "network_effects": "low" if sector in ["retail", "food"] else "medium",
            "economies_of_scale": "high" if sector in ["manufacturing", "auto"] else "medium"
        }
    
    def _identify_differentiation_opportunities(self, sector: str, location_type: str) -> List[str]:
        """Identify differentiation opportunities."""
        
        opportunities = []
        
        if sector == "food":
            opportunities = ["Unique cuisine", "Farm-to-table", "Dietary specialization", "Experience dining"]
        elif sector == "retail":
            opportunities = ["Curated selection", "Personal service", "Local products", "Omnichannel experience"]
        elif sector == "electronics":
            opportunities = ["Technical expertise", "Repair services", "Education/training", "Custom solutions"]
        elif sector == "auto":
            opportunities = ["Specialized services", "Mobile service", "Electric vehicle focus", "Performance tuning"]
        else:
            opportunities = ["Specialized expertise", "Superior service", "Unique offerings", "Technology integration"]
        
        # Add location-specific opportunities
        if location_type == "small_town":
            opportunities.append("Community connection")
        elif location_type == "urban_high_income":
            opportunities.append("Premium positioning")
        
        return opportunities[:4]
    
    # Summary creation methods
    
    def _create_market_positioning_summary(self, comprehensive_analysis: Dict[str, Any],
                                         market_intelligence_data: Dict[str, Any],
                                         business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create market positioning summary."""
        
        market_data = market_intelligence_data.get("market_data", {})
        competitive_position = market_data.get("competitive_position", {})
        
        return {
            "current_position": competitive_position.get("market_position", "unknown"),
            "competitive_strength": competitive_position.get("competitive_strength", "unknown"),
            "market_percentile": competitive_position.get("market_percentile", 50),
            "positioning_score": competitive_position.get("market_percentile", 50),
            "key_differentiators": market_intelligence_data.get("competitive_data", {}).get("differentiation_opportunities", [])[:3],
            "positioning_recommendation": self._determine_optimal_positioning(competitive_position, market_data)
        }
    
    def _determine_optimal_positioning(self, competitive_position: Dict[str, Any], market_data: Dict[str, Any]) -> str:
        """Determine optimal market positioning strategy."""
        
        market_percentile = competitive_position.get("market_percentile", 50)
        competition_level = market_data.get("competition_level", "medium")
        
        if market_percentile >= 75:
            return "maintain_leadership"
        elif market_percentile >= 50 and competition_level in ["high", "very_high"]:
            return "differentiation_focus"
        elif market_percentile < 50:
            return "value_positioning"
        else:
            return "competitive_improvement"
    
    def _create_competitive_landscape_summary(self, comprehensive_analysis: Dict[str, Any],
                                            market_intelligence_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create competitive landscape summary."""
        
        competitive_data = market_intelligence_data.get("competitive_data", {})
        competition_analysis = competitive_data.get("competition_analysis", {})
        
        return {
            "competition_intensity": competition_analysis.get("intensity_level", "medium"),
            "market_structure": competition_analysis.get("market_structure", "fragmented"),
            "barriers_to_entry": competition_analysis.get("barriers_to_entry", "medium"),
            "competitive_threats": competitive_data.get("competitive_dynamics", {}).get("price_competition_intensity", "medium"),
            "market_gaps": competitive_data.get("market_gaps", []),
            "competitive_opportunities": competitive_data.get("differentiation_opportunities", [])[:3]
        }
    
    def _create_market_opportunities_summary(self, comprehensive_analysis: Dict[str, Any],
                                           market_intelligence_data: Dict[str, Any],
                                           business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create market opportunities summary."""
        
        market_data = market_intelligence_data.get("market_data", {})
        opportunity_analysis = market_data.get("opportunity_analysis", {})
        
        current_revenue = sum(business_data.get('monthly_revenue', [0]))
        market_size = market_data.get("market_size", {}).get("serviceable_market", 1000000)
        
        return {
            "opportunity_score": opportunity_analysis.get("opportunity_score", 50),
            "opportunity_level": opportunity_analysis.get("opportunity_level", "medium"),
            "market_size": market_size,
            "current_penetration": (current_revenue / market_size * 100) if market_size > 0 else 0,
            "growth_potential": max(0, market_size - current_revenue),
            "key_opportunities": self._extract_key_opportunities(market_intelligence_data, current_revenue)
        }
    
    def _extract_key_opportunities(self, market_intelligence_data: Dict[str, Any], current_revenue: float) -> List[Dict[str, Any]]:
        """Extract key market opportunities."""
        
        opportunities = []
        
        # Market gaps as opportunities
        market_gaps = market_intelligence_data.get("competitive_data", {}).get("market_gaps", [])
        for gap in market_gaps[:2]:
            opportunities.append({
                "type": "market_gap",
                "description": gap.get("gap", "Market opportunity"),
                "estimated_value": gap.get("market_size", current_revenue * 0.2),
                "difficulty": gap.get("implementation_difficulty", "medium")
            })
        
        # Seasonal opportunities
        seasonal_data = market_intelligence_data.get("market_data", {}).get("seasonal_patterns", {})
        peak_factor = max(seasonal_data.get("monthly_factors", {}).values()) if seasonal_data.get("monthly_factors") else 1.2
        if peak_factor > 1.3:
            opportunities.append({
                "type": "seasonal_optimization",
                "description": "Capitalize on peak seasonal demand",
                "estimated_value": current_revenue * (peak_factor - 1),
                "difficulty": "low"
            })
        
        return opportunities[:3]
    
    def _create_economic_environment_summary(self, comprehensive_analysis: Dict[str, Any],
                                           market_intelligence_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create economic environment summary."""
        
        economic_data = market_intelligence_data.get("economic_data", {})
        
        return {
            "economic_health_score": economic_data.get("economic_health_score", 50),
            "business_cycle_phase": economic_data.get("business_cycle_phase", "stable"),
            "economic_impact": economic_data.get("economic_impact", {}),
            "market_sentiment": economic_data.get("market_sentiment", {}),
            "sector_resilience": economic_data.get("sector_resilience", {}),
            "economic_outlook": economic_data.get("economic_projections", {})
        }
    
    def _create_consumer_insights_summary(self, market_intelligence_data: Dict[str, Any],
                                        business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create consumer insights summary."""
        
        consumer_data = market_intelligence_data.get("consumer_data", {})
        consumer_profile = consumer_data.get("consumer_profile", {})
        spending_patterns = consumer_data.get("spending_patterns", {})
        
        return {
            "consumer_profile": consumer_profile,
            "spending_patterns": spending_patterns,
            "market_penetration": consumer_data.get("market_penetration", {}),
            "acquisition_strategy": consumer_data.get("acquisition_analysis", {}),
            "consumer_trends": self._identify_consumer_trends(consumer_profile, spending_patterns)
        }
    
    def _identify_consumer_trends(self, consumer_profile: Dict[str, Any], spending_patterns: Dict[str, Any]) -> List[str]:
        """Identify key consumer trends."""
        
        trends = []
        
        if consumer_profile.get("lifestyle_preferences", {}).get("convenience_focused", 0) > 0.7:
            trends.append("High demand for convenience solutions")
        
        if spending_patterns.get("discretionary_spending", 0) > 0.35:
            trends.append("Strong discretionary spending capacity")
        
        if consumer_profile.get("shopping_behavior", {}).get("online_preference", 0) > 0.6:
            trends.append("Preference for online/digital channels")
        
        if spending_patterns.get("price_sensitivity", 0) > 0.6:
            trends.append("High price sensitivity")
        
        return trends[:3]
    
    def _create_sector_analysis_summary(self, comprehensive_analysis: Dict[str, Any],
                                      market_intelligence_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create sector analysis summary."""
        
        sector_data = market_intelligence_data.get("sector_data", {})
        
        return {
            "sector_health": sector_data.get("sector_health", {}),
            "growth_trajectory": sector_data.get("growth_trajectory", "moderate"),
            "performance_vs_sector": sector_data.get("sector_performance", {}),
            "disruption_risks": sector_data.get("disruption_risks", []),
            "sector_outlook": self._assess_sector_outlook(sector_data)
        }
    
    def _assess_sector_outlook(self, sector_data: Dict[str, Any]) -> str:
        """Assess overall sector outlook."""
        
        growth_trajectory = sector_data.get("growth_trajectory", "moderate")
        sector_health = sector_data.get("sector_health", {})
        health_score = sector_health.get("overall_health_score", 50)
        
        if health_score >= 70 and growth_trajectory in ["strong_stable_growth", "moderate_growth"]:
            return "positive"
        elif health_score >= 50:
            return "neutral"
        else:
            return "challenging"
    
    def _calculate_market_intelligence_scores(self, comprehensive_analysis: Dict[str, Any],
                                            market_intelligence_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate market intelligence scores."""
        
        scores = {}
        
        # Market positioning score
        market_data = market_intelligence_data.get("market_data", {})
        competitive_position = market_data.get("competitive_position", {})
        scores["market_positioning"] = competitive_position.get("market_percentile", 50)
        
        # Competitive landscape score
        competitive_data = market_intelligence_data.get("competitive_data", {})
        competition_analysis = competitive_data.get("competition_analysis", {})
        competition_level = competition_analysis.get("intensity_level", "medium")
        competition_score_map = {"low": 80, "medium": 60, "high": 40, "very_high": 20}
        scores["competitive_environment"] = competition_score_map.get(competition_level, 50)
        
        # Economic environment score
        economic_data = market_intelligence_data.get("economic_data", {})
        scores["economic_environment"] = economic_data.get("economic_health_score", 50)
        
        # Market opportunity score
        opportunity_analysis = market_data.get("opportunity_analysis", {})
        scores["market_opportunity"] = opportunity_analysis.get("opportunity_score", 50)
        
        # Consumer market score
        consumer_data = market_intelligence_data.get("consumer_data", {})
        consumer_profile = consumer_data.get("consumer_profile", {})
        spending_power = consumer_profile.get("spending_power", 1.0)
        scores["consumer_market"] = min(100, spending_power * 50 + 25)
        
        # Sector performance score
        sector_data = market_intelligence_data.get("sector_data", {})
        sector_health = sector_data.get("sector_health", {})
        scores["sector_performance"] = sector_health.get("overall_health_score", 50)
        
        # Overall market intelligence score
        weights = {
            "market_positioning": 0.25,
            "competitive_environment": 0.20,
            "economic_environment": 0.15,
            "market_opportunity": 0.20,
            "consumer_market": 0.10,
            "sector_performance": 0.10
        }
        
        scores["overall_market_intelligence"] = sum(
            scores[key] * weights[key] for key in scores.keys() if key in weights
        )
        
        return scores
    
    # Utility methods
    
    def _get_data_sources_used(self) -> List[str]:
        """Get list of data sources used in analysis."""
        
        return [
            "US Census Bureau Demographics",
            "Bureau of Labor Statistics Employment Data",
            "Federal Reserve Economic Data (FRED)",
            "Alpha Vantage Market Data",
            "US Sector Performance Benchmarks",
            "Regional Economic Indicators",
            "Multi-Gemini AI Analysis Engine",
            "Consumer Spending Pattern Analysis",
            "Competitive Intelligence Database"
        ]
    
    def _assess_analysis_completeness(self, enhanced_intelligence: Dict[str, Any]) -> float:
        """Assess completeness of market intelligence analysis."""
        
        required_components = [
            "market_intelligence",
            "market_scores",
            "strategic_market_recommendations",
            "executive_summary"
        ]
        
        completed = sum(
            1 for component in required_components 
            if component in enhanced_intelligence and enhanced_intelligence[component]
        )
        
        return completed / len(required_components)
    
    # Cache management methods
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cached data is still valid."""
        
        if cache_key not in self._cache_timestamps:
            return False
        
        age = datetime.now().timestamp() - self._cache_timestamps[cache_key]
        return age < self._cache_duration
    
    def _cache_data(self, cache_key: str, data: Dict[str, Any]) -> None:
        """Cache data with timestamp."""
        
        self._market_cache[cache_key] = data
        self._cache_timestamps[cache_key] = datetime.now().timestamp()
    
    def _get_cached_data(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get cached data if valid."""
        
        if self._is_cache_valid(cache_key):
            return self._market_cache.get(cache_key)
        
        return None
    

# Additional utility functions for market intelligence

def calculate_market_attractiveness_score(sector: str, location_type: str, economic_health: float) -> float:
   """Calculate overall market attractiveness score."""
   
   base_score = 50
   
   # Sector growth component
   sector_data = get_us_sector_data(sector)
   if sector_data:
       growth_rate = sector_data.get("base_performance", {}).get("growth_rate", 0)
       base_score += growth_rate * 200
   
   # Location attractiveness
   location_multiplier = get_us_sector_location_multiplier(sector, location_type)
   base_score += (location_multiplier - 1.0) * 30
   
   # Economic health component
   base_score += (economic_health - 50) * 0.4
   
   # Competition adjustment
   competition_level = get_us_competition_level(sector, location_type)
   competition_adjustments = {"low": 15, "medium": 0, "high": -10, "very_high": -20}
   base_score += competition_adjustments.get(competition_level, 0)
   
   return min(100, max(0, base_score))


def estimate_market_entry_cost(sector: str, location_type: str) -> Dict[str, float]:
   """Estimate market entry costs by sector and location."""
   
   base_costs = {
       "food": {"startup": 75000, "inventory": 15000, "equipment": 35000, "marketing": 5000},
       "retail": {"startup": 50000, "inventory": 25000, "equipment": 15000, "marketing": 10000},
       "electronics": {"startup": 60000, "inventory": 40000, "equipment": 20000, "marketing": 8000},
       "auto": {"startup": 80000, "inventory": 50000, "equipment": 30000, "marketing": 7000},
       "professional_services": {"startup": 25000, "inventory": 5000, "equipment": 15000, "marketing": 15000}
   }
   
   location_multipliers = {
       "urban_high_income": 1.5,
       "suburban": 1.0,
       "small_town": 0.7,
       "business_district": 1.3
   }
   
   sector_costs = base_costs.get(sector, base_costs["retail"])
   location_multiplier = location_multipliers.get(location_type, 1.0)
   
   return {
       cost_type: cost * location_multiplier 
       for cost_type, cost in sector_costs.items()
   }


def calculate_revenue_potential(business_data: Dict[str, Any], market_data: Dict[str, Any]) -> Dict[str, float]:
   """Calculate revenue growth potential based on market conditions."""
   
   current_revenue = sum(business_data.get('monthly_revenue', [0]))
   market_size = market_data.get("market_size", {}).get("serviceable_market", current_revenue * 5)
   
   # Conservative, realistic, optimistic scenarios
   market_penetration = current_revenue / market_size if market_size > 0 else 0.1
   
   potential = {
       "conservative": current_revenue * 1.1,  # 10% growth
       "realistic": current_revenue * 1.25,   # 25% growth
       "optimistic": min(market_size * 0.1, current_revenue * 1.5)  # 50% growth or 10% market share
   }
   
   return potential