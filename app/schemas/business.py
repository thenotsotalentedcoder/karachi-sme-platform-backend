"""Pydantic schemas for business data."""

from typing import List, Optional
from pydantic import BaseModel, Field, validator
from datetime import datetime


class BusinessBase(BaseModel):
    """Base business schema with common fields."""
    
    business_name: str = Field(..., min_length=2, max_length=255, description="Business name")
    sector: str = Field(..., description="Business sector")
    location_area: str = Field(..., description="Location area in Karachi")
    business_type: str = Field(..., description="Type of business")
    monthly_expenses: float = Field(..., ge=0, description="Average monthly expenses in PKR")
    current_cash: float = Field(..., ge=0, description="Current cash available in PKR")
    employees_count: int = Field(..., ge=0, description="Number of employees")
    years_in_business: int = Field(..., ge=0, le=100, description="Years in business")
    primary_customers: str = Field(..., description="Primary customer type")
    main_challenges: Optional[List[str]] = Field(default=[], description="Main business challenges")
    business_goals: Optional[List[str]] = Field(default=[], description="Business goals")
    notes: Optional[str] = Field(default="", max_length=1000, description="Additional notes")


class BusinessCreate(BusinessBase):
    """Schema for creating a new business."""
    
    monthly_revenue: List[float] = Field(
        ..., 
        min_items=6, 
        max_items=6, 
        description="Monthly revenue for last 6 months (oldest to newest)"
    )
    
    @validator('monthly_revenue')
    def validate_monthly_revenue(cls, v):
        """Validate monthly revenue data."""
        if not v or len(v) != 6:
            raise ValueError('Monthly revenue must contain exactly 6 values')
        
        for revenue in v:
            if revenue < 0:
                raise ValueError('Monthly revenue values must be non-negative')
        
        return v
    
    @validator('sector')
    def validate_sector(cls, v):
        """Validate business sector."""
        valid_sectors = {'electronics', 'textile', 'auto', 'food', 'retail'}
        if v.lower() not in valid_sectors:
            raise ValueError(f'Sector must be one of: {", ".join(valid_sectors)}')
        return v.lower()
    
    @validator('location_area')
    def validate_location(cls, v):
        """Validate Karachi location."""
        valid_locations = {
            'clifton', 'dha', 'saddar', 'tariq_road', 'gulshan', 
            'gulistan_e_johar', 'korangi', 'landhi', 'north_karachi', 'nazimabad'
        }
        location_clean = v.lower().replace(' ', '_').replace('-', '_')
        if location_clean not in valid_locations:
            raise ValueError(f'Location must be one of: {", ".join(valid_locations)}')
        return location_clean
    
    @validator('business_type')
    def validate_business_type(cls, v):
        """Validate business type."""
        valid_types = {'retail_shop', 'manufacturing', 'service_provider', 'trading_wholesale'}
        business_type_clean = v.lower().replace(' ', '_').replace('/', '_')
        if business_type_clean not in valid_types:
            raise ValueError(f'Business type must be one of: {", ".join(valid_types)}')
        return business_type_clean
    
    @validator('primary_customers')
    def validate_primary_customers(cls, v):
        """Validate primary customers."""
        valid_customers = {
            'local_walk_ins', 'regular_customers', 'online_delivery', 
            'wholesale_buyers', 'corporate_clients'
        }
        customer_clean = v.lower().replace(' ', '_').replace('-', '_')
        if customer_clean not in valid_customers:
            raise ValueError(f'Primary customers must be one of: {", ".join(valid_customers)}')
        return customer_clean


class BusinessResponse(BusinessBase):
    """Schema for business response."""
    
    id: int
    monthly_revenue: List[float]
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class BusinessUpdate(BaseModel):
    """Schema for updating business data."""
    
    business_name: Optional[str] = Field(None, min_length=2, max_length=255)
    monthly_revenue: Optional[List[float]] = Field(None, min_items=6, max_items=6)
    monthly_expenses: Optional[float] = Field(None, ge=0)
    current_cash: Optional[float] = Field(None, ge=0)
    employees_count: Optional[int] = Field(None, ge=0)
    main_challenges: Optional[List[str]] = None
    business_goals: Optional[List[str]] = None
    notes: Optional[str] = Field(None, max_length=1000)


class BusinessSummary(BaseModel):
    """Schema for business summary information."""
    
    id: int
    business_name: str
    sector: str
    location_area: str
    current_revenue: float  # Latest month revenue
    revenue_trend: str  # "increasing", "decreasing", "stable"
    performance_score: Optional[float] = None
    last_analysis: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class BusinessAnalysisRequest(BaseModel):
    """Schema for business analysis request."""
    
    business_data: BusinessCreate
    analysis_options: Optional[dict] = Field(
        default={
            "include_investment_advice": True,
            "include_expansion_analysis": True,
            "include_market_comparison": True,
            "detail_level": "standard"  # "basic", "standard", "detailed"
        }
    )


class QuickBusinessInput(BaseModel):
    """Schema for quick business analysis without storing data."""
    
    sector: str = Field(..., description="Business sector")
    location_area: str = Field(..., description="Karachi location")
    monthly_revenue: List[float] = Field(..., min_items=6, max_items=6)
    monthly_expenses: float = Field(..., ge=0)
    current_cash: float = Field(..., ge=0)
    business_type: str = Field(..., description="Type of business")
    years_in_business: int = Field(..., ge=0, le=100)
    
    @validator('monthly_revenue')
    def validate_revenue(cls, v):
        """Validate revenue data."""
        if len(v) != 6:
            raise ValueError('Must provide exactly 6 months of revenue data')
        for revenue in v:
            if revenue < 0:
                raise ValueError('Revenue values must be non-negative')
        return v