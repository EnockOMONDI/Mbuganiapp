#!/usr/bin/env python3
"""
Production Diagnostic Script for Mbugani Luxe Adventures
Comprehensive troubleshooting for production deployment issues
"""

import os
import sys
import django
from pathlib import Path

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tours_travels.settings')
django.setup()

from django.conf import settings
from django.db import connection
from adminside.models import Package, Destination, Itinerary

def check_environment():
    """Check environment configuration"""
    print("🔍 ENVIRONMENT DIAGNOSTICS")
    print("=" * 50)

    # Check Django environment
    django_env = os.environ.get('DJANGO_ENV', 'development')
    print(f"🌍 DJANGO_ENV: {django_env}")

    # Check DEBUG status
    debug_status = "❌ DEBUG=True (PROBLEM)" if settings.DEBUG else "✅ DEBUG=False (GOOD)"
    print(f"🐛 DEBUG: {debug_status}")

    # Check database configuration
    db_config = settings.DATABASES['default']
    db_engine = db_config.get('ENGINE', '')
    if 'postgresql' in db_engine:
        print("🗄️  Database: PostgreSQL (Production)")
        print(f"📍 Host: {db_config.get('HOST', 'Unknown')}")
        print(f"🔌 Port: {db_config.get('PORT', 'Unknown')}")
        print(f"📊 Database: {db_config.get('NAME', 'Unknown')}")
    elif 'sqlite' in db_engine:
        print("🗄️  Database: SQLite (Development - PROBLEM)")
        print(f"📁 Path: {db_config.get('NAME', 'Unknown')}")
    else:
        print(f"🗄️  Database: {db_engine} (Unknown)")

    # Check allowed hosts
    allowed_hosts = settings.ALLOWED_HOSTS
    print(f"🌐 ALLOWED_HOSTS: {allowed_hosts}")

    # Check site URL
    site_url = getattr(settings, 'SITE_URL', 'Not set')
    print(f"🔗 SITE_URL: {site_url}")

    print()

def check_database_connection():
    """Check database connectivity"""
    print("🔌 DATABASE CONNECTION TEST")
    print("=" * 30)

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print("✅ Database connection: SUCCESS")
        print(f"📊 Test query result: {result}")

        # Check if tables exist
        cursor.execute("""
            SELECT COUNT(*) FROM information_schema.tables
            WHERE table_schema = 'public'
        """)
        table_count = cursor.fetchone()[0]
        print(f"📋 Tables in database: {table_count}")

    except Exception as e:
        print(f"❌ Database connection: FAILED - {e}")
        print("🔧 Possible issues:")
        print("   - Wrong database credentials")
        print("   - Database server not running")
        print("   - Network connectivity issues")
        print("   - SSL configuration problems")

    print()

def check_data_integrity():
    """Check data integrity and counts"""
    print("📊 DATA INTEGRITY CHECK")
    print("=" * 25)

    try:
        # Check package counts
        total_packages = Package.objects.count()
        published_packages = Package.objects.filter(status=Package.PUBLISHED).count()

        print(f"📦 Total Packages: {total_packages}")
        print(f"✅ Published Packages: {published_packages}")

        if total_packages == 0:
            print("❌ PROBLEM: No packages found in database")
        elif total_packages < 10:
            print(f"⚠️  WARNING: Only {total_packages} packages (expected 10+)")
        else:
            print("✅ Package count looks good")

        # Check destinations
        destination_count = Destination.objects.count()
        print(f"🗺️  Destinations: {destination_count}")

        # Check itineraries
        itinerary_count = Itinerary.objects.count()
        packages_with_itineraries = Package.objects.filter(itinerary__isnull=False).distinct().count()
        print(f"🗺️  Itineraries: {itinerary_count}")
        print(f"📍 Packages with itineraries: {packages_with_itineraries}")

        if packages_with_itineraries == 0:
            print("❌ PROBLEM: No packages have itineraries")
        elif packages_with_itineraries < 2:
            print(f"⚠️  WARNING: Only {packages_with_itineraries} packages have itineraries (expected 2+)")

        # List packages if any exist
        if total_packages > 0:
            print("\n📋 Package List:")
            for package in Package.objects.all()[:10]:  # Show first 10
                status_icon = "✅" if package.status == Package.PUBLISHED else "⏸️"
                print(f"  {status_icon} {package.name}")

    except Exception as e:
        print(f"❌ Data integrity check: FAILED - {e}")

    print()

