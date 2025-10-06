#!/usr/bin/env python
"""
Production Email Test Script for Mbugani Luxe Adventures
Tests Gmail SMTP configuration and quote request email functionality
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tours_travels.settings_prod')
django.setup()

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from users.models import QuoteRequest
from users.views import send_quote_request_emails
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_basic_email():
    """Test basic email sending functionality"""
    print("🧪 Testing basic email functionality...")
    
    try:
        send_mail(
            subject='Test Email - Mbugani Luxe Adventures',
            message='This is a test email to verify SMTP configuration.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['djsean@mbuganiluxeadventures.com'],
            fail_silently=False,
        )
        print("✅ Basic email test PASSED")
        return True
    except Exception as e:
        print(f"❌ Basic email test FAILED: {e}")
        return False

def test_quote_request_emails():
    """Test quote request email functionality"""
    print("🧪 Testing quote request email functionality...")
    
    try:
        # Create a test quote request
        quote_request = QuoteRequest.objects.create(
            full_name="Test User",
            email="djsean@mbuganiluxeadventures.com",
            phone_number="+254701363551",
            destination="Kenya Safari",
            preferred_travel_dates="December 2024",
            number_of_travelers=2,
            special_requests="This is a test quote request for email verification."
        )
        
        print(f"📝 Created test quote request ID: {quote_request.id}")
        
        # Test email sending
        success = send_quote_request_emails(quote_request)
        
        if success:
            print("✅ Quote request email test PASSED")
            print(f"📧 Confirmation email sent to: {quote_request.email}")
            print(f"📧 Admin notification sent to: {settings.ADMIN_EMAIL}")
        else:
            print("❌ Quote request email test FAILED")
        
        # Clean up test data
        quote_request.delete()
        print("🧹 Test data cleaned up")
        
        return success
        
    except Exception as e:
        print(f"❌ Quote request email test FAILED: {e}")
        return False

def check_email_configuration():
    """Check email configuration settings"""
    print("🔧 Checking email configuration...")
    
    config = {
        'EMAIL_BACKEND': getattr(settings, 'EMAIL_BACKEND', 'Not set'),
        'EMAIL_HOST': getattr(settings, 'EMAIL_HOST', 'Not set'),
        'EMAIL_PORT': getattr(settings, 'EMAIL_PORT', 'Not set'),
        'EMAIL_USE_TLS': getattr(settings, 'EMAIL_USE_TLS', 'Not set'),
        'EMAIL_HOST_USER': getattr(settings, 'EMAIL_HOST_USER', 'Not set'),
        'EMAIL_HOST_PASSWORD': '***HIDDEN***' if getattr(settings, 'EMAIL_HOST_PASSWORD', None) else 'Not set',
        'DEFAULT_FROM_EMAIL': getattr(settings, 'DEFAULT_FROM_EMAIL', 'Not set'),
        'ADMIN_EMAIL': getattr(settings, 'ADMIN_EMAIL', 'Not set'),
    }
    
    print("📋 Current Email Configuration:")
    for key, value in config.items():
        print(f"   {key}: {value}")
    
    # Check for common issues
    issues = []
    
    if config['EMAIL_BACKEND'] != 'django.core.mail.backends.smtp.EmailBackend':
        issues.append("EMAIL_BACKEND should be 'django.core.mail.backends.smtp.EmailBackend'")
    
    if config['EMAIL_HOST'] != 'smtp.gmail.com':
        issues.append("EMAIL_HOST should be 'smtp.gmail.com'")
    
    if config['EMAIL_PORT'] != 587:
        issues.append("EMAIL_PORT should be 587")
    
    if not config['EMAIL_USE_TLS']:
        issues.append("EMAIL_USE_TLS should be True")
    
    if config['EMAIL_HOST_PASSWORD'] == 'Not set':
        issues.append("EMAIL_HOST_PASSWORD is not set")
    
    if issues:
        print("⚠️  Configuration Issues Found:")
        for issue in issues:
            print(f"   - {issue}")
        return False
    else:
        print("✅ Email configuration looks good")
        return True

def main():
    """Main test function"""
    print("🚀 Starting Mbugani Luxe Adventures Email Test")
    print("=" * 50)
    
    # Check configuration
    config_ok = check_email_configuration()
    print()
    
    # Test basic email
    basic_ok = test_basic_email()
    print()
    
    # Test quote request emails
    quote_ok = test_quote_request_emails()
    print()
    
    # Summary
    print("📊 Test Summary:")
    print(f"   Configuration: {'✅ PASS' if config_ok else '❌ FAIL'}")
    print(f"   Basic Email: {'✅ PASS' if basic_ok else '❌ FAIL'}")
    print(f"   Quote Emails: {'✅ PASS' if quote_ok else '❌ FAIL'}")
    
    if all([config_ok, basic_ok, quote_ok]):
        print("\n🎉 All tests PASSED! Email functionality is working correctly.")
        return True
    else:
        print("\n❌ Some tests FAILED. Please check the configuration and try again.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
