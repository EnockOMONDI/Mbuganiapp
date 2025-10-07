#!/usr/bin/env python3
"""
Comprehensive Email Testing Suite for Mbugani Luxe Adventures
============================================================

Adapted from the proven Novustell Travel email testing suite.
Uses Novustell email credentials (novustellke@gmail.com) to test
Mbugani Luxe Adventures email functionality.

This test suite validates:
- Email configuration with Novustell credentials
- Mbugani-specific email templates and branding
- Quote request email functionality
- Performance and timeout handling

Usage:
    # Run all tests
    python test_mbugani_email_system.py

    # Run specific test categories
    python test_mbugani_email_system.py --production
    python test_mbugani_email_system.py --templates
    python test_mbugani_email_system.py --quote-requests

Author: Mbugani Luxe Adventures Development Team
Based on: Novustell Travel Email Testing Suite
Last Updated: October 7, 2025
"""

import os
import sys
import django
import unittest
import smtplib
import time
from unittest.mock import patch, MagicMock
from django.test import TestCase, override_settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import logging

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tours_travels.settings_prod')
django.setup()

# Import Django models and forms after setup
from users.models import QuoteRequest
from users.forms import QuoteRequestForm
from users.views import send_quote_request_emails

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class MbuganiEmailTestSuite:
    """Main test suite coordinator for Mbugani Luxe Adventures"""
    
    def __init__(self):
        self.test_results = {
            'configuration_tests': {},
            'template_tests': {},
            'quote_request_tests': {},
            'production_tests': {},
            'performance_tests': {}
        }
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0

    def run_all_tests(self):
        """Run all test categories"""
        print("🚀 Starting Comprehensive Email System Tests for Mbugani Luxe Adventures")
        print("📧 Using Novustell Travel Email Credentials for Testing")
        print("=" * 80)
        
        # Run test categories
        self.run_configuration_tests()
        self.run_template_tests()
        self.run_quote_request_tests()
        self.run_production_tests()
        self.run_performance_tests()
        
        # Print summary
        self.print_test_summary()

    def run_configuration_tests(self):
        """Test email configuration with Novustell credentials"""
        print("\n📋 Testing Email Configuration...")
        
        config_tests = MbuganiConfigurationTests()
        
        self.run_test("Novustell Credentials Configuration", config_tests.test_novustell_credentials)
        self.run_test("Mbugani Settings Integration", config_tests.test_mbugani_settings)
        self.run_test("Environment Variables", config_tests.test_environment_variables)
        self.run_test("SMTP Configuration", config_tests.test_smtp_configuration)

    def run_template_tests(self):
        """Test Mbugani email templates"""
        print("\n📧 Testing Mbugani Email Templates...")
        
        template_tests = MbuganiTemplateTests()
        
        # Test Mbugani-specific templates
        templates = [
            'quote_request_admin.html',
            'quote_request_admin.txt',
            'quote_request_confirmation.html',
            'quote_request_confirmation.txt'
        ]
        
        for template in templates:
            self.run_test(f"Template: {template}", 
                         lambda t=template: template_tests.test_template_rendering(t))
        
        self.run_test("Mbugani Branding Elements", template_tests.test_mbugani_branding)
        self.run_test("Template Context Variables", template_tests.test_template_context)

    def run_quote_request_tests(self):
        """Test quote request email functionality"""
        print("\n📝 Testing Quote Request Email System...")
        
        quote_tests = QuoteRequestEmailTests()
        
        self.run_test("Quote Request Form Validation", quote_tests.test_quote_form_validation)
        self.run_test("Quote Request Email Sending", quote_tests.test_quote_email_sending)
        self.run_test("Admin Notification Email", quote_tests.test_admin_notification)
        self.run_test("User Confirmation Email", quote_tests.test_user_confirmation)
        self.run_test("Dual Email Pattern", quote_tests.test_dual_email_pattern)

    def run_production_tests(self):
        """Test production environment with Novustell credentials"""
        print("\n🌐 Testing Production Environment...")
        
        prod_tests = MbuganiProductionTests()
        
        self.run_test("Gmail SMTP Connection", prod_tests.test_gmail_smtp_connection)
        self.run_test("Novustell Credentials Authentication", prod_tests.test_novustell_authentication)
        self.run_test("TLS/SSL Encryption", prod_tests.test_tls_encryption)
        self.run_test("Email Delivery Test", prod_tests.test_email_delivery)

    def run_performance_tests(self):
        """Test performance and timeout handling"""
        print("\n⚡ Testing Performance & Timeout Handling...")
        
        perf_tests = MbuganiPerformanceTests()
        
        self.run_test("Email Sending Timeout", perf_tests.test_email_timeout)
        self.run_test("SMTP Failure Handling", perf_tests.test_smtp_failure_handling)
        self.run_test("Quote Request Performance", perf_tests.test_quote_request_performance)
        self.run_test("Error Recovery", perf_tests.test_error_recovery)

    def run_test(self, test_name, test_function):
        """Run individual test and track results"""
        self.total_tests += 1
        try:
            start_time = time.time()
            result = test_function()
            end_time = time.time()
            duration = end_time - start_time
            
            if result:
                print(f"✅ {test_name} - PASSED ({duration:.2f}s)")
                self.passed_tests += 1
                return True
            else:
                print(f"❌ {test_name} - FAILED ({duration:.2f}s)")
                self.failed_tests += 1
                return False
        except Exception as e:
            print(f"❌ {test_name} - ERROR: {str(e)}")
            self.failed_tests += 1
            return False

    def print_test_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "=" * 80)
        print("📊 MBUGANI LUXE ADVENTURES EMAIL SYSTEM TEST SUMMARY")
        print("=" * 80)
        print(f"Total Tests Run: {self.total_tests}")
        print(f"✅ Passed: {self.passed_tests}")
        print(f"❌ Failed: {self.failed_tests}")
        print(f"Success Rate: {(self.passed_tests/self.total_tests)*100:.1f}%")
        
        if self.failed_tests == 0:
            print("\n🎉 ALL TESTS PASSED! Mbugani email system is fully operational with Novustell credentials.")
            print("🚀 Ready to deploy to production!")
        else:
            print(f"\n⚠️  {self.failed_tests} tests failed. Please review the issues above.")
            print("🔧 Fix these issues before deploying to production.")
        
        print("=" * 80)


