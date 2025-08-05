"""Pydantic schemas for US business analysis results."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class USInsightBase(BaseModel):
    """Base insight schema for US businesses."""
    
    insight_type: str = Field(..., description="Type of insight")
    category: str = Field(..., description="business_performance/market_analysis/financial_health/growth_strategy")
    priority: str = Field(..., description="critical/high/medium/low")
    urgency: str = Field(..., description="immediate/short_term/medium_term/long_term")
    title: str = Field(..., description="Insight title")
    message: str = Field(..., description="Detailed insight message")
    
    # US-specific impact metrics
    potential_impact_amount: Optional[float] = Field(None, description="Expected impact in USD")
    impact_timeframe: Optional[str] = Field(None, description="Timeframe for impact realization")
    confidence_score: float = Field(default=0.8, ge=0, le=1, description="AI confidence level")
    
    # US economic context
    economic_factors: Optional[List[str]] = Field(default=[], description="Relevant US economic factors")
    market_context: Optional[Dict[str, Any]] = Field(default={}, description="US market conditions context")


class USInsightResponse(USInsightBase):
    """Schema for US business insight response."""
    
    id: int
    analysis_id: int
    supporting_evidence: Optional[Dict[str, Any]] = None
    data_quality: str = Field(default="good", description="excellent/good/fair/poor")
    created_at: datetime
    
    class Config:
        from_attributes = True


class USRecommendationBase(BaseModel):
    """Base recommendation schema for US businesses."""
    
    category: str = Field(..., description="immediate/strategic/investment/operational/compliance")
    action_type: str = Field(..., description="pricing/marketing/financing/expansion/cost_reduction")
    priority: str = Field(..., description="critical/high/medium/low")
    
    title: str = Field(..., description="Recommendation title")
    description: str = Field(..., description="Detailed description")
    specific_action: str = Field(..., description="Specific action to take")
    rationale: str = Field(..., description="Why this recommendation is important")
    
    # US business outcomes
    expected_outcome: str = Field(..., description="Expected measurable outcome")
    expected_revenue_impact: Optional[float] = Field(None, description="Expected revenue change (USD)")
    expected_cost_impact: Optional[float] = Field(None, description="Expected cost change (USD)")
    expected_roi: Optional[float] = Field(None, description="Expected ROI percentage")
    timeframe: str = Field(..., description="Implementation timeframe")
    
    # US implementation details
    investment_required: Optional[float] = Field(None, description="Required investment (USD)")
    difficulty_level: str = Field(..., description="easy/medium/hard/very_hard")
    implementation_steps: Optional[List[str]] = Field(default=[], description="Step-by-step implementation")
    required_resources: Optional[List[str]] = Field(default=[], description="Required resources")
    success_metrics: Optional[List[str]] = Field(default=[], description="Success measurement metrics")
    
    # US regulatory and compliance
    regulatory_considerations: Optional[List[str]] = Field(default=[], description="US regulatory factors")
    tax_implications: Optional[Dict[str, Any]] = Field(default={}, description="US tax considerations")
    compliance_requirements: Optional[List[str]] = Field(default=[], description="Compliance needs")


class USRecommendationResponse(USRecommendationBase):
    """Schema for US business recommendation response."""
    
    id: int
    analysis_id: int
    
    # Implementation tracking
    is_implemented: bool = False
    implementation_date: Optional[datetime] = None
    implementation_notes: Optional[str] = None
    actual_outcome: Optional[str] = None
    actual_roi: Optional[float] = None
    
    # Performance tracking
    success_probability: float = Field(default=0.7, description="Probability of success")
    effectiveness_score: Optional[float] = Field(None, description="Post-implementation effectiveness")
    lessons_learned: Optional[str] = None
    
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class USPerformanceMetrics(BaseModel):
    """Schema for US business performance metrics."""
    
    # Overall performance
    performance_score: float = Field(..., ge=0, le=100, description="Overall performance score")
    business_health_grade: str = Field(..., description="A/B/C/D/F grade")
    
    # Financial performance vs US benchmarks
    revenue_growth_rate: float = Field(..., description="Annualized revenue growth rate")
    sector_growth_rate: float = Field(..., description="US sector average growth rate")
    performance_ratio: float = Field(..., description="Business vs US sector performance")
    
    # US-specific financial metrics
    revenue_trend: str = Field(..., description="increasing/declining/stable")
    profit_margin: float = Field(..., description="Current profit margin")
    cash_flow_status: str = Field(..., description="healthy/tight/critical")
    cash_runway_months: Optional[float] = Field(None, description="Months of cash remaining")
    
    # US market position
    market_position: str = Field(..., description="leader/strong/average/weak")
    market_percentile: Optional[float] = Field(None, ge=0, le=100, description="Percentile ranking")
    competitive_position: str = Field(..., description="dominant/competitive/struggling")
    
    # US economic sensitivity
    fed_rate_sensitivity: float = Field(..., description="Federal funds rate sensitivity")
    inflation_sensitivity: float = Field(..., description="Inflation sensitivity")
    economic_resilience_score: float = Field(..., ge=0, le=100, description="Recession resistance")
    
    # Risk metrics
    overall_risk_level: str = Field(..., description="low/medium/high/critical")
    financial_risk: float = Field(..., ge=0, le=100, description="Financial risk score")
    market_risk: float = Field(..., ge=0, le=100, description="Market risk score")
    operational_risk: float = Field(..., ge=0, le=100, description="Operational risk score")
    volatility_score: float = Field(..., ge=0, le=100, description="Revenue volatility measure")


class USMarketComparison(BaseModel):
    """Schema for US market comparison data."""
    
    # Business vs US market
    your_revenue: float = Field(..., description="Business current annual revenue")
    us_market_average: float = Field(..., description="US market average revenue")
    sector_top_performers: float = Field(..., description="Top 10% performers average")
    your_rank_percentile: float = Field(..., ge=0, le=100, description="US percentile ranking")
    
    # US sector analysis
    sector_growth: float = Field(..., description="US sector growth rate")
    sector_health_score: float = Field(..., ge=0, le=100, description="Sector health in US")
    location_factor: float = Field(..., description="Location advantage/disadvantage factor")
    
    # US competitive landscape
    competition_intensity: float = Field(..., ge=1, le=10, description="US market competition level")
    market_saturation: float = Field(..., ge=0, le=100, description="Market saturation percentage")
    barriers_to_entry: str = Field(..., description="high/medium/low")
    
    # US economic context
    economic_tailwinds: List[str] = Field(default=[], description="US economic factors helping business")
    economic_headwinds: List[str] = Field(default=[], description="US economic factors hindering business")


class USInvestmentAdvice(BaseModel):
    """Schema for US investment recommendations."""
    
    # Investment capacity analysis
    available_capital: float = Field(..., description="Available investment capital (USD)")
    recommended_cash_reserve: float = Field(..., description="Recommended emergency fund (USD)")
    investment_capacity: float = Field(..., description="Available for investment (USD)")
    risk_profile: str = Field(..., description="conservative/moderate/aggressive")
    
    # US investment allocation
    recommended_allocation: Dict[str, float] = Field(..., description="Investment allocation percentages")
    business_reinvestment: float = Field(..., description="Recommended business reinvestment (USD)")
    market_investments: float = Field(..., description="Recommended market investments (USD)")
    
    # Specific US investment opportunities
    recommended_investments: List[Dict[str, Any]] = Field(..., description="Specific investment options")
    investment_reasoning: str = Field(..., description="Investment rationale")
    expected_annual_return: float = Field(..., description="Expected annual return rate")
    
    # US-specific considerations
    tax_optimization_strategies: List[Dict[str, Any]] = Field(default=[], description="US tax strategies")
    retirement_planning: Optional[Dict[str, Any]] = Field(None, description="401k/IRA recommendations")
    diversification_advice: str = Field(..., description="Portfolio diversification guidance")
    
    # Risk management
    risk_tolerance_assessment: str = Field(..., description="Risk tolerance evaluation")
    hedging_strategies: List[str] = Field(default=[], description="Risk hedging approaches")


class USActionPlan(BaseModel):
    """Schema for US business action plan."""
    
    # Immediate actions (next 30 days)
    immediate_actions: List[Dict[str, Any]] = Field(..., description="Critical actions for next 30 days")
    
    # Short-term actions (1-3 months)
    short_term_actions: List[Dict[str, Any]] = Field(..., description="Actions for next 1-3 months")
    
    # Strategic actions (3-12 months)
    strategic_actions: List[Dict[str, Any]] = Field(..., description="Strategic actions for 3-12 months")
    
    # US business metrics to track
    key_metrics_to_track: List[Dict[str, str]] = Field(..., description="Critical KPIs to monitor")
    success_milestones: List[Dict[str, Any]] = Field(..., description="Success milestones and dates")
    
    # US economic monitoring
    economic_indicators_to_watch: List[str] = Field(default=[], description="US economic indicators to monitor")
    market_trends_to_track: List[str] = Field(default=[], description="Market trends to follow")
    
    # Resource allocation
    budget_allocation: Dict[str, float] = Field(..., description="Budget allocation by category")
    timeline_overview: str = Field(..., description="Overall timeline and sequencing")


class USCompleteAnalysisResponse(BaseModel):
    """Schema for complete US business analysis response."""
    
    # Business identification
    business_id: Optional[int] = None
    analysis_id: int
    analysis_date: datetime
    
    # Core US analysis results
    performance_metrics: USPerformanceMetrics
    main_insight: USInsightResponse
    market_comparison: USMarketComparison
    
    # US-specific recommendations
    recommendations: List[USRecommendationResponse]
    investment_advice: USInvestmentAdvice
    action_plan: USActionPlan
    
    # US market and economic context
    economic_context: Dict[str, Any] = Field(..., description="US economic conditions context")
    market_context: Dict[str, Any] = Field(..., description="US market conditions context")
    
    # Supporting US data for visualizations
    chart_data: Dict[str, Any] = Field(..., description="US market chart and visualization data")
    benchmark_data: Dict[str, Any] = Field(..., description="US industry benchmark data")
    
    # US regulatory and compliance insights
    regulatory_landscape: Optional[Dict[str, Any]] = Field(None, description="US regulatory environment")
    compliance_checklist: Optional[List[str]] = Field(None, description="US compliance requirements")
    
    # Analysis metadata
    confidence_level: float = Field(..., ge=0, le=1, description="Overall analysis confidence")
    data_sources: List[str] = Field(..., description="US data sources used")
    analysis_methodology: str = Field(..., description="Analysis approach used")
    
    # Next steps for US business
    next_review_date: datetime = Field(..., description="Recommended next analysis date")
    monitoring_schedule: Dict[str, str] = Field(..., description="Ongoing monitoring recommendations")
    
    class Config:
        from_attributes = True


class USQuickAnalysisResponse(BaseModel):
    """Schema for quick US business analysis response."""
    
    # Quick performance summary
    performance_score: float = Field(..., ge=0, le=100, description="Overall performance score")
    business_health_grade: str = Field(..., description="A/B/C/D/F grade")
    
    # Key insights
    main_message: str = Field(..., description="Primary insight message")
    key_recommendations: List[str] = Field(..., description="Top 3-5 recommendations")
    
    # US investment capacity
    investment_capacity: float = Field(..., description="Available investment capacity (USD)")
    recommended_investments: List[str] = Field(..., description="Quick investment suggestions")
    
    # Next actions
    next_actions: List[str] = Field(..., description="Immediate next actions")
    priority_focus: str = Field(..., description="Primary area to focus on")
    
    # US market position
    market_position: str = Field(..., description="Quick market position assessment")
    competitive_status: str = Field(..., description="Competitive position summary")
    
    # Economic impact
    economic_impact: str = Field(..., description="Current US economic impact on business")
    timing_assessment: str = Field(..., description="Market timing evaluation")
    
    class Config:
        from_attributes = True


class USAnalysisStatus(BaseModel):
    """Schema for US business analysis processing status."""
    
    status: str = Field(..., description="processing/completed/failed")
    progress_percentage: int = Field(..., ge=0, le=100, description="Analysis progress")
    current_step: str = Field(..., description="Current processing step")
    
    # US-specific processing steps
    data_sources_processed: List[str] = Field(default=[], description="US data sources processed")
    economic_data_status: str = Field(default="pending", description="US economic data processing")
    market_data_status: str = Field(default="pending", description="US market data processing")
    
    estimated_completion: Optional[datetime] = None
    error_message: Optional[str] = None
    
    # Performance metrics
    processing_time_seconds: Optional[float] = None
    data_quality_score: Optional[float] = Field(None, ge=0, le=1, description="Input data quality")


class USAnalysisHistoryResponse(BaseModel):
    """Schema for US business analysis history."""
    
    analysis_id: int
    business_name: str
    analysis_date: datetime
    
    # Performance tracking over time
    performance_score: float
    performance_trend: str = Field(..., description="improving/stable/declining")
    
    # Key changes
    main_insight_summary: str
    recommendations_count: int
    implemented_recommendations: int
    
    # US economic context at time of analysis
    economic_conditions_summary: str
    fed_rate_at_analysis: Optional[float] = None
    inflation_rate_at_analysis: Optional[float] = None
    
    # Implementation status
    implementation_status: str = Field(..., description="excellent/good/fair/poor")
    roi_achieved: Optional[float] = None
    
    class Config:
        from_attributes = True


class USInvestmentRecommendationResponse(BaseModel):
    """Schema for US investment recommendation response."""
    
    id: int
    analysis_id: int
    
    # Investment details
    investment_type: str = Field(..., description="business_reinvestment/market_investment/real_estate")
    investment_category: str = Field(..., description="growth/income/diversification/tax_optimization")
    risk_level: str = Field(..., description="conservative/moderate/aggressive")
    
    title: str
    description: str
    rationale: str
    
    # US investment specifics
    recommended_amount: float = Field(..., description="Recommended investment amount (USD)")
    minimum_amount: Optional[float] = Field(None, description="Minimum viable amount (USD)")
    expected_annual_return: float = Field(..., description="Expected annual return percentage")
    time_horizon: str = Field(..., description="short_term/medium_term/long_term")
    
    # US tax and regulatory
    tax_advantages: Optional[Dict[str, Any]] = Field(None, description="US tax benefits")
    regulatory_protection: Optional[Dict[str, Any]] = Field(None, description="US regulatory protections")
    liquidity_considerations: Optional[str] = Field(None, description="Liquidity factors")
    
    # Implementation
    implementation_steps: Optional[List[str]] = Field(None, description="Implementation guidance")
    recommended_timing: Optional[str] = Field(None, description="Optimal timing")
    exit_strategy: Optional[str] = Field(None, description="Exit considerations")
    
    # Performance tracking
    is_implemented: bool = False
    implementation_date: Optional[datetime] = None
    actual_return: Optional[float] = None
    
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True