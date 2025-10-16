#!/usr/bin/env python3
"""
Render Diagnostics and Log Checker
Helps diagnose issues with the Mbugani Luxe Adventures deployment
"""

import requests
import json
import time
from datetime import datetime, timedelta

def check_render_service_status():
    """Check if the Render service is accessible"""
    print("🌐 CHECKING RENDER SERVICE STATUS")
    print("=" * 50)
    
    urls_to_check = [
        "https://www.mbuganiluxeadventures.com",
        "https://mbuganiapp.onrender.com",
        "https://www.mbuganiluxeadventures.com/health/",
        "https://www.mbuganiluxeadventures.com/quote/",
    ]
    
    for url in urls_to_check:
        try:
            print(f"\n🔍 Testing: {url}")
            start_time = time.time()
            response = requests.get(url, timeout=30)
            end_time = time.time()
            
            response_time = end_time - start_time
            print(f"   Status: {response.status_code}")
            print(f"   Response Time: {response_time:.2f}s")
            
            if response.status_code == 200:
                print("   ✅ Service is accessible")
            elif response.status_code == 404:
                print("   ⚠️  Page not found (might be expected)")
            elif response.status_code >= 500:
                print("   ❌ Server error detected")
            else:
                print(f"   ⚠️  Unexpected status: {response.status_code}")
                
        except requests.exceptions.Timeout:
            print("   ❌ Request timed out")
        except requests.exceptions.ConnectionError:
            print("   ❌ Connection failed")
        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_quote_request_submission():
    """Test quote request submission to identify the exact error"""
    print("\n📝 TESTING QUOTE REQUEST SUBMISSION")
    print("=" * 50)
    
    base_url = "https://www.mbuganiluxeadventures.com"
    quote_url = f"{base_url}/quote/"
    
    session = requests.Session()
    
    try:
        # Step 1: Get the form
        print("📋 Step 1: Loading quote request form...")
        response = session.get(quote_url, timeout=30)
        print(f"   Form load status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"   ❌ Cannot load form: {response.status_code}")
            return False
        
        # Extract CSRF token
        csrf_token = None
        if 'csrfmiddlewaretoken' in response.text:
            import re
            csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
            if csrf_match:
                csrf_token = csrf_match.group(1)
                print(f"   ✅ CSRF token obtained")
        
        # Step 2: Submit the form
        print("\n📤 Step 2: Submitting quote request...")
        
        form_data = {
            'full_name': 'Test User - Diagnostic',
            'email': 'test@mbuganiluxeadventures.com',
            'phone_number': '+254712345678',
            'destination': 'Maasai Mara',
            'preferred_travel_dates': '2024-08-15 to 2024-08-20',
            'number_of_travelers': 2,
            'special_requests': 'This is a diagnostic test submission - please ignore'
        }
        
        if csrf_token:
            form_data['csrfmiddlewaretoken'] = csrf_token
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Diagnostic Tool)',
            'Referer': quote_url,
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        
        print("   Submitting form data...")
        start_time = time.time()
        
        try:
            response = session.post(quote_url, data=form_data, headers=headers, timeout=60)
            end_time = time.time()
            
            response_time = end_time - start_time
            print(f"   Response status: {response.status_code}")
            print(f"   Response time: {response_time:.2f}s")
            print(f"   Final URL: {response.url}")
            
            if response.status_code == 200:
                if 'Thank you' in response.text or 'success' in response.text.lower():
                    print("   ✅ Quote request successful!")
                    return True
                else:
                    print("   ⚠️  Form processed but no success message found")
                    # Check for error messages
                    if 'error' in response.text.lower():
                        print("   ❌ Error indicators found in response")
            elif response.status_code == 302:
                print("   ✅ Quote request redirected (likely successful)")
                return True
            elif response.status_code == 500:
                print("   ❌ Internal Server Error (500)")
                print("   🔍 This is the error we need to fix!")
                
                # Show response content for debugging
                print(f"\n📄 Error Response (first 500 chars):")
                print(response.text[:500])
                return False
            else:
                print(f"   ❌ Unexpected status: {response.status_code}")
                return False
                
        except requests.exceptions.Timeout:
            print("   ❌ Request timed out (>60 seconds)")
            print("   🔍 This suggests a server-side timeout issue")
            return False
            
    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        return False

