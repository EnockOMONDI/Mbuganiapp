#!/bin/bash

# Railway Environment Variables Setup Script
# This script helps you set up environment variables for Railway.app

echo "🚂 Railway.app Environment Variables Setup"
echo "=========================================="
echo ""
echo "📋 Copy these environment variables to Railway dashboard:"
echo ""

echo "# Django Core"
echo "DJANGO_SETTINGS_MODULE=tours_travels.settings_prod"
echo "DEBUG=False"
echo ""

echo "# Database (COPY FROM RENDER)"
echo "DATABASE_URL=<COPY_YOUR_SUPABASE_URL_FROM_RENDER>"
echo "SECRET_KEY=<COPY_FROM_RENDER>"
echo ""

echo "# Email Configuration"
echo "EMAIL_HOST_USER=mbuganiluxeadventures@gmail.com"
echo "EMAIL_HOST_PASSWORD=ewxdvlrxgphzjrdf"
echo "DEFAULT_FROM_EMAIL=Mbugani Luxe Adventures <mbuganiluxeadventures@gmail.com>"
echo "ADMIN_EMAIL=info@mbuganiluxeadventures.com"
echo "JOBS_EMAIL=careers@mbuganiluxeadventures.com"
echo "NEWSLETTER_EMAIL=news@mbuganiluxeadventures.com"
echo ""

echo "# Site Configuration"
echo "SITE_URL=https://www.mbuganiluxeadventures.com"
echo "ALLOWED_HOSTS=www.mbuganiluxeadventures.com,mbuganiluxeadventures.com"
echo ""

echo "# Railway Specific"
echo "NIXPACKS_NO_DEFAULT_PORT=true"
echo "RAILWAY_ENVIRONMENT=production"
echo ""

echo "🔐 IMPORTANT:"
echo "1. Go to Render dashboard → mbuganiapp → Environment"
echo "2. Copy DATABASE_URL and SECRET_KEY values"
echo "3. Add all variables to Railway dashboard → Variables"
echo "4. Deploy to start the worker"
echo ""

echo "✅ After setup, your architecture will be:"
echo "   Render.com: Web service (Django app)"
echo "   Railway.app: Worker service (Django-Q background tasks)"
echo "   Supabase: Shared PostgreSQL database"
