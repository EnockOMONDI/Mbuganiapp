#!/usr/bin/env python
"""
Production Email Test for Mbugani Luxe Adventures
Tests real SMTP email sending using production settings
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Force production settings for email testing
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tours_travels.settings_prod')
django.setup()

from django.conf import settings
from django.core.mail import send_mail
from users.models import QuoteRequest
from users.views import send_quote_request_emails
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_smtp_connection():
    """Test basic SMTP connection"""
    print("\n" + "="*60)
    print("🔌 SMTP CONNECTION TEST")
    print("="*60)
    
    print(f"Email Backend: {settings.EMAIL_BACKEND}")
    print(f"SMTP Host: {settings.EMAIL_HOST}")
    print(f"SMTP Port: {settings.EMAIL_PORT}")
    print(f"Use TLS: {settings.EMAIL_USE_TLS}")
    print(f"Host User: {settings.EMAIL_HOST_USER}")
    print(f"From Email: {settings.DEFAULT_FROM_EMAIL}")
    
    try:
        # Test basic email sending
        result = send_mail(
            subject='SMTP Test - Mbugani Luxe Adventures',
            message='This is a test email to verify SMTP configuration.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['djsean@mbuganiluxeadventures.com'],
            fail_silently=False,
        )
        
        if result == 1:
            print("✅ SMTP connection successful - test email sent!")
            return True
        else:
            print("❌ SMTP connection failed - no emails sent")
            return False
            
    except Exception as e:
        print(f"❌ SMTP connection error: {e}")
        return False

def test_quote_request_emails():
    """Test quote request email functionality with real SMTP"""
    print("\n" + "="*60)
    print("📧 QUOTE REQUEST EMAIL TEST")
    print("="*60)
    
    try:
        # Create test quote request
        quote_request = QuoteRequest.objects.create(
            full_name="Production Email Test",
            email="djsean@mbuganiluxeadventures.com",
            phone_number="+254701234567",
            destination="Serengeti National Park",
            preferred_travel_dates="January 2025",
            number_of_travelers=4,
            special_requests="Testing production email functionality. This is a real test of the SMTP configuration."
        )
        
        print(f"✅ Test quote request created: ID {quote_request.id}")
        
        # Send emails using production SMTP
        result = send_quote_request_emails(quote_request)
        
        print(f"\n📊 Email Sending Results:")
        print(f"   Overall Success: {result['overall_success']}")
        print(f"   Confirmation Email: {'✅' if result['confirmation_email']['sent'] else '❌'}")
        print(f"   Admin Notification: {'✅' if result['admin_email']['sent'] else '❌'}")
        
        if result['confirmation_email']['error_message']:
            print(f"   Confirmation Error: {result['confirmation_email']['error_message']}")
            
        if result['admin_email']['error_message']:
            print(f"   Admin Error: {result['admin_email']['error_message']}")
        
        print(f"\n🔧 Technical Details:")
        print(f"   Email Backend: {result['environment']['email_backend']}")
        print(f"   SMTP Host: {result['environment']['smtp_host']}")
        print(f"   From Email: {result['environment']['from_email']}")
        
        # Cleanup
        quote_request.delete()
        print(f"\n🧹 Test quote request {quote_request.id} cleaned up")
        
        return result['overall_success']
        
    except Exception as e:
        print(f"❌ Quote request email test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🌍 MBUGANI LUXE ADVENTURES - PRODUCTION EMAIL TEST")
    print("="*60)
    print("⚠️  This test will send REAL EMAILS using production SMTP settings")
    print("📧 Test emails will be sent to: djsean@mbuganiluxeadventures.com")
    print("📧 Admin notifications will be sent to: info@mbuganiluxeadventures.com")
    
    # Confirm before proceeding
    response = input("\n🤔 Do you want to proceed with sending real emails? (y/N): ")
    if response.lower() != 'y':
        print("❌ Test cancelled by user")
        return
    
    print("\n🚀 Starting production email tests...")
    
    # Test 1: Basic SMTP connection
    smtp_success = test_smtp_connection()
    
    # Test 2: Quote request emails (only if SMTP works)
    if smtp_success:
        quote_success = test_quote_request_emails()
    else:
        quote_success = False
        print("\n⏭️  Skipping quote request test due to SMTP connection failure")
    
    # Final summary
    print("\n" + "="*60)
    print("📊 PRODUCTION EMAIL TEST SUMMARY")
    print("="*60)
    
    if smtp_success and quote_success:
        print("✅ ALL TESTS PASSED - Email functionality is working correctly!")
        print("📧 Check your email inbox for test messages")
        print("📧 Verify admin received notification at info@mbuganiluxeadventures.com")
    elif smtp_success:
        print("⚠️  PARTIAL SUCCESS - SMTP works but quote request emails failed")
        print("🔧 Check the error messages above for troubleshooting")
    else:
        print("❌ TESTS FAILED - SMTP connection issues")
        print("🔧 Check email configuration and credentials")
    
    print("\n🎯 Next Steps:")
    print("   - Verify emails were received in inbox")
    print("   - Test the quote form on the live website")
    print("   - Monitor production logs for any email errors")
    print("   - Set up email delivery monitoring")

if __name__ == "__main__":
    main()
