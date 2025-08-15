#!/usr/bin/env python
"""
Script to test admin login functionality
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tours_travels.settings_dev')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.test import Client, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.messages.middleware import MessageMiddleware

def test_admin_login():
    print('=== COMPREHENSIVE ADMIN LOGIN TEST ===')
    
    # Test 1: Basic authentication
    print('1. Testing basic authentication...')
    user = authenticate(username='mbuganiluxeadventures', password='mbuganiluxeadventurespassword')
    if user:
        print('✅ Basic authentication successful')
    else:
        print('❌ Basic authentication failed')
        return
    
    # Test 2: User permissions
    print('\n2. Testing user permissions...')
    print(f'   is_active: {user.is_active}')
    print(f'   is_staff: {user.is_staff}')
    print(f'   is_superuser: {user.is_superuser}')
    
    if not user.is_staff:
        print('❌ User is not staff - cannot access admin')
        return
    
    # Test 3: Check admin configuration
    print('\n3. Testing admin configuration...')
    try:
        from django.contrib import admin
        from django.urls import reverse
        
        print(f'   Admin site: {admin.site.__class__.__name__}')
        
        # Check if admin URLs are configured
        try:
            admin_url = reverse('admin:index')
            print(f'   Admin URL: {admin_url}')
        except Exception as e:
            print(f'   ❌ Admin URL error: {e}')
            
    except Exception as e:
        print(f'   ❌ Admin configuration error: {e}')
    
    # Test 4: Session handling
    print('\n4. Testing session handling...')
    try:
        from django.conf import settings
        print(f'   Session engine: {settings.SESSION_ENGINE}')
        print(f'   Session cookie name: {settings.SESSION_COOKIE_NAME}')
        print(f'   Session cookie age: {settings.SESSION_COOKIE_AGE}')
        
    except Exception as e:
        print(f'   ❌ Session configuration error: {e}')
    
    # Test 5: Middleware check
    print('\n5. Testing middleware configuration...')
    try:
        from django.conf import settings
        middleware = settings.MIDDLEWARE
        
        required_middleware = [
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
        ]
        
        for mw in required_middleware:
            if mw in middleware:
                print(f'   ✅ {mw.split(".")[-1]} configured')
            else:
                print(f'   ❌ {mw.split(".")[-1]} missing')
                
    except Exception as e:
        print(f'   ❌ Middleware check error: {e}')
    
    print('\n=== TROUBLESHOOTING SUGGESTIONS ===')
    print('If you are still experiencing login issues, try the following:')
    print('1. Clear your browser cache and cookies')
    print('2. Try using an incognito/private browser window')
    print('3. Check browser developer tools for JavaScript errors')
    print('4. Ensure you are accessing the correct admin URL: http://localhost:8000/admin/')
    print('5. Make sure the Django development server is running')
    print('6. Try logging in with these exact credentials:')
    print('   Username: mbuganiluxeadventures')
    print('   Password: mbuganiluxeadventurespassword')
    print('7. Check if there are any browser extensions blocking the login')

if __name__ == "__main__":
    test_admin_login()
