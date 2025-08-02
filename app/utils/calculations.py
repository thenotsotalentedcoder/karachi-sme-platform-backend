"""Utility functions for business calculations and data processing."""

import statistics
import math
from typing import List, Dict, Any, Optional, Tuple


def calculate_growth_rate(values: List[float], periods: int = None) -> float:
    """Calculate growth rate between periods."""
    if not values or len(values) < 2:
        return 0.0
    
    if periods is None:
        periods = len(values) - 1
    
    start_value = values[0] if values[0] > 0 else 0.01  # Avoid division by zero
    end_value = values[-1]
    
    if start_value <= 0:
        return 0.0
    
    # Compound annual growth rate formula: (End/Start)^(1/periods) - 1
    growth_rate = (end_value / start_value) ** (1 / periods) - 1
    return growth_rate


def calculate_moving_average(values: List[float], window: int = 3) -> List[float]:
    """Calculate moving average with specified window."""
    if len(values) < window:
        return values
    
    moving_averages = []
    for i in range(len(values) - window + 1):
        avg = sum(values[i:i + window]) / window
        moving_averages.append(avg)
    
    return moving_averages


def calculate_volatility(values: List[float]) -> float:
    """Calculate volatility (coefficient of variation)."""
    if not values or len(values) < 2:
        return 0.0
    
    mean_value = statistics.mean(values)
    if mean_value == 0:
        return 0.0
    
    std_deviation = statistics.stdev(values)
    volatility = std_deviation / mean_value
    
    return volatility


def calculate_trend_direction(values: List[float]) -> str:
    """Determine trend direction using linear regression."""
    if not values or len(values) < 3:
        return "insufficient_data"
    
    n = len(values)
    x_values = list(range(n))
    
    # Calculate linear regression slope
    x_mean = statistics.mean(x_values)
    y_mean = statistics.mean(values)
    
    numerator = sum((x_values[i] - x_mean) * (values[i] - y_mean) for i in range(n))
    denominator = sum((x_values[i] - x_mean) ** 2 for i in range(n))
    
    if denominator == 0:
        return "stable"
    
    slope = numerator / denominator
    
    # Determine trend based on slope
    if slope > 0.05:
        return "increasing"
    elif slope < -0.05:
        return "declining"
    else:
        return "stable"


def calculate_profit_margin(revenue: float, expenses: float) -> float:
    """Calculate profit margin percentage."""
    if revenue <= 0:
        return 0.0
    
    profit = revenue - expenses
    margin = profit / revenue
    
    return max(0.0, margin)  # Don't return negative margins


def calculate_cash_runway(current_cash: float, monthly_burn: float) -> float:
    """Calculate how many months of cash runway remaining."""
    if monthly_burn <= 0:
        return float('inf')
    
    runway = current_cash / monthly_burn
    return max(0.0, runway)


def calculate_revenue_per_customer(total_revenue: float, customer_count: int) -> float:
    """Calculate average revenue per customer."""
    if customer_count <= 0:
        return 0.0
    
    return total_revenue / customer_count


def calculate_customer_lifetime_value(avg_purchase: float, purchase_frequency: float, 
                                    retention_months: float) -> float:
    """Calculate customer lifetime value."""
    if any(val <= 0 for val in [avg_purchase, purchase_frequency, retention_months]):
        return 0.0
    
    monthly_value = avg_purchase * purchase_frequency
    lifetime_value = monthly_value * retention_months
    
    return lifetime_value


def calculate_break_even_point(fixed_costs: float, variable_cost_per_unit: float,
                              price_per_unit: float) -> float:
    """Calculate break-even point in units."""
    if price_per_unit <= variable_cost_per_unit:
        return float('inf')  # Never breaks even
    
    contribution_margin = price_per_unit - variable_cost_per_unit
    break_even_units = fixed_costs / contribution_margin
    
    return break_even_units


def calculate_return_on_investment(initial_investment: float, final_value: float,
                                 time_period_years: float) -> float:
    """Calculate annualized return on investment."""
    if initial_investment <= 0 or time_period_years <= 0:
        return 0.0
    
    total_return = (final_value - initial_investment) / initial_investment
    
    if time_period_years == 1:
        return total_return
    
    # Annualize the return
    annualized_return = (1 + total_return) ** (1 / time_period_years) - 1
    
    return annualized_return


