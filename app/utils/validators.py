"""Input validation utilities for business data."""

import re
from typing import Any, List, Dict, Optional, Union
from datetime import datetime


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def validate_business_name(name: str) -> str:
    """Validate and clean business name."""
    if not name or not isinstance(name, str):
        raise ValidationError("Business name is required")
    
    cleaned_name = name.strip()
    
    if len(cleaned_name) < 2:
        raise ValidationError("Business name must be at least 2 characters")
    
    if len(cleaned_name) > 255:
        raise ValidationError("Business name must be less than 255 characters")
    
    # Remove excessive whitespace
    cleaned_name = re.sub(r'\s+', ' ', cleaned_name)
    
    return cleaned_name


def validate_sector(sector: str) -> str:
    """Validate business sector."""
    valid_sectors = {
        'electronics', 'textile', 'auto', 'food', 'retail'
    }
    
    if not sector or not isinstance(sector, str):
        raise ValidationError("Sector is required")
    
    sector_clean = sector.lower().strip()
    
    if sector_clean not in valid_sectors:
        raise ValidationError(f"Invalid sector. Must be one of: {', '.join(valid_sectors)}")
    
    return sector_clean


def validate_karachi_location(location: str) -> str:
    """Validate Karachi location."""
    valid_locations = {
        'clifton', 'dha', 'saddar', 'tariq_road', 'gulshan', 
        'gulistan_e_johar', 'korangi', 'landhi', 'north_karachi', 'nazimabad'
    }
    
    if not location or not isinstance(location, str):
        raise ValidationError("Location is required")
    
    # Clean location string
    location_clean = location.lower().strip().replace(' ', '_').replace('-', '_')
    
    if location_clean not in valid_locations:
        raise ValidationError(f"Invalid location. Must be one of: {', '.join(valid_locations)}")
    
    return location_clean


def validate_business_type(business_type: str) -> str:
    """Validate business type."""
    valid_types = {
        'retail_shop', 'manufacturing', 'service_provider', 'trading_wholesale'
    }
    
    if not business_type or not isinstance(business_type, str):
        raise ValidationError("Business type is required")
    
    type_clean = business_type.lower().strip().replace(' ', '_').replace('/', '_')
    
    if type_clean not in valid_types:
        raise ValidationError(f"Invalid business type. Must be one of: {', '.join(valid_types)}")
    
    return type_clean


def validate_primary_customers(customers: str) -> str:
    """Validate primary customer type."""
    valid_customers = {
        'local_walk_ins', 'regular_customers', 'online_delivery', 
        'wholesale_buyers', 'corporate_clients'
    }
    
    if not customers or not isinstance(customers, str):
        raise ValidationError("Primary customers type is required")
    
    customers_clean = customers.lower().strip().replace(' ', '_').replace('-', '_')
    
    if customers_clean not in valid_customers:
        raise ValidationError(f"Invalid customer type. Must be one of: {', '.join(valid_customers)}")
    
    return customers_clean


def validate_monthly_revenue(revenue: List[float]) -> List[float]:
    """Validate monthly revenue data."""
    if not revenue or not isinstance(revenue, list):
        raise ValidationError("Monthly revenue data is required")
    
    if len(revenue) != 6:
        raise ValidationError("Monthly revenue must contain exactly 6 values")
    
    validated_revenue = []
    
    for i, value in enumerate(revenue):
        try:
            float_value = float(value)
            if float_value < 0:
                raise ValidationError(f"Revenue for month {i+1} cannot be negative")
            if float_value > 100000000:  # 10 crore limit
                raise ValidationError(f"Revenue for month {i+1} seems unreasonably high")
            validated_revenue.append(float_value)
        except (ValueError, TypeError):
            raise ValidationError(f"Invalid revenue value for month {i+1}")
    
    return validated_revenue


def validate_monthly_expenses(expenses: float) -> float:
    """Validate monthly expenses."""
    try:
        expenses_float = float(expenses)
    except (ValueError, TypeError):
        raise ValidationError("Monthly expenses must be a valid number")
    
    if expenses_float < 0:
        raise ValidationError("Monthly expenses cannot be negative")
    
    if expenses_float > 50000000:  # 5 crore limit
        raise ValidationError("Monthly expenses seem unreasonably high")
    
    return expenses_float


