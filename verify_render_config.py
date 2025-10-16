#!/usr/bin/env python
"""
Verify Render.yaml Email Configuration
Checks that all email environment variables are correctly set for automatic deployment
"""

import yaml
import sys
from pathlib import Path

def verify_render_config():
    """Verify render.yaml email configuration"""
    
    print("🔍 Verifying Render.yaml Email Configuration")
    print("=" * 50)
    
    # Load render.yaml
    render_file = Path("render.yaml")
    if not render_file.exists():
        print("❌ render.yaml file not found!")
        return False
    
    try:
        with open(render_file, 'r') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Error reading render.yaml: {e}")
        return False
    
    # Expected email configuration
    expected_config = {
        'EMAIL_HOST_USER': 'mbuganiluxeadventures@gmail.com',
        'EMAIL_HOST_PASSWORD': 'grdg fofh myne wdpf',
        'DEFAULT_FROM_EMAIL': 'MBUGANI LUXE ADVENTURES <mbuganiluxeadventures@gmail.com>',
        'ADMIN_EMAIL': 'info@mbuganiluxeadventures.com',
        'JOBS_EMAIL': 'careers@mbuganiluxeadventures.com',
        'NEWSLETTER_EMAIL': 'news@mbuganiluxeadventures.com'
    }
    
    # Check web service configuration
    web_service = None
    worker_service = None
    
    for service in config.get('services', []):
        if service.get('type') == 'web':
            web_service = service
        elif service.get('type') == 'worker':
            worker_service = service
    
    if not web_service:
        print("❌ Web service not found in render.yaml!")
        return False
    
    print("🌐 Checking Web Service Email Configuration:")
    web_env_vars = {env['key']: env.get('value', 'NOT_SET') for env in web_service.get('envVars', [])}
    
    all_correct = True
    for key, expected_value in expected_config.items():
        actual_value = web_env_vars.get(key, 'NOT_FOUND')
        
        if actual_value == expected_value:
            print(f"   ✅ {key}: {actual_value}")
        else:
            print(f"   ❌ {key}: Expected '{expected_value}', Got '{actual_value}'")
            all_correct = False
    
    # Check worker service if it exists
    if worker_service:
        print("\n🔧 Checking Worker Service Email Configuration:")
        worker_env_vars = {env['key']: env.get('value', 'NOT_SET') for env in worker_service.get('envVars', [])}
        
        for key, expected_value in expected_config.items():
            actual_value = worker_env_vars.get(key, 'NOT_FOUND')
            
            if actual_value == expected_value:
                print(f"   ✅ {key}: {actual_value}")
            elif actual_value == 'NOT_FOUND' and key == 'DEFAULT_FROM_EMAIL':
                # DEFAULT_FROM_EMAIL might not be in worker service, that's OK
                print(f"   ⚠️  {key}: Not set (OK for worker service)")
            else:
                print(f"   ❌ {key}: Expected '{expected_value}', Got '{actual_value}'")
                all_correct = False
    
    # Check for sync: false (which would require manual setting)
    print("\n🔒 Checking for Manual Sync Requirements:")
    manual_sync_found = False
    
    for service in config.get('services', []):
        for env_var in service.get('envVars', []):
            if env_var.get('sync') == False and env_var['key'] in expected_config:
                print(f"   ⚠️  {env_var['key']}: sync: false (requires manual setting)")
                manual_sync_found = True
    
    if not manual_sync_found:
        print("   ✅ No manual sync requirements found - all email vars will auto-deploy")
    
    # Summary
    print("\n📊 Configuration Summary:")
    print(f"   Web Service Email Config: {'✅ CORRECT' if all_correct else '❌ NEEDS FIXING'}")
    print(f"   Auto-deployment Ready: {'✅ YES' if not manual_sync_found else '❌ NO (manual sync required)'}")
    
    if all_correct and not manual_sync_found:
        print("\n🎉 SUCCESS: Render.yaml is correctly configured!")
        print("📤 When you push your next commit, Render.com will automatically:")
        print("   - Set EMAIL_HOST_PASSWORD to: grdg fofh myne wdpf")
        print("   - Set DEFAULT_FROM_EMAIL to: MBUGANI LUXE ADVENTURES <mbuganiluxeadventures@gmail.com>")
        print("   - Set all other email environment variables correctly")
        print("   - Deploy with working email functionality")
        return True
    else:
        print("\n❌ ISSUES FOUND: Please fix the configuration before deploying")
        return False

def verify_env_file():
    """Verify .env file matches render.yaml"""
    
    print("\n🔍 Verifying .env File Configuration")
    print("=" * 50)
    
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found!")
        return False
    
    # Read .env file
    env_vars = {}
    try:
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key] = value
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        return False
    
    # Expected values
    expected_env = {
        'EMAIL_HOST_USER': 'mbuganiluxeadventures@gmail.com',
        'EMAIL_HOST_PASSWORD': 'grdg fofh myne wdpf',
        'DEFAULT_FROM_EMAIL': 'MBUGANI LUXE ADVENTURES <mbuganiluxeadventures@gmail.com>',
        'ADMIN_EMAIL': 'info@mbuganiluxeadventures.com',
        'JOBS_EMAIL': 'careers@mbuganiluxeadventures.com',
        'NEWSLETTER_EMAIL': 'news@mbuganiluxeadventures.com'
    }
    
    all_correct = True
    for key, expected_value in expected_env.items():
        actual_value = env_vars.get(key, 'NOT_FOUND')
        
        if actual_value == expected_value:
            print(f"   ✅ {key}: {actual_value}")
        else:
            print(f"   ❌ {key}: Expected '{expected_value}', Got '{actual_value}'")
            all_correct = False
    
    return all_correct

if __name__ == "__main__":
    print("🚀 Mbugani Luxe Adventures - Render Configuration Verification")
    print("=" * 60)
    
    render_ok = verify_render_config()
    env_ok = verify_env_file()
    
    print("\n" + "=" * 60)
    print("📋 FINAL VERIFICATION RESULTS:")
    print(f"   Render.yaml Configuration: {'✅ PASS' if render_ok else '❌ FAIL'}")
    print(f"   .env File Configuration: {'✅ PASS' if env_ok else '❌ FAIL'}")
    
    if render_ok and env_ok:
        print("\n🎉 ALL CHECKS PASSED!")
        print("🚀 Ready for deployment - email functionality will work automatically!")
    else:
        print("\n❌ CONFIGURATION ISSUES FOUND!")
        print("🔧 Please fix the issues above before deploying.")
    
    sys.exit(0 if (render_ok and env_ok) else 1)
