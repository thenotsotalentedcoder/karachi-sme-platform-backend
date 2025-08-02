"""Seed database with sample data for testing and demonstration."""

import sys
import os
from pathlib import Path

# Add the parent directory to the path so we can import app modules
sys.path.append(str(Path(__file__).parent.parent))

from app.database import SessionLocal, create_tables
from app.models.business import Business
from app.models.market import KarachiMarketData, SectorPerformance, EconomicIndicators
from datetime import datetime

def create_sample_businesses():
    """Create sample businesses for testing."""
    
    sample_businesses = [
        {
            "business_name": "Ahmed's Mobile Center",
            "sector": "electronics",
            "location_area": "saddar",
            "business_type": "retail_shop",
            "monthly_revenue": [750000, 680000, 620000, 580000, 650000, 720000],
            "monthly_expenses": 450000,
            "current_cash": 850000,
            "employees_count": 3,
            "years_in_business": 5,
            "primary_customers": "local_walk_ins",
            "main_challenges": ["declining_sales", "high_competition"],
            "business_goals": ["increase_profits", "improve_cash_flow"],
            "notes": "Family electronics business facing increased competition"
        },
        {
            "business_name": "Fatima's Kitchen",
            "sector": "food",
            "location_area": "clifton",
            "business_type": "retail_shop",
            "monthly_revenue": [400000, 420000, 450000, 480000, 510000, 540000],
            "monthly_expenses": 320000,
            "current_cash": 650000,
            "employees_count": 6,
            "years_in_business": 3,
            "primary_customers": "regular_customers",
            "main_challenges": ["staff_operational_issues"],
            "business_goals": ["expand_open_new_location", "increase_profits"],
            "notes": "Growing restaurant looking to expand"
        },
        {
            "business_name": "Hassan Textile Mills",
            "sector": "textile",
            "location_area": "korangi",
            "business_type": "manufacturing",
            "monthly_revenue": [1200000, 1150000, 1100000, 1000000, 950000, 980000],
            "monthly_expenses": 750000,
            "current_cash": 1200000,
            "employees_count": 25,
            "years_in_business": 12,
            "primary_customers": "wholesale_buyers",
            "main_challenges": ["supplier_problems", "cash_flow_issues"],
            "business_goals": ["improve_cash_flow", "invest_surplus_money"],
            "notes": "Established textile manufacturer facing market challenges"
        },
        {
            "business_name": "Speed Auto Parts",
            "sector": "auto",
            "location_area": "korangi",
            "business_type": "retail_shop",
            "monthly_revenue": [600000, 650000, 580000, 620000, 640000, 680000],
            "monthly_expenses": 420000,
            "current_cash": 350000,
            "employees_count": 4,
            "years_in_business": 7,
            "primary_customers": "regular_customers",
            "main_challenges": ["inventory_management", "supplier_problems"],
            "business_goals": ["increase_profits", "improve_cash_flow"],
            "notes": "Auto parts dealer serving motorcycle market"
        },
        {
            "business_name": "Zara General Store",
            "sector": "retail",
            "location_area": "gulshan",
            "business_type": "retail_shop",
            "monthly_revenue": [380000, 400000, 420000, 410000, 450000, 470000],
            "monthly_expenses": 280000,
            "current_cash": 420000,
            "employees_count": 2,
            "years_in_business": 8,
            "primary_customers": "local_walk_ins",
            "main_challenges": ["high_competition", "marketing_customer_acquisition"],
            "business_goals": ["increase_profits", "expand_open_new_location"],
            "notes": "Neighborhood store with loyal customer base"
        }
    ]
    
    return sample_businesses


