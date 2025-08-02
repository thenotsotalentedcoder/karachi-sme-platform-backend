"""Pydantic schemas for analysis results."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class InsightBase(BaseModel):
    """Base insight schema."""
    
    insight_type: str = Field(..., description="Type of insight")
    priority: str = Field(..., description="Priority level")
    title: str = Field(..., description="Insight title")
    message: str = Field(..., description="Insight message")
    impact_amount: Optional[float] = Field(None, description="Expected impact in PKR")
    timeframe: Optional[str] = Field(None, description="Timeframe for impact")
    confidence_score: float = Field(default=0.8, ge=0, le=1, description="Confidence level")


class InsightResponse(InsightBase):
    """Schema for insight response."""
    
    id: int
    supporting_data: Optional[Dict[str, Any]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class RecommendationBase(BaseModel):
    """Base recommendation schema."""
    
    category: str = Field(..., description="Recommendation category")
    action_type: str = Field(..., description="Type of action")
    title: str = Field(..., description="Recommendation title")
    description: str = Field(..., description="Detailed description")
    specific_action: str = Field(..., description="Specific action to take")
    expected_outcome: str = Field(..., description="Expected outcome")
    expected_amount: Optional[float] = Field(None, description="Expected benefit in PKR")
    timeframe: str = Field(..., description="Implementation timeframe")
    investment_required: Optional[float] = Field(None, description="Required investment in PKR")
    difficulty_level: str = Field(..., description="Implementation difficulty")


class RecommendationResponse(RecommendationBase):
    """Schema for recommendation response."""
    
    id: int
    implementation_steps: Optional[List[str]] = None
    is_implemented: bool = False
    implementation_date: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class PerformanceMetrics(BaseModel):
    """Schema for business performance metrics."""
    
    performance_score: float = Field(..., ge=0, le=100, description="Overall performance score")
    business_growth_rate: float = Field(..., description="Monthly business growth rate")
    sector_growth_rate: float = Field(..., description="Sector average growth rate")
    performance_ratio: float = Field(..., description="Business vs sector performance ratio")
    revenue_trend: str = Field(..., description="Revenue trend direction")
    profit_margin: float = Field(..., description="Current profit margin")
    cash_flow_status: str = Field(..., description="Cash flow health status")
    market_position: str = Field(..., description="Market position")
    competition_level: str = Field(..., description="Competition level")
    business_risk_level: str = Field(..., description="Business risk assessment")
    volatility_score: float = Field(..., ge=0, le=1, description="Business volatility score")


class MarketComparison(BaseModel):
    """Schema for market comparison data."""
    
    your_revenue: float = Field(..., description="Business current revenue")
    market_average: float = Field(..., description="Market average revenue")
    top_performers: float = Field(..., description="Top 10% performers average")
    your_rank_percentile: float = Field(..., ge=0, le=100, description="Percentile ranking")
    sector_growth: float = Field(..., description="Sector growth rate")
    location_factor: float = Field(..., description="Location advantage/disadvantage")


class InvestmentAdvice(BaseModel):
    """Schema for investment recommendations."""
    
    available_capital: float = Field(..., description="Available investment capital")
    risk_profile: str = Field(..., description="Business risk profile")
    recommended_investments: List[Dict[str, Any]] = Field(..., description="Investment options")
    investment_reasoning: str = Field(..., description="Investment rationale")
    expected_annual_return: float = Field(..., description="Expected annual return rate")
    diversification_advice: str = Field(..., description="Diversification recommendations")


class ActionPlan(BaseModel):
    """Schema for actionable business plan."""
    
    immediate_actions: List[Dict[str, Any]] = Field(..., description="Actions for this week")
    short_term_actions: List[Dict[str, Any]] = Field(..., description="Actions for this month")
    strategic_actions: List[Dict[str, Any]] = Field(..., description="Actions for next 3-6 months")
    key_metrics_to_track: List[Dict[str, str]] = Field(..., description="Metrics to monitor")
    success_milestones: List[Dict[str, Any]] = Field(..., description="Success milestones")


class CompleteAnalysisResponse(BaseModel):
    """Schema for complete business analysis response."""
    
    # Business identification
    business_id: Optional[int] = None
    analysis_id: int
    
    # Core analysis
    performance_metrics: PerformanceMetrics
    main_insight: InsightResponse
    market_comparison: MarketComparison
    
    # Recommendations
    recommendations: List[RecommendationResponse]
    investment_advice: InvestmentAdvice
    action_plan: ActionPlan
    
    # Supporting data
    chart_data: Dict[str, Any] = Field(..., description="Data for charts and visualizations")
    market_context: Dict[str, Any] = Field(..., description="Market context information")
    
    # Metadata
    analysis_date: datetime
    confidence_level: float = Field(..., ge=0, le=1, description="Overall analysis confidence")
    
    class Config:
        from_attributes = True


class QuickAnalysisResponse(BaseModel):
    """Schema for quick analysis response without full details."""
    
    performance_score: float
    main_message: str
    key_recommendations: List[str]
    investment_capacity: float
    next_actions: List[str]
    market_position: str
    
    class Config:
        from_attributes = True


class AnalysisStatus(BaseModel):
    """Schema for analysis processing status."""
    
    status: str = Field(..., description="Processing status")
    progress_percentage: int = Field(..., ge=0, le=100, description="Progress percentage")
    current_step: str = Field(..., description="Current processing step")
    estimated_completion: Optional[datetime] = None
    error_message: Optional[str] = None


class AnalysisHistoryResponse(BaseModel):
    """Schema for analysis history."""
    
    analysis_id: int
    business_name: str
    analysis_date: datetime
    performance_score: float
    main_insight_summary: str
    recommendations_count: int
    implementation_status: str
    
    class Config:
        from_attributes = True