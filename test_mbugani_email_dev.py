#!/usr/bin/env python3
"""
Development Environment Email Test for Mbugani Luxe Adventures
==============================================================

Tests email functionality using development settings with the new Mbugani Gmail credentials.

Author: Mbugani Luxe Adventures Development Team
Date: October 7, 2025
"""

import os
import sys
import django
from pathlib import Path

# Add project to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Set up Django with development settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tours_travels.settings')
django.setup()

from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
import smtplib

# Color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header():
    """Print test header"""
    print("=" * 80)
    print(f"{BLUE}🧪 DEVELOPMENT ENVIRONMENT EMAIL TEST{RESET}")
    print(f"{BLUE}Mbugani Luxe Adventures{RESET}")
    print("=" * 80)
    print()

def print_configuration():
    """Print current email configuration"""
    print(f"{YELLOW}📋 Current Email Configuration:{RESET}")
    print(f"  Django Settings Module: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
    print(f"  EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"  EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"  EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"  EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"  EMAIL_USE_SSL: {getattr(settings, 'EMAIL_USE_SSL', False)}")
    print(f"  EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"  DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print(f"  ADMIN_EMAIL: {settings.ADMIN_EMAIL}")
    print(f"  JOBS_EMAIL: {settings.JOBS_EMAIL}")
    print(f"  NEWSLETTER_EMAIL: {settings.NEWSLETTER_EMAIL}")
    print(f"  DEBUG: {settings.DEBUG}")
    print()

def test_smtp_authentication():
    """Test SMTP authentication"""
    print(f"{BLUE}Test 1: SMTP Authentication{RESET}")
    print("-" * 80)
    
    try:
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT, timeout=10)
        print(f"{GREEN}✅ Connected to {settings.EMAIL_HOST}:{settings.EMAIL_PORT}{RESET}")
        
        server.starttls()
        print(f"{GREEN}✅ TLS encryption enabled{RESET}")
        
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        print(f"{GREEN}✅ Authentication successful with {settings.EMAIL_HOST_USER}{RESET}")
        
        server.quit()
        print(f"{GREEN}✅ Connection closed cleanly{RESET}")
        print()
        return True
        
    except Exception as e:
        print(f"{RED}❌ SMTP Authentication failed: {str(e)}{RESET}")
        print()
        return False

def test_simple_email():
    """Test sending a simple email"""
    print(f"{BLUE}Test 2: Simple Email Sending{RESET}")
    print("-" * 80)
    
    try:
        result = send_mail(
            subject='Mbugani Email System Test - Development',
            message='This is a test email from the Mbugani Luxe Adventures development environment.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=['info@mbuganiluxeadventures.com'],
            fail_silently=False
        )
        
        if result == 1:
            print(f"{GREEN}✅ Simple email sent successfully{RESET}")
            print(f"   From: {settings.EMAIL_HOST_USER}")
            print(f"   To: info@mbuganiluxeadventures.com")
            print()
            return True
        else:
            print(f"{RED}❌ Email sending failed (returned {result}){RESET}")
            print()
            return False
            
    except Exception as e:
        print(f"{RED}❌ Email sending failed: {str(e)}{RESET}")
        print()
        return False

def test_html_email():
    """Test sending HTML email with template"""
    print(f"{BLUE}Test 3: HTML Email with Template{RESET}")
    print("-" * 80)
    
    try:
        # Create HTML content
        html_content = """
        <html>
          <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2 style="color: #291c1a;">✅ Mbugani Email System Test</h2>
            <p>This is a test HTML email from the <strong>Mbugani Luxe Adventures</strong> development environment.</p>
            <hr>
            <p><strong>Configuration Details:</strong></p>
            <ul>
              <li>Email Host: smtp.gmail.com</li>
              <li>Port: 587</li>
              <li>TLS: Enabled</li>
              <li>Account: mbuganiluxeadventures@gmail.com</li>
            </ul>
            <hr>
            <p style="color: #28a745;">If you received this email, the development email system is working correctly!</p>
          </body>
        </html>
        """
        
        text_content = "This is a test email from Mbugani Luxe Adventures development environment."
        
        # Create email
        email = EmailMultiAlternatives(
            subject='Mbugani HTML Email Test - Development',
            body=text_content,
            from_email=f'Mbugani Luxe Adventures <{settings.EMAIL_HOST_USER}>',
            to=['info@mbuganiluxeadventures.com']
        )
        email.attach_alternative(html_content, "text/html")
        
        # Send email
        result = email.send(fail_silently=False)
        
        if result == 1:
            print(f"{GREEN}✅ HTML email sent successfully{RESET}")
            print(f"   From: Mbugani Luxe Adventures <{settings.EMAIL_HOST_USER}>")
            print(f"   To: info@mbuganiluxeadventures.com")
            print(f"   Format: HTML + Plain Text")
            print()
            return True
        else:
            print(f"{RED}❌ HTML email sending failed (returned {result}){RESET}")
            print()
            return False
            
    except Exception as e:
        print(f"{RED}❌ HTML email sending failed: {str(e)}{RESET}")
        print()
        return False

def test_dual_email_pattern():
    """Test dual email pattern (admin + client)"""
    print(f"{BLUE}Test 4: Dual Email Pattern (Admin + Client){RESET}")
    print("-" * 80)
    
    try:
        # Admin email
        admin_result = send_mail(
            subject='Admin Notification - Test',
            message='This is a test admin notification email.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False
        )
        
        # Client email
        client_result = send_mail(
            subject='Client Confirmation - Test',
            message='This is a test client confirmation email.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=['info@mbuganiluxeadventures.com'],
            fail_silently=False
        )
        
        if admin_result == 1 and client_result == 1:
            print(f"{GREEN}✅ Dual email pattern successful{RESET}")
            print(f"   Admin email sent to: {settings.ADMIN_EMAIL}")
            print(f"   Client email sent to: info@mbuganiluxeadventures.com")
            print()
            return True
        else:
            print(f"{RED}❌ Dual email pattern failed{RESET}")
            print(f"   Admin result: {admin_result}")
            print(f"   Client result: {client_result}")
            print()
            return False
            
    except Exception as e:
        print(f"{RED}❌ Dual email pattern failed: {str(e)}{RESET}")
        print()
        return False

def print_summary(results):
    """Print test summary"""
    print("=" * 80)
    print(f"{BLUE}📊 DEVELOPMENT TEST SUMMARY{RESET}")
    print("=" * 80)
    
    total = len(results)
    passed = sum(results.values())
    failed = total - passed
    
    print(f"Total Tests: {total}")
    print(f"{GREEN}Passed: {passed}{RESET}")
    print(f"{RED}Failed: {failed}{RESET}")
    print()
    
    for test_name, result in results.items():
        status = f"{GREEN}✅ PASSED{RESET}" if result else f"{RED}❌ FAILED{RESET}"
        print(f"  {test_name}: {status}")
    
    print()
    if failed == 0:
        print(f"{GREEN}🎉 ALL DEVELOPMENT TESTS PASSED!{RESET}")
        print(f"{GREEN}The email system is ready for production deployment.{RESET}")
    else:
        print(f"{YELLOW}⚠️  {failed} test(s) failed. Please review the errors above.{RESET}")
    
    print("=" * 80)

def main():
    """Main test function"""
    print_header()
    print_configuration()
    
    # Run tests
    results = {
        'SMTP Authentication': test_smtp_authentication(),
        'Simple Email': test_simple_email(),
        'HTML Email': test_html_email(),
        'Dual Email Pattern': test_dual_email_pattern()
    }
    
    # Print summary
    print_summary(results)
    
    # Exit with appropriate code
    sys.exit(0 if all(results.values()) else 1)

if __name__ == '__main__':
    main()

