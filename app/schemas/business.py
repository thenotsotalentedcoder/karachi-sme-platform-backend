# app/schemas/business.py
"""Pydantic schemas for US business data."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime
import re


class USBusinessBase(BaseModel):
    """Base US business schema with common fields."""
    
    business_name: str = Field(..., min_length=2, max_length=255, description="Business name")
    
    # US Business identification
    ein_number: Optional[str] = Field(None, description="Employer Identification Number (XX-XXXXXXX)")
    naics_code: Optional[str] = Field(None, description="6-digit NAICS code")
    business_structure: Optional[str] = Field(None, description="LLC, Corporation, Partnership, etc.")
    
    # Industry classification
    sector: str = Field(..., description="Business sector")
    industry_description: Optional[str] = Field(None, max_length=500, description="Detailed industry description")
    
    # US Location data
    street_address: Optional[str] = Field(None, max_length=255, description="Street address")
    city: str = Field(..., min_length=2, max_length=100, description="City name")
    state: str = Field(..., min_length=2, max_length=2, description="2-letter state code")
    zip_code: str = Field(..., description="ZIP code (5 or 9 digits)")
    county: Optional[str] = Field(None, description="County name")
    metro_area: Optional[str] = Field(None, description="Metropolitan Statistical Area")
    
    # Financial data (12 months)
    monthly_expenses: List[float] = Field(..., min_items=12, max_items=12, description="12 months of expenses")
    cost_of_goods_sold: Optional[List[float]] = Field(None, min_items=12, max_items=12, description="12 months of COGS")
    current_cash: float = Field(..., ge=0, description="Current cash available")
    business_assets: Optional[float] = Field(None, ge=0, description="Total business assets")
    outstanding_debt: Optional[float] = Field(None, ge=0, description="Total outstanding debt")
    business_credit_score: Optional[int] = Field(None, ge=0, le=100, description="Business credit score")
    
    # Business operations
    employees_count: int = Field(..., ge=0, description="Number of employees")
    years_in_business: int = Field(..., ge=0, le=150, description="Years in business")
    is_seasonal_business: bool = Field(False, description="Whether business is seasonal")
    business_model: Optional[str] = Field(None, description="B2B, B2C, B2B2C, etc.")
    
    # Customer and market data
    primary_customer_type: Optional[List[str]] = Field(default=[], description="Primary customer types")
    revenue_streams: Optional[List[str]] = Field(default=[], description="Revenue stream sources")
    target_market: Optional[str] = Field(None, max_length=500, description="Target market description")
    marketing_channels: Optional[List[str]] = Field(default=[], description="Marketing channels used")
    
    # Competition
    main_competitors: Optional[List[str]] = Field(default=[], description="Main competitor names")
    unique_value_proposition: Optional[str] = Field(None, max_length=500, description="Unique value proposition")
    competitive_advantages: Optional[List[str]] = Field(default=[], description="Competitive advantages")
    
    # Goals and challenges
    business_goals: Optional[List[str]] = Field(default=[], description="Business goals")
    main_challenges: Optional[List[str]] = Field(default=[], description="Main business challenges")
    expansion_plans: Optional[List[str]] = Field(default=[], description="Expansion plans")
    investment_interests: Optional[List[str]] = Field(default=[], description="Investment interests")
    
    # Additional info
    certifications: Optional[List[str]] = Field(default=[], description="Business certifications")
    licenses: Optional[List[str]] = Field(default=[], description="Required business licenses")
    notes: Optional[str] = Field(default="", max_length=1000, description="Additional notes")


class USBusinessCreate(USBusinessBase):
    """Schema for creating a new US business."""
    
    monthly_revenue: List[float] = Field(
        ..., 
        min_items=12, 
        max_items=12, 
        description="Monthly revenue for last 12 months (oldest to newest)"
    )
    
    @validator('monthly_revenue')
    def validate_monthly_revenue(cls, v):
        """Validate monthly revenue data."""
        if not v or len(v) != 12:
            raise ValueError('Monthly revenue must contain exactly 12 values')
        
        for i, revenue in enumerate(v):
            if revenue < 0:
                raise ValueError(f'Revenue for month {i+1} must be non-negative')
            if revenue > 50000000:  # $50M monthly limit
                raise ValueError(f'Revenue for month {i+1} seems unreasonably high')
        
        return v
    
    @validator('monthly_expenses')
    def validate_monthly_expenses(cls, v):
        """Validate monthly expenses data."""
        if not v or len(v) != 12:
            raise ValueError('Monthly expenses must contain exactly 12 values')
        
        for i, expense in enumerate(v):
            if expense < 0:
                raise ValueError(f'Expenses for month {i+1} must be non-negative')
            if expense > 40000000:  # $40M monthly limit
                raise ValueError(f'Expenses for month {i+1} seem unreasonably high')
        
        return v
    
    @validator('ein_number')
    def validate_ein(cls, v):
        """Validate EIN format."""
        if v is None:
            return v
        
        # EIN format: XX-XXXXXXX
        ein_pattern = r'^\d{2}-\d{7}$'
        if not re.match(ein_pattern, v):
            raise ValueError('EIN must be in format XX-XXXXXXX (e.g., 12-3456789)')
        
        return v
    
    @validator('naics_code')
    def validate_naics(cls, v):
        """Validate NAICS code format."""
        if v is None:
            return v
        
        # NAICS codes are 2-6 digits
        if not v.isdigit() or len(v) < 2 or len(v) > 6:
            raise ValueError('NAICS code must be 2-6 digits')
        
        return v
    
    @validator('sector')
    def validate_sector(cls, v):
        """Validate business sector."""
        valid_sectors = {
            'electronics', 'food', 'retail', 'auto', 'professional_services', 
            'manufacturing', 'construction', 'healthcare'
        }
        if v.lower() not in valid_sectors:
            raise ValueError(f'Sector must be one of: {", ".join(valid_sectors)}')
        return v.lower()
    
    @validator('state')
    def validate_state(cls, v):
        """Validate US state code."""
        us_states = {
            'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
            'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
            'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
            'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
            'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'DC'
        }
        if v.upper() not in us_states:
            raise ValueError(f'State must be a valid US state code')
        return v.upper()
    
    @validator('zip_code')
    def validate_zip_code(cls, v):
        """Validate ZIP code format."""
        # ZIP formats: 12345 or 12345-6789
        zip_pattern = r'^\d{5}(-\d{4})?$'
        if not re.match(zip_pattern, v):
            raise ValueError('ZIP code must be in format 12345 or 12345-6789')
        return v
    
    @validator('business_structure')
    def validate_business_structure(cls, v):
        """Validate business structure."""
        if v is None:
            return v
        
        valid_structures = {
            'sole_proprietorship', 'partnership', 'llc', 'corporation', 
            's_corporation', 'c_corporation', 'nonprofit'
        }
        structure_clean = v.lower().replace(' ', '_').replace('-', '_')
        if structure_clean not in valid_structures:
            raise ValueError(f'Business structure must be one of: {", ".join(valid_structures)}')
        return structure_clean
    
    @validator('business_goals')
    def validate_business_goals(cls, v):
        """Validate business goals."""
        if not v:
            return []
        
        valid_goals = {
            'increase_revenue', 'improve_profitability', 'expand_locations', 
            'hire_employees', 'improve_cash_flow', 'reduce_costs', 
            'enter_new_markets', 'launch_new_products', 'improve_operations',
            'build_brand', 'go_digital', 'get_funding', 'exit_business'
        }
        
        validated_goals = []
        for goal in v:
            goal_clean = goal.lower().replace(' ', '_').replace('-', '_')
            if goal_clean in valid_goals:
                validated_goals.append(goal_clean)
        
        return validated_goals
    
    @validator('main_challenges')
    def validate_main_challenges(cls, v):
        """Validate main challenges."""
        if not v:
            return []
        
        valid_challenges = {
            'cash_flow', 'competition', 'finding_customers', 'hiring_staff',
            'regulations', 'supply_chain', 'technology', 'marketing',
            'rising_costs', 'economic_uncertainty', 'debt_management',
            'inventory_management', 'customer_retention', 'scaling_operations'
        }
        
        validated_challenges = []
        for challenge in v:
            challenge_clean = challenge.lower().replace(' ', '_').replace('-', '_')
            if challenge_clean in valid_challenges:
                validated_challenges.append(challenge_clean)
        
        return validated_challenges


class USBusinessResponse(USBusinessBase):
    """Schema for US business response."""
    
    id: int
    monthly_revenue: List[float]
    location_type: Optional[str] = None  # Will be classified automatically
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class USBusinessUpdate(BaseModel):
    """Schema for updating US business data."""
    
    business_name: Optional[str] = Field(None, min_length=2, max_length=255)
    monthly_revenue: Optional[List[float]] = Field(None, min_items=12, max_items=12)
    monthly_expenses: Optional[List[float]] = Field(None, min_items=12, max_items=12)
    current_cash: Optional[float] = Field(None, ge=0)
    business_assets: Optional[float] = Field(None, ge=0)
    outstanding_debt: Optional[float] = Field(None, ge=0)
    employees_count: Optional[int] = Field(None, ge=0)
    main_challenges: Optional[List[str]] = None
    business_goals: Optional[List[str]] = None
    notes: Optional[str] = Field(None, max_length=1000)


class USBusinessSummary(BaseModel):
    """Schema for US business summary information."""
    
    id: int
    business_name: str
    sector: str
    city: str
    state: str
    current_monthly_revenue: float  # Latest month revenue
    revenue_trend: str  # "increasing", "decreasing", "stable"
    annual_revenue: float  # Sum of 12 months
    employees_count: int
    years_in_business: int
    performance_score: Optional[float] = None
    last_analysis: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class USBusinessAnalysisRequest(BaseModel):
    """Schema for US business analysis request."""
    
    business_data: USBusinessCreate
    analysis_options: Optional[Dict[str, Any]] = Field(
        default={
            "include_investment_advice": True,
            "include_market_comparison": True,
            "include_economic_impact": True,
            "include_growth_analysis": True,
            "include_risk_assessment": True,
            "detail_level": "comprehensive"  # "basic", "standard", "comprehensive"
        }
    )
    economic_context: Optional[Dict[str, Any]] = Field(
        default={}, description="Additional economic context if available"
    )


class QuickUSBusinessInput(BaseModel):
    """Schema for quick US business analysis without storing data."""
    
    sector: str = Field(..., description="Business sector")
    city: str = Field(..., description="City name")
    state: str = Field(..., description="2-letter state code")
    zip_code: str = Field(..., description="ZIP code")
    monthly_revenue: List[float] = Field(..., min_items=12, max_items=12)
    monthly_expenses: List[float] = Field(..., min_items=12, max_items=12)
    current_cash: float = Field(..., ge=0)
    employees_count: int = Field(..., ge=0)
    years_in_business: int = Field(..., ge=0, le=150)
    
    @validator('monthly_expenses')
    def validate_monthly_expenses(cls, v):
        """Validate monthly expenses data."""
        if not v or len(v) != 12:
            raise ValueError('Monthly expenses must contain exactly 12 values')
        
        for i, expense in enumerate(v):
            if expense < 0:
                raise ValueError(f'Expenses for month {i+1} must be non-negative')
            if expense > 40000000:  # $40M monthly limit
                raise ValueError(f'Expenses for month {i+1} seem unreasonably high')
        
        return v
    
    @validator('ein_number')
    def validate_ein(cls, v):
        """Validate EIN format."""
        if v is None:
            return v
        
        # EIN format: XX-XXXXXXX
        ein_pattern = r'^\d{2}-\d{7}$'
        if not re.match(ein_pattern, v):
            raise ValueError('EIN must be in format XX-XXXXXXX (e.g., 12-3456789)')
        
        return v
    
    @validator('naics_code')
    def validate_naics(cls, v):
        """Validate NAICS code format."""
        if v is None:
            return v
        
        # NAICS codes are 2-6 digits
        if not v.isdigit() or len(v) < 2 or len(v) > 6:
            raise ValueError('NAICS code must be 2-6 digits')
        
        return v
    
    @validator('sector')
    def validate_sector(cls, v):
        """Validate business sector."""
        valid_sectors = {
            'electronics', 'food', 'retail', 'auto', 'professional_services', 
            'manufacturing', 'construction', 'healthcare'
        }
        if v.lower() not in valid_sectors:
            raise ValueError(f'Sector must be one of: {", ".join(valid_sectors)}')
        return v.lower()
    
    @validator('state')
    def validate_state(cls, v):
        """Validate US state code."""
        us_states = {
            'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
            'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
            'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
            'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
            'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'DC'
        }
        if v.upper() not in us_states:
            raise ValueError(f'State must be a valid US state code')
        return v.upper()
    
    @validator('zip_code')
    def validate_zip_code(cls, v):
        """Validate ZIP code format."""
        # ZIP formats: 12345 or 12345-6789
        zip_pattern = r'^\d{5}(-\d{4})?$'
        if not re.match(zip_pattern, v):
            raise ValueError('ZIP code must be in format 12345 or 12345-6789')
        return v
    
    @validator('business_structure')
    def validate_business_structure(cls, v):
        """Validate business structure."""
        if v is None:
            return v
        
        valid_structures = {
            'sole_proprietorship', 'partnership', 'llc', 'corporation', 
            's_corporation', 'c_corporation', 'nonprofit'
        }
        structure_clean = v.lower().replace(' ', '_').replace('-', '_')
        if structure_clean not in valid_structures:
            raise ValueError(f'Business structure must be one of: {", ".join(valid_structures)}')
        return structure_clean
    
    @validator('business_goals')
    def validate_business_goals(cls, v):
        """Validate business goals."""
        if not v:
            return []
        
        valid_goals = {
            'increase_revenue', 'improve_profitability', 'expand_locations', 
            'hire_employees', 'improve_cash_flow', 'reduce_costs', 
            'enter_new_markets', 'launch_new_products', 'improve_operations',
            'build_brand', 'go_digital', 'get_funding', 'exit_business'
        }
        
        validated_goals = []
        for goal in v:
            goal_clean = goal.lower().replace(' ', '_').replace('-', '_')
            if goal_clean in valid_goals:
                validated_goals.append(goal_clean)
        
        return validated_goals
    
    @validator('main_challenges')
    def validate_main_challenges(cls, v):
        """Validate main challenges."""
        if not v:
            return []
        
        valid_challenges = {
            'cash_flow', 'competition', 'finding_customers', 'hiring_staff',
            'regulations', 'supply_chain', 'technology', 'marketing',
            'rising_costs', 'economic_uncertainty', 'debt_management',
            'inventory_management', 'customer_retention', 'scaling_operations'
        }
        
        validated_challenges = []
        for challenge in v:
            challenge_clean = challenge.lower().replace(' ', '_').replace('-', '_')
            if challenge_clean in valid_challenges:
                validated_challenges.append(challenge_clean)
        
        return validated_challenges


class USBusinessResponse(USBusinessBase):
    """Schema for US business response."""
    
    id: int
    monthly_revenue: List[float]
    location_type: Optional[str] = None  # Will be classified automatically
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class USBusinessUpdate(BaseModel):
    """Schema for updating US business data."""
    
    business_name: Optional[str] = Field(None, min_length=2, max_length=255)
    monthly_revenue: Optional[List[float]] = Field(None, min_items=12, max_items=12)
    monthly_expenses: Optional[List[float]] = Field(None, min_items=12, max_items=12)
    current_cash: Optional[float] = Field(None, ge=0)
    business_assets: Optional[float] = Field(None, ge=0)
    outstanding_debt: Optional[float] = Field(None, ge=0)
    employees_count: Optional[int] = Field(None, ge=0)
    main_challenges: Optional[List[str]] = None
    business_goals: Optional[List[str]] = None
    notes: Optional[str] = Field(None, max_length=1000)


class USBusinessSummary(BaseModel):
    """Schema for US business summary information."""
    
    id: int
    business_name: str
    sector: str
    city: str
    state: str
    current_monthly_revenue: float  # Latest month revenue
    revenue_trend: str  # "increasing", "decreasing", "stable"
    annual_revenue: float  # Sum of 12 months
    employees_count: int
    years_in_business: int
    performance_score: Optional[float] = None
    last_analysis: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class USBusinessAnalysisRequest(BaseModel):
    """Schema for US business analysis request."""
    
    business_data: USBusinessCreate
    analysis_options: Optional[Dict[str, Any]] = Field(
        default={
            "include_investment_advice": True,
            "include_market_comparison": True,
            "include_economic_impact": True,
            "include_growth_analysis": True,
            "include_risk_assessment": True,
            "detail_level": "comprehensive"  # "basic", "standard", "comprehensive"
        }
    )
    economic_context: Optional[Dict[str, Any]] = Field(
        default={}, description="Additional economic context if available"
    )


class QuickUSBusinessInput(BaseModel):
    """Schema for quick US business analysis without storing data."""
    
    sector: str = Field(..., description="Business sector")
    city: str = Field(..., description="City name")
    state: str = Field(..., description="2-letter state code")
    zip_code: str = Field(..., description="ZIP code")
    monthly_revenue: List[float] = Field(..., min_items=12, max_items=12)
    monthly_expenses: List[float] = Field(..., min_items=12, max_items=12)
    current_cash: float = Field(..., ge=0)
    employees_count: int = Field(..., ge=0)
    years_in_business: int = Field(..., ge=0, le=150)
    
    @validator('monthly_revenue', 'monthly_expenses')
    def validate_financial_data(cls, v):
        """Validate financial data arrays."""
        if len(v) != 12:
            raise ValueError('Must provide exactly 12 months of data')
        for i, value in enumerate(v):
            if value < 0:
                raise ValueError(f'Financial values must be non-negative (month {i+1})')
        return v
    
    @validator('sector')
    def validate_sector_quick(cls, v):
        """Validate business sector for quick input."""
        valid_sectors = {
            'electronics', 'food', 'retail', 'auto', 'professional_services', 
            'manufacturing', 'construction', 'healthcare'
        }
        if v.lower() not in valid_sectors:
            raise ValueError(f'Sector must be one of: {", ".join(valid_sectors)}')
        return v.lower()
    
    @validator('state')
    def validate_state_quick(cls, v):
        """Validate US state code for quick input."""
        us_states = {
            'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
            'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
            'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
            'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
            'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'DC'
        }
        if v.upper() not in us_states:
            raise ValueError(f'State must be a valid US state code')
        return v.upper()
    
    @validator('zip_code')
    def validate_zip_code_quick(cls, v):
        """Validate ZIP code format for quick input."""
        zip_pattern = r'^\d{5}(-\d{4})?$'
        if not re.match(zip_pattern, v):
            raise ValueError('ZIP code must be in format 12345 or 12345-6789')
        return v