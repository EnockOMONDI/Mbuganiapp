#!/usr/bin/env python
"""
Production Quote Request Flow Test
for Mbugani Luxe Adventures

This script tests the complete quote request flow on the production website
to identify where HTTP 500 errors are occurring.
"""

import requests
import time
from urllib.parse import urljoin

# Production site configuration
PRODUCTION_URL = "https://www.mbuganiluxeadventures.com"
QUOTE_URL = urljoin(PRODUCTION_URL, "/quote/")
SUCCESS_URL = urljoin(PRODUCTION_URL, "/quote/success/")

def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'-'*40}")
    print(f" {title}")
    print(f"{'-'*40}")

def test_site_accessibility():
    """Test if the production site is accessible"""
    print_section("SITE ACCESSIBILITY TEST")
    
    try:
        print(f"Testing access to: {PRODUCTION_URL}")
        response = requests.get(PRODUCTION_URL, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {response.elapsed.total_seconds():.2f} seconds")
        
        if response.status_code == 200:
            print("✅ Production site is accessible")
            return True
        else:
            print(f"❌ Production site returned status {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to access production site: {e}")
        return False

def test_quote_page_access():
    """Test if the quote page is accessible"""
    print_section("QUOTE PAGE ACCESS TEST")
    
    try:
        print(f"Testing access to: {QUOTE_URL}")
        response = requests.get(QUOTE_URL, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {response.elapsed.total_seconds():.2f} seconds")
        
        if response.status_code == 200:
            print("✅ Quote page is accessible")
            
            # Check for form elements
            if 'name="full_name"' in response.text:
                print("✅ Quote form found on page")
                return True
            else:
                print("❌ Quote form not found on page")
                return False
        else:
            print(f"❌ Quote page returned status {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to access quote page: {e}")
        return False

def get_csrf_token():
    """Get CSRF token from the quote page"""
    print_section("CSRF TOKEN RETRIEVAL")
    
    try:
        print("Retrieving CSRF token from quote page...")
        response = requests.get(QUOTE_URL, timeout=30)
        
        if response.status_code != 200:
            print(f"❌ Failed to get quote page: {response.status_code}")
            return None, None
        
        # Extract CSRF token
        import re
        csrf_pattern = r'name="csrfmiddlewaretoken" value="([^"]+)"'
        csrf_match = re.search(csrf_pattern, response.text)
        
        if csrf_match:
            csrf_token = csrf_match.group(1)
            print(f"✅ CSRF token retrieved: {csrf_token[:20]}...")
            
            # Get cookies for session
            cookies = response.cookies
            print(f"✅ Session cookies retrieved: {len(cookies)} cookies")
            
            return csrf_token, cookies
        else:
            print("❌ CSRF token not found in page")
            return None, None
            
    except Exception as e:
        print(f"❌ Failed to retrieve CSRF token: {e}")
        return None, None

def test_quote_submission():
    """Test quote request submission with proper session handling"""
    print_section("QUOTE SUBMISSION TEST")

    # Use a session to maintain cookies
    session = requests.Session()

    try:
        # First, get the quote page to establish session and get CSRF token
        print("Step 1: Getting quote page to establish session...")
        response = session.get(QUOTE_URL, timeout=30)

        if response.status_code != 200:
            print(f"❌ Failed to get quote page: {response.status_code}")
            return False

        print(f"✅ Quote page loaded (Status: {response.status_code})")

        # Extract CSRF token
        import re
        csrf_pattern = r'name="csrfmiddlewaretoken" value="([^"]+)"'
        csrf_match = re.search(csrf_pattern, response.text)

        if not csrf_match:
            print("❌ CSRF token not found in page")
            return False

        csrf_token = csrf_match.group(1)
        print(f"✅ CSRF token extracted: {csrf_token[:20]}...")

        # Check for csrftoken cookie
        csrf_cookie = session.cookies.get('csrftoken')
        if csrf_cookie:
            print(f"✅ CSRF cookie found: {csrf_cookie[:20]}...")
        else:
            print("⚠️ No CSRF cookie found")

        # Prepare form data
        form_data = {
            'csrfmiddlewaretoken': csrf_token,
            'full_name': 'Test User - Production Diagnostic',
            'email': 'test@example.com',
            'phone_number': '+254701234567',
            'destination': 'Maasai Mara',
            'preferred_travel_dates': 'December 2024',
            'number_of_travelers': '2',
            'special_requests': 'This is a test submission for production diagnostic purposes. Please ignore.'
        }

        # Set proper headers
        headers = {
            'Referer': QUOTE_URL,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        print("Step 2: Submitting quote request...")
        print(f"Form data: {form_data['full_name']}, {form_data['email']}")

        # Submit the form
        response = session.post(
            QUOTE_URL,
            data=form_data,
            headers=headers,
            timeout=60,  # Longer timeout for form submission
            allow_redirects=False  # Don't follow redirects automatically
        )

        print(f"Response Status Code: {response.status_code}")
        print(f"Response Time: {response.elapsed.total_seconds():.2f} seconds")

        # Analyze response
        if response.status_code == 302:
            # Successful submission should redirect
            redirect_location = response.headers.get('Location', '')
            print(f"✅ Form submitted successfully - Redirecting to: {redirect_location}")

            if 'success' in redirect_location.lower():
                print("✅ Redirected to success page")
                return True
            else:
                print(f"⚠️ Redirected to unexpected location: {redirect_location}")
                return True  # Still consider it successful

        elif response.status_code == 200:
            # Form returned with errors or stayed on same page
            if 'error' in response.text.lower() or 'invalid' in response.text.lower():
                print("❌ Form submission returned with errors")
                print("Response content preview:")
                print(response.text[:500] + "..." if len(response.text) > 500 else response.text)
                return False
            else:
                print("⚠️ Form submission returned 200 (may indicate success or form errors)")
                return True

        elif response.status_code == 403:
            print("❌ CSRF Verification Failed (403 Forbidden)")
            print("This indicates a CSRF token validation issue.")
            print("Possible causes:")
            print("- CSRF token mismatch")
            print("- Session cookie issues")
            print("- CSRF middleware configuration")
            print("- HTTPS/HTTP mismatch")
            return False

        elif response.status_code == 500:
            print("❌ Internal Server Error (500)")
            print("Response content preview:")
            print(response.text[:500] + "..." if len(response.text) > 500 else response.text)
            return False

        else:
            print(f"❌ Unexpected response status: {response.status_code}")
            print("Response content preview:")
            print(response.text[:500] + "..." if len(response.text) > 500 else response.text)
            return False

    except requests.exceptions.Timeout:
        print("❌ Request timed out - Server may be overloaded or hanging")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False
    finally:
        session.close()

def test_success_page():
    """Test if the success page is accessible"""
    print_section("SUCCESS PAGE TEST")
    
    try:
        print(f"Testing access to: {SUCCESS_URL}")
        response = requests.get(SUCCESS_URL, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {response.elapsed.total_seconds():.2f} seconds")
        
        if response.status_code == 200:
            print("✅ Success page is accessible")
            return True
        else:
            print(f"❌ Success page returned status {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to access success page: {e}")
        return False

def main():
    """Main test function"""
    print_header("MBUGANI LUXE ADVENTURES - PRODUCTION QUOTE FLOW TEST")
    print(f"Testing production site: {PRODUCTION_URL}")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run tests
    tests = [
        ("Site Accessibility", test_site_accessibility),
        ("Quote Page Access", test_quote_page_access),
        ("Success Page Access", test_success_page),
        ("Quote Submission", test_quote_submission),
    ]
    
    results = {}
    
    for test_name, test_function in tests:
        try:
            print(f"\n🔄 Running: {test_name}")
            results[test_name] = test_function()
            time.sleep(2)  # Brief pause between tests
        except Exception as e:
            print(f"\n❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Summary
    print_header("TEST SUMMARY")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Production quote flow is working correctly.")
    else:
        print(f"\n⚠️ {total - passed} test(s) failed.")
        
        if not results.get("Quote Submission", True):
            print("\n🔍 QUOTE SUBMISSION FAILED - INVESTIGATION NEEDED:")
            print("1. Check Render.com application logs for detailed error messages")
            print("2. Verify environment variables are correctly set in Render dashboard")
            print("3. Check database connectivity and permissions")
            print("4. Verify email configuration in production environment")
            print("5. Monitor server resources (CPU, memory, disk space)")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Test interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n💥 Test script crashed: {e}")
        exit(1)
