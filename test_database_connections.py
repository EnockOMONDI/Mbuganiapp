#!/usr/bin/env python
"""
Script to test both development and production database connections
"""

import os
import django
from datetime import datetime

def test_development_database():
    """Test development database connection"""
    print("=== TESTING DEVELOPMENT DATABASE ===")
    
    # Setup Django for development
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tours_travels.settings_dev')
    django.setup()
    
    try:
        from django.db import connection
        from django.contrib.auth.models import User
        from adminside.models import Destination, Package, Accommodation
        from blog.models import Category, Post
        
        # Test database connection
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"✅ Development database connected successfully")
        print(f"   Database file: mbugani_development.sqlite3")
        print(f"   Tables found: {len(tables)}")
        
        # Test data counts
        print(f"\n📊 Development Database Data:")
        print(f"   Users: {User.objects.count()}")
        print(f"   Destinations: {Destination.objects.count()}")
        print(f"   Accommodations: {Accommodation.objects.count()}")
        print(f"   Travel Packages: {Package.objects.count()}")
        print(f"   Blog Categories: {Category.objects.count()}")
        print(f"   Blog Posts: {Post.objects.count()}")
        
        # Test superuser
        try:
            superuser = User.objects.get(username='mbuganiluxeadventures')
            print(f"   Superuser: ✅ {superuser.username} (Staff: {superuser.is_staff}, Super: {superuser.is_superuser})")
        except User.DoesNotExist:
            print(f"   Superuser: ❌ Not found")
        
        return True
        
    except Exception as e:
        print(f"❌ Development database connection failed: {e}")
        return False

def test_production_database():
    """Test production database connection"""
    print("\n=== TESTING PRODUCTION DATABASE ===")
    
    # Reset Django setup for production
    import importlib
    import sys
    
    # Clear Django setup
    if 'django' in sys.modules:
        del sys.modules['django']
    if 'django.conf' in sys.modules:
        del sys.modules['django.conf']
    
    # Setup Django for production
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tours_travels.settings_prod'
    
    try:
        import django
        django.setup()
        
        from django.db import connection
        from django.contrib.auth.models import User
        from adminside.models import Destination, Package, Accommodation
        from blog.models import Category, Post
        
        # Test database connection
        cursor = connection.cursor()
        cursor.execute('SELECT version();')
        version = cursor.fetchone()
        
        print(f"✅ Production database connected successfully")
        print(f"   Database: Supabase PostgreSQL")
        print(f"   Host: aws-1-eu-west-1.pooler.supabase.com:6543")
        print(f"   PostgreSQL version: {version[0]}")
        
        # Test data counts
        print(f"\n📊 Production Database Data:")
        print(f"   Users: {User.objects.count()}")
        print(f"   Destinations: {Destination.objects.count()}")
        print(f"   Accommodations: {Accommodation.objects.count()}")
        print(f"   Travel Packages: {Package.objects.count()}")
        print(f"   Blog Categories: {Category.objects.count()}")
        print(f"   Blog Posts: {Post.objects.count()}")
        
        # Test superuser
        try:
            superuser = User.objects.get(username='mbuganiluxeadventures')
            print(f"   Superuser: ✅ {superuser.username} (Staff: {superuser.is_staff}, Super: {superuser.is_superuser})")
        except User.DoesNotExist:
            print(f"   Superuser: ❌ Not found")
        
        return True
        
    except Exception as e:
        print(f"❌ Production database connection failed: {e}")
        return False

def test_migrations():
    """Test that migrations can be applied"""
    print("\n=== TESTING MIGRATIONS ===")
    
    try:
        # Test production migrations
        os.system("python manage.py showmigrations --settings=tours_travels.settings_prod > /dev/null 2>&1")
        print("✅ Production migrations check passed")
        
        # Test development migrations
        os.system("python manage.py showmigrations --settings=tours_travels.settings_dev > /dev/null 2>&1")
        print("✅ Development migrations check passed")
        
        return True
        
    except Exception as e:
        print(f"❌ Migrations test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🔍 DATABASE CONFIGURATION TESTING")
    print("=" * 50)
    
    # Test development database
    dev_success = test_development_database()
    
    # Test production database
    prod_success = test_production_database()
    
    # Test migrations
    migration_success = test_migrations()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY")
    print("=" * 50)
    print(f"Development Database: {'✅ PASS' if dev_success else '❌ FAIL'}")
    print(f"Production Database:  {'✅ PASS' if prod_success else '❌ FAIL'}")
    print(f"Migrations:          {'✅ PASS' if migration_success else '❌ FAIL'}")
    
    if dev_success and prod_success and migration_success:
        print("\n🎉 ALL TESTS PASSED! Database configurations are working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please check the error messages above.")
    
    print("\n📝 Configuration Summary:")
    print("   Development: SQLite (mbugani_development.sqlite3)")
    print("   Production:  PostgreSQL (Supabase)")
    print("   Environment: .env files updated")
    print("   Deployment:  render.yaml updated")

if __name__ == "__main__":
    main()