def normalize_score(value: float, min_value: float, max_value: float, 
                   target_min: float = 0, target_max: float = 100) -> float:
    """Normalize a value to a target range."""
    if max_value == min_value:
        return target_min
    
    # Clamp value to input range
    value = max(min_value, min(max_value, value))
    
    # Normalize to 0-1 range
    normalized = (value - min_value) / (max_value - min_value)
    
    # Scale to target range
    scaled = normalized * (target_max - target_min) + target_min
    
    return scaled


def calculate_percentile_rank(value: float, dataset: List[float]) -> float:
    """Calculate percentile rank of value in dataset."""
    if not dataset:
        return 50.0  # Default to median
    
    sorted_data = sorted(dataset)
    n = len(sorted_data)
    
    # Count values less than or equal to target value
    count_below = sum(1 for x in sorted_data if x < value)
    count_equal = sum(1 for x in sorted_data if x == value)
    
    # Calculate percentile rank
    percentile = (count_below + 0.5 * count_equal) / n * 100
    
    return percentile


def calculate_correlation(x_values: List[float], y_values: List[float]) -> float:
    """Calculate correlation coefficient between two datasets."""
    if len(x_values) != len(y_values) or len(x_values) < 2:
        return 0.0
    
    try:
        correlation = statistics.correlation(x_values, y_values)
        return correlation
    except statistics.StatisticsError:
        return 0.0


def calculate_seasonal_index(values: List[float], season_length: int = 12) -> List[float]:
    """Calculate seasonal indices for time series data."""
    if len(values) < season_length * 2:
        return [1.0] * season_length
    
    # Calculate average for each seasonal period
    seasonal_averages = []
    overall_average = statistics.mean(values)
    
    for season in range(season_length):
        season_values = [values[i] for i in range(season, len(values), season_length)]
        if season_values:
            season_avg = statistics.mean(season_values)
            seasonal_index = season_avg / overall_average if overall_average > 0 else 1.0
            seasonal_averages.append(seasonal_index)
        else:
            seasonal_averages.append(1.0)
    
    return seasonal_averages


def calculate_compound_growth(initial_value: float, growth_rate: float, periods: int) -> float:
    """Calculate compound growth over multiple periods."""
    if periods <= 0:
        return initial_value
    
    final_value = initial_value * ((1 + growth_rate) ** periods)
    return final_value


def calculate_simple_forecast(historical_values: List[float], periods_ahead: int,
                            growth_rate: Optional[float] = None) -> List[float]:
    """Generate simple forecast based on historical data."""
    if not historical_values:
        return []
    
    if growth_rate is None:
        growth_rate = calculate_growth_rate(historical_values)
    
    last_value = historical_values[-1]
    forecast = []
    
    for i in range(1, periods_ahead + 1):
        forecasted_value = last_value * ((1 + growth_rate) ** i)
        forecast.append(forecasted_value)
    
    return forecast


def calculate_z_score(value: float, dataset: List[float]) -> float:
    """Calculate z-score (standard score) of value in dataset."""
    if not dataset or len(dataset) < 2:
        return 0.0
    
    mean_value = statistics.mean(dataset)
    std_dev = statistics.stdev(dataset)
    
    if std_dev == 0:
        return 0.0
    
    z_score = (value - mean_value) / std_dev
    return z_score


def calculate_confidence_interval(dataset: List[float], confidence_level: float = 0.95) -> Tuple[float, float]:
    """Calculate confidence interval for dataset."""
    if not dataset or len(dataset) < 2:
        return (0.0, 0.0)
    
    mean_value = statistics.mean(dataset)
    std_error = statistics.stdev(dataset) / math.sqrt(len(dataset))
    
    # Use t-distribution critical value (approximation for large samples)
    # For 95% confidence, t ≈ 1.96
    t_critical = 1.96 if confidence_level == 0.95 else 2.58  # 99% confidence
    
    margin_of_error = t_critical * std_error
    
    lower_bound = mean_value - margin_of_error
    upper_bound = mean_value + margin_of_error
    
    return (lower_bound, upper_bound)


