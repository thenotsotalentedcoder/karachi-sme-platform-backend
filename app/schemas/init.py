"""Pydantic schemas package."""

from app.schemas.business import (
    BusinessBase,
    BusinessCreate,
    BusinessResponse,
    BusinessUpdate,
    BusinessSummary,
    BusinessAnalysisRequest,
    QuickBusinessInput,
)

from app.schemas.analysis import (
    InsightBase,
    InsightResponse,
    RecommendationBase,
    RecommendationResponse,
    PerformanceMetrics,
    MarketComparison,
    InvestmentAdvice,
    ActionPlan,
    CompleteAnalysisResponse,
    QuickAnalysisResponse,
    AnalysisStatus,
    AnalysisHistoryResponse,
)

from app.schemas.market import (
    MarketDataBase,
    KarachiMarketDataResponse,
    SectorPerformanceResponse,
    EconomicIndicatorsResponse,
    MarketTrendAnalysis,
    LocationAnalysis,
    SectorBenchmarks,
    MarketForecast,
    CompetitiveAnalysis,
    MarketInsightsResponse,
)

# Export all schemas
__all__ = [
    # Business schemas
    "BusinessBase",
    "BusinessCreate",
    "BusinessResponse", 
    "BusinessUpdate",
    "BusinessSummary",
    "BusinessAnalysisRequest",
    "QuickBusinessInput",
    
    # Analysis schemas
    "InsightBase",
    "InsightResponse",
    "RecommendationBase", 
    "RecommendationResponse",
    "PerformanceMetrics",
    "MarketComparison",
    "InvestmentAdvice",
    "ActionPlan",
    "CompleteAnalysisResponse",
    "QuickAnalysisResponse",
    "AnalysisStatus",
    "AnalysisHistoryResponse",
    
    # Market schemas
    "MarketDataBase",
    "KarachiMarketDataResponse",
    "SectorPerformanceResponse",
    "EconomicIndicatorsResponse", 
    "MarketTrendAnalysis",
    "LocationAnalysis",
    "SectorBenchmarks",
    "MarketForecast",
    "CompetitiveAnalysis",
    "MarketInsightsResponse",
]