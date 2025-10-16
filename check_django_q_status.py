#!/usr/bin/env python
"""
Django-Q Status Checker for Mbugani Luxe Adventures

This script checks the status of Django-Q in production:
- Verifies database tables exist
- Shows queued tasks
- Checks configuration
- Tests database connectivity

Usage:
    python check_django_q_status.py
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

from django.db import connection
from django.conf import settings
import logging

def check_database_connection():
    """Check if we can connect to the database"""
    print("🔍 Checking database connection...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result:
                print("✅ Database connection successful")
                return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def check_django_q_tables():
    """Check if Django-Q tables exist"""
    print("\n🔍 Checking Django-Q database tables...")
    
    required_tables = [
        'django_q_task',
        'django_q_schedule',
        'django_q_ormq',
        'django_q_failure'
    ]
    
    try:
        with connection.cursor() as cursor:
            # Get all table names
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name LIKE 'django_q%'
            """)
            existing_tables = [row[0] for row in cursor.fetchall()]
            
            print(f"📋 Found Django-Q tables: {existing_tables}")
            
            missing_tables = [table for table in required_tables if table not in existing_tables]
            
            if missing_tables:
                print(f"❌ Missing Django-Q tables: {missing_tables}")
                print("💡 Run: python manage.py migrate --settings=tours_travels.settings_prod")
                return False
            else:
                print("✅ All Django-Q tables exist")
                return True
                
    except Exception as e:
        print(f"❌ Error checking tables: {e}")
        return False

def check_queued_tasks():
    """Check queued tasks in the database"""
    print("\n🔍 Checking queued tasks...")
    
    try:
        from django_q.models import Task, OrmQ
        
        # Check OrmQ (task queue)
        queued_count = OrmQ.objects.count()
        print(f"📊 Tasks in queue (OrmQ): {queued_count}")
        
        if queued_count > 0:
            print("📋 Queued tasks:")
            for task in OrmQ.objects.all()[:5]:  # Show first 5
                print(f"   • Task: {task.task} (ID: {task.id})")
        
        # Check Task history
        total_tasks = Task.objects.count()
        successful_tasks = Task.objects.filter(success=True).count()
        failed_tasks = Task.objects.filter(success=False).count()
        
        print(f"📊 Task history:")
        print(f"   • Total tasks: {total_tasks}")
        print(f"   • Successful: {successful_tasks}")
        print(f"   • Failed: {failed_tasks}")
        
        # Show recent tasks
        if total_tasks > 0:
            print("📋 Recent tasks:")
            for task in Task.objects.order_by('-started')[:5]:
                status = "✅ Success" if task.success else "❌ Failed"
                print(f"   • {task.name}: {status} (Started: {task.started})")
        
        return queued_count > 0
        
    except Exception as e:
        print(f"❌ Error checking tasks: {e}")
        return False

def check_django_q_config():
    """Check Django-Q configuration"""
    print("\n🔍 Checking Django-Q configuration...")
    
    try:
        q_cluster = getattr(settings, 'Q_CLUSTER', None)
        if not q_cluster:
            print("❌ Q_CLUSTER not configured")
            return False
        
        print("✅ Q_CLUSTER configuration found:")
        for key, value in q_cluster.items():
            print(f"   • {key}: {value}")
        
        # Check if django_q is in INSTALLED_APPS
        if 'django_q' in settings.INSTALLED_APPS:
            print("✅ django_q in INSTALLED_APPS")
        else:
            print("❌ django_q not in INSTALLED_APPS")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking configuration: {e}")
        return False

def test_task_creation():
    """Test creating a simple task"""
    print("\n🔍 Testing task creation...")
    
    try:
        from django_q.tasks import async_task
        
        # Create a simple test task
        task_id = async_task(
            'django.core.management.color.no_style',  # Simple built-in function
            task_name='test_task_creation',
            timeout=30,
        )
        
        print(f"✅ Test task created: {task_id}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating test task: {e}")
        return False

def main():
    """Main diagnostic function"""
    print("🚀 Django-Q Status Check for Mbugani Luxe Adventures")
    print("=" * 60)
    
    # Check environment
    print(f"🌍 Environment: {os.environ.get('DJANGO_ENV', 'development')}")
    print(f"⚙️  Settings module: {settings.SETTINGS_MODULE}")
    print(f"🗄️  Database: {settings.DATABASES['default']['NAME']}")
    
    # Run checks
    checks = [
        ("Database Connection", check_database_connection),
        ("Django-Q Tables", check_django_q_tables),
        ("Django-Q Configuration", check_django_q_config),
        ("Queued Tasks", check_queued_tasks),
        ("Task Creation Test", test_task_creation),
    ]
    
    results = {}
    for check_name, check_func in checks:
        try:
            results[check_name] = check_func()
        except Exception as e:
            print(f"❌ {check_name} failed with error: {e}")
            results[check_name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY:")
    for check_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} {check_name}")
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS:")
    if not results.get("Django-Q Tables", False):
        print("   1. Run migrations: python manage.py migrate --settings=tours_travels.settings_prod")
    
    if not results.get("Queued Tasks", False):
        print("   2. No tasks in queue - this is normal if worker is processing them")
    
    if not all(results.values()):
        print("   3. Check Render worker service logs for errors")
        print("   4. Verify worker service is running on Render dashboard")
    else:
        print("   🎉 All checks passed! Django-Q should be working correctly.")

if __name__ == "__main__":
    main()
