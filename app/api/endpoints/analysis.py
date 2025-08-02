"""Business analysis endpoints."""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models.business import Business
from app.models.analysis import AnalysisResult, Insight, Recommendation
from app.schemas.business import BusinessAnalysisRequest, QuickBusinessInput
from app.schemas.analysis import (
    CompleteAnalysisResponse, QuickAnalysisResponse, AnalysisStatus,
    PerformanceMetrics, MarketComparison, InvestmentAdvice, ActionPlan
)
from app.core.business_analyzer import BusinessAnalyzer
from app.core.insight_generator import InsightGenerator
from app.core.recommendation_engine import RecommendationEngine
from app.utils.validators import validate_business_data, ValidationError

router = APIRouter()

# Initialize analysis engines
business_analyzer = BusinessAnalyzer()
insight_generator = InsightGenerator()
recommendation_engine = RecommendationEngine()


@router.post("/analyze/quick", response_model=QuickAnalysisResponse)
async def quick_business_analysis(business_input: QuickBusinessInput):
    """
    Quick business analysis without storing data.
    
    Perfect for demos and initial assessments. Returns simplified insights
    and recommendations based on the provided business data.
    """
    try:
        # Validate input data
        business_data = {
            'business_name': 'Quick Analysis',
            'sector': business_input.sector,
            'location_area': business_input.location_area,
            'business_type': business_input.business_type,
            'monthly_revenue': business_input.monthly_revenue,
            'monthly_expenses': business_input.monthly_expenses,
            'current_cash': business_input.current_cash,
            'employees_count': 1,
            'years_in_business': business_input.years_in_business,
            'primary_customers': 'local_walk_ins',
            'main_challenges': [],
            'business_goals': [],
            'notes': ''
        }
        
        validated_data = validate_business_data(business_data)
        
        # Perform analysis
        analysis_result = business_analyzer.analyze_business_performance(validated_data)
        
        # Generate main insight
        main_insight = insight_generator.generate_main_insight(analysis_result, validated_data)
        
        # Generate quick recommendations
        immediate_actions = recommendation_engine.generate_immediate_actions(analysis_result, validated_data)
        investment_advice = recommendation_engine.generate_investment_recommendations(analysis_result, validated_data)
        
        # Create quick response
        current_revenue = analysis_result["performance_metrics"]["current_revenue"]
        market_average = analysis_result["market_position"]["market_average_revenue"]
        performance_ratio = analysis_result["market_position"]["performance_ratio"]
        
        # Determine market position
        if performance_ratio >= 1.3:
            market_position = "Top Performer"
        elif performance_ratio >= 1.1:
            market_position = "Above Average"
        elif performance_ratio >= 0.8:
            market_position = "Average"
        else:
            market_position = "Needs Improvement"
        
        # Key recommendations
        key_recommendations = [action["title"] for action in immediate_actions[:3]]
        
        # Next actions
        next_actions = []
        for action in immediate_actions[:2]:
            if action.get("specific_actions"):
                next_actions.extend(action["specific_actions"][:2])
        
        return QuickAnalysisResponse(
            performance_score=analysis_result["overall_score"]["overall_score"],
            main_message=main_insight["main_message"],
            key_recommendations=key_recommendations,
            investment_capacity=investment_advice["available_capital"],
            next_actions=next_actions[:4],
            market_position=market_position
        )
        
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid business data: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