def smooth_values(values: List[float], smoothing_factor: float = 0.3) -> List[float]:
    """Apply exponential smoothing to values."""
    if not values:
        return []
    
    smoothed = [values[0]]  # First value unchanged
    
    for i in range(1, len(values)):
        smoothed_value = (smoothing_factor * values[i] + 
                         (1 - smoothing_factor) * smoothed[i-1])
        smoothed.append(smoothed_value)
    
    return smoothed


def calculate_efficiency_ratio(output: float, input: float) -> float:
    """Calculate efficiency ratio (output/input)."""
    if input <= 0:
        return 0.0
    
    return output / input


def calculate_market_share(business_revenue: float, total_market_size: float) -> float:
    """Calculate market share percentage."""
    if total_market_size <= 0:
        return 0.0
    
    market_share = (business_revenue / total_market_size) * 100
    return min(100.0, market_share)  # Cap at 100%


def calculate_inventory_turnover(cost_of_goods_sold: float, average_inventory: float) -> float:
    """Calculate inventory turnover ratio."""
    if average_inventory <= 0:
        return 0.0
    
    turnover = cost_of_goods_sold / average_inventory
    return turnover


def calculate_working_capital(current_assets: float, current_liabilities: float) -> float:
    """Calculate working capital."""
    return current_assets - current_liabilities


def calculate_debt_to_equity(total_debt: float, total_equity: float) -> float:
    """Calculate debt-to-equity ratio."""
    if total_equity <= 0:
        return float('inf') if total_debt > 0 else 0.0
    
    return total_debt / total_equity


def format_currency(amount: float, currency: str = "PKR") -> str:
    """Format amount as currency string."""
    if currency == "PKR":
        if amount >= 10000000:  # 1 crore
            return f"Rs. {amount/10000000:.1f} crore"
        elif amount >= 100000:  # 1 lakh
            return f"Rs. {amount/100000:.1f} lakh"
        else:
            return f"Rs. {amount:,.0f}"
    else:
        return f"{currency} {amount:,.2f}"


def format_percentage(value: float, decimal_places: int = 1) -> str:
    """Format value as percentage string."""
    return f"{value * 100:.{decimal_places}f}%"


def format_growth_rate(growth_rate: float) -> str:
    """Format growth rate with appropriate sign and description."""
    percentage = growth_rate * 100
    
    if percentage > 0:
        return f"+{percentage:.1f}% growth"
    elif percentage < 0:
        return f"{percentage:.1f}% decline"
    else:
        return "0% (stable)"


def validate_positive_number(value: Any) -> float:
    """Validate and convert value to positive number."""
    try:
        num_value = float(value)
        return max(0.0, num_value)
    except (ValueError, TypeError):
        return 0.0


def validate_percentage(value: Any) -> float:
    """Validate and convert value to percentage (0-1 range)."""
    try:
        num_value = float(value)
        return max(0.0, min(1.0, num_value))
    except (ValueError, TypeError):
        return 0.0


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide two numbers, returning default if denominator is zero."""
    if denominator == 0:
        return default
    
    return numerator / denominator


def clamp_value(value: float, min_value: float, max_value: float) -> float:
    """Clamp value between min and max bounds."""
    return max(min_value, min(max_value, value))


def interpolate_missing_values(values: List[Optional[float]]) -> List[float]:
    """Interpolate missing values in a list."""
    if not values:
        return []
    
    result = []
    last_valid = None
    
    for i, value in enumerate(values):
        if value is not None:
            result.append(value)
            last_valid = value
        else:
            # Find next valid value for interpolation
            next_valid = None
            next_index = None
            
            for j in range(i + 1, len(values)):
                if values[j] is not None:
                    next_valid = values[j]
                    next_index = j
                    break
            
            # Interpolate or use fallback
            if last_valid is not None and next_valid is not None:
                # Linear interpolation
                distance = next_index - (i - 1)
                progress = 1 / distance
                interpolated = last_valid + (next_valid - last_valid) * progress
                result.append(interpolated)
            elif last_valid is not None:
                # Use last valid value
                result.append(last_valid)
            elif next_valid is not None:
                # Use next valid value
                result.append(next_valid)
            else:
                # No valid values, use 0
                result.append(0.0)
    
    return result