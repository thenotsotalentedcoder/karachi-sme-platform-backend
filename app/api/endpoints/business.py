"""Business data management endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.business import Business, BusinessAnalysisHistory
from app.schemas.business import (
    BusinessCreate, BusinessResponse, BusinessUpdate, 
    BusinessSummary, QuickBusinessInput
)
from app.utils.validators import validate_business_data, ValidationError

router = APIRouter()


@router.post("/businesses/", response_model=BusinessResponse, status_code=status.HTTP_201_CREATED)
async def create_business(
    business_data: BusinessCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new business record.
    
    This endpoint creates a complete business profile that can be used
    for future analysis and tracking.
    """
    try:
        # Validate the business data
        validated_data = validate_business_data(business_data.dict())
        
        # Create new business record
        db_business = Business(**validated_data)
        db.add(db_business)
        db.commit()
        db.refresh(db_business)
        
        return db_business
        
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create business: {str(e)}"
        )


@router.get("/businesses/", response_model=List[BusinessSummary])
async def list_businesses(
    sector: Optional[str] = None,
    location: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List businesses with optional filtering.
    
    Filter by sector and/or location to find specific businesses.
    """
    query = db.query(Business)
    
    if sector:
        query = query.filter(Business.sector == sector.lower())
    
    if location:
        location_clean = location.lower().replace(' ', '_').replace('-', '_')
        query = query.filter(Business.location_area == location_clean)
    
    businesses = query.offset(skip).limit(limit).all()
    
    # Convert to summary format
    business_summaries = []
    for business in businesses:
        current_revenue = business.monthly_revenue[-1] if business.monthly_revenue else 0
        
        # Calculate revenue trend
        if len(business.monthly_revenue) >= 2:
            recent_avg = sum(business.monthly_revenue[-2:]) / 2
            earlier_avg = sum(business.monthly_revenue[:2]) / 2 if len(business.monthly_revenue) >= 4 else business.monthly_revenue[0]
            
            if recent_avg > earlier_avg * 1.05:
                revenue_trend = "increasing"
            elif recent_avg < earlier_avg * 0.95:
                revenue_trend = "decreasing"
            else:
                revenue_trend = "stable"
        else:
            revenue_trend = "insufficient_data"
        
        summary = BusinessSummary(
            id=business.id,
            business_name=business.business_name,
            sector=business.sector,
            location_area=business.location_area,
            current_revenue=current_revenue,
            revenue_trend=revenue_trend,
            performance_score=None,  # Will be filled if analysis exists
            last_analysis=None
        )
        
        business_summaries.append(summary)
    
    return business_summaries


@router.get("/businesses/{business_id}", response_model=BusinessResponse)
async def get_business(
    business_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific business by ID.
    
    Returns complete business information including all financial data.
    """
    business = db.query(Business).filter(Business.id == business_id).first()
    
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Business with ID {business_id} not found"
        )
    
    return business


@router.put("/businesses/{business_id}", response_model=BusinessResponse)
async def update_business(
    business_id: int,
    business_update: BusinessUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing business record.
    
    Only provided fields will be updated. Revenue data updates will
    trigger new analysis recommendations.
    """
    business = db.query(Business).filter(Business.id == business_id).first()
    
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Business with ID {business_id} not found"
        )
    
    try:
        # Update only provided fields
        update_data = business_update.dict(exclude_unset=True)
        
        # Validate updated data if critical fields are changed
        if any(field in update_data for field in ['monthly_revenue', 'monthly_expenses', 'current_cash']):
            # Get current data and apply updates for validation
            current_data = {
                'business_name': business.business_name,
                'sector': business.sector,
                'location_area': business.location_area,
                'business_type': business.business_type,
                'monthly_revenue': business.monthly_revenue,
                'monthly_expenses': business.monthly_expenses,
                'current_cash': business.current_cash,
                'employees_count': business.employees_count,
                'years_in_business': business.years_in_business,
                'primary_customers': business.primary_customers,
                'main_challenges': business.main_challenges or [],
                'business_goals': business.business_goals or [],
                'notes': business.notes or '',
            }
            current_data.update(update_data)
            validate_business_data(current_data)
        
        # Apply updates
        for field, value in update_data.items():
            setattr(business, field, value)
        
        db.commit()
        db.refresh(business)
        
        return business
        
    except ValidationError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update business: {str(e)}"
        )


@router.delete("/businesses/{business_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_business(
    business_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a business record.
    
    This will also delete all associated analysis history.
    """
    business = db.query(Business).filter(Business.id == business_id).first()
    
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Business with ID {business_id} not found"
        )
    
    try:
        # Delete associated analysis history first
        db.query(BusinessAnalysisHistory).filter(
            BusinessAnalysisHistory.business_id == business_id
        ).delete()
        
        # Delete the business
        db.delete(business)
        db.commit()
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete business: {str(e)}"
        )


