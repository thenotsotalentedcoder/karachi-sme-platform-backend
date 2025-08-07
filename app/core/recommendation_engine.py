import asyncio
import logging
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime, timedelta
import json
import statistics
from enum import Enum
from dataclasses import dataclass
import math

from app.core.multi_gemini_engine import MultiGeminiEngine
from app.core.business_analyzer import USBusinessAnalyzer
from app.core.market_generator import USMarketIntelligence
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
    classify_us_location_type
)
from app.config import settings, GEMINI_KEYS, OPENROUTER_KEYS

logger = logging.getLogger(__name__)


class RecommendationCategory(Enum):
   """Categories of business recommendations."""
   IMMEDIATE_CRITICAL = "immediate_critical"
   FINANCIAL_OPTIMIZATION = "financial_optimization"
   GROWTH_ACCELERATION = "growth_acceleration"
   MARKET_EXPANSION = "market_expansion"
   INVESTMENT_OPPORTUNITIES = "investment_opportunities"
   RISK_MITIGATION = "risk_mitigation"
   OPERATIONAL_EFFICIENCY = "operational_efficiency"
   STRATEGIC_POSITIONING = "strategic_positioning"
   TECHNOLOGY_DIGITAL = "technology_digital"
   COMPLIANCE_REGULATORY = "compliance_regulatory"


class RecommendationPriority(Enum):
   """Priority levels for recommendations."""
   CRITICAL = "critical"
   HIGH = "high"
   MEDIUM = "medium"
   LOW = "low"


class RecommendationUrgency(Enum):
   """Urgency levels for recommendations."""
   IMMEDIATE = "immediate"      # 0-30 days
   SHORT_TERM = "short_term"    # 1-3 months
   MEDIUM_TERM = "medium_term"  # 3-6 months
   LONG_TERM = "long_term"      # 6+ months


@dataclass
class RecommendationMetrics:
   """Metrics for recommendation impact and feasibility."""
   expected_roi: Optional[float] = None
   expected_revenue_impact: Optional[float] = None
   expected_cost_impact: Optional[float] = None
   implementation_cost: Optional[float] = None
   payback_period_months: Optional[int] = None
   success_probability: float = 0.7
   risk_level: str = "medium"
   effort_level: str = "medium"
   confidence_score: float = 0.8


@dataclass
class USBusinessRecommendation:
   """Comprehensive US business recommendation structure."""
   
   # Identification
   recommendation_id: str
   category: RecommendationCategory
   priority: RecommendationPriority
   urgency: RecommendationUrgency
   
   # Core recommendation
   title: str
   description: str
   rationale: str
   specific_actions: List[str]
   
   # Business impact
   expected_outcomes: List[str]
   success_metrics: List[str]
   metrics: RecommendationMetrics
   
   # Implementation details
   implementation_timeline: str
   implementation_steps: List[Dict[str, Any]]
   required_resources: List[str]
   prerequisites: List[str]
   
   # US-specific context
   economic_context: Dict[str, Any]
   regulatory_considerations: List[str]
   tax_implications: Dict[str, Any]
   compliance_requirements: List[str]
   
   # Dependencies and relationships
   dependent_recommendations: List[str]
   conflicting_recommendations: List[str]
   synergistic_recommendations: List[str]
   
   # Monitoring and tracking
   key_performance_indicators: List[str]
   milestone_checkpoints: List[Dict[str, Any]]
   review_schedule: str
   
   # AI analysis metadata
   ai_confidence: float
   data_sources: List[str]
   analysis_methodology: str
   generated_at: datetime
   
   def to_dict(self) -> Dict[str, Any]:
       """Convert recommendation to dictionary format."""
       return {
           "recommendation_id": self.recommendation_id,
           "category": self.category.value,
           "priority": self.priority.value,
           "urgency": self.urgency.value,
           "title": self.title,
           "description": self.description,
           "rationale": self.rationale,
           "specific_actions": self.specific_actions,
           "expected_outcomes": self.expected_outcomes,
           "success_metrics": self.success_metrics,
           "metrics": {
               "expected_roi": self.metrics.expected_roi,
               "expected_revenue_impact": self.metrics.expected_revenue_impact,
               "expected_cost_impact": self.metrics.expected_cost_impact,
               "implementation_cost": self.metrics.implementation_cost,
               "payback_period_months": self.metrics.payback_period_months,
               "success_probability": self.metrics.success_probability,
               "risk_level": self.metrics.risk_level,
               "effort_level": self.metrics.effort_level,
               "confidence_score": self.metrics.confidence_score
           },
           "implementation": {
               "timeline": self.implementation_timeline,
               "steps": self.implementation_steps,
               "required_resources": self.required_resources,
               "prerequisites": self.prerequisites
           },
           "us_context": {
               "economic_context": self.economic_context,
               "regulatory_considerations": self.regulatory_considerations,
               "tax_implications": self.tax_implications,
               "compliance_requirements": self.compliance_requirements
           },
           "relationships": {
               "dependent_recommendations": self.dependent_recommendations,
               "conflicting_recommendations": self.conflicting_recommendations,
               "synergistic_recommendations": self.synergistic_recommendations
           },
           "monitoring": {
               "kpis": self.key_performance_indicators,
               "milestones": self.milestone_checkpoints,
               "review_schedule": self.review_schedule
           },
           "metadata": {
               "ai_confidence": self.ai_confidence,
               "data_sources": self.data_sources,
               "analysis_methodology": self.analysis_methodology,
               "generated_at": self.generated_at.isoformat()
           }
       }