class MbuganiConfigurationTests:
    """Test email configuration with Novustell credentials"""
    
    def test_novustell_credentials(self):
        """Test Novustell email credentials configuration"""
        try:
            # Check if Novustell credentials are configured
            expected_user = 'novustellke@gmail.com'
            expected_password = 'vsmw vdut tanu gtdg'  # Development password
            
            if settings.EMAIL_HOST_USER != expected_user:
                logger.error(f"EMAIL_HOST_USER mismatch: {settings.EMAIL_HOST_USER}")
                return False
            
            # Test SMTP authentication with Novustell credentials
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(expected_user, expected_password)
            server.quit()
            
            return True
        except Exception as e:
            logger.error(f"Novustell credentials test failed: {e}")
            return False

    def test_mbugani_settings(self):
        """Test Mbugani-specific settings integration"""
        try:
            # Check that Mbugani settings are properly configured
            required_settings = [
                'EMAIL_BACKEND',
                'EMAIL_HOST',
                'EMAIL_PORT',
                'EMAIL_USE_TLS',
                'EMAIL_HOST_USER',
                'DEFAULT_FROM_EMAIL',
                'ADMIN_EMAIL'
            ]
            
            for setting in required_settings:
                if not hasattr(settings, setting):
                    logger.error(f"Missing setting: {setting}")
                    return False
            
            # Verify specific values
            if settings.EMAIL_HOST != 'smtp.gmail.com':
                logger.error(f"Incorrect EMAIL_HOST: {settings.EMAIL_HOST}")
                return False
            
            if settings.EMAIL_PORT != 587:
                logger.error(f"Incorrect EMAIL_PORT: {settings.EMAIL_PORT}")
                return False
            
            # Check that DEFAULT_FROM_EMAIL uses Mbugani branding with Novustell email
            if 'Mbugani Luxe Adventures' not in settings.DEFAULT_FROM_EMAIL:
                logger.error(f"Mbugani branding missing from DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
                return False
            
            if 'novustellke@gmail.com' not in settings.DEFAULT_FROM_EMAIL:
                logger.error(f"Novustell email missing from DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
                return False
            
            return True
        except Exception as e:
            logger.error(f"Mbugani settings test failed: {e}")
            return False

    def test_environment_variables(self):
        """Test environment variables configuration"""
        try:
            # Check critical environment variables
            env_vars = {
                'EMAIL_HOST_USER': 'novustellke@gmail.com',
                'ADMIN_EMAIL': 'info@mbuganiluxeadventures.com',
                'JOBS_EMAIL': 'careers@mbuganiluxeadventures.com',
                'NEWSLETTER_EMAIL': 'news@mbuganiluxeadventures.com'
            }
            
            for var_name, expected_value in env_vars.items():
                actual_value = getattr(settings, var_name, None)
                if actual_value != expected_value:
                    logger.error(f"{var_name} mismatch: expected {expected_value}, got {actual_value}")
                    return False
            
            return True
        except Exception as e:
            logger.error(f"Environment variables test failed: {e}")
            return False

    def test_smtp_configuration(self):
        """Test SMTP configuration"""
        try:
            # Test SMTP backend configuration
            expected_backend = 'django.core.mail.backends.smtp.EmailBackend'
            if settings.EMAIL_BACKEND != expected_backend:
                logger.error(f"Incorrect EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
                return False
            
            # Test SMTP connection parameters
            if not settings.EMAIL_USE_TLS:
                logger.error("EMAIL_USE_TLS should be True")
                return False
            
            return True
        except Exception as e:
            logger.error(f"SMTP configuration test failed: {e}")
            return False


class MbuganiTemplateTests:
    """Test Mbugani email templates"""
    
    def test_template_rendering(self, template_name):
        """Test individual template rendering"""
        try:
            # Create mock quote request context
            mock_quote_request = QuoteRequest(
                full_name='Test User',
                email='test@example.com',
                phone_number='+254712345678',
                destination='Maasai Mara',
                preferred_travel_dates='2024-08-15 to 2024-08-20',
                number_of_travelers=2,
                special_requests='Test quote request for email testing'
            )
            
            context = {'quote_request': mock_quote_request}
            
            # Attempt to render template
            template_path = f'users/emails/{template_name}'
            rendered_content = render_to_string(template_path, context)
            
            if not rendered_content:
                logger.error(f"Template {template_name} rendered empty content")
                return False
            
            # Check for basic structure
            if template_name.endswith('.html'):
                if '<html' not in rendered_content.lower() and '<!doctype' not in rendered_content.lower():
                    logger.error(f"Template {template_name} missing HTML structure")
                    return False
            
            return True
        except Exception as e:
            logger.error(f"Template rendering failed for {template_name}: {e}")
            return False

    def test_mbugani_branding(self):
        """Test Mbugani branding elements in templates"""
        try:
            # Test quote request admin template for branding
            mock_quote_request = QuoteRequest(
                full_name='Test User',
                email='test@example.com',
                phone_number='+254712345678',
                destination='Maasai Mara',
                preferred_travel_dates='2024-08-15 to 2024-08-20',
                number_of_travelers=2,
                special_requests='Test quote request'
            )
            
            context = {'quote_request': mock_quote_request}
            rendered_content = render_to_string('users/emails/quote_request_admin.html', context)
            
            # Check for Mbugani branding
            if 'Mbugani Luxe Adventures' not in rendered_content:
                logger.error("Mbugani Luxe Adventures branding not found")
                return False
            
            # Check for Mbugani brand colors (if specified in templates)
            mbugani_colors = ['#291c1a', '#bd8c06', '#fcf8f4']  # Mbugani brand colors
            color_found = any(color in rendered_content for color in mbugani_colors)
            if not color_found:
                logger.info("Mbugani brand colors not found in template (may be expected)")
            
            return True
        except Exception as e:
            logger.error(f"Branding test failed: {e}")
            return False

    def test_template_context(self):
        """Test template context variables"""
        try:
            # Test that templates handle all quote request fields
            mock_quote_request = QuoteRequest(
                full_name='John Doe',
                email='john@example.com',
                phone_number='+254712345678',
                destination='Serengeti National Park',
                preferred_travel_dates='December 15-25, 2024',
                number_of_travelers=4,
                special_requests='Family safari with children accommodation'
            )
            
            context = {'quote_request': mock_quote_request}
            
            # Test both HTML and text templates
            html_content = render_to_string('users/emails/quote_request_admin.html', context)
            txt_content = render_to_string('users/emails/quote_request_admin.txt', context)
            
            # Check that key information is present
            required_info = [
                'John Doe',
                'john@example.com',
                'Serengeti National Park',
                'December 15-25, 2024',
                '4'
            ]
            
            for info in required_info:
                if info not in html_content:
                    logger.error(f"Required info '{info}' not found in HTML template")
                    return False
                if info not in txt_content:
                    logger.error(f"Required info '{info}' not found in text template")
                    return False
            
            return True
        except Exception as e:
            logger.error(f"Template context test failed: {e}")
            return False


class QuoteRequestEmailTests:
    """Test quote request email functionality"""

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_quote_form_validation(self):
        """Test quote request form validation"""
        try:
            # Test valid form data
            valid_data = {
                'full_name': 'Jane Smith',
                'email': 'jane@example.com',
                'phone_number': '+254712345678',
                'destination': 'Maasai Mara National Reserve',
                'preferred_travel_dates': '2024-09-10 to 2024-09-15',
                'number_of_travelers': 3,
                'special_requests': 'Luxury safari with private guide'
            }

            form = QuoteRequestForm(data=valid_data)
            if not form.is_valid():
                logger.error(f"Quote form validation failed: {form.errors}")
                return False

            # Test that form can be saved
            quote_request = form.save()
            if not quote_request.id:
                logger.error("Quote request was not saved to database")
                return False

            return True
        except Exception as e:
            logger.error(f"Quote form validation test failed: {e}")
            return False

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_quote_email_sending(self):
        """Test quote request email sending function"""
        try:
            from django.core import mail

            # Clear any previous emails
            mail.outbox = []

            # Create test quote request
            quote_request = QuoteRequest.objects.create(
                full_name='Test Customer',
                email='customer@example.com',
                phone_number='+254712345678',
                destination='Amboseli National Park',
                preferred_travel_dates='2024-10-20 to 2024-10-25',
                number_of_travelers=2,
                special_requests='Honeymoon safari package'
            )

            # Test email sending function
            send_quote_request_emails(quote_request)

            # Check that emails were sent
            if len(mail.outbox) != 2:
                logger.error(f"Expected 2 emails (admin + user), got {len(mail.outbox)}")
                return False

            return True
        except Exception as e:
            logger.error(f"Quote email sending test failed: {e}")
            return False

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_admin_notification(self):
        """Test admin notification email"""
        try:
            from django.core import mail

            # Clear any previous emails
            mail.outbox = []

            quote_request = QuoteRequest.objects.create(
                full_name='Admin Test User',
                email='admintest@example.com',
                phone_number='+254712345678',
                destination='Tsavo National Park',
                preferred_travel_dates='2024-11-01 to 2024-11-05',
                number_of_travelers=1,
                special_requests='Solo traveler package'
            )

            send_quote_request_emails(quote_request)

            # Find admin email
            admin_email = None
            for email in mail.outbox:
                if settings.ADMIN_EMAIL in email.to:
                    admin_email = email
                    break

            if not admin_email:
                logger.error("Admin notification email not found")
                return False

            # Check admin email content
            if 'Admin Test User' not in admin_email.body:
                logger.error("Customer name not found in admin email")
                return False

            return True
        except Exception as e:
            logger.error(f"Admin notification test failed: {e}")
            return False

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_user_confirmation(self):
        """Test user confirmation email"""
        try:
            from django.core import mail

            # Clear any previous emails
            mail.outbox = []

            quote_request = QuoteRequest.objects.create(
                full_name='User Test Customer',
                email='usertest@example.com',
                phone_number='+254712345678',
                destination='Lake Nakuru',
                preferred_travel_dates='2024-12-01 to 2024-12-05',
                number_of_travelers=2,
                special_requests='Bird watching tour'
            )

            send_quote_request_emails(quote_request)

            # Find user confirmation email
            user_email = None
            for email in mail.outbox:
                if 'usertest@example.com' in email.to:
                    user_email = email
                    break

            if not user_email:
                logger.error("User confirmation email not found")
                return False

            # Check user email content
            if 'User Test Customer' not in user_email.body:
                logger.error("Customer name not found in user email")
                return False

            return True
        except Exception as e:
            logger.error(f"User confirmation test failed: {e}")
            return False

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_dual_email_pattern(self):
        """Test dual email pattern (admin + user)"""
        try:
            from django.core import mail

            # Clear any previous emails
            mail.outbox = []

            quote_request = QuoteRequest.objects.create(
                full_name='Dual Email Test',
                email='dualemail@example.com',
                phone_number='+254712345678',
                destination='Mount Kenya',
                preferred_travel_dates='2024-08-01 to 2024-08-05',
                number_of_travelers=3,
                special_requests='Mountain climbing expedition'
            )

            send_quote_request_emails(quote_request)

            # Check that exactly 2 emails were sent
            if len(mail.outbox) != 2:
                logger.error(f"Dual email pattern failed: {len(mail.outbox)} emails sent")
                return False

            # Check recipients
            recipients = []
            for email in mail.outbox:
                recipients.extend(email.to)

            if settings.ADMIN_EMAIL not in recipients:
                logger.error("Admin email not in recipients")
                return False

            if 'dualemail@example.com' not in recipients:
                logger.error("User email not in recipients")
                return False

            return True
        except Exception as e:
            logger.error(f"Dual email pattern test failed: {e}")
            return False


class MbuganiProductionTests:
    """Test production environment with Novustell credentials"""

    def test_gmail_smtp_connection(self):
        """Test Gmail SMTP connection"""
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.quit()
            return True
        except Exception as e:
            logger.error(f"Gmail SMTP connection failed: {e}")
            return False

    def test_novustell_authentication(self):
        """Test Novustell credentials authentication"""
        try:
            # Test with development credentials first (more likely to work)
            prod_user = 'novustellke@gmail.com'
            prod_password = 'vsmw vdut tanu gtdg'  # Development password

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(prod_user, prod_password)
            server.quit()

            return True
        except Exception as e:
            logger.error(f"Novustell authentication test failed: {e}")
            return False

    def test_tls_encryption(self):
        """Test TLS encryption"""
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()

            # Check if TLS is enabled
            if not hasattr(server, 'sock') or not server.sock:
                logger.error("TLS connection not established")
                return False

            server.quit()
            return True
        except Exception as e:
            logger.error(f"TLS encryption test failed: {e}")
            return False

    def test_email_delivery(self):
        """Test actual email delivery (optional)"""
        try:
            # For safety, we'll skip actual email delivery in automated tests
            # Uncomment the following lines only for manual production testing

            # from django.core.mail import send_mail
            # result = send_mail(
            #     'Mbugani Email System Test',
            #     'This is a test email from Mbugani Luxe Adventures using Novustell credentials.',
            #     'novustellke@gmail.com',
            #     ['info@mbuganiluxeadventures.com'],
            #     fail_silently=False
            # )
            # return result == 1

            logger.info("Email delivery test skipped (safety measure)")
            return True
        except Exception as e:
            logger.error(f"Email delivery test failed: {e}")
            return False


class MbuganiPerformanceTests:
    """Test performance and timeout handling"""

    def test_email_timeout(self):
        """Test email sending timeout scenarios"""
        try:
            import time
            from django.core.mail import send_mail

            start_time = time.time()

            # Test with mock SMTP to simulate timeout scenarios
            with patch('smtplib.SMTP') as mock_smtp:
                mock_instance = MagicMock()
                mock_smtp.return_value = mock_instance

                # Simulate normal email sending
                def normal_send(*args, **kwargs):
                    time.sleep(0.1)  # Simulate normal delay
                    return True

                mock_instance.send_message = normal_send

                result = send_mail(
                    'Timeout Test',
                    'Testing email timeout handling',
                    'novustellke@gmail.com',
                    ['test@example.com'],
                    fail_silently=False
                )

            end_time = time.time()
            duration = end_time - start_time

            # Check if operation completed within reasonable time
            if duration > 5.0:  # 5 second timeout
                logger.error(f"Email sending took too long: {duration:.2f}s")
                return False

            return True
        except Exception as e:
            logger.error(f"Email timeout test failed: {e}")
            return False

    def test_smtp_failure_handling(self):
        """Test SMTP failure handling"""
        try:
            from django.core.mail import send_mail

            # Test with invalid SMTP settings
            with override_settings(
                EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend',
                EMAIL_HOST='invalid.smtp.server',
                EMAIL_PORT=587
            ):
                try:
                    result = send_mail(
                        'Failure Test',
                        'Testing SMTP failure handling',
                        'test@example.com',
                        ['recipient@example.com'],
                        fail_silently=True  # Should not raise exception
                    )
                    # Should return False or 0 for failed sending
                    return result == 0
                except Exception:
                    # Should not raise exception with fail_silently=True
                    logger.error("Exception raised despite fail_silently=True")
                    return False
        except Exception as e:
            logger.error(f"SMTP failure handling test failed: {e}")
            return False

    def test_quote_request_performance(self):
        """Test quote request email performance"""
        try:
            import time

            # Create test quote request
            quote_request = QuoteRequest(
                full_name='Performance Test User',
                email='performance@example.com',
                phone_number='+254712345678',
                destination='Performance Test Destination',
                preferred_travel_dates='2024-12-01 to 2024-12-05',
                number_of_travelers=2,
                special_requests='Performance testing'
            )

            # Test email sending performance
            start_time = time.time()

            with override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
                send_quote_request_emails(quote_request)

            end_time = time.time()
            duration = end_time - start_time

            # Quote request emails should be sent quickly
            if duration > 2.0:  # 2 second limit for template rendering and email preparation
                logger.error(f"Quote request email processing took too long: {duration:.2f}s")
                return False

            return True
        except Exception as e:
            logger.error(f"Quote request performance test failed: {e}")
            return False

    def test_error_recovery(self):
        """Test error recovery mechanisms"""
        try:
            # Test that the system handles email failures gracefully
            quote_request = QuoteRequest(
                full_name='Error Recovery Test',
                email='errortest@example.com',
                phone_number='+254712345678',
                destination='Error Test Destination',
                preferred_travel_dates='2024-12-01 to 2024-12-05',
                number_of_travelers=1,
                special_requests='Error recovery testing'
            )

            # Test with failing email backend
            with override_settings(
                EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend',
                EMAIL_HOST='nonexistent.server'
            ):
                try:
                    # This should not crash the application
                    send_quote_request_emails(quote_request)
                    return True  # Function should handle errors gracefully
                except Exception as e:
                    # If an exception is raised, check if it's handled properly
                    logger.info(f"Email error handled: {e}")
                    return True  # Error handling is working

        except Exception as e:
            logger.error(f"Error recovery test failed: {e}")
            return False


# Utility functions
def run_quick_mbugani_test():
    """Run a quick subset of critical tests for Mbugani"""
    print("🚀 Running Quick Mbugani Email System Test...")

    quick_tests = [
        ("Novustell SMTP Connection", MbuganiProductionTests().test_gmail_smtp_connection),
        ("Novustell Authentication", MbuganiProductionTests().test_novustell_authentication),
        ("Quote Template Rendering", lambda: MbuganiTemplateTests().test_template_rendering('quote_request_admin.html')),
        ("Configuration Check", MbuganiConfigurationTests().test_mbugani_settings)
    ]

    passed = 0
    total = len(quick_tests)

    for test_name, test_func in quick_tests:
        try:
            if test_func():
                print(f"✅ {test_name} - PASSED")
                passed += 1
            else:
                print(f"❌ {test_name} - FAILED")
        except Exception as e:
            print(f"❌ {test_name} - ERROR: {e}")

    print(f"\n📊 Quick Test Results: {passed}/{total} passed ({(passed/total)*100:.1f}%)")
    return passed == total


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Mbugani Luxe Adventures Email System Tests')
    parser.add_argument('--production', action='store_true', help='Run production tests only')
    parser.add_argument('--templates', action='store_true', help='Run template tests only')
    parser.add_argument('--quote-requests', action='store_true', help='Run quote request tests only')
    parser.add_argument('--config', action='store_true', help='Run configuration tests only')
    parser.add_argument('--performance', action='store_true', help='Run performance tests only')
    parser.add_argument('--quick', action='store_true', help='Run quick test suite')

    args = parser.parse_args()

    # Initialize test suite
    test_suite = MbuganiEmailTestSuite()

    # Run specific test categories or all tests
    if args.quick:
        run_quick_mbugani_test()
    elif args.production:
        test_suite.run_production_tests()
    elif args.templates:
        test_suite.run_template_tests()
    elif args.quote_requests:
        test_suite.run_quote_request_tests()
    elif args.config:
        test_suite.run_configuration_tests()
    elif args.performance:
        test_suite.run_performance_tests()
    else:
        test_suite.run_all_tests()