@router.get("/businesses/{business_id}/analysis-history")
async def get_business_analysis_history(
    business_id: int,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get analysis history for a business.
    
    Returns the most recent analysis results to track business progress over time.
    """
    business = db.query(Business).filter(Business.id == business_id).first()
    
    if not business:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Business with ID {business_id} not found"
        )
    
    analysis_history = db.query(BusinessAnalysisHistory).filter(
        BusinessAnalysisHistory.business_id == business_id
    ).order_by(BusinessAnalysisHistory.created_at.desc()).limit(limit).all()
    
    return analysis_history


@router.get("/sectors/", response_model=List[str])
async def get_available_sectors():
    """
    Get list of available business sectors.
    
    Returns all sectors supported by the platform for Karachi businesses.
    """
    return ["electronics", "textile", "auto", "food", "retail"]


@router.get("/locations/", response_model=List[str])
async def get_available_locations():
    """
    Get list of available Karachi locations.
    
    Returns all locations in Karachi where we provide market intelligence.
    """
    return [
        "clifton", "dha", "saddar", "tariq_road", "gulshan", 
        "gulistan_e_johar", "korangi", "landhi", "north_karachi", "nazimabad"
    ]


@router.get("/business-types/", response_model=List[str])
async def get_business_types():
    """
    Get list of available business types.
    
    Returns all business operation types supported by the platform.
    """
    return ["retail_shop", "manufacturing", "service_provider", "trading_wholesale"]


@router.get("/customer-types/", response_model=List[str])
async def get_customer_types():
    """
    Get list of primary customer types.
    
    Returns all customer categories for business classification.
    """
    return [
        "local_walk_ins", "regular_customers", "online_delivery", 
        "wholesale_buyers", "corporate_clients"
    ]


@router.get("/challenges/", response_model=List[str])
async def get_common_challenges():
    """
    Get list of common business challenges.
    
    Returns typical challenges faced by Karachi SMEs for selection.
    """
    return [
        "declining_sales", "high_competition", "cash_flow_issues", 
        "supplier_problems", "marketing_customer_acquisition",
        "inventory_management", "staff_operational_issues"
    ]


@router.get("/goals/", response_model=List[str])
async def get_business_goals():
    """
    Get list of common business goals.
    
    Returns typical business objectives for goal setting.
    """
    return [
        "increase_profits", "expand_open_new_location", "improve_cash_flow",
        "invest_surplus_money", "get_bank_loan"
    ]


@router.post("/businesses/validate")
async def validate_business_data_endpoint(business_data: QuickBusinessInput):
    """
    Validate business data without creating a record.
    
    Use this endpoint to validate form data before submission.
    """
    try:
        # Convert QuickBusinessInput to dict for validation
        data_dict = {
            'business_name': 'Validation Test',  # Placeholder
            'sector': business_data.sector,
            'location_area': business_data.location_area,
            'business_type': business_data.business_type,
            'monthly_revenue': business_data.monthly_revenue,
            'monthly_expenses': business_data.monthly_expenses,
            'current_cash': business_data.current_cash,
            'employees_count': 1,  # Placeholder
            'years_in_business': business_data.years_in_business,
            'primary_customers': 'local_walk_ins',  # Placeholder
        }
        
        validated_data = validate_business_data(data_dict)
        
        # Calculate basic metrics for preview
        current_revenue = validated_data['monthly_revenue'][-1]
        monthly_expenses = validated_data['monthly_expenses']
        profit_margin = max(0, (current_revenue - monthly_expenses) / current_revenue) if current_revenue > 0 else 0
        
        return {
            "valid": True,
            "message": "Business data is valid",
            "preview_metrics": {
                "current_monthly_revenue": current_revenue,
                "estimated_profit_margin": f"{profit_margin*100:.1f}%",
                "monthly_profit": current_revenue - monthly_expenses,
                "cash_runway_months": validated_data['current_cash'] / monthly_expenses if monthly_expenses > 0 else 999
            }
        }
        
    except ValidationError as e:
        return {
            "valid": False,
            "message": str(e),
            "preview_metrics": None
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Validation error: {str(e)}"
        )


@router.get("/businesses/stats/summary")
async def get_platform_stats(db: Session = Depends(get_db)):
    """
    Get platform usage statistics.
    
    Returns summary statistics about businesses using the platform.
    """
    try:
        total_businesses = db.query(Business).count()
        
        # Count by sector
        sector_counts = {}
        for sector in ["electronics", "textile", "auto", "food", "retail"]:
            count = db.query(Business).filter(Business.sector == sector).count()
            sector_counts[sector] = count
        
        # Count by location
        location_counts = {}
        locations = ["clifton", "dha", "saddar", "tariq_road", "gulshan", "korangi"]
        for location in locations:
            count = db.query(Business).filter(Business.location_area == location).count()
            location_counts[location] = count
        
        return {
            "total_businesses": total_businesses,
            "businesses_by_sector": sector_counts,
            "businesses_by_location": location_counts,
            "platform_coverage": {
                "sectors_covered": 5,
                "locations_covered": 10,
                "karachi_market_coverage": "comprehensive"
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get platform stats: {str(e)}"
        )