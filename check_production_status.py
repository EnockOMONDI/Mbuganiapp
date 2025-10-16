#!/usr/bin/env python3
"""
Production Status Checker for Mbugani Luxe Adventures
Checks environment configuration and provides deployment instructions
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
from adminside.models import Package

def check_environment():
    """Check current environment configuration"""
    print("🔍 Checking Production Environment Status")
    print("=" * 50)

    # Check Django environment
    django_env = os.environ.get('DJANGO_ENV', 'development')
    print(f"🌍 DJANGO_ENV: {django_env}")

    # Check DEBUG status
    debug_status = "❌ DEBUG=True (Development Mode)" if settings.DEBUG else "✅ DEBUG=False (Production Mode)"
    print(f"🐛 DEBUG: {debug_status}")

    # Check database
    db_engine = settings.DATABASES['default']['ENGINE']
    if 'postgresql' in db_engine:
        print("🗄️  Database: PostgreSQL (Production)")
    elif 'sqlite' in db_engine:
        print("🗄️  Database: SQLite (Development)")
    else:
        print(f"🗄️  Database: {db_engine}")

    # Check allowed hosts
    allowed_hosts = settings.ALLOWED_HOSTS
    print(f"🌐 ALLOWED_HOSTS: {allowed_hosts}")

    # Check site URL
    site_url = getattr(settings, 'SITE_URL', 'Not set')
    print(f"🔗 SITE_URL: {site_url}")

    print()

def check_database():
    """Check database content"""
    print("📊 Checking Database Content")
    print("=" * 30)

    try:
        package_count = Package.objects.count()
        published_packages = Package.objects.filter(status=Package.PUBLISHED).count()

        print(f"📦 Total Packages: {package_count}")
        print(f"✅ Published Packages: {published_packages}")

        if package_count > 0:
            print("\n📋 Package List:")
            for package in Package.objects.all():
                status_icon = "✅" if package.status == Package.PUBLISHED else "⏸️"
                print(f"  {status_icon} {package.name}")

        # Check for itineraries
        packages_with_itineraries = Package.objects.filter(itinerary__isnull=False).distinct()
        itinerary_count = packages_with_itineraries.count()
        print(f"\n🗺️  Packages with Itineraries: {itinerary_count}")

        if itinerary_count > 0:
            print("\n📅 Itinerary Details:")
            for package in packages_with_itineraries:
                days_count = package.itinerary.days.count()
                print(f"  📍 {package.name}: {days_count} days")

    except Exception as e:
        print(f"❌ Database Error: {e}")

    print()

def provide_solutions():
    """Provide solutions for identified issues"""
    print("🔧 Production Deployment Solutions")
    print("=" * 40)

    django_env = os.environ.get('DJANGO_ENV', 'development')

    if django_env != 'production':
        print("1. 🚨 DJANGO_ENV not set to 'production'")
        print("   Solution: Set environment variable DJANGO_ENV=production")
        print("   Example: export DJANGO_ENV=production")
        print()

    if settings.DEBUG:
        print("2. 🚨 DEBUG=True (showing development server message)")
        print("   Solution: Ensure DJANGO_ENV=production is set")
        print("   Check: Production settings should override DEBUG=False")
        print()

    package_count = Package.objects.count()
    if package_count < 10:
        print("3. 🚨 Database sync needed (only {} packages vs expected 10)".format(package_count))
        print("   Solution: Run data synchronization commands:")
        print("   ")
        print("   # On local machine (dump data):")
        print("   python manage.py sync_production_data --dump-only")
        print("   ")
        print("   # On production server (load data):")
        print("   python manage.py sync_production_data --load-only")
        print("   ")
        print("   # Or run both steps on production server:")
        print("   python manage.py sync_production_data")
        print()

    # Check for itineraries
    packages_with_itineraries = Package.objects.filter(itinerary__isnull=False).distinct()
    if packages_with_itineraries.count() == 0:
        print("4. 🚨 No itineraries found")
        print("   Solution: Run itinerary creation command:")
        print("   python manage.py create_sample_itineraries")
        print()

    print("📋 Complete Production Deployment Checklist:")
    print("1. Set DJANGO_ENV=production environment variable")
    print("2. Run: python manage.py migrate")
    print("3. Run: python manage.py sync_production_data")
    print("4. Run: python manage.py create_sample_itineraries")
    print("5. Run: python manage.py collectstatic --noinput")
    print("6. Restart web server")
    print("7. Verify admin access and package count")

if __name__ == '__main__':
    check_environment()
    check_database()
    provide_solutions()