def check_environment_variables():
    """Check critical environment variables"""
    print("\n🔧 ENVIRONMENT VARIABLES STATUS")
    print("=" * 50)
    
    print("📋 Critical variables that should be set in Render:")
    critical_vars = [
        "DATABASE_URL",
        "EMAIL_HOST_USER", 
        "EMAIL_HOST_PASSWORD",
        "DEFAULT_FROM_EMAIL",
        "ADMIN_EMAIL",
        "UPLOADCARE_PUBLIC_KEY",
        "UPLOADCARE_SECRET_KEY",
        "SECRET_KEY",
        "DEBUG",
        "ALLOWED_HOSTS"
    ]
    
    for var in critical_vars:
        print(f"   • {var}")
    
    print("\n⚠️  UPLOADCARE KEYS MUST BE SET MANUALLY:")
    print("   1. Go to Render Dashboard")
    print("   2. Select your Mbuganiapp service")
    print("   3. Go to Environment tab")
    print("   4. Add these variables:")
    print("      - UPLOADCARE_PUBLIC_KEY: 6fb55bb425b16d386db6")
    print("      - UPLOADCARE_SECRET_KEY: 3086089d3d2ac096684d")

def render_logs_instructions():
    """Provide instructions for checking Render logs"""
    print("\n📊 HOW TO CHECK RENDER LOGS")
    print("=" * 50)
    
    print("🌐 Via Render Dashboard:")
    print("   1. Go to https://dashboard.render.com")
    print("   2. Select your 'Mbuganiapp' service")
    print("   3. Click on 'Logs' tab")
    print("   4. Look for recent errors around quote request submissions")
    print("   5. Filter by 'Error' level to see only errors")
    
    print("\n🔍 What to look for in logs:")
    print("   • HTTP 500 errors")
    print("   • Email sending errors")
    print("   • Database connection errors")
    print("   • Timeout errors")
    print("   • SMTP authentication errors")
    print("   • Template rendering errors")
    
    print("\n📝 Common error patterns:")
    print("   • 'SMTPAuthenticationError'")
    print("   • 'socket.timeout'")
    print("   • 'ConnectionRefusedError'")
    print("   • 'TemplateDoesNotExist'")
    print("   • 'DatabaseError'")
    
    print("\n⚡ Real-time log monitoring:")
    print("   • Keep the logs tab open")
    print("   • Submit a quote request on the website")
    print("   • Watch for errors in real-time")

def deployment_checklist():
    """Provide deployment checklist"""
    print("\n✅ DEPLOYMENT CHECKLIST")
    print("=" * 50)
    
    checklist = [
        ("Environment Variables", "Set all critical variables in Render dashboard"),
        ("UPLOADCARE Keys", "Manually add UPLOADCARE_PUBLIC_KEY and UPLOADCARE_SECRET_KEY"),
        ("Database Connection", "Verify Supabase PostgreSQL connection"),
        ("Email Configuration", "Test Gmail SMTP with app password"),
        ("Static Files", "Ensure static files are collected properly"),
        ("Health Check", "Verify /health/ endpoint responds"),
        ("Domain Configuration", "Check custom domain DNS settings"),
        ("SSL Certificate", "Verify HTTPS is working"),
        ("Logs Monitoring", "Check for any startup errors"),
        ("Quote Request Test", "Test quote submission after deployment")
    ]
    
    for i, (item, description) in enumerate(checklist, 1):
        print(f"   {i:2d}. ✅ {item}")
        print(f"       {description}")

def main():
    """Main diagnostic function"""
    print("🚀 MBUGANI LUXE ADVENTURES - RENDER DIAGNOSTICS")
    print("=" * 60)
    print(f"🕐 Diagnostic Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run all diagnostic checks
    check_render_service_status()
    
    # Test quote request
    quote_success = test_quote_request_submission()
    
    # Environment variables check
    check_environment_variables()
    
    # Render logs instructions
    render_logs_instructions()
    
    # Deployment checklist
    deployment_checklist()
    
    # Summary
    print(f"\n🎯 DIAGNOSTIC SUMMARY")
    print("=" * 50)
    
    if quote_success:
        print("✅ Quote request system is working!")
        print("🎉 No immediate issues detected")
    else:
        print("❌ Quote request system has issues")
        print("🔧 Follow the troubleshooting steps above")
        print("\n🚨 IMMEDIATE ACTIONS NEEDED:")
        print("   1. Check Render logs for specific error messages")
        print("   2. Verify UPLOADCARE keys are set in Render dashboard")
        print("   3. Test email configuration")
        print("   4. Check database connectivity")
    
    print(f"\n📞 SUPPORT:")
    print("   • Check Render documentation: https://render.com/docs")
    print("   • Review Django logs for detailed error information")
    print("   • Test individual components (database, email, templates)")

if __name__ == "__main__":
    main()
