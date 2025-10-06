#!/usr/bin/env python
"""
Production Email Diagnostic Script
Identifies why emails are not being sent despite success logs
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
import logging
import smtplib
import ssl

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_environment_variables():
    """Check if all email environment variables are loaded correctly"""
    print("🔍 Checking Environment Variables")
    print("=" * 50)
    
    env_vars = {
        'EMAIL_HOST_USER': os.getenv('EMAIL_HOST_USER'),
        'EMAIL_HOST_PASSWORD': os.getenv('EMAIL_HOST_PASSWORD'),
        'DEFAULT_FROM_EMAIL': os.getenv('DEFAULT_FROM_EMAIL'),
        'ADMIN_EMAIL': os.getenv('ADMIN_EMAIL'),
        'JOBS_EMAIL': os.getenv('JOBS_EMAIL'),
        'NEWSLETTER_EMAIL': os.getenv('NEWSLETTER_EMAIL'),
    }
    
    all_set = True
    for key, value in env_vars.items():
        if value:
            if 'PASSWORD' in key:
                print(f"   ✅ {key}: ***HIDDEN*** (length: {len(value)})")
            else:
                print(f"   ✅ {key}: {value}")
        else:
            print(f"   ❌ {key}: NOT SET")
            all_set = False
    
    return all_set

def check_django_settings():
    """Check Django email settings"""
    print("\n📧 Checking Django Email Settings")
    print("=" * 50)
    
    settings_to_check = {
        'EMAIL_BACKEND': settings.EMAIL_BACKEND,
        'EMAIL_HOST': settings.EMAIL_HOST,
        'EMAIL_PORT': settings.EMAIL_PORT,
        'EMAIL_USE_TLS': settings.EMAIL_USE_TLS,
        'EMAIL_HOST_USER': settings.EMAIL_HOST_USER,
        'EMAIL_HOST_PASSWORD': '***HIDDEN***' if settings.EMAIL_HOST_PASSWORD else 'NOT SET',
        'DEFAULT_FROM_EMAIL': settings.DEFAULT_FROM_EMAIL,
        'ADMIN_EMAIL': settings.ADMIN_EMAIL,
        'EMAIL_TIMEOUT': getattr(settings, 'EMAIL_TIMEOUT', 'Not set'),
    }
    
    for key, value in settings_to_check.items():
        print(f"   {key}: {value}")
    
    # Check for common issues
    issues = []
    if not settings.EMAIL_HOST_PASSWORD:
        issues.append("EMAIL_HOST_PASSWORD is not set")
    if settings.EMAIL_BACKEND != 'django.core.mail.backends.smtp.EmailBackend':
        issues.append(f"EMAIL_BACKEND is {settings.EMAIL_BACKEND}, should be smtp.EmailBackend")
    
    return len(issues) == 0, issues

def test_smtp_connection_direct():
    """Test direct SMTP connection to Gmail"""
    print("\n🌐 Testing Direct SMTP Connection")
    print("=" * 50)
    
    try:
        print(f"Connecting to {settings.EMAIL_HOST}:{settings.EMAIL_PORT}...")
        
        # Create SMTP connection
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.set_debuglevel(1)  # Enable debug output
        
        print("Starting TLS...")
        server.starttls()
        
        print("Attempting login...")
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        
        print("✅ SMTP connection successful!")
        server.quit()
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ SMTP Authentication Error: {e}")
        print("🔍 Check if Gmail app password is correct and not expired")
        return False
    except smtplib.SMTPConnectError as e:
        print(f"❌ SMTP Connection Error: {e}")
        print("🔍 Check if SMTP server and port are correct")
        return False
    except Exception as e:
        print(f"❌ SMTP Error: {e}")
        return False

def test_django_email_with_logging():
    """Test Django email sending with detailed logging"""
    print("\n📨 Testing Django Email Sending")
    print("=" * 50)
    
    try:
        # Test basic email
        print("Sending test email...")
        
        result = send_mail(
            subject='Test Email - Mbugani Luxe Adventures Diagnostic',
            message='This is a test email to diagnose email sending issues.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['djsean@mbuganiluxeadventures.com'],
            fail_silently=False,  # Don't hide errors
        )
        
        print(f"✅ Django send_mail returned: {result}")
        return True
        
    except Exception as e:
        print(f"❌ Django email sending failed: {e}")
        print(f"Error type: {type(e).__name__}")
        return False

def test_quote_request_email_templates():
    """Test quote request email template rendering"""
    print("\n📄 Testing Quote Request Email Templates")
    print("=" * 50)
    
    try:
        # Create a test quote request object
        test_quote = QuoteRequest(
            id=999,
            full_name="Test User",
            email="test@example.com",
            phone_number="+254701363551",
            destination="Test Destination",
            preferred_travel_dates="Test Dates",
            number_of_travelers=2,
            special_requests="Test request"
        )
        
        # Test confirmation template
        print("Testing confirmation email template...")
        user_html = render_to_string('users/emails/quote_request_confirmation.html', {
            'quote_request': test_quote
        })
        print(f"✅ Confirmation template rendered ({len(user_html)} characters)")
        
        # Test admin template
        print("Testing admin email template...")
        admin_html = render_to_string('users/emails/quote_request_admin.html', {
            'quote_request': test_quote
        })
        print(f"✅ Admin template rendered ({len(admin_html)} characters)")
        
        return True
        
    except Exception as e:
        print(f"❌ Template rendering failed: {e}")
        return False

def test_quote_request_email_function():
    """Test the actual quote request email function with fail_silently=False"""
    print("\n🧪 Testing Quote Request Email Function")
    print("=" * 50)
    
    try:
        # Create a real test quote request
        quote_request = QuoteRequest.objects.create(
            full_name="Email Diagnostic Test",
            email="djsean@mbuganiluxeadventures.com",
            phone_number="+254701363551",
            destination="Test Destination",
            preferred_travel_dates="Test Dates",
            number_of_travelers=1,
            special_requests="Email diagnostic test - please ignore"
        )
        
        print(f"Created test quote request ID: {quote_request.id}")
        
        # Test email sending with fail_silently=False to see actual errors
        print("Testing email sending with error reporting...")
        
        # Send confirmation email
        user_subject = 'Quote Request Received - Mbugani Luxe Adventures'
        user_html = render_to_string('users/emails/quote_request_confirmation.html', {
            'quote_request': quote_request
        })
        
        result1 = send_mail(
            subject=user_subject,
            message='',
            html_message=user_html,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[quote_request.email],
            fail_silently=False,  # Show actual errors
        )
        
        print(f"✅ Confirmation email result: {result1}")
        
        # Send admin email
        admin_subject = f'New Quote Request - {quote_request.full_name}'
        admin_html = render_to_string('users/emails/quote_request_admin.html', {
            'quote_request': quote_request
        })
        
        result2 = send_mail(
            subject=admin_subject,
            message='',
            html_message=admin_html,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False,  # Show actual errors
        )
        
        print(f"✅ Admin email result: {result2}")
        
        # Clean up
        quote_request.delete()
        print("🧹 Test data cleaned up")
        
        return result1 > 0 and result2 > 0
        
    except Exception as e:
        print(f"❌ Quote request email function failed: {e}")
        print(f"Error type: {type(e).__name__}")
        return False

def main():
    """Main diagnostic function"""
    print("🚀 Mbugani Luxe Adventures - Email Production Diagnostic")
    print("=" * 60)
    
    # Run all diagnostic tests
    env_ok = check_environment_variables()
    settings_ok, settings_issues = check_django_settings()
    smtp_ok = test_smtp_connection_direct()
    django_email_ok = test_django_email_with_logging()
    templates_ok = test_quote_request_email_templates()
    quote_function_ok = test_quote_request_email_function()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 DIAGNOSTIC SUMMARY")
    print("=" * 60)
    print(f"Environment Variables: {'✅ PASS' if env_ok else '❌ FAIL'}")
    print(f"Django Settings: {'✅ PASS' if settings_ok else '❌ FAIL'}")
    print(f"SMTP Connection: {'✅ PASS' if smtp_ok else '❌ FAIL'}")
    print(f"Django Email: {'✅ PASS' if django_email_ok else '❌ FAIL'}")
    print(f"Email Templates: {'✅ PASS' if templates_ok else '❌ FAIL'}")
    print(f"Quote Function: {'✅ PASS' if quote_function_ok else '❌ FAIL'}")
    
    if not settings_ok:
        print("\n⚠️  Django Settings Issues:")
        for issue in settings_issues:
            print(f"   - {issue}")
    
    overall_success = all([env_ok, settings_ok, smtp_ok, django_email_ok, templates_ok, quote_function_ok])
    
    if overall_success:
        print("\n🎉 ALL TESTS PASSED - Email should be working!")
    else:
        print("\n❌ ISSUES FOUND - Email delivery will fail")
        print("🔧 Fix the failed tests above to resolve email issues")
    
    return overall_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
