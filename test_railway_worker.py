#!/usr/bin/env python
"""
Test Railway Django-Q Worker

This script tests if the Django-Q worker can process tasks without serialization errors.
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

from django_q.tasks import async_task
from django.utils import timezone

def test_simple_task():
    """Test a simple task to verify Django-Q is working"""
    
    def simple_test_task(message, **kwargs):
        """Simple test task that just returns a message"""
        print(f"✅ Test task executed: {message}")
        return {
            'success': True,
            'message': message,
            'timestamp': timezone.now().isoformat(),
            'kwargs_received': list(kwargs.keys())
        }
    
    try:
        print("🧪 Testing Django-Q task execution...")
        
        # Queue a simple test task
        task_id = async_task(
            simple_test_task,
            "Hello from Railway worker!",
            task_name='test_railway_worker',
            timeout=30,
            retry=3,
        )
        
        print(f"✅ Test task queued successfully: {task_id}")
        print("📋 Check Railway logs for task execution")
        print("🎯 Expected log: '✅ Test task executed: Hello from Railway worker!'")
        
        return True
        
    except Exception as e:
        print(f"❌ Error queuing test task: {e}")
        return False

def main():
    """Main test function"""
    print("🚂 Railway Django-Q Worker Test")
    print("=" * 40)
    print()
    
    # Test basic Django setup
    try:
        from django.conf import settings
        print(f"✅ Django settings loaded: {settings.SETTINGS_MODULE}")
        print(f"✅ Database configured: {settings.DATABASES['default']['ENGINE']}")
        print(f"✅ Django-Q configured: {settings.Q_CLUSTER['name']}")
        print()
    except Exception as e:
        print(f"❌ Django setup error: {e}")
        return
    
    # Test task queueing
    success = test_simple_task()
    
    print()
    if success:
        print("🎉 Test completed successfully!")
        print("📝 Next steps:")
        print("1. Check Railway logs for task execution")
        print("2. Test quote request submission on your website")
        print("3. Verify email delivery")
    else:
        print("❌ Test failed - check error messages above")

if __name__ == "__main__":
    main()
