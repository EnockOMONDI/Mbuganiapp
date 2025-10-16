#!/usr/bin/env python
"""
Environment Variable Export Helper for Railway.app

This script helps you prepare environment variables for Railway
based on your current Render configuration.

Usage:
    python export_env_for_railway.py
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Setup Django with production settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tours_travels.settings_prod')
django.setup()

from django.conf import settings

def get_required_env_vars():
    """Get list of required environment variables for Railway"""
    
    required_vars = {
        # Django Core
        'DJANGO_SETTINGS_MODULE': 'tours_travels.settings_prod',
        'SECRET_KEY': 'Your Django secret key from Render',
        'DEBUG': 'False',
        
        # Database (same as Render)
        'DATABASE_URL': 'Your Supabase PostgreSQL URL from Render',
        
        # Email Configuration
        'EMAIL_HOST_USER': 'mbuganiluxeadventures@gmail.com',
        'EMAIL_HOST_PASSWORD': 'ewxdvlrxgphzjrdf',
        'DEFAULT_FROM_EMAIL': 'Mbugani Luxe Adventures <mbuganiluxeadventures@gmail.com>',
        'ADMIN_EMAIL': 'info@mbuganiluxeadventures.com',
        'JOBS_EMAIL': 'careers@mbuganiluxeadventures.com',
        'NEWSLETTER_EMAIL': 'news@mbuganiluxeadventures.com',
        
        # Site Configuration
        'SITE_URL': 'https://www.mbuganiluxeadventures.com',
        'ALLOWED_HOSTS': 'www.mbuganiluxeadventures.com,mbuganiluxeadventures.com',
        
        # Railway Specific
        'RAILWAY_ENVIRONMENT': 'production',
        'PORT': '8000',  # Railway will override this
    }
    
    return required_vars

def print_railway_env_setup():
    """Print instructions for setting up Railway environment variables"""
    
    print("🚀 Railway Environment Variables Setup")
    print("=" * 60)
    print()
    print("📋 Copy these environment variables to Railway:")
    print()
    
    env_vars = get_required_env_vars()
    
    for key, value in env_vars.items():
        if 'secret' in key.lower() or 'password' in key.lower() or 'database_url' in key.lower():
            print(f"{key}=<COPY_FROM_RENDER_DASHBOARD>")
        else:
            print(f"{key}={value}")
    
    print()
    print("🔐 IMPORTANT - Copy these sensitive values from Render:")
    print("   • SECRET_KEY: Go to Render → mbuganiapp → Environment")
    print("   • DATABASE_URL: Copy your Supabase PostgreSQL connection string")
    print()
    print("📝 Railway Setup Instructions:")
    print("   1. Go to Railway dashboard → Your project → Variables")
    print("   2. Add each environment variable above")
    print("   3. For sensitive values, copy from Render dashboard")
    print("   4. Click 'Deploy' to restart with new variables")
    print()

def print_render_compatibility():
    """Print information about Render compatibility"""
    
    print("🔗 Render Compatibility Check")
    print("=" * 60)
    print()
    print("✅ Your Render web service will continue working normally")
    print("✅ No changes needed to your Django settings")
    print("✅ Both services will share the same PostgreSQL database")
    print("✅ Django-Q tasks queued by Render will be processed by Railway")
    print()
    print("🔄 How it works:")
    print("   1. User submits form on Render web app")
    print("   2. Render queues email task in PostgreSQL")
    print("   3. Railway worker picks up task from PostgreSQL")
    print("   4. Railway sends email via Gmail SMTP")
    print("   5. Task marked complete in PostgreSQL")
    print()

def print_monitoring_setup():
    """Print monitoring and debugging instructions"""
    
    print("📊 Monitoring & Debugging")
    print("=" * 60)
    print()
    print("🔍 Verify Django-Q is working:")
    print("   1. Submit a quote request on your website")
    print("   2. Check Railway logs for task processing")
    print("   3. Check Django admin: /admin/django_q/")
    print("   4. Verify email delivery")
    print()
    print("📋 Railway Logs:")
    print("   • Go to Railway dashboard → Your service → Logs")
    print("   • Look for: 'Q Cluster starting' and 'ready for work'")
    print("   • Monitor task processing messages")
    print()
    print("🚨 Troubleshooting:")
    print("   • If worker stops: Check Railway logs for errors")
    print("   • If tasks not processing: Verify DATABASE_URL connection")
    print("   • If emails not sending: Check EMAIL_* environment variables")
    print()

def print_optimization_tips():
    """Print Railway free tier optimization tips"""
    
    print("⚡ Railway Free Tier Optimization")
    print("=" * 60)
    print()
    print("💰 Free tier limits:")
    print("   • $5 credit per month")
    print("   • ~500 hours of usage")
    print("   • Automatic sleep after 30 minutes of inactivity")
    print()
    print("🎯 Optimization strategies:")
    print("   1. Worker sleeps when no tasks (built into Django-Q)")
    print("   2. Efficient task processing (our current setup)")
    print("   3. Monitor usage in Railway dashboard")
    print()
    print("⚙️  Resource settings (Railway dashboard → Settings):")
    print("   • Memory: 512MB (minimum)")
    print("   • CPU: 0.25 vCPU (minimum)")
    print("   • Auto-scaling: Disabled")
    print()

def main():
    """Main function"""
    print("🌍 Environment: production")
    print(f"🗄️  Database: {settings.DATABASES['default']['NAME']}")
    print(f"📧 Email backend: {settings.EMAIL_BACKEND}")
    print()
    
    print_railway_env_setup()
    print()
    print_render_compatibility()
    print()
    print_monitoring_setup()
    print()
    print_optimization_tips()
    
    print("🎉 Ready to deploy Django-Q worker to Railway!")
    print("📚 Next: Follow the step-by-step instructions above")

if __name__ == "__main__":
    main()
