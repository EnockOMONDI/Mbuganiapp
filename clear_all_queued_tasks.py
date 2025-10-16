#!/usr/bin/env python
"""
Clear All Queued Django-Q Tasks

This script removes ALL queued tasks from the Django-Q queue.
Use this to start fresh and remove any problematic tasks.
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

from django_q.models import OrmQ

def clear_all_queued_tasks():
    """Remove all queued tasks"""
    
    print("🧹 Clear All Queued Django-Q Tasks")
    print("=" * 60)
    print()
    
    # Get count of queued tasks
    queued_count = OrmQ.objects.count()
    
    print(f"📊 Found {queued_count} queued task(s)")
    
    if queued_count == 0:
        print("✅ Queue is already empty")
        return
    
    print()
    print("⚠️  This will delete ALL queued tasks (including the problematic one)")
    print("⚠️  Any pending email tasks will need to be resubmitted")
    print()
    
    # Delete all queued tasks
    print("🗑️  Deleting all queued tasks...")
    deleted_count, _ = OrmQ.objects.all().delete()
    
    print(f"✅ Deleted {deleted_count} queued task(s)")
    print()
    print("🎉 Queue is now empty!")
    print()
    print("📝 Next steps:")
    print("1. Check Railway logs - serialization errors should stop")
    print("2. Submit a new quote request to test email delivery")
    print("3. Monitor Railway logs for successful task processing")
    print()
    print("💡 The Railway worker will now only process new tasks")

def main():
    """Main function"""
    try:
        clear_all_queued_tasks()
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
