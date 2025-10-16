#!/usr/bin/env python3
"""
Environment Variables Comparison Tool
Compares .env file with render.yaml configuration
"""

import os
import re
from pathlib import Path

def parse_env_file(file_path):
    """Parse .env file and return dictionary of variables"""
    env_vars = {}
    
    if not os.path.exists(file_path):
        print(f"❌ .env file not found: {file_path}")
        return env_vars
    
    with open(file_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            
            # Parse KEY=VALUE format
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                # Remove quotes if present
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                
                env_vars[key] = value
    
    return env_vars

def parse_render_yaml(file_path):
    """Parse render.yaml and extract environment variables"""
    render_vars = {}
    
    if not os.path.exists(file_path):
        print(f"❌ render.yaml file not found: {file_path}")
        return render_vars
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Extract environment variables from envVars section
    in_env_vars = False
    for line in content.split('\n'):
        line = line.strip()
        
        if 'envVars:' in line:
            in_env_vars = True
            continue
        
        if in_env_vars:
            # Check if we've left the envVars section
            if line and not line.startswith('-') and not line.startswith('key:') and not line.startswith('value:') and not line.startswith('generateValue:') and not line.startswith('sync:'):
                if not line.startswith('#') and ':' in line and not line.startswith(' '):
                    in_env_vars = False
            
            # Parse key-value pairs
            if line.startswith('- key:'):
                current_key = line.replace('- key:', '').strip()
            elif line.startswith('key:'):
                current_key = line.replace('key:', '').strip()
            elif line.startswith('value:') and 'current_key' in locals():
                value = line.replace('value:', '').strip()
                render_vars[current_key] = value
                del current_key
            elif line.startswith('generateValue:') and 'current_key' in locals():
                render_vars[current_key] = '<GENERATED>'
                del current_key
    
    return render_vars

def compare_env_variables():
    """Compare environment variables between .env and render.yaml"""
    print("🔍 ENVIRONMENT VARIABLES COMPARISON")
    print("=" * 60)
    
    # Parse both files
    env_vars = parse_env_file('.env')
    render_vars = parse_render_yaml('render.yaml')
    
    print(f"📄 .env file variables: {len(env_vars)}")
    print(f"📄 render.yaml variables: {len(render_vars)}")
    print()
    
    # Get all unique keys
    all_keys = set(env_vars.keys()) | set(render_vars.keys())
    
    # Critical variables that must match
    critical_vars = {
        'DATABASE_URL', 'EMAIL_HOST_USER', 'EMAIL_HOST_PASSWORD', 
        'DEFAULT_FROM_EMAIL', 'ADMIN_EMAIL', 'SITE_URL',
        'UPLOADCARE_PUBLIC_KEY', 'UPLOADCARE_SECRET_KEY',
        'DEBUG', 'ALLOWED_HOSTS'
    }
    
    # Variables that are expected to be different or generated
    expected_different = {
        'SECRET_KEY', 'PORT', 'RENDER_EXTERNAL_HOSTNAME'
    }
    
    matches = []
    mismatches = []
    env_only = []
    render_only = []
    
    for key in sorted(all_keys):
        env_value = env_vars.get(key, '<NOT SET>')
        render_value = render_vars.get(key, '<NOT SET>')
        
        if key in env_vars and key in render_vars:
            if env_value == render_value:
                matches.append((key, env_value))
            else:
                mismatches.append((key, env_value, render_value))
        elif key in env_vars:
            env_only.append((key, env_value))
        else:
            render_only.append((key, render_value))
    
    # Display results
    print("✅ MATCHING VARIABLES:")
    print("-" * 40)
    for key, value in matches:
        status = "🔑 CRITICAL" if key in critical_vars else "📝 NORMAL"
        print(f"{status} {key}: {value[:50]}{'...' if len(value) > 50 else ''}")
    
    print(f"\n❌ MISMATCHED VARIABLES ({len(mismatches)}):")
    print("-" * 40)
    for key, env_val, render_val in mismatches:
        status = "🚨 CRITICAL" if key in critical_vars else "⚠️  NORMAL"
        expected = "✅ EXPECTED" if key in expected_different else "❌ UNEXPECTED"
        print(f"{status} {expected} {key}:")
        print(f"   .env:        {env_val[:50]}{'...' if len(env_val) > 50 else ''}")
        print(f"   render.yaml: {render_val[:50]}{'...' if len(render_val) > 50 else ''}")
        print()
    
    print(f"📄 ONLY IN .ENV ({len(env_only)}):")
    print("-" * 40)
    for key, value in env_only:
        print(f"   {key}: {value[:50]}{'...' if len(value) > 50 else ''}")
    
    print(f"\n📄 ONLY IN RENDER.YAML ({len(render_only)}):")
    print("-" * 40)
    for key, value in render_only:
        print(f"   {key}: {value[:50]}{'...' if len(value) > 50 else ''}")
    
    # Check critical variables
    print(f"\n🔍 CRITICAL VARIABLES CHECK:")
    print("-" * 40)
    critical_issues = []
    
    for var in critical_vars:
        if var not in env_vars and var not in render_vars:
            critical_issues.append(f"❌ {var}: Missing from both files")
        elif var not in render_vars:
            critical_issues.append(f"⚠️  {var}: Missing from render.yaml")
        elif var not in env_vars:
            critical_issues.append(f"⚠️  {var}: Missing from .env")
        elif env_vars[var] != render_vars[var]:
            critical_issues.append(f"❌ {var}: Values don't match")
        else:
            print(f"✅ {var}: Configured correctly")
    
    if critical_issues:
        print("\n🚨 CRITICAL ISSUES FOUND:")
        for issue in critical_issues:
            print(f"   {issue}")
    else:
        print("\n🎉 All critical variables are configured correctly!")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    print("-" * 40)
    
    if mismatches:
        print("1. Review mismatched variables above")
        print("2. Update render.yaml or .env to ensure consistency")
    
    if env_only:
        print("3. Consider adding missing variables to render.yaml")
    
    if render_only:
        print("4. Consider adding missing variables to .env for local development")
    
    print("5. Ensure UPLOADCARE keys are set manually in Render dashboard")
    print("6. Verify SECRET_KEY is generated automatically by Render")
    
    return len(critical_issues) == 0

def check_uploadcare_config():
    """Check Uploadcare configuration specifically"""
    print(f"\n🖼️  UPLOADCARE CONFIGURATION CHECK:")
    print("-" * 40)
    
    env_vars = parse_env_file('.env')
    
    uploadcare_public = env_vars.get('UPLOADCARE_PUBLIC_KEY', '')
    uploadcare_secret = env_vars.get('UPLOADCARE_SECRET_KEY', '')
    
    if uploadcare_public:
        print(f"✅ UPLOADCARE_PUBLIC_KEY: {uploadcare_public}")
    else:
        print("❌ UPLOADCARE_PUBLIC_KEY: Not set in .env")
    
    if uploadcare_secret:
        print(f"✅ UPLOADCARE_SECRET_KEY: {uploadcare_secret[:10]}...")
    else:
        print("❌ UPLOADCARE_SECRET_KEY: Not set in .env")
    
    print("\n📝 Note: Uploadcare keys should be set manually in Render dashboard")
    print("   Go to: Render Dashboard > Your Service > Environment > Add Environment Variable")

def main():
    """Main function"""
    print("🚀 MBUGANI LUXE ADVENTURES - ENVIRONMENT CHECK")
    print("=" * 60)
    
    # Check if files exist
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        return
    
    if not os.path.exists('render.yaml'):
        print("❌ render.yaml file not found!")
        return
    
    # Run comparisons
    env_ok = compare_env_variables()
    check_uploadcare_config()
    
    print(f"\n🎯 SUMMARY:")
    print("-" * 40)
    if env_ok:
        print("✅ Environment configuration looks good!")
        print("🚀 Ready for deployment to Render")
    else:
        print("❌ Environment configuration issues found")
        print("🔧 Please fix the critical issues above before deploying")

if __name__ == "__main__":
    main()
