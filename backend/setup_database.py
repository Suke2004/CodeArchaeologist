#!/usr/bin/env python3
"""
Database setup script for CodeArchaeologist.
Run this script to initialize the database and verify the connection.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables FIRST, before any other imports
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from database import init_db, check_db_connection, engine
from models import Base
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Initialize database and verify connection."""
    
    print("=" * 60)
    print("CodeArchaeologist Database Setup")
    print("=" * 60)
    print()
    
    # Check if DATABASE_URL is set
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ ERROR: DATABASE_URL environment variable is not set!")
        print()
        print("Please add your Neon Postgres connection string to backend/.env:")
        print()
        print("DATABASE_URL=postgresql://user:password@your-neon-host.neon.tech/codearchaeologist?sslmode=require")
        print()
        return 1
    
    # Mask password in URL for display
    display_url = database_url
    if "@" in display_url:
        parts = display_url.split("@")
        user_pass = parts[0].split("//")[1]
        if ":" in user_pass:
            user = user_pass.split(":")[0]
            display_url = display_url.replace(user_pass, f"{user}:****")
    
    print(f"📊 Database URL: {display_url}")
    print()
    
    # Test connection
    print("🔌 Testing database connection...")
    if not check_db_connection():
        print("❌ Failed to connect to database!")
        print()
        print("Please check:")
        print("  1. Your DATABASE_URL is correct")
        print("  2. Your Neon database is running")
        print("  3. Your IP is allowed in Neon's firewall settings")
        print("  4. You have internet connectivity")
        return 1
    
    print("✅ Database connection successful!")
    print()
    
    # Create tables
    print("📋 Creating database tables...")
    try:
        init_db()
        print("✅ Database tables created successfully!")
        print()
        
        # List created tables
        print("📊 Created tables:")
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        for table in tables:
            print(f"  - {table}")
        print()
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return 1
    
    print("=" * 60)
    print("✅ Database setup complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("  1. Install dependencies: pip install -r requirements.txt")
    print("  2. Start the server: uvicorn main:app --reload")
    print("  3. Visit: http://localhost:8000/docs")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
