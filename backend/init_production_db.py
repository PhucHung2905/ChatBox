#!/usr/bin/env python3
"""
Production Database Initialization Script
Run this after deploying to create database schema
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from database import User, ChatHistory, init_db, create_admin_if_not_exists

def init_production_db():
    """Initialize database for production"""
    
    print("🔄 Initializing Production Database...")
    
    with app.app_context():
        try:
            print("✓ Creating database tables...")
            init_db()
            
            print("✓ Creating default admin user...")
            create_admin_if_not_exists()
            
            # Verify database connection
            print("✓ Verifying database connection...")
            user_count = User.query.count()
            print(f"✓ Found {user_count} users in database")
            
            print("\n✅ Database initialization completed successfully!")
            print("\n📋 Next steps:")
            print("1. Login with admin account")
            print("2. Upload knowledge base documents")
            print("3. Configure Gemini API key")
            print("4. Initialize vector database")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error initializing database: {str(e)}")
            print(f"Details: {e}")
            return False

if __name__ == '__main__':
    success = init_production_db()
    sys.exit(0 if success else 1)