class USRecommendationEngine:
   """Advanced US SME recommendation engine with AI-powered insights."""
   
   def __init__(self):
       self.multi_gemini_engine = MultiGeminiEngine()
       self.business_analyzer = USBusinessAnalyzer()
       self.market_intelligence = USMarketIntelligence()
       
       # Recommendation tracking and optimization
       self.recommendation_history = {}
       self.success_patterns = {}
       self.sector_patterns = {}
       
       # US-specific recommendation templates
       self.us_recommendation_templates = self._initialize_us_templates()
       
       # Performance tracking
       self.engine_metrics = {
           "total_recommendations": 0,
           "successful_implementations": 0,
           "average_roi_achieved": 0.0,
           "recommendation_accuracy": 0.0,
           "processing_times": []
       }
   
   async def generate_comprehensive_recommendations(self, 
                                                  business_data: Dict[str, Any],
                                                  analysis_results: Optional[Dict[str, Any]] = None,
                                                  focus_areas: Optional[List[str]] = None,
                                                  max_recommendations: int = 15) -> Dict[str, Any]:
       """
       Generate comprehensive US business recommendations.
       
       Args:
           business_data: Complete US business information
           analysis_results: Existing analysis results (optional)
           focus_areas: Specific areas to focus recommendations on
           max_recommendations: Maximum number of recommendations to generate
           
       Returns:
           Comprehensive recommendation package with prioritized actions
       """
       
       start_time = datetime.now()
       logger.info(f"Generating comprehensive recommendations for {business_data.get('business_name', 'Business')}")
       
       try:
           # Get or perform business analysis
           if not analysis_results:
               analysis_results = await self.business_analyzer.analyze_us_business_comprehensive(business_data)
           
           # Get market intelligence
           market_intelligence = await self.market_intelligence.analyze_complete_market_intelligence(business_data)
           
           # Get current economic context
           economic_data = get_current_us_economic_indicators()
           economic_impact = calculate_us_economic_impact(
               business_data.get('sector', ''), business_data
           )
           
           # Generate recommendations across all categories
           all_recommendations = await self._generate_multi_category_recommendations(
               business_data, analysis_results, market_intelligence, economic_data, focus_areas
           )
           
           # Prioritize and select top recommendations
           prioritized_recommendations = self._prioritize_recommendations(
               all_recommendations, business_data, analysis_results
           )
           
           # Limit to max recommendations
           final_recommendations = prioritized_recommendations[:max_recommendations]
           
           # Create implementation roadmap
           implementation_roadmap = self._create_implementation_roadmap(
               final_recommendations, business_data
           )
           
           # Generate success tracking framework
           success_framework = self._create_success_tracking_framework(
               final_recommendations, business_data
           )
           
           # Calculate overall impact projections
           impact_projections = self._calculate_impact_projections(
               final_recommendations, business_data, analysis_results
           )
           
           # Generate executive summary
           executive_summary = await self._generate_executive_summary(
               final_recommendations, impact_projections, business_data
           )
           
           execution_time = (datetime.now() - start_time).total_seconds()
           
           recommendation_package = {
               "executive_summary": executive_summary,
               "recommendations": [rec.to_dict() for rec in final_recommendations],
               "implementation_roadmap": implementation_roadmap,
               "success_framework": success_framework,
               "impact_projections": impact_projections,
               "economic_context": {
                   "current_indicators": economic_data,
                   "business_impact": economic_impact,
                   "market_sentiment": get_us_market_sentiment(business_data.get('sector', ''))
               },
               "recommendation_metadata": {
                   "total_recommendations_generated": len(all_recommendations),
                   "final_recommendations_selected": len(final_recommendations),
                   "focus_areas": focus_areas or [],
                   "generation_time_seconds": execution_time,
                   "confidence_level": self._calculate_overall_confidence(final_recommendations),
                   "analysis_completeness": self._assess_analysis_completeness(analysis_results),
                   "data_sources": self._get_data_sources_used()
               }
           }
           
           # Update engine metrics
           self._update_engine_metrics(execution_time, len(final_recommendations))
           
           logger.info(f"Generated {len(final_recommendations)} recommendations in {execution_time:.2f}s")
           return recommendation_package
           
       except Exception as e:
           logger.error(f"Error generating recommendations: {str(e)}")
           return self._create_fallback_recommendations(business_data, str(e))
   
   async def _generate_multi_category_recommendations(self, 
                                                    business_data: Dict[str, Any],
                                                    analysis_results: Dict[str, Any],
                                                    market_intelligence: Dict[str, Any],
                                                    economic_data: Dict[str, Any],
                                                    focus_areas: Optional[List[str]]) -> List[USBusinessRecommendation]:
       """Generate recommendations across multiple categories."""
       
       all_recommendations = []
       
       # Generate recommendations by category
       recommendation_generators = [
           self._generate_immediate_critical_recommendations,
           self._generate_financial_optimization_recommendations,
           self._generate_growth_acceleration_recommendations,
           self._generate_market_expansion_recommendations,
           self._generate_investment_recommendations,
           self._generate_risk_mitigation_recommendations,
           self._generate_operational_efficiency_recommendations,
           self._generate_strategic_positioning_recommendations,
           self._generate_technology_digital_recommendations,
           self._generate_compliance_regulatory_recommendations
       ]
       
       # Execute generators in parallel
       generator_tasks = []
       for generator in recommendation_generators:
           if not focus_areas or any(area in generator.__name__ for area in focus_areas):
               task = asyncio.create_task(
                   generator(business_data, analysis_results, market_intelligence, economic_data)
               )
               generator_tasks.append(task)
       
       # Collect results
       category_results = await asyncio.gather(*generator_tasks, return_exceptions=True)
       
       # Combine all recommendations
       for result in category_results:
           if isinstance(result, list):
               all_recommendations.extend(result)
           elif isinstance(result, Exception):
               logger.error(f"Recommendation generator failed: {str(result)}")
       
       return all_recommendations
   
   async def _generate_immediate_critical_recommendations(self, 
                                                        business_data: Dict[str, Any],
                                                        analysis_results: Dict[str, Any],
                                                        market_intelligence: Dict[str, Any],
                                                        economic_data: Dict[str, Any]) -> List[USBusinessRecommendation]:
       """Generate immediate critical recommendations for urgent business needs."""
       
       recommendations = []
       
       # Check for critical cash flow issues
       financial_health = analysis_results.get("financial_health", {})
       cash_runway = financial_health.get("cash_runway_months", 6)
       
       if cash_runway < 3:
           recommendations.append(USBusinessRecommendation(
               recommendation_id="critical_001",
               category=RecommendationCategory.IMMEDIATE_CRITICAL,
               priority=RecommendationPriority.CRITICAL,
               urgency=RecommendationUrgency.IMMEDIATE,
               title="Emergency Cash Flow Stabilization",
               description="Critical cash flow situation requires immediate action to prevent business closure",
               rationale=f"With only {cash_runway:.1f} months of cash runway, immediate cash flow improvement is essential for business survival",
               specific_actions=[
                   "Accelerate accounts receivable collection with 15-day payment terms",
                   "Negotiate 60-day payment extensions with key suppliers",
                   "Implement daily cash flow monitoring dashboard",
                   "Reduce all non-essential expenses by 30%",
                   "Apply for emergency SBA lending or business line of credit"
               ],
               expected_outcomes=[
                   f"Extend cash runway from {cash_runway:.1f} to 6+ months",
                   "Stabilize daily cash position",
                   "Reduce financial stress and enable strategic focus"
               ],
               success_metrics=[
                   "Daily cash balance tracking",
                   "Accounts receivable aging under 30 days",
                   "Cash runway extended to 6+ months"
               ],
               metrics=RecommendationMetrics(
                   expected_revenue_impact=0,
                   expected_cost_impact=-business_data.get('monthly_expenses', 50000) * 0.2,
                   implementation_cost=5000,
                   payback_period_months=1,
                   success_probability=0.9,
                   risk_level="low",
                   effort_level="high",
                   confidence_score=0.95
               ),
               implementation_timeline="0-14 days",
               implementation_steps=[
                   {"step": 1, "action": "Create daily cash flow dashboard", "days": 2},
                   {"step": 2, "action": "Contact all customers with outstanding invoices", "days": 3},
                   {"step": 3, "action": "Negotiate supplier payment terms", "days": 5},
                   {"step": 4, "action": "Apply for emergency funding", "days": 7},
                   {"step": 5, "action": "Implement expense reduction plan", "days": 14}
               ],
               required_resources=["Cash flow management software", "Credit application documents", "Negotiation time"],
               prerequisites=["Access to customer payment data", "Supplier contact information"],
               economic_context=economic_data,
               regulatory_considerations=["SBA lending requirements", "State business continuity regulations"],
               tax_implications={"expense_deductions": "Accelerated collection may affect quarterly tax payments"},
               compliance_requirements=["Maintain customer contract terms", "Comply with supplier agreements"],
               dependent_recommendations=[],
               conflicting_recommendations=[],
               synergistic_recommendations=["financial_optimization_001"],
               key_performance_indicators=["Daily cash balance", "Days sales outstanding", "Cash runway months"],
               milestone_checkpoints=[
                   {"milestone": "Cash flow dashboard active", "target_date": "Day 3"},
                   {"milestone": "Customer payment acceleration", "target_date": "Day 7"},
                   {"milestone": "Expense reduction implemented", "target_date": "Day 14"}
               ],
               review_schedule="daily",
               ai_confidence=0.95,
               data_sources=["Financial analysis", "Cash flow projections"],
               analysis_methodology="Critical threshold analysis",
               generated_at=datetime.now()
           ))
       
       # Check for regulatory compliance issues
       sector = business_data.get('sector', '')
       if sector in ['food', 'healthcare', 'manufacturing']:
           recommendations.append(USBusinessRecommendation(
               recommendation_id="critical_002",
               category=RecommendationCategory.IMMEDIATE_CRITICAL,
               priority=RecommendationPriority.HIGH,
               urgency=RecommendationUrgency.IMMEDIATE,
               title="Regulatory Compliance Audit and Remediation",
               description="Conduct immediate compliance audit to prevent regulatory issues",
               rationale=f"Businesses in {sector} sector face strict US regulatory requirements that can result in significant penalties if not properly maintained",
               specific_actions=[
                   "Conduct comprehensive compliance audit within 30 days",
                   "Update all required licenses and permits",
                   "Implement compliance tracking system",
                   "Train staff on current regulatory requirements",
                   "Establish relationship with compliance consultant"
               ],
               expected_outcomes=[
                   "100% regulatory compliance",
                   "Reduced risk of penalties and fines",
                   "Improved operational confidence"
               ],
               success_metrics=[
                   "All licenses current and valid",
                   "Zero compliance violations",
                   "Staff compliance training completion rate"
               ],
               metrics=RecommendationMetrics(
                   expected_revenue_impact=0,
                   expected_cost_impact=15000,
                   implementation_cost=8000,
                   payback_period_months=3,
                   success_probability=0.85,
                   risk_level="low",
                   effort_level="medium",
                   confidence_score=0.9
               ),
               implementation_timeline="0-30 days",
               implementation_steps=[
                   {"step": 1, "action": "Schedule compliance audit", "days": 3},
                   {"step": 2, "action": "Review all current licenses", "days": 7},
                   {"step": 3, "action": "Update expired or missing permits", "days": 14},
                   {"step": 4, "action": "Implement tracking system", "days": 21},
                   {"step": 5, "action": "Complete staff training", "days": 30}
               ],
               required_resources=["Compliance consultant", "Legal review", "Staff training time"],
               prerequisites=["Current license inventory", "Regulatory requirement documentation"],
               economic_context=economic_data,
               regulatory_considerations=[f"US {sector} industry regulations", "State licensing requirements", "Federal compliance mandates"],
               tax_implications={"business_expenses": "Compliance costs are tax-deductible business expenses"},
               compliance_requirements=[f"{sector.title()} industry standards", "State business licensing", "Federal regulatory compliance"],
               dependent_recommendations=[],
               conflicting_recommendations=[],
               synergistic_recommendations=["operational_efficiency_001"],
               key_performance_indicators=["License validity status", "Compliance violations count", "Audit score"],
               milestone_checkpoints=[
                   {"milestone": "Compliance audit completed", "target_date": "Day 14"},
                   {"milestone": "All licenses updated", "target_date": "Day 21"},
                   {"milestone": "Staff training completed", "target_date": "Day 30"}
               ],
               review_schedule="monthly",
               ai_confidence=0.9,
               data_sources=["Regulatory databases", "Industry compliance standards"],
               analysis_methodology="Regulatory risk assessment",
               generated_at=datetime.now()
           ))
       
       return recommendations
   
   async def _generate_financial_optimization_recommendations(self, 
                                                            business_data: Dict[str, Any],
                                                            analysis_results: Dict[str, Any],
                                                            market_intelligence: Dict[str, Any],
                                                            economic_data: Dict[str, Any]) -> List[USBusinessRecommendation]:
       """Generate financial optimization recommendations."""
       
       recommendations = []
       
       # Analyze current financial performance
       financial_health = analysis_results.get("financial_health", {})
       profit_margin = financial_health.get("profitability", {}).get("net_margin", 0.1)
       monthly_revenue = business_data.get('monthly_revenue', [])
       current_monthly_revenue = monthly_revenue[-1] if monthly_revenue else 0
       
       # Revenue optimization recommendation
       if profit_margin < 0.15:  # Below 15% margin
           recommendations.append(USBusinessRecommendation(
               recommendation_id="financial_001",
               category=RecommendationCategory.FINANCIAL_OPTIMIZATION,
               priority=RecommendationPriority.HIGH,
               urgency=RecommendationUrgency.SHORT_TERM,
               title="Profit Margin Enhancement Strategy",
               description="Implement comprehensive profit margin improvement through pricing optimization and cost management",
               rationale=f"Current profit margin of {profit_margin*100:.1f}% is below industry benchmark of 15%, indicating significant improvement opportunity",
               specific_actions=[
                   "Conduct comprehensive pricing analysis vs competitors",
                   "Implement value-based pricing for premium products/services",
                   "Negotiate better supplier terms to reduce COGS by 5-8%",
                   "Eliminate or repriced low-margin products/services",
                   "Implement activity-based costing to identify profit centers"
               ],
               expected_outcomes=[
                   f"Increase profit margin from {profit_margin*100:.1f}% to 18%+",
                   f"Additional monthly profit of ${current_monthly_revenue * 0.05:,.0f}",
                   "Improved cash flow and business sustainability"
               ],
               success_metrics=[
                   "Gross profit margin percentage",
                   "Net profit margin percentage", 
                   "Revenue per customer",
                   "Customer acquisition cost vs lifetime value"
               ],
               metrics=RecommendationMetrics(
                   expected_roi=0.25,
                   expected_revenue_impact=current_monthly_revenue * 12 * 0.08,
                   expected_cost_impact=-current_monthly_revenue * 12 * 0.03,
                   implementation_cost=8000,
                   payback_period_months=2,
                   success_probability=0.8,
                   risk_level="low",
                   effort_level="medium",
                   confidence_score=0.85
               ),
               implementation_timeline="1-3 months",
               implementation_steps=[
                   {"step": 1, "action": "Complete pricing analysis", "days": 14},
                   {"step": 2, "action": "Negotiate supplier terms", "days": 30},
                   {"step": 3, "action": "Implement pricing changes", "days": 45},
                   {"step": 4, "action": "Monitor margin improvements", "days": 60},
                   {"step": 5, "action": "Optimize based on results", "days": 90}
               ],
               required_resources=["Pricing analysis tools", "Supplier negotiation time", "Financial tracking system"],
               prerequisites=["Historical pricing data", "Competitor pricing intelligence", "Supplier contracts"],
               economic_context=economic_data,
               regulatory_considerations=["Price discrimination regulations", "Fair competition laws"],
               tax_implications={"pricing_strategy": "Pricing changes may affect quarterly tax estimates"},
               compliance_requirements=["Truth in advertising", "Contract terms compliance"],
               dependent_recommendations=[],
               conflicting_recommendations=[],
               synergistic_recommendations=["growth_001", "market_expansion_001"],
               key_performance_indicators=["Gross margin %", "Net margin %", "Revenue per transaction"],
               milestone_checkpoints=[
                   {"milestone": "Pricing analysis completed", "target_date": "Day 14"},
                   {"milestone": "New pricing implemented", "target_date": "Day 45"},
                   {"milestone": "5% margin improvement achieved", "target_date": "Day 90"}
               ],
               review_schedule="monthly",
               ai_confidence=0.85,
               data_sources=["Financial analysis", "Market pricing data", "Industry benchmarks"],
               analysis_methodology="Financial ratio analysis with market comparison",
               generated_at=datetime.now()
           ))
       
       # Cash flow optimization
       recommendations.append(USBusinessRecommendation(
           recommendation_id="financial_002",
           category=RecommendationCategory.FINANCIAL_OPTIMIZATION,
           priority=RecommendationPriority.MEDIUM,
           urgency=RecommendationUrgency.SHORT_TERM,
           title="Cash Flow Acceleration Program",
           description="Optimize cash conversion cycle to improve working capital management",
           rationale="Faster cash conversion improves liquidity and reduces financing needs while supporting growth",
           specific_actions=[
               "Implement net-15 payment terms for new customers",
               "Offer 2% early payment discounts for payments within 10 days",
               "Establish automated invoicing and payment reminder system",
               "Negotiate 45-day payment terms with key suppliers",
               "Implement inventory just-in-time management"
           ],
           expected_outcomes=[
               "Reduce cash conversion cycle by 15-20 days",
               f"Improve cash flow by ${current_monthly_revenue * 0.15:,.0f} per month",
               "Reduce financing needs and interest expenses"
           ],
           success_metrics=[
               "Days sales outstanding (DSO)",
               "Cash conversion cycle days",
               "Monthly cash flow variance"
           ],
           metrics=RecommendationMetrics(
               expected_revenue_impact=current_monthly_revenue * 0.1,
               expected_cost_impact=-current_monthly_revenue * 0.02,
               implementation_cost=5000,
               payback_period_months=1,
               success_probability=0.85,
               risk_level="low",
               effort_level="medium",
               confidence_score=0.8
           ),
           implementation_timeline="1-2 months",
           implementation_steps=[
               {"step": 1, "action": "Analyze current cash conversion cycle", "days": 7},
               {"step": 2, "action": "Update customer payment terms", "days": 14},
               {"step": 3, "action": "Implement automated systems", "days": 30},
               {"step": 4, "action": "Negotiate supplier terms", "days": 45},
               {"step": 5, "action": "Optimize inventory management", "days": 60}
           ],
           required_resources=["Accounting software upgrade", "Customer communication", "Supplier negotiations"],
           prerequisites=["Current cash flow analysis", "Customer contract review"],
           economic_context=economic_data,
           regulatory_considerations=["Fair debt collection practices", "Customer contract laws"],
           tax_implications={"cash_flow": "Timing of revenue recognition may affect tax obligations"},
           compliance_requirements=["Customer agreement modifications", "Payment processing compliance"],
           dependent_recommendations=[],
           conflicting_recommendations=[],
           synergistic_recommendations=["financial_001", "operational_001"],
           key_performance_indicators=["DSO days", "Cash flow cycle time", "Working capital ratio"],
           milestone_checkpoints=[
               {"milestone": "New payment terms implemented", "target_date": "Day 14"},
               {"milestone": "Automated systems active", "target_date": "Day 30"},
               {"milestone": "Cash flow improvement measured", "target_date": "Day 60"}
           ],
           review_schedule="weekly",
           ai_confidence=0.8,
           data_sources=["Cash flow analysis", "Working capital metrics"],
           analysis_methodology="Cash conversion cycle optimization analysis",
           generated_at=datetime.now()
       ))
       
       return recommendations
   
   async def _generate_growth_acceleration_recommendations(self, 
                                                         business_data: Dict[str, Any],
                                                         analysis_results: Dict[str, Any],
                                                         market_intelligence: Dict[str, Any],
                                                         economic_data: Dict[str, Any]) -> List[USBusinessRecommendation]:
       """Generate growth acceleration recommendations."""
       
       recommendations = []
       
       # Analyze growth potential
       performance_metrics = analysis_results.get("performance_analysis", {})
       growth_trajectory = performance_metrics.get("performance_trend", "stable")
       current_revenue = sum(business_data.get('monthly_revenue', [0]))
       
       # Customer acquisition acceleration
       if growth_trajectory in ["stable", "improving"]:
           sector = business_data.get('sector', '')
           location_type = classify_us_location_type(
               business_data.get('city', ''),
               business_data.get('state', ''),
               business_data.get('zip_code', '')
           )
           
           recommendations.append(USBusinessRecommendation(
               recommendation_id="growth_001",
               category=RecommendationCategory.GROWTH_ACCELERATION,
               priority=RecommendationPriority.HIGH,
               urgency=RecommendationUrgency.SHORT_TERM,
               title="Strategic Customer Acquisition Campaign",
               description="Launch comprehensive customer acquisition program targeting high-value segments",
               rationale=f"Current stable performance provides foundation for accelerated customer acquisition in {sector} sector",
               specific_actions=[
                   "Develop ideal customer profile (ICP) based on current high-value customers",
                   "Launch targeted digital marketing campaign with $10K monthly budget",
                   "Implement referral program with 15% commission for existing customers",
                   "Establish partnerships with 3-5 complementary businesses",
                   "Optimize Google Ads and local SEO for 50% visibility increase"
               ],
               expected_outcomes=[
                   "Increase monthly new customers by 40%",
                   f"Generate additional ${current_revenue * 0.25:,.0f} annual revenue",
                   "Reduce customer acquisition cost by 20% through optimization"
               ],
               success_metrics=[
                   "New customer acquisition rate",
                   "Customer acquisition cost (CAC)",
                   "Customer lifetime value (CLV)",
                   "Marketing ROI"
               ],
               metrics=RecommendationMetrics(
                   expected_roi=0.35,
                   expected_revenue_impact=current_revenue * 0.25,
                   expected_cost_impact=120000,  # Annual marketing investment
                   implementation_cost=25000,
                   payback_period_months=8,
                   success_probability=0.75,
                   risk_level="medium",
                   effort_level="high",
                   confidence_score=0.8
               ),
               implementation_timeline="2-6 months",
               implementation_steps=[
                   {"step": 1, "action": "Develop ideal customer profile", "days": 14},
                   {"step": 2, "action": "Launch digital marketing campaigns", "days": 30},
                   {"step": 3, "action": "Implement referral program", "days": 45},
                   {"step": 4, "action": "Establish strategic partnerships", "days": 90},
                   {"step": 5, "action": "Optimize and scale successful channels", "days": 180}
               ],
               required_resources=["Marketing budget", "Digital marketing expertise", "CRM system", "Analytics tools"],
               prerequisites=["Customer data analysis", "Marketing channel assessment", "Budget allocation"],
               economic_context=economic_data,
               regulatory_considerations=["Digital marketing compliance", "Data privacy regulations", "Advertising truth standards"],
               tax_implications={"marketing_expenses": "Marketing costs are fully tax-deductible business expenses"},
               compliance_requirements=["GDPR/CCPA data handling", "FTC advertising guidelines", "Industry advertising standards"],
               dependent_recommendations=[],
               conflicting_recommendations=[],
               synergistic_recommendations=["financial_001", "technology_001"],
               key_performance_indicators=["Monthly new customers", "CAC", "CLV", "Marketing ROI", "Revenue growth rate"],
               milestone_checkpoints=[
                   {"milestone": "Marketing campaigns launched", "target_date": "Day 30"},
                   {"milestone": "Referral program active", "target_date": "Day 45"},
                   {"milestone": "20% customer increase achieved", "target_date": "Day 90"},
                   {"milestone": "40% customer increase achieved", "target_date": "Day 180"}
               ],
               review_schedule="monthly",
               ai_confidence=0.8,
               data_sources=["Customer analytics", "Market research", "Competitive analysis"],
               analysis_methodology="Customer acquisition funnel optimization analysis",
               generated_at=datetime.now()
           ))
       
       # Product/Service expansion recommendation
       if current_revenue > 500000:  # For established businesses
           recommendations.append(USBusinessRecommendation(
               recommendation_id="growth_002",
               category=RecommendationCategory.GROWTH_ACCELERATION,
               priority=RecommendationPriority.MEDIUM,
               urgency=RecommendationUrgency.MEDIUM_TERM,
               title="Strategic Product Line Extension",
               description="Expand product/service offerings to increase revenue per customer and market share",
               rationale="Strong financial foundation supports strategic expansion into complementary products/services",
               specific_actions=[
                   "Conduct customer needs analysis to identify expansion opportunities",
                   "Develop 2-3 new complementary products/services",
                   "Test market new offerings with existing customer base",
                   "Implement upselling and cross-selling training for staff",
                   "Launch new products with introductory pricing strategy"
               ],
               expected_outcomes=[
                   "Increase average order value by 30%",
                   f"Generate additional ${current_revenue * 0.2:,.0f} annual revenue",
                   "Strengthen customer relationships and retention"
               ],
               success_metrics=[
                   "Average order value",
                   "Products per customer",
                   "New product revenue contribution",
                   "Customer retention rate"
               ],
               metrics=RecommendationMetrics(
                   expected_roi=0.40,
                   expected_revenue_impact=current_revenue * 0.2,
                   expected_cost_impact=80000,
                   implementation_cost=50000,
                   payback_period_months=6,
                   success_probability=0.7,
                   risk_level="medium",
                   effort_level="high",
                   confidence_score=0.75
               ),
               implementation_timeline="3-6 months",
               implementation_steps=[
                   {"step": 1, "action": "Customer needs analysis", "days": 30},
                   {"step": 2, "action": "Product development planning", "days": 60},
                   {"step": 3, "action": "Prototype and test with customers", "days": 90},
                   {"step": 4, "action": "Staff training on new offerings", "days": 120},
                   {"step": 5, "action": "Full market launch", "days": 180}
               ],
               required_resources=["Product development budget", "Market research", "Staff training", "Marketing materials"],
               prerequisites=["Customer feedback analysis", "Market opportunity assessment", "Competitive positioning"],
               economic_context=economic_data,
               regulatory_considerations=["Product safety regulations", "Industry compliance standards"],
               tax_implications={"product_development": "R&D and product development costs may qualify for tax credits"},
               compliance_requirements=["Product safety standards", "Labeling requirements", "Quality assurance"],
               dependent_recommendations=["growth_001"],
               conflicting_recommendations=[],
               synergistic_recommendations=["market_expansion_001", "operational_001"],
               key_performance_indicators=["New product revenue %", "AOV", "Customer retention", "Cross-sell rate"],
               milestone_checkpoints=[
                   {"milestone": "Customer needs analysis completed", "target_date": "Day 30"},
                   {"milestone": "Product prototypes ready", "target_date": "Day 90"},
                   {"milestone": "Staff training completed", "target_date": "Day 120"},
                   {"milestone": "New products launched", "target_date": "Day 180"}
               ],
               review_schedule="monthly",
               ai_confidence=0.75,
               data_sources=["Customer feedback", "Market analysis", "Revenue analytics"],
               analysis_methodology="Product-market fit analysis with revenue modeling",
               generated_at=datetime.now()
           ))
       
       return recommendations
   
   async def _generate_market_expansion_recommendations(self, 
                                                      business_data: Dict[str, Any],
                                                      analysis_results: Dict[str, Any],
                                                      market_intelligence: Dict[str, Any],
                                                      economic_data: Dict[str, Any]) -> List[USBusinessRecommendation]:
       """Generate market expansion recommendations."""
       
       recommendations = []
       
       # Analyze expansion readiness
       performance_metrics = analysis_results.get("performance_analysis", {})
       overall_score = performance_metrics.get("overall_score", 50)
       cash_runway = analysis_results.get("financial_health", {}).get("cash_runway_months", 3)
       
       # Geographic expansion recommendation
       if overall_score > 70 and cash_runway > 6:
           current_state = business_data.get('state', 'CA')
           sector = business_data.get('sector', '')
           
           # Identify target expansion markets
           expansion_targets = self._identify_expansion_markets(current_state, sector)
           
           recommendations.append(USBusinessRecommendation(
               recommendation_id="expansion_001",
               category=RecommendationCategory.MARKET_EXPANSION,
               priority=RecommendationPriority.MEDIUM,
               urgency=RecommendationUrgency.MEDIUM_TERM,
               title=f"Strategic Geographic Expansion to {expansion_targets[0]}",
               description=f"Expand operations to {expansion_targets[0]} market to capture new revenue opportunities",
               rationale=f"Strong performance (score: {overall_score}) and healthy cash position support geographic expansion",
               specific_actions=[
                   f"Conduct detailed market research in {expansion_targets[0]}",
                   "Develop local partnership strategy or direct market entry plan",
                   "Establish local marketing and customer acquisition channels",
                   "Adapt products/services for local market preferences",
                   "Set up operational infrastructure for new market"
               ],
               expected_outcomes=[
                   f"Establish profitable operations in {expansion_targets[0]}",
                   "Increase total addressable market by 40-60%",
                   "Reduce business concentration risk through diversification"
               ],
               success_metrics=[
                   "New market revenue contribution",
                   "Market penetration rate",
                   "Customer acquisition cost in new market",
                   "Return on expansion investment"
               ],
               metrics=RecommendationMetrics(
                   expected_roi=0.25,
                   expected_revenue_impact=sum(business_data.get('monthly_revenue', [0])) * 0.4,
                   expected_cost_impact=200000,
                   implementation_cost=150000,
                   payback_period_months=18,
                   success_probability=0.6,
                   risk_level="high",
                   effort_level="very_high",
                   confidence_score=0.7
               ),
               implementation_timeline="6-12 months",
               implementation_steps=[
                   {"step": 1, "action": f"Complete {expansion_targets[0]} market research", "days": 60},
                   {"step": 2, "action": "Develop market entry strategy", "days": 90},
                   {"step": 3, "action": "Establish local partnerships/operations", "days": 180},
                   {"step": 4, "action": "Launch local marketing campaigns", "days": 240},
                   {"step": 5, "action": "Scale operations based on results", "days": 365}
               ],
               required_resources=["Market research budget", "Legal/regulatory consultation", "Local partnerships", "Marketing budget"],
               prerequisites=["Financial stability confirmation", "Operational scalability assessment", "Legal structure review"],
               economic_context=economic_data,
               regulatory_considerations=[f"{expansion_targets[0]} business licensing", "Interstate commerce regulations", "Tax obligations"],
               tax_implications={"multi_state": f"Multi-state tax obligations in {expansion_targets[0]}", "nexus_rules": "Sales tax nexus considerations"},
               compliance_requirements=[f"{expansion_targets[0]} business registration", "Local licensing requirements", "Insurance adjustments"],
               dependent_recommendations=["growth_001", "operational_001"],
               conflicting_recommendations=[],
               synergistic_recommendations=["technology_001", "financial_002"],
               key_performance_indicators=["New market revenue", "Market share", "Expansion ROI", "Customer metrics"],
               milestone_checkpoints=[
                   {"milestone": "Market research completed", "target_date": "Day 60"},
                   {"milestone": "Market entry plan approved", "target_date": "Day 90"},
                   {"milestone": "Operations established", "target_date": "Day 180"},
                   {"milestone": "Revenue generation started", "target_date": "Day 240"}
               ],
               review_schedule="monthly",
               ai_confidence=0.7,
               data_sources=["Market research", "Demographic data", "Competitive analysis"],
               analysis_methodology="Geographic expansion feasibility analysis",
               generated_at=datetime.now()
           ))
       
       return recommendations
   
   async def _generate_investment_recommendations(self, 
                                                business_data: Dict[str, Any],
                                                analysis_results: Dict[str, Any],
                                                market_intelligence: Dict[str, Any],
                                                economic_data: Dict[str, Any]) -> List[USBusinessRecommendation]:
       """Generate investment opportunity recommendations."""
       
       recommendations = []
       
       # Get investment capacity analysis
       current_cash = business_data.get('current_cash', 0)
       monthly_expenses = business_data.get('monthly_expenses', 50000)
       available_capital = max(0, current_cash - (monthly_expenses * 6))  # Keep 6 months runway
       
       if available_capital > 25000:  # Minimum investment threshold
           
           # Business reinvestment recommendation
           recommendations.append(USBusinessRecommendation(
               recommendation_id="investment_001",
               category=RecommendationCategory.INVESTMENT_OPPORTUNITIES,
               priority=RecommendationPriority.MEDIUM,
               urgency=RecommendationUrgency.MEDIUM_TERM,
               title="Strategic Business Reinvestment Program",
               description="Reinvest excess capital into high-ROI business improvements and growth initiatives",
               rationale=f"Available capital of ${available_capital:,.0f} provides opportunity for strategic reinvestment",
               specific_actions=[
                   f"Allocate ${available_capital * 0.4:,.0f} to technology and automation upgrades",
                   f"Invest ${available_capital * 0.3:,.0f} in marketing and customer acquisition",
                   f"Reserve ${available_capital * 0.2:,.0f} for inventory or equipment expansion",
                   f"Maintain ${available_capital * 0.1:,.0f} for opportunistic investments"
               ],
               expected_outcomes=[
                   "25-40% ROI on business reinvestment",
                   "Improved operational efficiency and competitiveness",
                   "Accelerated business growth and market position"
               ],
               success_metrics=[
                   "ROI on invested capital",
                   "Operational efficiency improvements",
                   "Revenue growth acceleration",
                   "Market share gains"
               ],
               metrics=RecommendationMetrics(
                   expected_roi=0.32,
                   expected_revenue_impact=sum(business_data.get('monthly_revenue', [0])) * 0.15,
                   expected_cost_impact=available_capital * -1,
                   implementation_cost=available_capital,
                   payback_period_months=12,
                   success_probability=0.8,
                   risk_level="medium",
                   effort_level="high",
                   confidence_score=0.85
               ),
               implementation_timeline="3-6 months",
               implementation_steps=[
                   {"step": 1, "action": "Prioritize investment opportunities by ROI", "days": 14},
                   {"step": 2, "action": "Begin technology and automation upgrades", "days": 30},
                   {"step": 3, "action": "Launch enhanced marketing campaigns", "days": 45},
                   {"step": 4, "action": "Execute equipment/inventory expansion", "days": 90},
                   {"step": 5, "action": "Monitor and optimize investment returns", "days": 180}
               ],
               required_resources=["Capital allocation planning", "Vendor selection", "Implementation management"],
               prerequisites=["ROI analysis completion", "Cash flow projections", "Strategic planning"],
               economic_context=economic_data,
               regulatory_considerations=["Capital expenditure reporting", "Depreciation schedules"],
               tax_implications={"capital_expenditures": "Equipment purchases qualify for bonus depreciation", "business_expenses": "Marketing and operational expenses are immediately deductible"},
               compliance_requirements=["Asset tracking and reporting", "Vendor compliance verification"],
               dependent_recommendations=[],
               conflicting_recommendations=[],
               synergistic_recommendations=["growth_001", "technology_001", "operational_001"],
               key_performance_indicators=["Investment ROI", "Operational efficiency metrics", "Revenue growth rate"],
               milestone_checkpoints=[
                   {"milestone": "Investment priorities established", "target_date": "Day 14"},
                   {"milestone": "Technology upgrades initiated", "target_date": "Day 30"},
                   {"milestone": "Marketing investment deployed", "target_date": "Day 45"},
                   {"milestone": "Equipment expansion completed", "target_date": "Day 90"}
               ],
               review_schedule="monthly",
               ai_confidence=0.85,
               data_sources=["Financial analysis", "ROI projections", "Market opportunity assessment"],
               analysis_methodology="Capital allocation optimization analysis",
               generated_at=datetime.now()
           ))
           
           # Market investment recommendation
           if available_capital > 50000:
               recommendations.append(USBusinessRecommendation(
                   recommendation_id="investment_002",
                   category=RecommendationCategory.INVESTMENT_OPPORTUNITIES,
                   priority=RecommendationPriority.LOW,
                   urgency=RecommendationUrgency.LONG_TERM,
                   title="Diversified Market Investment Portfolio",
                   description="Create diversified investment portfolio to build wealth and hedge against business risks",
                   rationale="Excess capital above business needs should be invested for long-term wealth building and risk diversification",
                   specific_actions=[
                       f"Invest ${min(available_capital * 0.3, 50000):,.0f} in diversified index funds",
                       f"Allocate ${min(available_capital * 0.2, 30000):,.0f} to sector-specific ETFs",
                       f"Consider ${min(available_capital * 0.1, 20000):,.0f} in real estate investment trusts (REITs)",
                       "Establish systematic investment plan with monthly contributions",
                       "Review and rebalance portfolio quarterly"
                   ],
                   expected_outcomes=[
                       "8-10% average annual investment returns",
                       "Reduced overall business risk through diversification",
                       "Long-term wealth accumulation and financial security"
                   ],
                   success_metrics=[
                       "Portfolio annual return",
                       "Risk-adjusted returns (Sharpe ratio)",
                       "Portfolio diversification metrics",
                       "Total investment value growth"
                   ],
                   metrics=RecommendationMetrics(
                       expected_roi=0.09,
                       expected_revenue_impact=0,  # Investment returns, not business revenue
                       expected_cost_impact=0,
                       implementation_cost=min(available_capital * 0.6, 100000),
                       payback_period_months=None,  # Long-term investment
                       success_probability=0.75,
                       risk_level="medium",
                       effort_level="low",
                       confidence_score=0.8
                   ),
                   implementation_timeline="1-2 months",
                   implementation_steps=[
                       {"step": 1, "action": "Open investment accounts with reputable brokers", "days": 7},
                       {"step": 2, "action": "Develop investment allocation strategy", "days": 14},
                       {"step": 3, "action": "Execute initial investment purchases", "days": 21},
                       {"step": 4, "action": "Set up automatic monthly contributions", "days": 30},
                       {"step": 5, "action": "Establish quarterly review schedule", "days": 60}
                   ],
                   required_resources=["Investment broker relationship", "Financial planning software", "Quarterly review time"],
                   prerequisites=["Emergency fund establishment", "Business cash flow stability", "Risk tolerance assessment"],
                   economic_context=economic_data,
                   regulatory_considerations=["Securities regulations", "Investment advisor regulations"],
                   tax_implications={"capital_gains": "Long-term capital gains tax advantages", "dividends": "Qualified dividend tax treatment"},
                   compliance_requirements=["Investment reporting requirements", "Tax reporting for gains/losses"],
                   dependent_recommendations=["investment_001"],
                   conflicting_recommendations=[],
                   synergistic_recommendations=["financial_002"],
                   key_performance_indicators=["Portfolio return", "Risk metrics", "Asset allocation balance"],
                   milestone_checkpoints=[
                       {"milestone": "Investment accounts opened", "target_date": "Day 7"},
                       {"milestone": "Initial investments executed", "target_date": "Day 21"},
                       {"milestone": "Automatic contributions active", "target_date": "Day 30"},
                       {"milestone": "First quarterly review completed", "target_date": "Day 90"}
                   ],
                   review_schedule="quarterly",
                   ai_confidence=0.8,
                   data_sources=["Market analysis", "Economic indicators", "Investment research"],
                   analysis_methodology="Modern portfolio theory with risk-return optimization",
                   generated_at=datetime.now()
               ))
       
       return recommendations
   
   async def _generate_risk_mitigation_recommendations(self, 
                                                     business_data: Dict[str, Any],
                                                     analysis_results: Dict[str, Any],
                                                     market_intelligence: Dict[str, Any],
                                                     economic_data: Dict[str, Any]) -> List[USBusinessRecommendation]:
       """Generate risk mitigation recommendations."""
       
       recommendations = []
       
       # Analyze risk profile
       risk_analysis = analysis_results.get("risk_analysis", {})
       overall_risk = risk_analysis.get("overall_risk_score", 50)
       financial_risks = risk_analysis.get("financial_risks", {})
       
       # Business continuity planning
       recommendations.append(USBusinessRecommendation(
           recommendation_id="risk_001",
           category=RecommendationCategory.RISK_MITIGATION,
           priority=RecommendationPriority.MEDIUM,
           urgency=RecommendationUrgency.SHORT_TERM,
           title="Comprehensive Business Continuity Plan",
           description="Develop and implement comprehensive business continuity and disaster recovery plan",
           rationale="Business continuity planning is essential for protecting against operational disruptions and ensuring long-term sustainability",
           specific_actions=[
               "Conduct comprehensive risk assessment and business impact analysis",
               "Develop written business continuity and disaster recovery procedures",
               "Establish data backup and recovery systems with cloud storage",
               "Create emergency communication plan for customers, suppliers, and employees",
               "Conduct quarterly business continuity drills and plan updates"
           ],
           expected_outcomes=[
               "Reduced business disruption risk by 70%",
               "Faster recovery time from operational incidents",
               "Improved customer and stakeholder confidence"
           ],
           success_metrics=[
               "Recovery time objectives (RTO)",
               "Recovery point objectives (RPO)",
               "Business continuity plan test success rate",
               "Incident response time"
           ],
           metrics=RecommendationMetrics(
               expected_revenue_impact=0,
               expected_cost_impact=15000,
               implementation_cost=12000,
               payback_period_months=None,  # Risk mitigation benefit
               success_probability=0.9,
               risk_level="low",
               effort_level="medium",
               confidence_score=0.85
           ),
           implementation_timeline="1-3 months",
           implementation_steps=[
               {"step": 1, "action": "Complete risk assessment", "days": 14},
               {"step": 2, "action": "Draft continuity procedures", "days": 30},
               {"step": 3, "action": "Implement backup systems", "days": 45},
               {"step": 4, "action": "Train staff on procedures", "days": 60},
               {"step": 5, "action": "Conduct first continuity drill", "days": 90}
           ],
           required_resources=["Business continuity consultant", "Cloud backup services", "Staff training time"],
           prerequisites=["Current operational process documentation", "IT infrastructure assessment"],
           economic_context=economic_data,
           regulatory_considerations=["Data protection regulations", "Industry continuity standards"],
           tax_implications={"business_insurance": "Business continuity investments may qualify for tax deductions"},
           compliance_requirements=["Data backup compliance", "Emergency notification requirements"],
           dependent_recommendations=[],
           conflicting_recommendations=[],
           synergistic_recommendations=["technology_001", "operational_001"],
           key_performance_indicators=["Plan completeness", "Drill success rate", "Recovery time", "System uptime"],
           milestone_checkpoints=[
               {"milestone": "Risk assessment completed", "target_date": "Day 14"},
               {"milestone": "Procedures documented", "target_date": "Day 30"},
               {"milestone": "Backup systems operational", "target_date": "Day 45"},
               {"milestone": "Staff training completed", "target_date": "Day 60"}
           ],
           review_schedule="quarterly",
           ai_confidence=0.85,
           data_sources=["Risk assessment", "Industry best practices", "Regulatory requirements"],
           analysis_methodology="Business impact analysis with continuity planning",
           generated_at=datetime.now()
       ))
       
       # Insurance coverage review
       recommendations.append(USBusinessRecommendation(
           recommendation_id="risk_002",
           category=RecommendationCategory.RISK_MITIGATION,
           priority=RecommendationPriority.MEDIUM,
           urgency=RecommendationUrgency.SHORT_TERM,
           title="Comprehensive Business Insurance Review",
           description="Review and optimize business insurance coverage to ensure adequate protection",
           rationale="Proper insurance coverage is critical for protecting against financial losses from various business risks",
           specific_actions=[
               "Conduct comprehensive insurance needs assessment",
               "Review current coverage limits and deductibles",
               "Obtain quotes for general liability, property, and business interruption insurance",
               "Consider cyber liability insurance for digital assets and data protection",
               "Implement key person life insurance for critical personnel"
           ],
           expected_outcomes=[
               "Comprehensive risk coverage with appropriate limits",
               "Reduced out-of-pocket risk exposure",
               "Cost-optimized insurance premium structure"
           ],
           success_metrics=[
               "Coverage adequacy assessment score",
               "Premium cost per dollar of coverage",
               "Claims processing efficiency",
               "Coverage gap identification and closure"
           ],
           metrics=RecommendationMetrics(
               expected_revenue_impact=0,
               expected_cost_impact=business_data.get('annual_revenue', 1000000) * 0.015,  # ~1.5% of revenue typical
               implementation_cost=2000,
               payback_period_months=None,  # Risk protection benefit
               success_probability=0.95,
               risk_level="low",
               effort_level="low",
               confidence_score=0.9
           ),
           implementation_timeline="1 month",
           implementation_steps=[
               {"step": 1, "action": "Conduct insurance needs assessment", "days": 7},
               {"step": 2, "action": "Request quotes from multiple insurers", "days": 14},
               {"step": 3, "action": "Compare coverage options and costs", "days": 21},
               {"step": 4, "action": "Select and purchase optimal coverage", "days": 28},
               {"step": 5, "action": "Schedule annual coverage review", "days": 30}
           ],
           required_resources=["Insurance broker consultation", "Business valuation assessment", "Risk analysis documentation"],
           prerequisites=["Current insurance policy review", "Business asset valuation", "Risk exposure assessment"],
           economic_context=economic_data,
           regulatory_considerations=["State insurance requirements", "Industry-specific insurance mandates"],
           tax_implications={"insurance_premiums": "Business insurance premiums are tax-deductible expenses"},
           compliance_requirements=["Minimum coverage requirements", "Certificate of insurance maintenance"],
           dependent_recommendations=["risk_001"],
           conflicting_recommendations=[],
           synergistic_recommendations=["financial_001"],
           key_performance_indicators=["Coverage adequacy %", "Premium optimization", "Claims response time"],
           milestone_checkpoints=[
               {"milestone": "Insurance assessment completed", "target_date": "Day 7"},
               {"milestone": "Quotes obtained and compared", "target_date": "Day 21"},
               {"milestone": "New coverage implemented", "target_date": "Day 28"}
           ],
           review_schedule="annually",
           ai_confidence=0.9,
           data_sources=["Insurance market analysis", "Risk assessment data", "Industry benchmarks"],
           analysis_methodology="Risk-based insurance needs analysis",
           generated_at=datetime.now()
       ))
       
       return recommendations
   
   async def _generate_operational_efficiency_recommendations(self, 
                                                            business_data: Dict[str, Any],
                                                            analysis_results: Dict[str, Any],
                                                            market_intelligence: Dict[str, Any],
                                                            economic_data: Dict[str, Any]) -> List[USBusinessRecommendation]:
       """Generate operational efficiency recommendations."""
       
       recommendations = []
       
       # Process automation recommendation
       employees_count = business_data.get('employees_count', 1)
       if employees_count > 3:  # Automation makes sense with some scale
           
           recommendations.append(USBusinessRecommendation(
               recommendation_id="operational_001",
               category=RecommendationCategory.OPERATIONAL_EFFICIENCY,
               priority=RecommendationPriority.MEDIUM,
               urgency=RecommendationUrgency.MEDIUM_TERM,
               title="Business Process Automation Initiative",
               description="Implement automation tools to streamline operations and improve efficiency",
               rationale="Process automation can significantly reduce manual work, improve accuracy, and free up staff for higher-value activities",
               specific_actions=[
                   "Audit current manual processes and identify automation opportunities",
                   "Implement customer relationship management (CRM) system",
                   "Automate invoicing, payment processing, and accounts receivable",
                   "Deploy project management and workflow automation tools",
                   "Integrate systems to eliminate duplicate data entry"
               ],
               expected_outcomes=[
                   "Reduce manual processing time by 40-60%",
                   "Improve accuracy and reduce errors by 80%",
                   "Free up 10-15 hours per week for strategic activities"
               ],
               success_metrics=[
                   "Hours saved per week through automation",
                   "Error rate reduction percentage",
                   "Employee productivity improvement",
                   "Customer service response time improvement"
               ],
               metrics=RecommendationMetrics(
                   expected_roi=0.30,
                   expected_revenue_impact=sum(business_data.get('monthly_revenue', [0])) * 0.08,
                   expected_cost_impact=-20000,  # Annual software costs
                   implementation_cost=35000,
                   payback_period_months=8,
                   success_probability=0.85,
                   risk_level="low",
                   effort_level="medium",
                   confidence_score=0.8
               ),
               implementation_timeline="2-4 months",
               implementation_steps=[
                   {"step": 1, "action": "Complete process automation audit", "days": 21},
                   {"step": 2, "action": "Select and procure automation tools", "days": 45},
                   {"step": 3, "action": "Implement CRM and core systems", "days": 75},
                   {"step": 4, "action": "Train staff on new systems", "days": 90},
                   {"step": 5, "action": "Optimize and expand automation", "days": 120}
               ],
               required_resources=["Automation software licenses", "Implementation consulting", "Staff training time", "IT support"],
               prerequisites=["Current process documentation", "IT infrastructure assessment", "Staff capability evaluation"],
               economic_context=economic_data,
               regulatory_considerations=["Data security compliance", "Software licensing compliance"],
               tax_implications={"software_expenses": "Software purchases may qualify for immediate expensing under Section 179"},
               compliance_requirements=["Data privacy compliance", "Software license compliance", "Employee training records"],
               dependent_recommendations=[],
               conflicting_recommendations=[],
               synergistic_recommendations=["technology_001", "growth_001", "financial_002"],
               key_performance_indicators=["Automation rate %", "Processing time reduction", "Error rate", "Employee satisfaction"],
               milestone_checkpoints=[
                   {"milestone": "Process audit completed", "target_date": "Day 21"},
                   {"milestone": "Automation tools selected", "target_date": "Day 45"},
                   {"milestone": "Core systems implemented", "target_date": "Day 75"},
                   {"milestone": "Staff training completed", "target_date": "Day 90"}
               ],
               review_schedule="monthly",
               ai_confidence=0.8,
               data_sources=["Process analysis", "Automation benchmarks", "ROI calculations"],
               analysis_methodology="Process efficiency analysis with automation ROI modeling",
               generated_at=datetime.now()
           ))
       
       return recommendations
   
   async def _generate_strategic_positioning_recommendations(self, 
                                                           business_data: Dict[str, Any],
                                                           analysis_results: Dict[str, Any],
                                                           market_intelligence: Dict[str, Any],
                                                           economic_data: Dict[str, Any]) -> List[USBusinessRecommendation]:
       """Generate strategic positioning recommendations."""
       
       recommendations = []
       
       # Competitive differentiation strategy
       competitive_analysis = analysis_results.get("competitive_analysis", {})
       competitive_strength = competitive_analysis.get("competitive_strength_score", 50)
       
       if competitive_strength < 70:  # Room for improvement
           recommendations.append(USBusinessRecommendation(
               recommendation_id="strategic_001",
               category=RecommendationCategory.STRATEGIC_POSITIONING,
               priority=RecommendationPriority.HIGH,
               urgency=RecommendationUrgency.MEDIUM_TERM,
               title="Competitive Differentiation Strategy",
               description="Develop and implement clear competitive differentiation to strengthen market position",
               rationale=f"Current competitive strength of {competitive_strength}/100 indicates opportunity to improve market positioning",
               specific_actions=[
                   "Conduct comprehensive competitive analysis and positioning audit",
                   "Identify and develop unique value propositions",
                   "Enhance customer service excellence as competitive advantage",
                   "Develop specialized expertise or niche market focus",
                   "Implement brand strengthening and marketing repositioning"
               ],
               expected_outcomes=[
                   "Improve competitive strength score to 80+",
                   "Increase customer retention by 25%",
                   "Enable premium pricing with 10-15% higher margins"
               ],
               success_metrics=[
                   "Competitive strength assessment score",
                   "Customer retention rate",
                   "Price premium achievement",
                   "Brand recognition metrics"
               ],
               metrics=RecommendationMetrics(
                   expected_roi=0.25,
                   expected_revenue_impact=sum(business_data.get('monthly_revenue', [0])) * 0.12,
                   expected_cost_impact=50000,
                   implementation_cost=40000,
                   payback_period_months=10,
                   success_probability=0.75,
                   risk_level="medium",
                   effort_level="high",
                   confidence_score=0.8
               ),
               implementation_timeline="3-6 months",
               implementation_steps=[
                   {"step": 1, "action": "Complete competitive positioning audit", "days": 30},
                   {"step": 2, "action": "Develop unique value propositions", "days": 60},
                   {"step": 3, "action": "Implement customer service enhancements", "days": 90},
                   {"step": 4, "action": "Launch brand repositioning campaign", "days": 120},
                   {"step": 5, "action": "Monitor competitive improvements", "days": 180}
               ],
               required_resources=["Market research", "Brand consulting", "Marketing campaign budget", "Staff training"],
               prerequisites=["Customer feedback analysis", "Competitive intelligence", "Brand audit"],
               economic_context=economic_data,
               regulatory_considerations=["Advertising compliance", "Fair competition practices"],
               tax_implications={"marketing_expenses": "Brand development and marketing costs are tax-deductible"},
               compliance_requirements=["Truth in advertising", "Intellectual property compliance"],
               dependent_recommendations=[],
               conflicting_recommendations=[],
               synergistic_recommendations=["growth_001", "operational_001"],
               key_performance_indicators=["Competitive position score", "Customer retention %", "Price premium %", "Brand awareness"],
               milestone_checkpoints=[
                   {"milestone": "Competitive audit completed", "target_date": "Day 30"},
                   {"milestone": "Value propositions defined", "target_date": "Day 60"},
                   {"milestone": "Service enhancements implemented", "target_date": "Day 90"},
                   {"milestone": "Brand campaign launched", "target_date": "Day 120"}
               ],
               review_schedule="monthly",
               ai_confidence=0.8,
               data_sources=["Competitive analysis", "Customer research", "Market positioning data"],
               analysis_methodology="Strategic positioning analysis with competitive benchmarking",
               generated_at=datetime.now()
           ))
       
       return recommendations
   
   async def _generate_technology_digital_recommendations(self, 
                                                        business_data: Dict[str, Any],
                                                        analysis_results: Dict[str, Any],
                                                        market_intelligence: Dict[str, Any],
                                                        economic_data: Dict[str, Any]) -> List[USBusinessRecommendation]:
       """Generate technology and digital transformation recommendations."""
       
       recommendations = []
       
       # Digital presence enhancement
       sector = business_data.get('sector', '')
       recommendations.append(USBusinessRecommendation(
           recommendation_id="technology_001",
           category=RecommendationCategory.TECHNOLOGY_DIGITAL,
           priority=RecommendationPriority.HIGH,
           urgency=RecommendationUrgency.SHORT_TERM,
           title="Comprehensive Digital Transformation Initiative",
           description="Modernize digital presence and capabilities to compete effectively in today's market",
           rationale="Strong digital presence is essential for customer acquisition, retention, and operational efficiency in modern business",
           specific_actions=[
               "Develop professional, mobile-optimized website with e-commerce capabilities",
               "Implement comprehensive social media marketing strategy",
               "Deploy customer relationship management (CRM) system",
               "Establish Google My Business and local SEO optimization",
               "Integrate online booking/ordering system for customer convenience"
           ],
           expected_outcomes=[
               "Increase online visibility by 300%",
               "Generate 25% of new customers through digital channels",
               "Improve customer engagement and retention by 30%"
           ],
           success_metrics=[
               "Website traffic and conversion rates",
               "Social media engagement metrics",
               "Online customer acquisition rate",
               "Digital revenue contribution percentage"
           ],
           metrics=RecommendationMetrics(
               expected_roi=0.40,
               expected_revenue_impact=sum(business_data.get('monthly_revenue', [0])) * 0.2,
               expected_cost_impact=30000,
               implementation_cost=25000,
               payback_period_months=6,
               success_probability=0.85,
               risk_level="low",
               effort_level="medium",
               confidence_score=0.85
           ),
           implementation_timeline="2-4 months",
           implementation_steps=[
               {"step": 1, "action": "Design and develop professional website", "days": 30},
               {"step": 2, "action": "Implement CRM system", "days": 45},
               {"step": 3, "action": "Launch social media presence", "days": 60},
               {"step": 4, "action": "Optimize for local search", "days": 75},
               {"step": 5, "action": "Deploy online booking/ordering", "days": 120}
           ],
           required_resources=["Web development", "CRM software", "Social media management", "SEO tools"],
           prerequisites=["Brand assets and content", "Business process documentation", "Customer data organization"],
           economic_context=economic_data,
           regulatory_considerations=["Data privacy compliance (GDPR/CCPA)", "E-commerce regulations", "Accessibility standards"],
           tax_implications={"technology_expenses": "Technology investments may qualify for immediate expensing or depreciation benefits"},
           compliance_requirements=["Website accessibility (ADA)", "Data protection compliance", "E-commerce regulations"],
           dependent_recommendations=[],
           conflicting_recommendations=[],
           synergistic_recommendations=["growth_001", "operational_001", "strategic_001"],
           key_performance_indicators=["Website traffic", "Online conversion rate", "Digital engagement", "Online revenue %"],
           milestone_checkpoints=[
               {"milestone": "Website launched", "target_date": "Day 30"},
               {"milestone": "CRM system operational", "target_date": "Day 45"},
               {"milestone": "Social media active", "target_date": "Day 60"},
               {"milestone": "Online systems integrated", "target_date": "Day 120"}
           ],
           review_schedule="monthly",
           ai_confidence=0.85,
           data_sources=["Digital marketing analysis", "Technology trends", "Customer behavior data"],
           analysis_methodology="Digital transformation roadmap with ROI modeling",
           generated_at=datetime.now()
       ))
       
       return recommendations
   
   async def _generate_compliance_regulatory_recommendations(self, 
                                                           business_data: Dict[str, Any],
                                                           analysis_results: Dict[str, Any],
                                                           market_intelligence: Dict[str, Any],
                                                           economic_data: Dict[str, Any]) -> List[USBusinessRecommendation]:
       """Generate compliance and regulatory recommendations."""
       
       recommendations = []
       
       # Tax optimization strategy
       annual_revenue = sum(business_data.get('monthly_revenue', [0]))
       if annual_revenue > 500000:  # For businesses with substantial revenue
           
           recommendations.append(USBusinessRecommendation(
               recommendation_id="compliance_001",
               category=RecommendationCategory.COMPLIANCE_REGULATORY,
               priority=RecommendationPriority.MEDIUM,
               urgency=RecommendationUrgency.SHORT_TERM,
               title="Strategic Tax Optimization and Compliance Review",
               description="Optimize tax strategy and ensure comprehensive compliance with US tax regulations",
               rationale=f"With annual revenue of ${annual_revenue:,.0f}, strategic tax planning can yield significant savings",
               specific_actions=[
                   "Conduct comprehensive tax strategy review with CPA",
                   "Evaluate business structure optimization (LLC, S-Corp, etc.)",
                   "Implement expense tracking and deduction maximization systems",
                   "Consider retirement plan contributions for tax advantages",
                   "Establish quarterly tax planning and payment schedule"
               ],
               expected_outcomes=[
                   "Reduce annual tax liability by 15-25%",
                   "Improve cash flow through optimized tax timing",
                   "Ensure 100% compliance with tax obligations"
               ],
               success_metrics=[
                   "Tax savings achieved vs prior year",
                   "Effective tax rate reduction",
                   "Compliance score (zero penalties/interest)",
                   "Cash flow improvement from tax optimization"
               ],
               metrics=RecommendationMetrics(
                   expected_revenue_impact=0,
                   expected_cost_impact=-annual_revenue * 0.05,  # Tax savings
                   implementation_cost=8000,
                   payback_period_months=2,
                   success_probability=0.9,
                   risk_level="low",
                   effort_level="medium",
                   confidence_score=0.85
               ),
               implementation_timeline="1-2 months",
               implementation_steps=[
                   {"step": 1, "action": "Schedule comprehensive tax review", "days": 7},
                   {"step": 2, "action": "Analyze business structure optimization", "days": 21},
                   {"step": 3, "action": "Implement expense tracking improvements", "days": 30},
                   {"step": 4, "action": "Set up retirement contributions", "days": 45},
                   {"step": 5, "action": "Establish quarterly tax planning", "days": 60}
               ],
               required_resources=["CPA/tax advisor consultation", "Accounting software upgrade", "Financial planning time"],
               prerequisites=["Financial records organization", "Current tax situation analysis", "Business goals clarification"],
               economic_context=economic_data,
               regulatory_considerations=["IRS tax code compliance", "State tax obligations", "Payroll tax requirements"],
               tax_implications={"tax_optimization": "Strategic tax planning within legal framework", "deduction_maximization": "Legitimate business expense optimization"},
               compliance_requirements=["Tax return filing", "Quarterly payment obligations", "Record keeping requirements"],
               dependent_recommendations=[],
               conflicting_recommendations=[],
               synergistic_recommendations=["investment_001", "financial_001"],
               key_performance_indicators=["Effective tax rate", "Tax savings $", "Compliance score", "Penalty avoidance"],
               milestone_checkpoints=[
                   {"milestone": "Tax review completed", "target_date": "Day 21"},
                   {"milestone": "Structure optimization decided", "target_date": "Day 30"},
                   {"milestone": "Systems implemented", "target_date": "Day 45"},
                   {"milestone": "Quarterly planning active", "target_date": "Day 60"}
               ],
               review_schedule="quarterly",
               ai_confidence=0.85,
               data_sources=["Tax code analysis", "Financial performance data", "CPA recommendations"],
               analysis_methodology="Tax optimization analysis with compliance verification",
               generated_at=datetime.now()
           ))
       
       return recommendations
   
   def _prioritize_recommendations(self, recommendations: List[USBusinessRecommendation],
                                 business_data: Dict[str, Any],
                                 analysis_results: Dict[str, Any]) -> List[USBusinessRecommendation]:
       """Prioritize recommendations based on business context and urgency."""
       
       # Calculate priority scores for each recommendation
       for rec in recommendations:
           rec.priority_score = self._calculate_priority_score(rec, business_data, analysis_results)
       
       # Sort by priority score (higher = more important)
       prioritized = sorted(recommendations, key=lambda x: x.priority_score, reverse=True)
       
       return prioritized
   
   def _calculate_priority_score(self, recommendation: USBusinessRecommendation,
                               business_data: Dict[str, Any],
                               analysis_results: Dict[str, Any]) -> float:
       """Calculate priority score for recommendation."""
       
       score = 0.0
       
       # Base priority weights
       priority_weights = {
           RecommendationPriority.CRITICAL: 100,
           RecommendationPriority.HIGH: 75,
           RecommendationPriority.MEDIUM: 50,
           RecommendationPriority.LOW: 25
       }
       score += priority_weights.get(recommendation.priority, 50)
       
       # Urgency weights
       urgency_weights = {
           RecommendationUrgency.IMMEDIATE: 50,
           RecommendationUrgency.SHORT_TERM: 35,
           RecommendationUrgency.MEDIUM_TERM: 20,
           RecommendationUrgency.LONG_TERM: 10
       }
       score += urgency_weights.get(recommendation.urgency, 20)
       
       # ROI impact (if available)
       if recommendation.metrics.expected_roi:
           score += min(recommendation.metrics.expected_roi * 100, 50)
       
       # Success probability
       score += recommendation.metrics.success_probability * 30
       
       # Confidence adjustment
       score *= recommendation.ai_confidence
       
       # Business context adjustments
       financial_health = analysis_results.get("financial_health", {})
       cash_runway = financial_health.get("cash_runway_months", 6)
       
       # Boost critical recommendations if cash is tight
       if cash_runway < 3 and recommendation.category == RecommendationCategory.IMMEDIATE_CRITICAL:
           score *= 1.5
       
       # Boost growth recommendations if financially stable
       if (cash_runway > 6 and 
           recommendation.category in [RecommendationCategory.GROWTH_ACCELERATION, 
                                     RecommendationCategory.MARKET_EXPANSION]):
           score *= 1.2
       
       return score
   
   def _create_implementation_roadmap(self, recommendations: List[USBusinessRecommendation],
                                    business_data: Dict[str, Any]) -> Dict[str, Any]:
       """Create implementation roadmap for recommendations."""
       
       roadmap = {
           "immediate_actions": [],  # 0-30 days
           "short_term_initiatives": [],  # 1-3 months
           "medium_term_projects": [],  # 3-6 months
           "long_term_goals": [],  # 6+ months
           "resource_requirements": {},
           "budget_allocation": {},
           "timeline_overview": ""
       }
       
       total_investment = 0
       
       for rec in recommendations:
           timeline_category = self._categorize_timeline(rec.implementation_timeline)
           
           roadmap_item = {
               "recommendation_id": rec.recommendation_id,
               "title": rec.title,
               "category": rec.category.value,
               "priority": rec.priority.value,
               "investment_required": rec.metrics.implementation_cost or 0,
               "expected_roi": rec.metrics.expected_roi or 0,
               "success_probability": rec.metrics.success_probability,
               "key_milestones": rec.milestone_checkpoints[:3]  # Top 3 milestones
           }
           
           roadmap[timeline_category].append(roadmap_item)
           total_investment += rec.metrics.implementation_cost or 0
       
       # Resource aggregation
       all_resources = []
       for rec in recommendations:
           all_resources.extend(rec.required_resources)
       
       roadmap["resource_requirements"] = {
           "total_resources": list(set(all_resources)),
           "critical_resources": self._identify_critical_resources(all_resources),
           "resource_timeline": self._create_resource_timeline(recommendations)
       }
       
       # Budget allocation
       roadmap["budget_allocation"] = {
           "total_investment_required": total_investment,
           "by_category": self._calculate_budget_by_category(recommendations),
           "by_timeline": self._calculate_budget_by_timeline(recommendations),
           "funding_sources": self._suggest_funding_sources(total_investment, business_data)
       }
       
       # Timeline overview
       roadmap["timeline_overview"] = self._create_timeline_narrative(recommendations)
       
       return roadmap
   
   def _create_success_tracking_framework(self, recommendations: List[USBusinessRecommendation],
                                        business_data: Dict[str, Any]) -> Dict[str, Any]:
       """Create success tracking framework for recommendations."""
       
       framework = {
           "overall_success_metrics": [],
           "recommendation_tracking": {},
           "performance_dashboard": {},
           "review_schedule": {},
           "success_milestones": [],
           "roi_tracking": {}
       }
       
       # Aggregate KPIs
       all_kpis = []
       for rec in recommendations:
           all_kpis.extend(rec.key_performance_indicators)
       
       framework["overall_success_metrics"] = list(set(all_kpis))
       
       # Individual recommendation tracking
       for rec in recommendations:
           framework["recommendation_tracking"][rec.recommendation_id] = {
               "title": rec.title,
               "success_metrics": rec.success_metrics,
               "kpis": rec.key_performance_indicators,
               "milestones": rec.milestone_checkpoints,
               "expected_roi": rec.metrics.expected_roi,
               "review_frequency": rec.review_schedule
           }
       
       # Performance dashboard structure
       framework["performance_dashboard"] = {
           "executive_summary": [
               "Total recommendations implemented",
               "Overall ROI achieved",
               "Implementation success rate",
               "Business performance improvement"
           ],
           "financial_metrics": [
               "Revenue growth rate",
               "Profit margin improvement",
               "Cash flow enhancement",
               "ROI on recommendations"
           ],
           "operational_metrics": [
               "Efficiency improvements",
               "Customer satisfaction",
               "Process optimization",
               "Technology adoption"
           ]
       }
       
       return framework
   
   def _calculate_impact_projections(self, recommendations: List[USBusinessRecommendation],
                                   business_data: Dict[str, Any],
                                   analysis_results: Dict[str, Any]) -> Dict[str, Any]:
       """Calculate overall impact projections from recommendations."""
       
       current_revenue = sum(business_data.get('monthly_revenue', [0]))
       current_expenses = business_data.get('monthly_expenses', 0)
       
       projections = {
           "financial_impact": {},
           "operational_impact": {},
           "strategic_impact": {},
           "timeline_projections": {},
           "confidence_intervals": {}
       }
       
       # Calculate financial impacts
       total_revenue_impact = sum(
           rec.metrics.expected_revenue_impact or 0 for rec in recommendations
       )
       total_cost_impact = sum(
           rec.metrics.expected_cost_impact or 0 for rec in recommendations
       )
       total_implementation_cost = sum(
           rec.metrics.implementation_cost or 0 for rec in recommendations
       )
       
       projections["financial_impact"] = {
           "current_annual_revenue": current_revenue,
           "projected_revenue_increase": total_revenue_impact,
           "projected_annual_revenue": current_revenue + total_revenue_impact,
           "revenue_increase_percentage": (total_revenue_impact / current_revenue * 100) if current_revenue > 0 else 0,
           "total_implementation_investment": total_implementation_cost,
           "net_annual_benefit": total_revenue_impact + total_cost_impact,
           "overall_roi": ((total_revenue_impact + total_cost_impact - total_implementation_cost) / total_implementation_cost * 100) if total_implementation_cost > 0 else 0
       }
       
       # Operational impact metrics
       efficiency_improvements = [
           rec for rec in recommendations 
           if rec.category == RecommendationCategory.OPERATIONAL_EFFICIENCY
       ]
       
       projections["operational_impact"] = {
           "efficiency_initiatives": len(efficiency_improvements),
           "estimated_time_savings": "20-40 hours per week",
           "process_automation_score": 75,
           "quality_improvement_score": 85
       }
       
       # Strategic impact assessment
       projections["strategic_impact"] = {
           "market_position_improvement": "15-25 percentile points",
           "competitive_advantage_enhancement": "Moderate to Strong",
           "business_resilience_improvement": "Significant",
           "growth_acceleration_potential": "High"
       }
       
       return projections
   
   async def _generate_executive_summary(self, recommendations: List[USBusinessRecommendation],
                                       impact_projections: Dict[str, Any],
                                       business_data: Dict[str, Any]) -> Dict[str, Any]:
       """Generate executive summary of recommendations."""
       
       # Use Multi-Gemini engine for executive summary
       key = self.multi_gemini_engine.get_optimal_key("synthesis_reporting")
       
       summary_prompt = f"""
       EXECUTIVE SUMMARY GENERATOR:
       
       Create a compelling executive summary for US business recommendations.
       
       BUSINESS: {business_data.get('business_name', 'Business')}
       SECTOR: {business_data.get('sector', 'N/A')}
       CURRENT REVENUE: ${sum(business_data.get('monthly_revenue', [0])):,.0f} annually
       
       RECOMMENDATIONS OVERVIEW:
       - Total Recommendations: {len(recommendations)}
       - Critical Priority: {len([r for r in recommendations if r.priority == RecommendationPriority.CRITICAL])}
       - High Priority: {len([r for r in recommendations if r.priority == RecommendationPriority.HIGH])}
       - Total Investment Required: ${sum(r.metrics.implementation_cost or 0 for r in recommendations):,.0f}
       
       PROJECTED IMPACT:
       {json.dumps(impact_projections.get('financial_impact', {}), indent=2)}
       
       PROVIDE EXECUTIVE SUMMARY IN JSON:
       {{
           "headline_message": "<compelling one-line summary>",
           "business_opportunity": "<key opportunity description>",
           "investment_overview": {{
               "total_investment": <total dollars>,
               "expected_return": <annual return dollars>,
               "payback_period": "<months>",
               "overall_roi": <percentage>
           }},
           "strategic_priorities": ["<priority 1>", "<priority 2>", "<priority 3>"],
           "immediate_actions": ["<action 1>", "<action 2>", "<action 3>"],
           "success_probability": <percentage>,
           "key_benefits": ["<benefit 1>", "<benefit 2>", "<benefit 3>"],
           "implementation_timeline": "<summary timeline>",
           "next_steps": ["<step 1>", "<step 2>", "<step 3>"]
       }}
       """
       
       try:
           executive_summary = await self.multi_gemini_engine._make_gemini_request(
               key, summary_prompt, "executive_summary"
           )
           return executive_summary
       except Exception as e:
           logger.error(f"Error generating executive summary: {str(e)}")
           return self._create_fallback_executive_summary(recommendations, impact_projections)
   
   # Helper methods for roadmap creation
   
   def _categorize_timeline(self, timeline: str) -> str:
       """Categorize implementation timeline."""
       timeline_lower = timeline.lower()
       if "immediate" in timeline_lower or ("0" in timeline_lower and "day" in timeline_lower):
           return "immediate_actions"
       elif "1-3" in timeline_lower or "short" in timeline_lower:
           return "short_term_initiatives"
       elif "3-6" in timeline_lower or "medium" in timeline_lower:
           return "medium_term_projects"
       else:
           return "long_term_goals"
   
   def _identify_critical_resources(self, all_resources: List[str]) -> List[str]:
       """Identify critical resources needed across recommendations."""
       resource_counts = {}
       for resource in all_resources:
           resource_counts[resource] = resource_counts.get(resource, 0) + 1
       
       # Return resources needed by multiple recommendations
       critical = [resource for resource, count in resource_counts.items() if count >= 2]
       return critical[:5]  # Top 5 critical resources
   
   def _create_resource_timeline(self, recommendations: List[USBusinessRecommendation]) -> Dict[str, List[str]]:
       """Create timeline of when resources are needed."""
       timeline = {
           "immediate": [],
           "short_term": [],
           "medium_term": [],
           "long_term": []
       }
       
       for rec in recommendations:
           timeline_cat = self._categorize_timeline(rec.implementation_timeline)
           timeline_key = timeline_cat.replace("_actions", "").replace("_initiatives", "_term").replace("_projects", "_term").replace("_goals", "_term")
           if timeline_key in timeline:
               timeline[timeline_key].extend(rec.required_resources)
       
       # Remove duplicates
       for key in timeline:
           timeline[key] = list(set(timeline[key]))
       
       return timeline
   
   def _calculate_budget_by_category(self, recommendations: List[USBusinessRecommendation]) -> Dict[str, float]:
       """Calculate budget allocation by recommendation category."""
       budget_by_category = {}
       
       for rec in recommendations:
           category = rec.category.value
           cost = rec.metrics.implementation_cost or 0
           budget_by_category[category] = budget_by_category.get(category, 0) + cost
       
       return budget_by_category
   
   def _calculate_budget_by_timeline(self, recommendations: List[USBusinessRecommendation]) -> Dict[str, float]:
       """Calculate budget allocation by timeline."""
       budget_by_timeline = {}
       
       for rec in recommendations:
           timeline_cat = self._categorize_timeline(rec.implementation_timeline)
           cost = rec.metrics.implementation_cost or 0
           budget_by_timeline[timeline_cat] = budget_by_timeline.get(timeline_cat, 0) + cost
       
       return budget_by_timeline
   
   def _suggest_funding_sources(self, total_investment: float, business_data: Dict[str, Any]) -> List[str]:
       """Suggest funding sources for recommendations."""
       sources = []
       current_cash = business_data.get('current_cash', 0)
       
       if current_cash >= total_investment:
           sources.append("Current business cash reserves")
       else:
           sources.extend([
               "Business cash flow reinvestment",
               "Small Business Administration (SBA) loans",
               "Business line of credit",
               "Equipment financing for technology purchases"
           ])
           
           if total_investment > 100000:
               sources.extend([
                   "Traditional bank term loans",
                   "Alternative business lending",
                   "Business investor partnerships"
               ])
       
       return sources
   
   def _create_timeline_narrative(self, recommendations: List[USBusinessRecommendation]) -> str:
       """Create narrative overview of implementation timeline."""
       
       immediate_count = len([r for r in recommendations if r.urgency == RecommendationUrgency.IMMEDIATE])
       short_term_count = len([r for r in recommendations if r.urgency == RecommendationUrgency.SHORT_TERM])
       medium_term_count = len([r for r in recommendations if r.urgency == RecommendationUrgency.MEDIUM_TERM])
       long_term_count = len([r for r in recommendations if r.urgency == RecommendationUrgency.LONG_TERM])
       
       narrative = f"Implementation spans 12-18 months with {immediate_count} immediate actions, "
       narrative += f"{short_term_count} short-term initiatives (1-3 months), "
       narrative += f"{medium_term_count} medium-term projects (3-6 months), "
       narrative += f"and {long_term_count} long-term strategic goals (6+ months). "
       narrative += "Critical cash flow and operational improvements take priority, "
       narrative += "followed by growth acceleration and strategic positioning initiatives."
       
       return narrative
   
   def _calculate_overall_confidence(self, recommendations: List[USBusinessRecommendation]) -> float:
       """Calculate overall confidence in recommendations."""
       if not recommendations:
           return 0.0
       
       weighted_confidence = sum(
           rec.ai_confidence * (rec.metrics.success_probability or 0.7)
           for rec in recommendations
       )
       
       return weighted_confidence / len(recommendations)
   
   def _assess_analysis_completeness(self, analysis_results: Dict[str, Any]) -> float:
       """Assess completeness of input analysis."""
       required_components = [
           "performance_analysis", "financial_health", "risk_analysis",
           "competitive_analysis", "market_intelligence"
       ]
       
       available_components = sum(1 for comp in required_components if comp in analysis_results)
       return available_components / len(required_components)
   
   def _get_data_sources_used(self) -> List[str]:
       """Get list of data sources used in analysis."""
       return [
           "US Business Performance Analysis",
           "Multi-Gemini AI Intelligence",
           "US Economic Indicators (FRED)",
           "Market Intelligence Analysis",
           "US Sector Performance Data",
           "Financial Health Assessment",
           "Risk Analysis Framework",
           "ROI Modeling and Projections"
       ]
   
   def _update_engine_metrics(self, execution_time: float, recommendations_count: int):
       """Update recommendation engine performance metrics."""
       self.engine_metrics["total_recommendations"] += recommendations_count
       self.engine_metrics["processing_times"].append(execution_time)
       
       # Calculate average processing time
       if self.engine_metrics["processing_times"]:
           self.engine_metrics["average_processing_time"] = statistics.mean(
               self.engine_metrics["processing_times"][-100:]  # Last 100 executions
           )
   
   def _initialize_us_templates(self) -> Dict[str, Any]:
       """Initialize US-specific recommendation templates."""
       return {
           "financial_optimization": {
               "cash_flow": "Accelerate receivables collection and optimize payment terms",
               "pricing": "Implement value-based pricing strategy with competitive analysis",
               "cost_reduction": "Identify and eliminate non-value-adding expenses"
           },
           "growth_strategies": {
               "customer_acquisition": "Multi-channel customer acquisition with digital focus",
               "market_expansion": "Geographic expansion to high-opportunity US markets",
               "product_development": "Develop complementary products/services for existing customers"
           },
           "us_compliance": {
               "tax_optimization": "Strategic tax planning within US tax framework",
               "regulatory": "Industry-specific compliance audit and improvement",
               "insurance": "Comprehensive business insurance review and optimization"
           }
       }
   
   def _identify_expansion_markets(self, current_state: str, sector: str) -> List[str]:
       """Identify potential expansion markets for US businesses."""
       
       # High-growth US markets by sector
       expansion_opportunities = {
           "electronics": ["Texas", "Florida", "North Carolina", "Washington", "Colorado"],
           "food": ["Florida", "Texas", "Arizona", "Nevada", "Tennessee"],
           "retail": ["Texas", "Florida", "North Carolina", "Tennessee", "Arizona"],
           "auto": ["Texas", "Florida", "North Carolina", "Tennessee", "South Carolina"],
           "professional_services": ["Texas", "Florida", "Washington", "Colorado", "North Carolina"]
       }
       
       potential_markets = expansion_opportunities.get(sector, ["Texas", "Florida", "North Carolina"])
       
       # Remove current state from recommendations
       filtered_markets = [market for market in potential_markets if market.upper() != current_state.upper()]
       
       return filtered_markets[:3]  # Top 3 recommendations
   
   def _create_fallback_recommendations(self, business_data: Dict[str, Any], error_message: str) -> Dict[str, Any]:
    """Create fallback recommendations when generation fails."""
    
    current_revenue = sum(business_data.get('monthly_revenue', [0]))
    current_cash = business_data.get('current_cash', 0)
    monthly_expenses = business_data.get('monthly_expenses', 0)
    
    return {
        "executive_summary": {
            "headline_message": "Unable to generate comprehensive recommendations due to technical issues",
            "business_opportunity": "Recommend retrying analysis for detailed recommendations",
            "investment_overview": {
                "total_investment": 0, 
                "expected_return": 0,
                "available_capital": max(0, current_cash - (monthly_expenses * 3))
            },
            "strategic_priorities": ["Retry comprehensive analysis", "Verify data completeness", "Check system status"],
            "immediate_actions": ["Contact system support", "Verify business data completeness", "Retry with reduced scope"],
            "success_probability": 0,
            "error_context": error_message
        },
        "recommendations": [
            {
                "recommendation_id": "fallback_001",
                "category": "system",
                "priority": "high",
                "urgency": "immediate",
                "title": "System Analysis Recovery",
                "description": "The comprehensive recommendation system encountered technical difficulties. Immediate action needed to restore full analysis capability.",
                "rationale": f"System error: {error_message[:200]}...",
                "specific_actions": [
                    "Verify all business data inputs are complete and accurate",
                    "Check API connectivity and system status",
                    "Retry analysis with focused scope if needed",
                    "Contact technical support if issues persist"
                ],
                "expected_outcomes": [
                    "Restored access to full recommendation engine",
                    "Complete business analysis and insights",
                    "Strategic recommendations for growth and optimization"
                ],
                "success_metrics": [
                    "Successful analysis completion",
                    "All recommendation categories generated",
                    "Confidence scores above 80%"
                ],
                "metrics": {
                    "expected_roi": 0,
                    "expected_revenue_impact": 0,
                    "expected_cost_impact": 0,
                    "implementation_cost": 0,
                    "payback_period_months": None,
                    "success_probability": 0.9,
                    "risk_level": "low",
                    "effort_level": "low",
                    "confidence_score": 0.3
                },
                "implementation_timeline": "immediate",
                "implementation_steps": [
                    {"step": 1, "action": "Verify data inputs", "days": 0},
                    {"step": 2, "action": "Check system status", "days": 0},
                    {"step": 3, "action": "Retry analysis", "days": 0}
                ],
                "required_resources": ["System access", "Technical support"],
                "prerequisites": ["Valid business data"],
                "economic_context": get_current_us_economic_indicators(),
                "regulatory_considerations": ["Data accuracy requirements"],
                "tax_implications": {},
                "compliance_requirements": ["System reliability standards"],
                "dependent_recommendations": [],
                "conflicting_recommendations": [],
                "synergistic_recommendations": [],
                "key_performance_indicators": ["System uptime", "Analysis success rate"],
                "milestone_checkpoints": [
                    {"milestone": "System restored", "target_date": "Immediate"}
                ],
                "review_schedule": "immediate",
                "ai_confidence": 0.3,
                "data_sources": ["System logs", "Error reports"],
                "analysis_methodology": "Error analysis and recovery",
                "generated_at": datetime.now()
            }
        ],
        "implementation_roadmap": {
            "immediate_actions": [
                {
                    "title": "System Recovery",
                    "timeline": "immediate",
                    "priority": "critical",
                    "actions": ["Verify inputs", "Retry analysis", "Contact support"]
                }
            ],
            "short_term_initiatives": [],
            "medium_term_projects": [],
            "long_term_goals": [],
            "resource_requirements": {
                "total_resources": ["Technical support", "System access"],
                "critical_resources": ["Technical support"],
                "resource_timeline": {"immediate": ["Technical support"]}
            },
            "budget_allocation": {
                "total_investment_required": 0,
                "by_category": {},
                "by_timeline": {},
                "funding_sources": []
            },
            "timeline_overview": "Immediate system recovery required before proceeding with business recommendations"
        },
        "success_framework": {
            "overall_success_metrics": ["Analysis completion", "System reliability"],
            "recommendation_tracking": {},
            "performance_dashboard": {
                "executive_summary": ["System status", "Analysis success rate"],
                "financial_metrics": [],
                "operational_metrics": ["System uptime", "Error rate"]
            }
        },
        "impact_projections": {
            "financial_impact": {
                "current_annual_revenue": current_revenue,
                "projected_revenue_increase": 0,
                "projected_annual_revenue": current_revenue,
                "revenue_increase_percentage": 0,
                "total_implementation_investment": 0,
                "net_annual_benefit": 0,
                "overall_roi": 0
            },
            "operational_impact": {
                "efficiency_initiatives": 0,
                "estimated_time_savings": "0 hours pending system recovery",
                "process_automation_score": 0,
                "quality_improvement_score": 0
            },
            "strategic_impact": {
                "market_position_improvement": "Pending analysis completion",
                "competitive_advantage_enhancement": "Unable to assess",
                "business_resilience_improvement": "Unable to assess",
                "growth_acceleration_potential": "Unable to assess"
            }
        },
        "economic_context": {
            "current_indicators": get_current_us_economic_indicators(),
            "business_impact": {"error": "Unable to calculate due to system error"},
            "market_sentiment": {"sentiment": "unknown", "error": "System unavailable"}
        },
        "recommendation_metadata": {
            "total_recommendations_generated": 1,
            "final_recommendations_selected": 1,
            "focus_areas": ["system_recovery"],
            "generation_time_seconds": 0,
            "confidence_level": 0.3,
            "analysis_completeness": 0.1,
            "data_sources": ["Error logs", "System diagnostics"],
            "error_details": {
                "error_message": error_message,
                "error_type": "system_failure",
                "recovery_recommendations": [
                    "Verify all API keys are valid and active",
                    "Check network connectivity",
                    "Ensure business data is complete and properly formatted",
                    "Try analysis with reduced scope",
                    "Contact technical support if issues persist"
                ],
                "system_diagnostics": {
                    "gemini_keys_available": len(GEMINI_KEYS) if GEMINI_KEYS else 0,
                    "openrouter_fallback": len(OPENROUTER_KEYS) > 0 if OPENROUTER_KEYS else False,
                    "data_pipeline_status": "unknown"
                }
            }
        }
    }