def check_sync_data_file():
    """Check the sync data file"""
    print("📁 SYNC DATA FILE CHECK")
    print("=" * 25)

    dump_file = 'production_sync_data.json'

    if os.path.exists(dump_file):
        file_size = os.path.getsize(dump_file)
        print(f"✅ Sync file exists: {dump_file}")
        print(f"📏 File size: {file_size} bytes")

        try:
            with open(dump_file, 'r') as f:
                data = f.read(500)  # Read first 500 chars
                if data.startswith('[') and 'model' in data:
                    print("✅ File format: Valid JSON")
                else:
                    print("❌ File format: Invalid JSON structure")

            # Count packages in dump file
            with open(dump_file, 'r') as f:
                content = f.read()
                package_count = content.count('"model": "adminside.package"')
                print(f"📦 Packages in dump file: {package_count}")

        except Exception as e:
            print(f"❌ File read error: {e}")
    else:
        print(f"❌ Sync file missing: {dump_file}")
        print("🔧 Run: python manage.py sync_production_data --dump-only")

    print()

def provide_solutions():
    """Provide comprehensive solutions"""
    print("🔧 PRODUCTION DEPLOYMENT SOLUTIONS")
    print("=" * 40)

    django_env = os.environ.get('DJANGO_ENV', 'development')
    debug_status = settings.DEBUG
    db_engine = settings.DATABASES['default'].get('ENGINE', '')

    issues_found = []

    if django_env != 'production':
        issues_found.append("DJANGO_ENV not set to 'production'")
        print("1. 🚨 DJANGO_ENV Configuration")
        print("   Current: development")
        print("   Required: production")
        print("   Solution: export DJANGO_ENV=production")
        print()

    if debug_status:
        issues_found.append("DEBUG=True (development server message)")
        print("2. 🚨 DEBUG Mode Active")
        print("   Current: DEBUG=True")
        print("   Required: DEBUG=False")
        print("   Solution: Ensure DJANGO_ENV=production is set")
        print()

    if 'sqlite' in db_engine:
        issues_found.append("Using SQLite instead of PostgreSQL")
        print("3. 🚨 Database Configuration")
        print("   Current: SQLite (Development)")
        print("   Required: PostgreSQL (Production)")
        print("   Solution: Check DATABASE_URL environment variable")
        print()

    package_count = Package.objects.count()
    if package_count < 10:
        issues_found.append(f"Low package count ({package_count} vs expected 10+)")
        print("4. 🚨 Database Synchronization")
        print(f"   Current packages: {package_count}")
        print("   Expected packages: 10+")
        print("   Solution: Run data synchronization")
        print()

    if not issues_found:
        print("✅ No critical issues detected!")
        print("🎉 Production environment looks properly configured")
    else:
        print(f"❌ Found {len(issues_found)} configuration issues:")
        for i, issue in enumerate(issues_found, 1):
            print(f"   {i}. {issue}")

    print("\n📋 Complete Production Deployment Checklist:")
    print("1. Set DJANGO_ENV=production environment variable")
    print("2. Verify DATABASE_URL is set for PostgreSQL")
    print("3. Run: python manage.py migrate")
    print("4. Run: python manage.py sync_production_data")
    print("5. Run: python manage.py create_sample_itineraries")
    print("6. Run: python manage.py collectstatic --noinput")
    print("7. Restart web server")
    print("8. Test admin interface and package counts")

    print("\n🔍 Quick Diagnostic Commands:")
    print("# Check environment:")
    print("echo $DJANGO_ENV")
    print()
    print("# Check database connectivity:")
    print("python manage.py dbshell --command='SELECT 1'")
    print()
    print("# Check package count:")
    print("python manage.py shell -c 'from adminside.models import Package; print(Package.objects.count())'")
    print()
    print("# Run full diagnostic:")
    print("python production_diagnostic.py")

if __name__ == '__main__':
    check_environment()
    check_database_connection()
    check_data_integrity()
    check_sync_data_file()
    provide_solutions()