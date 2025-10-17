#!/usr/bin/env python
"""
Railway Cache Table Setup Script

This script creates the Django cache table in the production database.
Run this once after deploying to Railway to fix the cache_table errors.
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Setup Django with production settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tours_travels.settings_prod')
django.setup()

from django.core.management import execute_from_command_line

def main():
    """Create cache table in production database"""
    print("🚂 Railway Cache Table Setup")
    print("=" * 40)
    print()
    
    try:
        print("📋 Creating cache table...")
        execute_from_command_line(['manage.py', 'createcachetable'])
        print("✅ Cache table created successfully!")
        print()
        print("🎉 Django-Q worker should now work without cache errors")
        
    except Exception as e:
        print(f"❌ Error creating cache table: {e}")
        print("💡 This might be normal if the table already exists")
        
    print()
    print("📝 Next steps:")
    print("1. Test quote request submission on your website")
    print("2. Check Railway logs for successful email processing")
    print("3. Verify emails are delivered")

if __name__ == "__main__":
    main()
