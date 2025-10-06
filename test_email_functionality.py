#!/usr/bin/env python
"""
Test script for Mbugani Luxe Adventures email functionality
Tests the quote request email sending in both development and production modes
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tours_travels.settings_dev')
django.setup()

from django.conf import settings
from users.models import QuoteRequest
from users.views import send_quote_request_emails
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_email_configuration():
    """Test current email configuration"""
    print("\n" + "="*60)
    print("📧 EMAIL CONFIGURATION TEST")
    print("="*60)
    
    print(f"Email Backend: {settings.EMAIL_BACKEND}")
    print(f"Email Host: {settings.EMAIL_HOST}")
    print(f"Email Port: {settings.EMAIL_PORT}")
    print(f"Email Use TLS: {settings.EMAIL_USE_TLS}")
    print(f"Email Host User: {settings.EMAIL_HOST_USER}")
    print(f"Default From Email: {settings.DEFAULT_FROM_EMAIL}")
    print(f"Admin Email: {settings.ADMIN_EMAIL}")
    print(f"Debug Mode: {settings.DEBUG}")
    
    # Check if real emails are enabled
    enable_real_emails = os.getenv('ENABLE_REAL_EMAILS', 'False').lower() == 'true'
    print(f"Real Emails Enabled: {enable_real_emails}")
    
    return enable_real_emails

def test_quote_request_creation():
    """Test creating a quote request"""
    print("\n" + "="*60)
    print("📝 QUOTE REQUEST CREATION TEST")
    print("="*60)
    
    try:
        # Create a test quote request
        quote_request = QuoteRequest.objects.create(
            full_name="Test User - Email Functionality",
            email="test@example.com",
            phone_number="+254701234567",
            destination="Maasai Mara National Reserve",
            preferred_travel_dates="December 2024 - January 2025",
            number_of_travelers=2,
            special_requests="Testing email functionality for quote requests. Please ignore this test request."
        )
        
        print(f"✅ Quote request created successfully: ID {quote_request.id}")
        print(f"   Name: {quote_request.full_name}")
        print(f"   Email: {quote_request.email}")
        print(f"   Destination: {quote_request.destination}")
        
        return quote_request
        
    except Exception as e:
        print(f"❌ Failed to create quote request: {e}")
        return None

def test_email_sending(quote_request):
    """Test sending emails for quote request"""
    print("\n" + "="*60)
    print("📤 EMAIL SENDING TEST")
    print("="*60)
    
    try:
        # Send emails
        result = send_quote_request_emails(quote_request)
        
        print(f"Overall Success: {result['overall_success']}")
        print(f"Confirmation Email Sent: {result['confirmation_email']['sent']}")
        print(f"Admin Email Sent: {result['admin_email']['sent']}")
        
        if result['confirmation_email']['error_message']:
            print(f"Confirmation Email Error: {result['confirmation_email']['error_message']}")
            
        if result['admin_email']['error_message']:
            print(f"Admin Email Error: {result['admin_email']['error_message']}")
            
        print(f"Email Backend Used: {result['environment']['email_backend']}")
        print(f"SMTP Host: {result['environment']['smtp_host']}")
        print(f"From Email: {result['environment']['from_email']}")
        
        if result['warnings']:
            print("⚠️  Warnings:")
            for warning in result['warnings']:
                print(f"   - {warning}")
                
        if result['recommendations']:
            print("💡 Recommendations:")
            for rec in result['recommendations']:
                print(f"   - {rec}")
        
        return result
        
    except Exception as e:
        print(f"❌ Failed to send emails: {e}")
        return None

def cleanup_test_data(quote_request):
    """Clean up test data"""
    print("\n" + "="*60)
    print("🧹 CLEANUP")
    print("="*60)
    
    try:
        if quote_request:
            quote_request.delete()
            print(f"✅ Test quote request {quote_request.id} deleted successfully")
    except Exception as e:
        print(f"❌ Failed to cleanup test data: {e}")

def main():
    """Main test function"""
    print("🌍 MBUGANI LUXE ADVENTURES - EMAIL FUNCTIONALITY TEST")
    print("="*60)
    
    # Test email configuration
    enable_real_emails = test_email_configuration()
    
    if not enable_real_emails:
        print("\n💡 To test real email sending, set environment variable:")
        print("   export ENABLE_REAL_EMAILS=true")
        print("   Then run this script again.")
    
    # Test quote request creation
    quote_request = test_quote_request_creation()
    
    if not quote_request:
        print("❌ Cannot proceed with email testing - quote request creation failed")
        return
    
    # Test email sending
    result = test_email_sending(quote_request)
    
    # Cleanup
    cleanup_test_data(quote_request)
    
    # Final summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    if result and result['overall_success']:
        print("✅ Email functionality test PASSED")
        if enable_real_emails:
            print("📧 Real emails were sent successfully")
        else:
            print("📧 Emails were printed to console (development mode)")
    else:
        print("❌ Email functionality test FAILED")
        print("🔧 Check the error messages above for troubleshooting")
    
    print("\n🎯 Next Steps:")
    if enable_real_emails:
        print("   - Check your email inbox for test emails")
        print("   - Verify admin email was received at info@mbuganiluxeadventures.com")
    else:
        print("   - Set ENABLE_REAL_EMAILS=true to test actual email sending")
    print("   - Test the quote form on the website")
    print("   - Monitor logs for any email errors in production")

if __name__ == "__main__":
    main()