def validate_current_cash(cash: float) -> float:
    """Validate current cash amount."""
    try:
        cash_float = float(cash)
    except (ValueError, TypeError):
        raise ValidationError("Current cash must be a valid number")
    
    if cash_float < 0:
        raise ValidationError("Current cash cannot be negative")
    
    if cash_float > 1000000000:  # 100 crore limit
        raise ValidationError("Current cash amount seems unreasonably high")
    
    return cash_float


def validate_employees_count(count: int) -> int:
    """Validate employee count."""
    try:
        count_int = int(count)
    except (ValueError, TypeError):
        raise ValidationError("Employee count must be a valid number")
    
    if count_int < 0:
        raise ValidationError("Employee count cannot be negative")
    
    if count_int > 10000:
        raise ValidationError("Employee count seems unreasonably high for SME")
    
    return count_int


def validate_years_in_business(years: int) -> int:
    """Validate years in business."""
    try:
        years_int = int(years)
    except (ValueError, TypeError):
        raise ValidationError("Years in business must be a valid number")
    
    if years_int < 0:
        raise ValidationError("Years in business cannot be negative")
    
    if years_int > 100:
        raise ValidationError("Years in business seems unreasonably high")
    
    return years_int


def validate_challenges_list(challenges: List[str]) -> List[str]:
    """Validate business challenges list."""
    valid_challenges = {
        'declining_sales', 'high_competition', 'cash_flow_issues', 
        'supplier_problems', 'marketing_customer_acquisition',
        'inventory_management', 'staff_operational_issues'
    }
    
    if not challenges:
        return []
    
    if not isinstance(challenges, list):
        raise ValidationError("Challenges must be a list")
    
    validated_challenges = []
    
    for challenge in challenges:
        if not isinstance(challenge, str):
            continue
        
        challenge_clean = challenge.lower().strip().replace(' ', '_').replace('/', '_')
        
        if challenge_clean in valid_challenges:
            validated_challenges.append(challenge_clean)
    
    return validated_challenges


def validate_goals_list(goals: List[str]) -> List[str]:
    """Validate business goals list."""
    valid_goals = {
        'increase_profits', 'expand_open_new_location', 'improve_cash_flow',
        'invest_surplus_money', 'get_bank_loan'
    }
    
    if not goals:
        return []
    
    if not isinstance(goals, list):
        raise ValidationError("Goals must be a list")
    
    validated_goals = []
    
    for goal in goals:
        if not isinstance(goal, str):
            continue
        
        goal_clean = goal.lower().strip().replace(' ', '_').replace('/', '_')
        
        if goal_clean in valid_goals:
            validated_goals.append(goal_clean)
    
    return validated_goals


def validate_notes(notes: str) -> str:
    """Validate and clean notes field."""
    if not notes:
        return ""
    
    if not isinstance(notes, str):
        return ""
    
    cleaned_notes = notes.strip()
    
    if len(cleaned_notes) > 1000:
        raise ValidationError("Notes must be less than 1000 characters")
    
    # Remove excessive whitespace
    cleaned_notes = re.sub(r'\s+', ' ', cleaned_notes)
    
    return cleaned_notes


def validate_email(email: str) -> str:
    """Validate email format."""
    if not email:
        raise ValidationError("Email is required")
    
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(email_pattern, email):
        raise ValidationError("Invalid email format")
    
    return email.lower().strip()


def validate_phone_number(phone: str) -> str:
    """Validate Pakistani phone number."""
    if not phone:
        raise ValidationError("Phone number is required")
    
    # Clean phone number
    phone_clean = re.sub(r'[^\d+]', '', phone)
    
    # Pakistani phone number patterns
    patterns = [
        r'^\+92[0-9]{10}$',  # +92xxxxxxxxxx
        r'^03[0-9]{9}$',     # 03xxxxxxxxx
        r'^92[0-9]{10}$',    # 92xxxxxxxxxx
    ]
    
    valid = any(re.match(pattern, phone_clean) for pattern in patterns)
    
    if not valid:
        raise ValidationError("Invalid Pakistani phone number format")
    
    return phone_clean


