#!/usr/bin/env python
"""
Cleanup Django-Q Tasks

This script removes problematic queued tasks from the Django-Q queue,
specifically the test_task_creation task that's causing serialization errors.
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

from django_q.models import OrmQ, Task

def cleanup_problematic_tasks():
    """Remove problematic tasks from the queue"""

    print("🧹 Django-Q Task Cleanup")
    print("=" * 60)
    print()

    # Find and delete problematic queued tasks
    print("📋 Checking for problematic queued tasks...")

    import pickle

    # Get all queued tasks
    all_queued = OrmQ.objects.all()
    total_count = all_queued.count()

    print(f"📊 Total queued tasks: {total_count}")
    print()

    problematic_tasks = []

    # Check each task for problematic content
    for orm_task in all_queued:
        try:
            # Unpickle the task payload to inspect it
            task_data = pickle.loads(orm_task.payload)
            task_name = task_data.get('name', 'unknown')
            task_func = task_data.get('func', 'unknown')

            # Check if it's a problematic task
            is_problematic = (
                task_name == 'test_task_creation' or
                'django.core.management.color' in str(task_func)
            )

            if is_problematic:
                problematic_tasks.append({
                    'orm_task': orm_task,
                    'name': task_name,
                    'func': task_func,
                })
                print(f"❌ Found problematic task:")
                print(f"   - ID: {orm_task.id}")
                print(f"   - Name: {task_name}")
                print(f"   - Function: {task_func}")
                print()

        except Exception as e:
            print(f"⚠️  Could not inspect task {orm_task.id}: {e}")

    # Delete problematic tasks
    if problematic_tasks:
        print(f"🗑️  Deleting {len(problematic_tasks)} problematic task(s)...")
        for task_info in problematic_tasks:
            task_info['orm_task'].delete()
        print(f"✅ Deleted {len(problematic_tasks)} problematic task(s)")
    else:
        print("✅ No problematic tasks found in queue")

    print()

    # Show remaining queued tasks
    remaining_tasks = OrmQ.objects.all()
    remaining_count = remaining_tasks.count()

    print(f"📊 Remaining queued tasks: {remaining_count}")

    if remaining_count > 0:
        print("\nQueued tasks:")
        for orm_task in remaining_tasks[:10]:  # Show first 10
            try:
                task_data = pickle.loads(orm_task.payload)
                task_name = task_data.get('name', 'unknown')
                task_func = task_data.get('func', 'unknown')
                print(f"   - {task_name} ({task_func})")
            except:
                print(f"   - Task {orm_task.id} (could not inspect)")

        if remaining_count > 10:
            print(f"   ... and {remaining_count - 10} more")

    print()
    
    # Show recent completed tasks
    recent_tasks = Task.objects.all().order_by('-stopped')[:5]
    
    if recent_tasks.exists():
        print("📜 Recent completed tasks:")
        for task in recent_tasks:
            status = "✅ Success" if task.success else "❌ Failed"
            print(f"   {status} - {task.name} (stopped: {task.stopped})")
    
    print()
    print("🎉 Cleanup complete!")
    print()
    print("📝 Next steps:")
    print("1. Check Railway logs - serialization errors should stop")
    print("2. Submit a new quote request to test email delivery")
    print("3. Monitor Railway logs for successful task processing")

def main():
    """Main cleanup function"""
    try:
        cleanup_problematic_tasks()
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