def _identify_expansion_markets(self, current_state: str, sector: str) -> List[str]:
    """Identify potential expansion markets for US businesses."""
    
    # High-growth US markets by sector
    expansion_opportunities = {
        "electronics": ["Texas", "Florida", "North Carolina", "Washington", "Colorado"],
        "food": ["Florida", "Texas", "Arizona", "Nevada", "Tennessee"],
        "retail": ["Texas", "Florida", "North Carolina", "Tennessee", "Arizona"],
        "auto": ["Texas", "Florida", "North Carolina", "Tennessee", "South Carolina"],
        "professional_services": ["Texas", "Florida", "Washington", "Colorado", "North Carolina"],
        "manufacturing": ["Texas", "North Carolina", "Tennessee", "Indiana", "Ohio"]
    }
    
    potential_markets = expansion_opportunities.get(sector, ["Texas", "Florida", "North Carolina"])
    
    # Remove current state from recommendations
    filtered_markets = [market for market in potential_markets if market.upper() != current_state.upper()]
    
    return filtered_markets[:3]  # Top 3 recommendations

def get_engine_performance_metrics(self) -> Dict[str, Any]:
    """Get recommendation engine performance metrics."""
    
    return {
        "engine_status": "operational",
        "total_analyses_completed": self.engine_metrics["total_recommendations"],
        "success_rate": (self.engine_metrics["successful_implementations"] / 
                        max(1, self.engine_metrics["total_recommendations"])),
        "average_roi_achieved": self.engine_metrics["average_roi_achieved"],
        "recommendation_accuracy": self.engine_metrics["recommendation_accuracy"],
        "average_processing_time": statistics.mean(self.engine_metrics["processing_times"][-10:]) if self.engine_metrics["processing_times"] else 0,
        "gemini_utilization": {
            "total_requests": sum(self.multi_gemini_engine.analysis_metrics["gemini_usage"].values()),
            "key_distribution": self.multi_gemini_engine.analysis_metrics["gemini_usage"],
            "fallback_usage": self.multi_gemini_engine.analysis_metrics["openrouter_fallbacks"]
        },
        "sector_patterns": self.sector_patterns,
        "success_patterns": self.success_patterns,
        "last_updated": datetime.now().isoformat()
    }

