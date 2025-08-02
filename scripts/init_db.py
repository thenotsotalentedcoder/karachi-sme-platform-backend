"""Initialize database with tables and seed data."""

import sys
import os
from pathlib import Path

# Add the parent directory to the path so we can import app modules
sys.path.append(str(Path(__file__).parent.parent))

from app.database import init_db, create_tables
from app.config import settings

def main():
    """Initialize the database."""
    print(f"Initializing database: {settings.DATABASE_URL}")
    
    try:
        # Initialize database
        init_db()
        print("✅ Database initialized successfully!")
        
        # Print table creation confirmation
        print("📊 Created tables:")
        print("  - businesses")
        print("  - business_analysis_history")
        print("  - analysis_results")
        print("  - insights")
        print("  - recommendations")
        print("  - karachi_market_data")
        print("  - sector_performance")
        print("  - economic_indicators")
        
        print(f"\n🚀 Database ready at: {settings.DATABASE_URL}")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()