def create_sample_market_data():
    """Create sample market data."""
    
    market_data = [
        {
            "sector": "electronics",
            "location_area": "saddar",
            "average_revenue": 750000,
            "revenue_growth_rate": 0.18,
            "competition_density": "very_high",
            "market_size": 15000000,
            "rent_cost_per_sqft": 800,
            "foot_traffic_level": "very_high",
            "customer_demographics": {
                "age_groups": {"18-30": 40, "30-45": 35, "45-60": 25},
                "income_levels": {"low": 30, "medium": 50, "high": 20}
            },
            "accessibility_score": 9.0,
            "local_purchasing_power": 1.0,
            "seasonal_factors": {"peak_months": [11, 12, 1], "low_months": [6, 7, 8]},
            "key_insights": ["Highest foot traffic in Karachi", "Price-conscious customers", "Intense competition"]
        },
        {
            "sector": "food",
            "location_area": "clifton",
            "average_revenue": 600000,
            "revenue_growth_rate": 0.12,
            "competition_density": "high",
            "market_size": 8000000,
            "rent_cost_per_sqft": 2000,
            "foot_traffic_level": "high",
            "customer_demographics": {
                "age_groups": {"25-35": 30, "35-50": 45, "50-65": 25},
                "income_levels": {"low": 10, "medium": 30, "high": 60}
            },
            "accessibility_score": 8.5,
            "local_purchasing_power": 1.5,
            "seasonal_factors": {"peak_months": [9, 12], "low_months": [6, 7]},
            "key_insights": ["Affluent customer base", "Premium pricing accepted", "Good infrastructure"]
        }
    ]
    
    return market_data


def create_sample_economic_indicators():
    """Create sample economic indicators."""
    
    return {
        "pkr_usd_rate": 278.50,
        "inflation_rate": 0.29,
        "interest_rate": 0.22,
        "gdp_growth_rate": 0.024,
        "unemployment_rate": 0.063,
        "consumer_confidence": 65.0,
        "ease_of_business_index": 72.0,
        "tax_policy_impact": 0.05,
        "regulatory_environment": "stable",
        "supply_chain_status": "constrained",
        "energy_cost_index": 1.85
    }


def seed_database():
    """Seed the database with sample data."""
    
    print("🌱 Starting database seeding...")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Create tables first
        create_tables()
        print("📊 Database tables ready")
        
        # Check if data already exists
        existing_businesses = db.query(Business).count()
        if existing_businesses > 0:
            print(f"⚠️  Database already contains {existing_businesses} businesses")
            response = input("Do you want to continue and add more sample data? (y/n): ")
            if response.lower() != 'y':
                print("❌ Seeding cancelled")
                return
        
        # Seed businesses
        print("👥 Creating sample businesses...")
        sample_businesses = create_sample_businesses()
        
        for business_data in sample_businesses:
            business = Business(**business_data)
            db.add(business)
            print(f"   ✅ Created: {business_data['business_name']}")
        
        # Seed market data
        print("📈 Creating sample market data...")
        market_data_list = create_sample_market_data()
        
        for market_data in market_data_list:
            market_record = KarachiMarketData(**market_data)
            db.add(market_record)
            print(f"   ✅ Created market data: {market_data['sector']} in {market_data['location_area']}")
        
        # Seed economic indicators
        print("💰 Creating economic indicators...")
        economic_data = create_sample_economic_indicators()
        economic_record = EconomicIndicators(
            date=datetime.now(),
            **economic_data
        )
        db.add(economic_record)
        print("   ✅ Created economic indicators")
        
        # Commit all changes
        db.commit()
        
        # Summary
        total_businesses = db.query(Business).count()
        total_market_data = db.query(KarachiMarketData).count()
        total_economic_data = db.query(EconomicIndicators).count()
        
        print("\n🎉 Database seeding completed successfully!")
        print(f"📊 Summary:")
        print(f"   • Businesses: {total_businesses}")
        print(f"   • Market data records: {total_market_data}")
        print(f"   • Economic indicators: {total_economic_data}")
        
        print(f"\n🚀 You can now start the API server with:")
        print(f"   cd backend")
        print(f"   uvicorn app.main:app --reload")
        print(f"\n📖 API documentation will be available at:")
        print(f"   http://localhost:8000/api/v1/docs")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
        raise
        
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()