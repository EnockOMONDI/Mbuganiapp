#!/usr/bin/env python
"""
Test script for Django-Q async email functionality in Mbugani Luxe Adventures

This script tests the async email tasks to ensure they work correctly
before deploying to production.

Usage:
    python test_async_emails.py

Requirements:
    - Django-Q worker must be running: python manage.py qcluster
    - Development environment with console email backend
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tours_travels.settings_dev')
django.setup()

from django_q.tasks import async_task
from users.models import QuoteRequest, JobApplication, NewsletterSubscription
from django.contrib.auth.models import User
import time


def test_quote_request_emails():
    """Test quote request email functionality"""
    print("\n🧪 Testing Quote Request Emails...")
    
    # Create a test quote request
    quote_request = QuoteRequest.objects.create(
        full_name="Test User",
        email="test@example.com",
        phone_number="+1234567890",
        destination="Serengeti National Park",
        travel_date="2024-12-01",
        number_of_adults=2,
        number_of_children=1,
        budget_range="$5000-$10000",
        special_requirements="Test async email functionality",
        how_did_you_hear="Website"
    )
    
    print(f"✅ Created test quote request: ID {quote_request.id}")
    
    # Queue the async email task
    task_id = async_task(
        'users.tasks.send_quote_request_emails_async',
        quote_request.id,
        task_name=f'test_quote_emails_{quote_request.id}',
        timeout=60,
        retry=5,
    )
    
    print(f"✅ Queued email task: {task_id}")
    print("📧 Check Django-Q worker logs for email processing...")
    
    return quote_request.id, task_id


def test_job_application_emails():
    """Test job application email functionality"""
    print("\n🧪 Testing Job Application Emails...")
    
    # Create a test job application
    job_application = JobApplication.objects.create(
        full_name="Test Applicant",
        email="applicant@example.com",
        phone_number="+1234567890",
        position="tour_guide",
        experience_years=3,
        cover_letter="Test async email functionality for job applications",
        resume_file=None  # Optional for testing
    )
    
    print(f"✅ Created test job application: ID {job_application.id}")
    
    # Queue the async email task
    task_id = async_task(
        'users.tasks.send_job_application_emails_async',
        job_application.id,
        task_name=f'test_job_emails_{job_application.id}',
        timeout=60,
        retry=5,
    )
    
    print(f"✅ Queued email task: {task_id}")
    print("📧 Check Django-Q worker logs for email processing...")
    
    return job_application.id, task_id


def test_newsletter_subscription_emails():
    """Test newsletter subscription email functionality"""
    print("\n🧪 Testing Newsletter Subscription Emails...")
    
    # Create a test newsletter subscription
    subscription = NewsletterSubscription.objects.create(
        email="subscriber@example.com",
        first_name="Test",
        last_name="Subscriber",
        interests="Wildlife Safari, Cultural Tours"
    )
    
    print(f"✅ Created test newsletter subscription: ID {subscription.id}")
    
    # Queue the async email task
    task_id = async_task(
        'users.tasks.send_newsletter_subscription_emails_async',
        subscription.id,
        task_name=f'test_newsletter_emails_{subscription.id}',
        timeout=60,
        retry=5,
    )
    
    print(f"✅ Queued email task: {task_id}")
    print("📧 Check Django-Q worker logs for email processing...")
    
    return subscription.id, task_id


def main():
    """Main test function"""
    print("🚀 Starting Django-Q Async Email Tests for Mbugani Luxe Adventures")
    print("=" * 70)
    
    # Check if Django-Q is configured
    from django.conf import settings
    if not hasattr(settings, 'Q_CLUSTER'):
        print("❌ Django-Q is not configured. Check your settings.")
        return
    
    print(f"✅ Django-Q configured: {settings.Q_CLUSTER['name']}")
    print(f"📧 Email backend: {settings.EMAIL_BACKEND}")
    
    # Run tests
    try:
        # Test 1: Quote Request Emails
        quote_id, quote_task = test_quote_request_emails()
        
        # Test 2: Job Application Emails
        job_id, job_task = test_job_application_emails()
        
        # Test 3: Newsletter Subscription Emails
        newsletter_id, newsletter_task = test_newsletter_subscription_emails()
        
        print("\n" + "=" * 70)
        print("🎉 All email tasks have been queued successfully!")
        print("\n📋 Summary:")
        print(f"   • Quote Request ID: {quote_id} → Task: {quote_task}")
        print(f"   • Job Application ID: {job_id} → Task: {job_task}")
        print(f"   • Newsletter Subscription ID: {newsletter_id} → Task: {newsletter_task}")
        
        print("\n🔍 Next Steps:")
        print("   1. Check Django-Q worker logs for task processing")
        print("   2. Verify emails appear in console (development mode)")
        print("   3. Check Django admin at /admin/django_q/ for task status")
        print("   4. Monitor task completion and any errors")
        
        print("\n⚠️  Note: In development mode, emails are printed to console")
        print("   In production, they will be sent via Gmail SMTP")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