def validate_percentage_value(value: float, field_name: str) -> float:
    """Validate percentage value (0-100)."""
    try:
        float_value = float(value)
    except (ValueError, TypeError):
        raise ValidationError(f"{field_name} must be a valid number")
    
    if float_value < 0 or float_value > 100:
        raise ValidationError(f"{field_name} must be between 0 and 100")
    
    return float_value


def validate_currency_amount(amount: float, field_name: str, max_amount: float = None) -> float:
    """Validate currency amount."""
    try:
        float_amount = float(amount)
    except (ValueError, TypeError):
        raise ValidationError(f"{field_name} must be a valid number")
    
    if float_amount < 0:
        raise ValidationError(f"{field_name} cannot be negative")
    
    if max_amount and float_amount > max_amount:
        raise ValidationError(f"{field_name} cannot exceed {max_amount:,.0f}")
    
    return float_amount


def sanitize_string_input(text: str, max_length: int = None) -> str:
    """Sanitize string input for security."""
    if not text or not isinstance(text, str):
        return ""
    
    # Remove potential HTML/script tags
    text = re.sub(r'<[^>]*>', '', text)
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    if max_length and len(text) > max_length:
        text = text[:max_length]
    
    return text


def validate_date_string(date_str: str) -> datetime:
    """Validate date string format."""
    if not date_str:
        raise ValidationError("Date is required")
    
    try:
        # Try common date formats
        for date_format in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y']:
            try:
                return datetime.strptime(date_str, date_format)
            except ValueError:
                continue
        
        raise ValueError("No valid date format found")
        
    except ValueError:
        raise ValidationError("Invalid date format. Use YYYY-MM-DD or DD/MM/YYYY")


def validate_business_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate complete business data dictionary."""
    validated_data = {}
    
    # Required fields validation
    required_fields = [
        'business_name', 'sector', 'location_area', 'business_type',
        'monthly_revenue', 'monthly_expenses', 'current_cash',
        'employees_count', 'years_in_business', 'primary_customers'
    ]
    
    for field in required_fields:
        if field not in data:
            raise ValidationError(f"Required field '{field}' is missing")
    
    # Validate each field
    validated_data['business_name'] = validate_business_name(data['business_name'])
    validated_data['sector'] = validate_sector(data['sector'])
    validated_data['location_area'] = validate_karachi_location(data['location_area'])
    validated_data['business_type'] = validate_business_type(data['business_type'])
    validated_data['monthly_revenue'] = validate_monthly_revenue(data['monthly_revenue'])
    validated_data['monthly_expenses'] = validate_monthly_expenses(data['monthly_expenses'])
    validated_data['current_cash'] = validate_current_cash(data['current_cash'])
    validated_data['employees_count'] = validate_employees_count(data['employees_count'])
    validated_data['years_in_business'] = validate_years_in_business(data['years_in_business'])
    validated_data['primary_customers'] = validate_primary_customers(data['primary_customers'])
    
    # Optional fields
    validated_data['main_challenges'] = validate_challenges_list(data.get('main_challenges', []))
    validated_data['business_goals'] = validate_goals_list(data.get('business_goals', []))
    validated_data['notes'] = validate_notes(data.get('notes', ''))
    
    # Business logic validations
    current_revenue = validated_data['monthly_revenue'][-1]
    monthly_expenses = validated_data['monthly_expenses']
    
    # Warn if expenses > revenue (but don't fail validation)
    if monthly_expenses > current_revenue * 1.5:
        # This is a warning, not an error
        pass
    
    # Warn if very high cash relative to revenue
    if validated_data['current_cash'] > current_revenue * 20:
        # This is unusual but not invalid
        pass
    
    return validated_data


def validate_api_input(data: Dict[str, Any], required_fields: List[str] = None) -> Dict[str, Any]:
    """Validate API input data."""
    if not isinstance(data, dict):
        raise ValidationError("Input must be a valid JSON object")
    
    if required_fields:
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")
    
    return data