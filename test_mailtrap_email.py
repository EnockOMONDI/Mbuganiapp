#!/usr/bin/env python
"""
Test script for Mailtrap HTTP API email sending
Tests all email functions to ensure they work correctly before deployment
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tours_travels.settings')
django.setup()

from users.tasks import (
    send_email_via_mailtrap,
    send_quote_request_emails,
    send_job_application_emails,
    send_newsletter_subscription_emails,
    send_booking_confirmation_email,
)
from users.models import QuoteRequest, JobApplication, NewsletterSubscription, Booking
from django.contrib.auth import get_user_model

User = get_user_model()


def test_basic_email():
    """Test 1: Basic email sending via Mailtrap API"""
    print("\n" + "="*80)
    print("TEST 1: Basic Email Sending")
    print("="*80)
    
    result = send_email_via_mailtrap(
        subject="Test Email - Mailtrap HTTP API",
        html_message="<h1>Test Email</h1><p>This is a test email from Mailtrap HTTP API integration.</p><p>If you receive this, the basic email function is working! ✅</p>",
        from_email="Mbugani Luxe Adventures <info@mbuganiluxeadventures.com>",
        recipient_list=["test@example.com"]
    )
    
    if result:
        print("✅ SUCCESS: Basic email sent successfully!")
        return True
    else:
        print("❌ FAILED: Basic email sending failed!")
        return False


def test_quote_request_email():
    """Test 2: Quote request email (using most recent quote request)"""
    print("\n" + "="*80)
    print("TEST 2: Quote Request Email")
    print("="*80)
    
    try:
        # Get the most recent quote request
        quote = QuoteRequest.objects.order_by('-created_at').first()
        
        if not quote:
            print("⚠️  SKIPPED: No quote requests found in database")
            return None
        
        print(f"📧 Testing with quote request: {quote.full_name} ({quote.email})")
        print(f"   Created: {quote.created_at}")
        
        result = send_quote_request_emails(quote.id)
        
        if result.get('success'):
            print(f"✅ SUCCESS: Quote request emails sent!")
            print(f"   Admin email: {result.get('admin_email_sent', False)}")
            print(f"   User email: {result.get('user_email_sent', False)}")
            return True
        else:
            print(f"❌ FAILED: Quote request emails failed!")
            print(f"   Error: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def test_job_application_email():
    """Test 3: Job application email (using most recent application)"""
    print("\n" + "="*80)
    print("TEST 3: Job Application Email")
    print("="*80)
    
    try:
        # Get the most recent job application
        application = JobApplication.objects.order_by('-created_at').first()
        
        if not application:
            print("⚠️  SKIPPED: No job applications found in database")
            return None
        
        print(f"📧 Testing with job application: {application.full_name} ({application.email})")
        print(f"   Position: {application.position}")
        print(f"   Created: {application.created_at}")
        
        result = send_job_application_emails(application.id)
        
        if result.get('success'):
            print(f"✅ SUCCESS: Job application emails sent!")
            print(f"   Admin email: {result.get('admin_email_sent', False)}")
            print(f"   Applicant email: {result.get('applicant_email_sent', False)}")
            return True
        else:
            print(f"❌ FAILED: Job application emails failed!")
            print(f"   Error: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def test_newsletter_subscription_email():
    """Test 4: Newsletter subscription email (using most recent subscription)"""
    print("\n" + "="*80)
    print("TEST 4: Newsletter Subscription Email")
    print("="*80)
    
    try:
        # Get the most recent newsletter subscription
        subscription = NewsletterSubscription.objects.order_by('-subscription_date').first()
        
        if not subscription:
            print("⚠️  SKIPPED: No newsletter subscriptions found in database")
            return None
        
        print(f"📧 Testing with subscription: {subscription.email}")
        print(f"   Created: {subscription.subscription_date}")
        
        result = send_newsletter_subscription_emails(subscription.id)
        
        if result.get('success'):
            print(f"✅ SUCCESS: Newsletter subscription emails sent!")
            print(f"   Admin email: {result.get('admin_email_sent', False)}")
            print(f"   Subscriber email: {result.get('subscriber_email_sent', False)}")
            return True
        else:
            print(f"❌ FAILED: Newsletter subscription emails failed!")
            print(f"   Error: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def test_booking_confirmation_email():
    """Test 5: Booking confirmation email (using most recent booking)"""
    print("\n" + "="*80)
    print("TEST 5: Booking Confirmation Email")
    print("="*80)
    
    try:
        # Get the most recent booking
        booking = Booking.objects.order_by('-created_at').first()
        
        if not booking:
            print("⚠️  SKIPPED: No bookings found in database")
            return None
        
        print(f"📧 Testing with booking: {booking.booking_reference}")
        print(f"   Customer: {booking.first_name} {booking.last_name} ({booking.email})")
        print(f"   Created: {booking.created_at}")
        
        result = send_booking_confirmation_email(booking.id)
        
        if result.get('success'):
            print(f"✅ SUCCESS: Booking confirmation email sent!")
            return True
        else:
            print(f"❌ FAILED: Booking confirmation email failed!")
            print(f"   Error: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "🚀"*40)
    print("MAILTRAP HTTP API EMAIL TESTING")
    print("Testing synchronous email sending before deployment")
    print("🚀"*40)
    
    # Check if we're in development mode
    from django.conf import settings
    print(f"\n📋 Environment: {os.getenv('DJANGO_ENV', 'development')}")
    print(f"📋 Debug Mode: {settings.DEBUG}")

    # Check for Mailtrap token (only in production settings)
    mailtrap_token = getattr(settings, 'MAILTRAP_API_TOKEN', None)
    print(f"📋 Mailtrap Token: {'✅ Set' if mailtrap_token else '❌ Not Set'}")

    if not mailtrap_token:
        print("\n⚠️  WARNING: MAILTRAP_API_TOKEN not found in settings!")
        print("   This is expected in development mode.")
        print("   To test with production settings, run:")
        print("   export DJANGO_ENV=production && python test_mailtrap_email.py")
        print("\n   Continuing with tests anyway...\n")
    
    # Run all tests
    results = {
        'basic_email': test_basic_email(),
        'quote_request': test_quote_request_email(),
        'job_application': test_job_application_email(),
        'newsletter': test_newsletter_subscription_email(),
        'booking_confirmation': test_booking_confirmation_email(),
    }
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    passed = sum(1 for v in results.values() if v is True)
    failed = sum(1 for v in results.values() if v is False)
    skipped = sum(1 for v in results.values() if v is None)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result is True else "❌ FAILED" if result is False else "⚠️  SKIPPED"
        print(f"{status}: {test_name.replace('_', ' ').title()}")
    
    print(f"\n📊 Results: {passed} passed, {failed} failed, {skipped} skipped (out of {total} tests)")
    
    if failed > 0:
        print("\n❌ SOME TESTS FAILED - Please fix issues before deploying!")
        sys.exit(1)
    elif passed == 0:
        print("\n⚠️  NO TESTS RAN - Please add test data to database!")
        sys.exit(0)
    else:
        print("\n✅ ALL TESTS PASSED - Ready to deploy!")
        sys.exit(0)


if __name__ == '__main__':
    main()