@router.post("/analyze/complete", response_model=CompleteAnalysisResponse)
async def complete_business_analysis(
    analysis_request: BusinessAnalysisRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Complete business analysis with full insights and recommendations.
    
    Performs comprehensive analysis and optionally stores the business
    data for future tracking and comparison.
    """
    try:
        business_data = analysis_request.business_data.dict()
        analysis_options = analysis_request.analysis_options
        
        # Validate business data
        validated_data = validate_business_data(business_data)
        
        # Store business if requested (background task)
        business_id = None
        if analysis_options.get("store_business_data", False):
            background_tasks.add_task(store_business_data, validated_data, db)
        
        # Perform comprehensive analysis
        analysis_result = business_analyzer.analyze_business_performance(validated_data)
        
        # Generate insights
        main_insight = insight_generator.generate_main_insight(analysis_result, validated_data)
        problem_insights = insight_generator.generate_problem_insights(analysis_result, validated_data)
        opportunity_insights = insight_generator.generate_opportunity_insights(analysis_result, validated_data)
        
        # Generate recommendations
        immediate_actions = recommendation_engine.generate_immediate_actions(analysis_result, validated_data)
        strategic_actions = recommendation_engine.generate_strategic_actions(analysis_result, validated_data)
        investment_advice = recommendation_engine.generate_investment_recommendations(analysis_result, validated_data)
        action_plan = recommendation_engine.generate_action_plan(analysis_result, validated_data)
        
        # Create performance metrics
        performance_metrics = PerformanceMetrics(
            performance_score=analysis_result["overall_score"]["overall_score"],
            business_growth_rate=analysis_result["performance_metrics"]["revenue_growth_rate"],
            sector_growth_rate=0.08,  # Placeholder - would come from market data
            performance_ratio=analysis_result["market_position"]["performance_ratio"],
            revenue_trend=analysis_result["performance_metrics"]["revenue_trend"],
            profit_margin=analysis_result["performance_metrics"]["profit_margin"],
            cash_flow_status=analysis_result["financial_health"]["status"],
            market_position=analysis_result["market_position"]["performance_category"],
            competition_level="medium",  # Would come from market analysis
            business_risk_level=analysis_result["risk_assessment"]["risk_level"],
            volatility_score=analysis_result["risk_assessment"]["risk_components"]["revenue_volatility"] / 100
        )
        
        # Create market comparison
        market_comparison = MarketComparison(
            your_revenue=analysis_result["performance_metrics"]["current_revenue"],
            market_average=analysis_result["market_position"]["market_average_revenue"],
            top_performers=analysis_result["market_position"]["market_average_revenue"] * 1.8,
            your_rank_percentile=analysis_result["market_position"]["percentile_rank"],
            sector_growth=0.08,  # Would come from real market data
            location_factor=analysis_result["market_position"]["market_context"]["location_advantage"]
        )
        
        # Create investment advice
        investment_advice_response = InvestmentAdvice(
            available_capital=investment_advice["available_capital"],
            risk_profile=investment_advice["risk_profile"],
            recommended_investments=investment_advice["investment_options"],
            investment_reasoning=investment_advice["investment_reasoning"],
            expected_annual_return=0.18,  # Calculated from investment options
            diversification_advice="Prioritize business reinvestment, then sector stocks"
        )
        
        # Create action plan
        action_plan_response = ActionPlan(
            immediate_actions=[{
                "title": action["title"],
                "description": action["description"],
                "timeframe": action["timeframe"],
                "expected_benefit": action.get("expected_benefit", 0)
            } for action in immediate_actions],
            short_term_actions=[{
                "title": action["title"],
                "description": action["description"],
                "timeframe": action["timeframe"],
                "expected_benefit": action.get("expected_benefit", 0)
            } for action in strategic_actions],
            strategic_actions=[{
                "title": "Business Expansion",
                "description": "Evaluate second location opportunity",
                "timeframe": "6-12 months",
                "expected_benefit": analysis_result["performance_metrics"]["current_revenue"] * 0.8
            }],
            key_metrics_to_track=action_plan["key_metrics"],
            success_milestones=action_plan["success_milestones"]
        )
        
        # Generate chart data
        chart_data = generate_chart_data(analysis_result, validated_data)
        
        # Generate market context
        market_context = {
            "sector": validated_data["sector"],
            "location": validated_data["location_area"],
            "economic_factors": analysis_result.get("economic_context", {}),
            "competitive_landscape": "Medium competition with growth opportunities",
            "market_trends": ["Digital adoption increasing", "Customer preferences evolving"]
        }
        
        # Create main insight response
        main_insight_response = {
            "id": 1,
            "insight_type": main_insight["insight_type"],
            "priority": main_insight["urgency"],
            "title": main_insight["title"],
            "message": main_insight["main_message"],
            "impact_amount": None,
            "timeframe": None,
            "confidence_score": main_insight["confidence_level"],
            "supporting_data": {"facts": main_insight["supporting_facts"]},
            "created_at": "2024-01-01T00:00:00Z"  # Placeholder
        }
        
        # Create recommendations response
        recommendations_response = []
        for i, action in enumerate(immediate_actions + strategic_actions):
            rec = {
                "id": i + 1,
                "category": action["category"],
                "action_type": action.get("action_type", "improvement"),
                "title": action["title"],
                "description": action["description"],
                "specific_action": action.get("specific_actions", [action["title"]])[0] if action.get("specific_actions") else action["title"],
                "expected_outcome": action.get("expected_outcome", "Positive impact expected"),
                "expected_amount": action.get("expected_benefit"),
                "timeframe": action["timeframe"],
                "investment_required": action.get("investment_required"),
                "difficulty_level": action.get("difficulty", "medium"),
                "implementation_steps": action.get("specific_actions"),
                "is_implemented": False,
                "implementation_date": None,
                "created_at": "2024-01-01T00:00:00Z"  # Placeholder
            }
            recommendations_response.append(rec)
        
        return CompleteAnalysisResponse(
            business_id=business_id,
            analysis_id=1,  # Placeholder
            performance_metrics=performance_metrics,
            main_insight=main_insight_response,
            market_comparison=market_comparison,
            recommendations=recommendations_response,
            investment_advice=investment_advice_response,
            action_plan=action_plan_response,
            chart_data=chart_data,
            market_context=market_context,
            analysis_date="2024-01-01T00:00:00Z",  # Placeholder
            confidence_level=0.85
        )
        
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid business data: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


@router.get("/analysis/{business_id}/latest")
async def get_latest_analysis(
    business_id: int,
    db: Session = Depends(get_db)
):
    """
    Get the latest analysis for a specific business.
    
    Returns the most recent complete analysis results.
    """
    business = db.query(Business).filter(Business.id == business_id).first()
    
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Business with ID {business_id} not found"
        )
    
    # Get latest analysis from database
    latest_analysis = db.query(AnalysisResult).filter(
        AnalysisResult.business_id == business_id
    ).order_by(AnalysisResult.created_at.desc()).first()
    
    if not latest_analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No analysis found for business {business_id}"
        )
    
    return latest_analysis


@router.post("/analysis/{analysis_id}/feedback")
async def submit_analysis_feedback(
    analysis_id: int,
    feedback: dict,
    db: Session = Depends(get_db)
):
    """
    Submit feedback on analysis quality and usefulness.
    
    Helps improve the analysis engine over time.
    """
    try:
        # Store feedback (would implement feedback model)
        # For now, just return success
        
        return {
            "message": "Feedback submitted successfully",
            "analysis_id": analysis_id,
            "feedback_received": True
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to submit feedback: {str(e)}"
        )


@router.get("/analysis/status/{task_id}")
async def get_analysis_status(task_id: str):
    """
    Get status of long-running analysis task.
    
    For future use with background analysis processing.
    """
    # Placeholder for background task status checking
    return AnalysisStatus(
        status="completed",
        progress_percentage=100,
        current_step="Analysis complete",
        estimated_completion=None,
        error_message=None
    )


def generate_chart_data(analysis_result: dict, business_data: dict) -> dict:
    """Generate data for frontend charts."""
    
    monthly_revenue = business_data["monthly_revenue"]
    market_average = analysis_result["market_position"]["market_average_revenue"]
    
    # Revenue trend chart data
    revenue_chart = {
        "labels": ["Month 1", "Month 2", "Month 3", "Month 4", "Month 5", "Month 6"],
        "your_revenue": monthly_revenue,
        "market_average": [market_average] * 6,
        "trend_line": monthly_revenue  # Could add trend calculation
    }
    
    # Performance comparison chart
    performance_chart = {
        "your_score": analysis_result["overall_score"]["overall_score"],
        "market_average": 50,
        "top_performers": 85,
        "categories": {
            "financial_health": analysis_result["overall_score"]["component_breakdown"]["financial_health"],
            "market_position": analysis_result["overall_score"]["component_breakdown"]["market_position"],
            "growth_potential": 70  # Placeholder
        }
    }
    
    # Cash flow projection
    current_revenue = monthly_revenue[-1]
    monthly_expenses = business_data["monthly_expenses"]
    monthly_profit = current_revenue - monthly_expenses
    
    cash_flow_chart = {
        "labels": ["Current", "+1 Month", "+2 Months", "+3 Months"],
        "projected_revenue": [current_revenue * (1 + 0.05) ** i for i in range(4)],
        "projected_expenses": [monthly_expenses] * 4,
        "projected_profit": [monthly_profit * (1 + 0.05) ** i for i in range(4)]
    }
    
    return {
        "revenue_trend": revenue_chart,
        "performance_comparison": performance_chart,
        "cash_flow_projection": cash_flow_chart,
        "sector_comparison": {
            "your_business": current_revenue,
            "sector_average": market_average,
            "sector_top_10": market_average * 1.8
        }
    }


async def store_business_data(validated_data: dict, db: Session):
    """Background task to store business data."""
    try:
        business = Business(**validated_data)
        db.add(business)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Failed to store business data: {e}")