def reset_engine_metrics(self) -> None:
    """Reset performance metrics (for maintenance/testing)."""
    
    self.engine_metrics = {
        "total_recommendations": 0,
        "successful_implementations": 0,
        "average_roi_achieved": 0.0,
        "recommendation_accuracy": 0.0,
        "processing_times": []
    }
    
    self.recommendation_history = {}
    self.success_patterns = {}
    self.sector_patterns = {}
    
    logger.info("Recommendation engine metrics reset")

def update_recommendation_outcome(self, recommendation_id: str, 
                                actual_outcome: Dict[str, Any]) -> Dict[str, Any]:
    """Update recommendation with actual implementation results."""
    
    if recommendation_id not in self.recommendation_history:
        return {"error": f"Recommendation {recommendation_id} not found"}
    
    # Update history with actual results
    self.recommendation_history[recommendation_id]["actual_outcome"] = actual_outcome
    self.recommendation_history[recommendation_id]["implementation_date"] = datetime.now()
    
    # Calculate accuracy
    expected_roi = self.recommendation_history[recommendation_id].get("expected_roi", 0)
    actual_roi = actual_outcome.get("actual_roi", 0)
    
    if expected_roi > 0:
        accuracy = min(1.0, actual_roi / expected_roi)
        self.recommendation_history[recommendation_id]["accuracy"] = accuracy
        
        # Update overall metrics
        self.engine_metrics["successful_implementations"] += 1
        
        # Update rolling accuracy
        recent_accuracies = [
            rec.get("accuracy", 0) for rec in self.recommendation_history.values() 
            if rec.get("accuracy") is not None
        ][-10:]  # Last 10 implementations
        
        if recent_accuracies:
            self.engine_metrics["recommendation_accuracy"] = sum(recent_accuracies) / len(recent_accuracies)
        
        # Update success patterns
        category = self.recommendation_history[recommendation_id].get("category", "unknown")
        if category not in self.success_patterns:
            self.success_patterns[category] = []
        self.success_patterns[category].append(accuracy)
    
    logger.info(f"Updated recommendation {recommendation_id} with actual outcomes")
    
    return {
        "status": "updated",
        "recommendation_id": recommendation_id,
        "accuracy": self.recommendation_history[recommendation_id].get("accuracy", 0),
        "implementation_success": actual_outcome.get("success", False)
    }

