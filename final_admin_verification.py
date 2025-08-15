#!/usr/bin/env python
"""
Final verification script for admin login
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tours_travels.settings_dev')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

def final_verification():
    print('=== FINAL ADMIN LOGIN VERIFICATION ===')
    
    # Get the user
    try:
        user = User.objects.get(username='mbuganiluxeadventures')
        print(f'✅ User found: {user.username}')
    except User.DoesNotExist:
        print('❌ User not found!')
        return
    
    # Test exact credentials
    credentials = {
        'username': 'mbuganiluxeadventures',
        'password': 'mbuganiluxeadventurespassword'
    }
    
    print(f'\nTesting credentials:')
    print(f'Username: "{credentials["username"]}"')
    print(f'Username length: {len(credentials["username"])}')
    print(f'Password: "{credentials["password"]}"')
    print(f'Password length: {len(credentials["password"])}')
    
    # Check for any hidden characters
    username_bytes = credentials['username'].encode('utf-8')
    password_bytes = credentials['password'].encode('utf-8')
    
    print(f'\nUsername bytes: {username_bytes}')
    print(f'Password bytes: {password_bytes}')
    
    # Test authentication
    auth_user = authenticate(
        username=credentials['username'],
        password=credentials['password']
    )
    
    if auth_user:
        print('\n✅ AUTHENTICATION SUCCESSFUL!')
        print('The credentials are working correctly.')
        
        # Additional checks
        print(f'\nUser details:')
        print(f'  ID: {auth_user.id}')
        print(f'  Username: {auth_user.username}')
        print(f'  Email: {auth_user.email}')
        print(f'  is_active: {auth_user.is_active}')
        print(f'  is_staff: {auth_user.is_staff}')
        print(f'  is_superuser: {auth_user.is_superuser}')
        print(f'  last_login: {auth_user.last_login}')
        
    else:
        print('\n❌ AUTHENTICATION FAILED!')
        
        # Try to debug the issue
        print('Debugging authentication failure...')
        
        # Check if user exists with exact username
        try:
            db_user = User.objects.get(username=credentials['username'])
            print(f'User exists in database: {db_user.username}')
            
            # Check password hash
            from django.contrib.auth.hashers import check_password
            password_valid = check_password(credentials['password'], db_user.password)
            print(f'Password hash check: {password_valid}')
            
            if not password_valid:
                print('Password does not match stored hash!')
                
        except User.DoesNotExist:
            print('User does not exist with this exact username!')
    
    print('\n=== BROWSER LOGIN INSTRUCTIONS ===')
    print('To log into the admin interface:')
    print('1. Make sure your Django development server is running:')
    print('   python manage.py runserver --settings=tours_travels.settings_dev')
    print('2. Open your browser and go to: http://localhost:8000/admin/')
    print('3. Use these exact credentials (copy and paste to avoid typos):')
    print('   Username: mbuganiluxeadventures')
    print('   Password: mbuganiluxeadventurespassword')
    print('4. If it still fails, try:')
    print('   - Clear browser cache and cookies')
    print('   - Use incognito/private browsing mode')
    print('   - Check browser console for JavaScript errors')
    print('   - Disable browser extensions temporarily')

if __name__ == "__main__":
    final_verification()
