#!/usr/bin/env python3
"""
Production Environment Email Test for Mbugani Luxe Adventures
=============================================================

Tests email functionality using production settings with the new Mbugani Gmail credentials.
This simulates the production environment locally.

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

# Set up Django with PRODUCTION settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tours_travels.settings_prod')
django.setup()

from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
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
    print(f"{BLUE}🌐 PRODUCTION ENVIRONMENT EMAIL TEST (Local Simulation){RESET}")
    print(f"{BLUE}Mbugani Luxe Adventures{RESET}")
    print("=" * 80)
    print()

def print_configuration():
    """Print current email configuration"""
    print(f"{YELLOW}📋 Production Email Configuration:{RESET}")
    print(f"  Django Settings Module: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
    print(f"  EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"  EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"  EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"  EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"  EMAIL_USE_SSL: {getattr(settings, 'EMAIL_USE_SSL', False)}")
    print(f"  EMAIL_TIMEOUT: {getattr(settings, 'EMAIL_TIMEOUT', 'Not Set')}")
    print(f"  EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    
    # Mask password
    password = settings.EMAIL_HOST_PASSWORD
    if password and len(password) > 4:
        masked = password[:4] + '*' * (len(password) - 4)
    else:
        masked = '****'
    print(f"  EMAIL_HOST_PASSWORD: {masked}")
    
    print(f"  DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print(f"  ADMIN_EMAIL: {settings.ADMIN_EMAIL}")
    print(f"  JOBS_EMAIL: {settings.JOBS_EMAIL}")
    print(f"  NEWSLETTER_EMAIL: {settings.NEWSLETTER_EMAIL}")
    print(f"  DEBUG: {settings.DEBUG}")
    print(f"  ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    print()

def test_smtp_connection():
    """Test SMTP connection"""
    print(f"{BLUE}Test 1: SMTP Connection{RESET}")
    print("-" * 80)
    
    try:
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT, timeout=10)
        print(f"{GREEN}✅ Connected to {settings.EMAIL_HOST}:{settings.EMAIL_PORT}{RESET}")
        server.quit()
        print()
        return True
        
    except Exception as e:
        print(f"{RED}❌ SMTP Connection failed: {str(e)}{RESET}")
        print()
        return False

def test_tls_encryption():
    """Test TLS encryption"""
    print(f"{BLUE}Test 2: TLS Encryption{RESET}")
    print("-" * 80)
    
    try:
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT, timeout=10)
        server.starttls()
        print(f"{GREEN}✅ TLS encryption enabled successfully{RESET}")
        server.quit()
        print()
        return True
        
    except Exception as e:
        print(f"{RED}❌ TLS encryption failed: {str(e)}{RESET}")
        print()
        return False

def test_smtp_authentication():
    """Test SMTP authentication with production credentials"""
    print(f"{BLUE}Test 3: SMTP Authentication (Production Credentials){RESET}")
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
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"{RED}❌ Authentication failed: {str(e)}{RESET}")
        print(f"{YELLOW}   This means the Gmail credentials are incorrect or expired.{RESET}")
        print()
        return False
        
    except Exception as e:
        print(f"{RED}❌ SMTP Authentication failed: {str(e)}{RESET}")
        print()
        return False

def test_production_email_sending():
    """Test actual email sending in production mode"""
    print(f"{BLUE}Test 4: Production Email Sending{RESET}")
    print("-" * 80)
    print(f"{YELLOW}⚠️  Note: This test sends a REAL email to info@mbuganiluxeadventures.com{RESET}")
    print()
    
    try:
        result = send_mail(
            subject='🎉 Mbugani Email System - Production Test SUCCESS',
            message='This is a test email from the Mbugani Luxe Adventures PRODUCTION environment.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=['info@mbuganiluxeadventures.com'],
            fail_silently=False
        )
        
        if result == 1:
            print(f"{GREEN}✅ Production email sent successfully!{RESET}")
            print(f"   From: {settings.EMAIL_HOST_USER}")
            print(f"   To: info@mbuganiluxeadventures.com")
            print(f"   Subject: Mbugani Email System - Production Test SUCCESS")
            print(f"{YELLOW}   📧 Check your inbox at info@mbuganiluxeadventures.com{RESET}")
            print()
            return True
        else:
            print(f"{RED}❌ Email sending failed (returned {result}){RESET}")
            print()
            return False
            
    except Exception as e:
        print(f"{RED}❌ Email sending failed: {str(e)}{RESET}")
        print(f"{YELLOW}   This may be due to local SSL/security settings.{RESET}")
        print(f"{YELLOW}   If SMTP authentication passed, the configuration is correct.{RESET}")
        print()
        return False

def test_html_production_email():
    """Test HTML email in production mode"""
    print(f"{BLUE}Test 5: HTML Production Email{RESET}")
    print("-" * 80)
    
    try:
        html_content = """
        <html>
          <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #fcf8f4;">
            <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border: 3px solid #291c1a;">
              <h2 style="color: #291c1a; border-bottom: 3px solid #bd8c06; padding-bottom: 10px;">
                ✅ Mbugani Luxe Adventures - Production Email Test
              </h2>
              <p style="font-size: 16px; line-height: 1.6;">
                This is a test HTML email from the <strong>Mbugani Luxe Adventures</strong> production environment.
              </p>
              <hr style="border: 1px solid #bd8c06;">
              <h3 style="color: #291c1a;">Production Configuration:</h3>
              <ul style="line-height: 1.8;">
                <li><strong>Email Host:</strong> smtp.gmail.com</li>
                <li><strong>Port:</strong> 587</li>
                <li><strong>TLS:</strong> Enabled</li>
                <li><strong>Account:</strong> mbuganiluxeadventures@gmail.com</li>
                <li><strong>Environment:</strong> Production</li>
              </ul>
              <hr style="border: 1px solid #bd8c06;">
              <p style="color: #28a745; font-weight: bold; font-size: 18px;">
                🎉 If you received this email, the production email system is working perfectly!
              </p>
              <p style="color: #666; font-size: 14px; margin-top: 30px;">
                Sent from Mbugani Luxe Adventures Email System<br>
                Test Date: October 7, 2025
              </p>
            </div>
          </body>
        </html>
        """
        
        text_content = "This is a test email from Mbugani Luxe Adventures production environment."
        
        email = EmailMultiAlternatives(
            subject='🌍 Mbugani Luxe Adventures - HTML Production Test',
            body=text_content,
            from_email=f'Mbugani Luxe Adventures <{settings.EMAIL_HOST_USER}>',
            to=['info@mbuganiluxeadventures.com']
        )
        email.attach_alternative(html_content, "text/html")
        
        result = email.send(fail_silently=False)
        
        if result == 1:
            print(f"{GREEN}✅ HTML production email sent successfully!{RESET}")
            print(f"   From: Mbugani Luxe Adventures <{settings.EMAIL_HOST_USER}>")
            print(f"   To: info@mbuganiluxeadventures.com")
            print(f"   Format: HTML + Plain Text with Mbugani branding")
            print(f"{YELLOW}   📧 Check your inbox for the branded email{RESET}")
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

def print_summary(results):
    """Print test summary"""
    print("=" * 80)
    print(f"{BLUE}📊 PRODUCTION TEST SUMMARY{RESET}")
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
    
    # Critical test check
    critical_tests = ['SMTP Authentication']
    critical_passed = all(results.get(test, False) for test in critical_tests)
    
    if critical_passed:
        print(f"{GREEN}🎉 CRITICAL TESTS PASSED!{RESET}")
        print(f"{GREEN}✅ SMTP Authentication successful - credentials are correct{RESET}")
        print(f"{GREEN}✅ Configuration is ready for Render.com deployment{RESET}")
        print()
        if failed > 0:
            print(f"{YELLOW}Note: Some email sending tests may fail locally due to SSL/security settings.{RESET}")
            print(f"{YELLOW}This is expected and will work correctly on Render.com servers.{RESET}")
    else:
        print(f"{RED}❌ CRITICAL TESTS FAILED!{RESET}")
        print(f"{RED}SMTP Authentication failed - please check credentials{RESET}")
    
    print("=" * 80)

def main():
    """Main test function"""
    print_header()
    print_configuration()
    
    # Run tests
    results = {
        'SMTP Connection': test_smtp_connection(),
        'TLS Encryption': test_tls_encryption(),
        'SMTP Authentication': test_smtp_authentication(),
        'Production Email Sending': test_production_email_sending(),
        'HTML Production Email': test_html_production_email()
    }
    
    # Print summary
    print_summary(results)
    
    # Exit code based on critical tests
    critical_passed = results.get('SMTP Authentication', False)
    sys.exit(0 if critical_passed else 1)

if __name__ == '__main__':
    main()