async def generate_sector_benchmark_report(self, sector: str) -> Dict[str, Any]:
    """Generate sector benchmark report for US businesses."""
    
    try:
        # Get US sector data
        sector_data = get_us_sector_data(sector)
        if not sector_data:
            return {"error": f"No data available for sector: {sector}"}
        
        # Get economic context
        economic_data = get_current_us_economic_indicators()
        
        # Calculate sector performance metrics
        sector_resilience = calculate_sector_resilience_score(sector)
        
        # Generate AI analysis of sector
        key = self.multi_gemini_engine.get_optimal_key("market_intelligence")
        
        prompt = f"""
        EXPERT US SECTOR ANALYST:
        
        Create comprehensive sector benchmark report for US {sector} businesses.
        
        SECTOR DATA:
        {json.dumps(sector_data, indent=2)}
        
        CURRENT US ECONOMIC CONTEXT:
        - Fed Funds Rate: {economic_data.get('fed_funds_rate', 5.0)}%
        - GDP Growth: {economic_data.get('gdp_growth', 2.4)}%
        - Inflation: {economic_data.get('inflation_rate', 3.2)}%
        - Small Business Optimism: {economic_data.get('small_business_optimism', 89)}
        
        SECTOR RESILIENCE:
        {json.dumps(sector_resilience, indent=2)}
        
        PROVIDE SECTOR BENCHMARK REPORT IN JSON:
        {{
            "sector_overview": {{
                "sector_name": "{sector}",
                "market_size": <estimated US market size>,
                "growth_rate": <sector growth rate>,
                "maturity_stage": "<emerging/growth/mature/declining>",
                "competitiveness": "<low/medium/high/very_high>",
                "consolidation_trend": "<fragmenting/stable/consolidating>"
            }},
            "performance_benchmarks": {{
                "average_annual_revenue": <sector average>,
                "top_quartile_revenue": <top 25% performance>,
                "median_profit_margin": <typical margin>,
                "average_employees": <typical staff size>,
                "revenue_per_employee": <productivity metric>,
                "customer_acquisition_cost": <typical CAC>,
                "customer_lifetime_value": <typical CLV>
            }},
            "financial_benchmarks": {{
                "cash_flow_cycles": <average days>,
                "inventory_turnover": <if applicable>,
                "receivables_days": <average collection>,
                "working_capital_ratio": <typical ratio>,
                "debt_to_equity": <sector average>,
                "return_on_assets": <ROA benchmark>
            }},
            "operational_benchmarks": {{
                "capacity_utilization": <percentage>,
                "quality_metrics": <sector quality standards>,
                "delivery_performance": <timing standards>,
                "customer_satisfaction": <satisfaction benchmarks>,
                "employee_productivity": <productivity measures>,
                "technology_adoption": <digitalization level>
            }},
            "market_dynamics": {{
                "demand_drivers": ["<driver 1>", "<driver 2>", "<driver 3>"],
                "supply_constraints": ["<constraint 1>", "<constraint 2>"],
                "pricing_trends": "<increasing/stable/declining>",
                "innovation_pace": "<rapid/moderate/slow>",
                "regulatory_environment": "<supportive/neutral/restrictive>",
                "entry_barriers": "<low/medium/high>"
            }},
            "economic_sensitivity": {{
                "recession_impact": "<severe/moderate/minimal>",
                "interest_rate_sensitivity": <-5 to 5 scale>,
                "inflation_impact": "<severe/moderate/minimal>",
                "employment_correlation": <correlation coefficient>,
                "seasonal_variation": <percentage variation>,
                "economic_leading_indicators": ["<indicator 1>", "<indicator 2>"]
            }},
            "competitive_landscape": {{
                "market_concentration": "<fragmented/moderately_concentrated/highly_concentrated>",
                "dominant_players_share": <percentage>,
                "small_business_share": <percentage>,
                "competitive_factors": ["<factor 1>", "<factor 2>", "<factor 3>"],
                "differentiation_opportunities": ["<opportunity 1>", "<opportunity 2>"],
                "price_competition_intensity": "<low/medium/high>"
            }},
            "success_factors": {{
                "critical_success_factors": ["<factor 1>", "<factor 2>", "<factor 3>"],
                "competitive_advantages": ["<advantage 1>", "<advantage 2>"],
                "common_failure_points": ["<failure 1>", "<failure 2>"],
                "best_practices": ["<practice 1>", "<practice 2>", "<practice 3>"]
            }},
            "growth_opportunities": {{
                "emerging_segments": ["<segment 1>", "<segment 2>"],
                "technology_opportunities": ["<tech 1>", "<tech 2>"],
                "geographic_expansion": ["<region 1>", "<region 2>"],
                "partnership_opportunities": ["<partnership 1>", "<partnership 2>"],
                "market_gaps": ["<gap 1>", "<gap 2>"]
            }},
            "risk_factors": {{
                "industry_risks": ["<risk 1>", "<risk 2>", "<risk 3>"],
                "technology_disruption": <0-100 risk score>,
                "regulatory_risks": ["<risk 1>", "<risk 2>"],
                "supply_chain_risks": ["<risk 1>", "<risk 2>"],
                "competitive_threats": ["<threat 1>", "<threat 2>"]
            }},
            "outlook_forecast": {{
                "12_month_outlook": "<positive/neutral/negative>",
                "key_trends": ["<trend 1>", "<trend 2>", "<trend 3>"],
                "growth_projections": <projected growth rate>,
                "major_changes_expected": ["<change 1>", "<change 2>"],
                "investment_climate": "<favorable/neutral/challenging>"
            }},
            "recommendations_for_sector": {{
                "strategic_priorities": ["<priority 1>", "<priority 2>", "<priority 3>"],
                "operational_focus": ["<focus 1>", "<focus 2>"],
                "investment_areas": ["<area 1>", "<area 2>"],
                "risk_mitigation": ["<mitigation 1>", "<mitigation 2>"],
                "timing_considerations": ["<consideration 1>", "<consideration 2>"]
            }},
            "confidence_level": <80-95>
        }}
        
        Focus on US market-specific insights and quantitative benchmarks.
        """
        
        sector_analysis = await self.multi_gemini_engine._make_gemini_request(
            key, prompt, "sector_analysis"
        )
        
        # Add metadata
        sector_analysis["report_metadata"] = {
            "report_date": datetime.now().isoformat(),
            "data_sources": [
                "US Sector Performance Database",
                "Federal Economic Data",
                "Industry Association Reports", 
                "Small Business Administration Data"
            ],
            "methodology": "Comprehensive sector analysis with AI insights",
            "update_frequency": "quarterly",
            "next_update": (datetime.now() + timedelta(days=90)).isoformat()
        }
        
        return sector_analysis
        
    except Exception as e:
        logger.error(f"Error generating sector benchmark report: {str(e)}")
        return {
            "error": str(e),
            "sector": sector,
            "fallback_data": sector_data,
            "report_date": datetime.now().isoformat()
        }

# Export the main class
__all__ = ["USRecommendationEngine"]