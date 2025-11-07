# 🌍 Mbugani Luxe Adventures

**Premium Safari & Adventure Tourism Platform**

A comprehensive Django-based web application for luxury safari tours, adventure packages, and travel experiences across East Africa.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
- [Environment Setup](#environment-setup)
- [Deployment](#deployment)
- [Security](#security)
- [Documentation](#documentation)
- [Support](#support)

---

## 🎯 Overview

Mbugani Luxe Adventures is a full-featured travel and tourism platform offering:

- **Safari Packages:** Multi-day bush safaris, Nairobi excursions, and outbound packages
- **Destination Management:** Hierarchical destination system (Countries → Cities → Places)
- **Accommodation Booking:** Integration with luxury lodges and hotels
- **Blog Platform:** Travel stories, guides, and destination insights
- **Quote System:** Custom quote requests with email notifications
- **Admin Dashboard:** Comprehensive management interface with Django Unfold

---

## ✨ Features

### Customer-Facing Features
- 🏞️ **Package Browsing:** Filter by category, destination, duration, and price
- 📧 **Quote Requests:** Custom travel planning with email confirmations
- 🏨 **Accommodation Listings:** Detailed hotel and lodge information
- 📝 **Travel Blog:** Engaging content with categories and tags
- 📱 **Responsive Design:** Mobile-first approach with modern UI
- 🔍 **Search & Filters:** Advanced filtering for packages and destinations

### Admin Features
- 🎨 **Modern Admin Interface:** Django Unfold with custom branding
- 📊 **Dashboard Analytics:** Booking statistics and performance metrics
- 🖼️ **Image Management:** Uploadcare CDN integration
- ✉️ **Email System:** Mailtrap API for reliable email delivery
- 🔐 **Security:** CSRF protection, SSL/TLS, HSTS headers
- 📦 **Package Management:** Create and manage travel packages with itineraries

---

## 🛠️ Technology Stack

### Backend
- **Framework:** Django 5.0.14
- **Language:** Python 3.12
- **Database:** PostgreSQL (Supabase)
- **Server:** Gunicorn with sync workers

### Frontend
- **Template Engine:** Django Templates
- **CSS Framework:** Custom CSS with responsive design
- **JavaScript:** Vanilla JS with modern ES6+
- **Fonts:** TAN-Garland-Regular (custom brand font)

### Third-Party Services
- **CDN:** Uploadcare (image/file hosting)
- **Email:** Mailtrap HTTP API
- **Hosting:** Render.com
- **Database:** Supabase PostgreSQL

### Key Dependencies
- `django==5.0.14` - Web framework
- `psycopg2-binary==2.9.10` - PostgreSQL adapter
- `gunicorn==23.0.0` - WSGI HTTP server
- `django-unfold==0.42.0` - Modern admin interface
- `django-ckeditor-5==0.2.15` - Rich text editor
- `pyuploadcare==5.1.0` - Uploadcare integration
- `mailtrap==2.0.1` - Email API client
- `python-decouple==3.8` - Environment variable management

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- PostgreSQL (or use Supabase)
- Git
- Virtual environment tool (venv, virtualenv, or conda)

### Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Mbuganiapp
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   # Create .env file (see Environment Setup section below)
   cp .env.secrate .env
   # Edit .env with your local configuration
   ```

5. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files:**
   ```bash
   python manage.py collectstatic --noinput
   ```

8. **Run development server:**
   ```bash
   python manage.py runserver
   ```

9. **Access the application:**
   - Frontend: http://localhost:8000
   - Admin: http://localhost:8000/admin

---

## 🔐 Environment Setup

### Required Environment Variables

Create a `.env` file in the project root with these variables:

```bash
# Django Core
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (for local development, use SQLite or local PostgreSQL)
# DATABASE_URL is only needed for production
# DATABASE_URL=postgresql://user:password@host:port/database

# Email Configuration (optional for local development)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=Your Name <your-email@gmail.com>

# Uploadcare (optional for local development)
UPLOADCARE_PUBLIC_KEY=your-public-key
UPLOADCARE_SECRET_KEY=your-secret-key

# Site Configuration
SITE_URL=http://localhost:8000
WHATSAPP_PHONE=
```

### Development vs Production

- **Development:** Uses SQLite database by default, simpler email backend
- **Production:** Uses PostgreSQL (Supabase), Mailtrap API, Uploadcare CDN

**⚠️ IMPORTANT:** Never commit `.env` files to version control!

---

## 📦 Deployment

### Deploying to Render.com

See **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** for comprehensive deployment instructions.

**Quick Steps:**

1. **Set up environment variables** in Render dashboard (see `.env.secrets`)
2. **Connect GitHub repository** to Render
3. **Select branch:** `mailltrapapi`
4. **Deploy** - Render will use `render.yaml` configuration

**Critical Environment Variables for Production:**
- `SECRET_KEY` - Django secret key
- `DATABASE_URL` - PostgreSQL connection string
- `MAILTRAP_API_TOKEN` - Email API token
- `UPLOADCARE_PUBLIC_KEY` - CDN public key
- `UPLOADCARE_SECRET_KEY` - CDN secret key

---

## 🔒 Security

### Security Features

✅ **HTTPS/SSL:** Enforced SSL redirect in production
✅ **HSTS:** HTTP Strict Transport Security enabled
✅ **CSRF Protection:** Django CSRF middleware active
✅ **Secure Cookies:** HTTPOnly and Secure flags set
✅ **Content Security Policy:** CSP headers configured
✅ **XSS Protection:** Template auto-escaping enabled
✅ **SQL Injection Protection:** Django ORM parameterized queries

### Security Best Practices

1. **Never commit secrets** to version control
3. **Use strong passwords** for admin accounts (16+ characters)
4. **Enable 2FA** on all third-party services
5. **Keep dependencies updated** regularly
6. **Monitor logs** for suspicious activity



### External Documentation

- **Django:** https://docs.djangoproject.com/
- **Django Unfold:** https://unfoldadmin.com/
- **Uploadcare:** https://uploadcare.com/docs/
- **Mailtrap:** https://mailtrap.io/docs/
- **Render:** https://render.com/docs

---

## 🧪 Testing

### Run Tests

```bash
# Run all tests
python run_tests.py

# Run specific app tests
python manage.py test adminside
python manage.py test users
python manage.py test blog

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### Test Coverage

- Unit tests for models, views, and forms
- Integration tests for email sending
- Admin interface tests
- API endpoint tests

---

## 🤝 Contributing

### Development Workflow

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Run tests: `python run_tests.py`
4. Commit changes: `git commit -m "Description of changes"`
5. Push to branch: `git push origin feature/your-feature`
6. Create Pull Request

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused
- Write tests for new features

---

## 📞 Support

### Getting Help

- **Issues:** Create an issue in the GitHub repository
- **Email:** enockomondike@gmail.com
- **WhatsApp:** +254726436676

### Dashboards

- **Render:** https://dashboard.render.com
- **Supabase:** https://supabase.com/dashboard
- **Mailtrap:** https://mailtrap.io/signin
- **Uploadcare:** https://uploadcare.com/

#  - Deployment Guide

**Last Updated:** November 7, 2025  
**Platform:** Render.com  
**Branch:** mailltrapapi  
**Python Version:** 3.12.0  
**Django Version:** 5.0.14

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Variables Setup](#environment-variables-setup)
3. [Initial Deployment](#initial-deployment)
4. [Post-Deployment Verification](#post-deployment-verification)
5. [Updating the Application](#updating-the-application)
6. [Troubleshooting](#troubleshooting)
7. [Security Best Practices](#security-best-practices)

---

## 🔧 Prerequisites

Before deploying, ensure you have:

- ✅ Render.com account (https://dashboard.render.com)
- ✅ GitHub repository access
- ✅ Supabase PostgreSQL database credentials
- ✅ Mailtrap API token
- ✅ Uploadcare API keys
- ✅ Access to `.env.secrets` file should contain (all production credentials)

---

## 🔐 Environment Variables Setup

### Step 1: Access Render Dashboard

1. Go to https://dashboard.render.com
2. Select your service: 
3. Click on the **Environment** tab

### Step 2: Add Critical Secrets

**⚠️ IMPORTANT:** These variables are NOT in `render.yaml` for security reasons.  
You MUST add them manually in the Render dashboard.

Open the `.env.secrets` file and add each of these variables:

#### 1. Django Secret Key
```
Key: SECRET_KEY
Value: 
```

#### 2. Database Connection
```
Key: DATABASE_URL
Value: 
```
**Format:** `postgresql://user:password@host:port/database`

#### 3. Mailtrap API Token
```
Key: MAILTRAP_API_TOKEN
Value: 
```

#### 4. Uploadcare Public Key
```
Key: UPLOADCARE_PUBLIC_KEY
Value: 
```

#### 5. Uploadcare Secret Key
```
Key: UPLOADCARE_SECRET_KEY
Value: 
```

### Step 3: Verify Auto-Configured Variables

These variables are automatically set from `render.yaml`:

- ✅ `DJANGO_SETTINGS_MODULE` = `tours_travels.settings_prod`
- ✅ `DEBUG` = `False`
- ✅ `ALLOWED_HOSTS` = ``
- ✅ `SITE_URL` = ``
- ✅ `DEFAULT_FROM_EMAIL` = ``
- ✅ `ADMIN_EMAIL` = ``
- ✅ `JOBS_EMAIL` = ``
- ✅ `NEWSLETTER_EMAIL` = ``
- ✅ `WHATSAPP_PHONE` = ``


## Initial Deployment

### Step 1: Connect Repository

1. In Render dashboard, click **New** → **Web Service**
2. Connect your GitHub repository
3. Select branch: **mailltrapapi**
4. Service name: **Mbuganiapp**
5. Region: **Frankfurt** (or closest to your users)
6. Plan: **Starter** (or higher)

### Step 2: Configure Build Settings

Render will automatically detect `render.yaml` and use these settings:

**Build Command:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
python manage.py collectstatic --noinput --settings=tours_travels.settings_prod
python manage.py migrate --settings=tours_travels.settings_prod
python manage.py createcachetable --settings=tours_travels.settings_prod
```

**Start Command:**
```bash
gunicorn tours_travels.wsgi:application \
  --bind 0.0.0.0:$PORT \
  --workers $WEB_CONCURRENCY \
  --timeout $GUNICORN_TIMEOUT \
  --worker-class sync \
  --worker-connections 1000 \
  --max-requests 1000 \
  --max-requests-jitter 100 \
  --preload \
  --access-logfile - \
  --error-logfile - \
  --log-level info
```

### Step 3: Deploy

1. Click **Create Web Service**
2. Wait for build to complete (5-10 minutes)
3. Monitor logs for any errors

---

## ✅ Post-Deployment Verification

### 1. Check Deployment Logs

Look for these success messages:
```
🚀 Production settings loaded
📧 Production mode: Using Mailtrap HTTP API (synchronous)
🗄️ Database: postgresql://...
🌐 Site URL: https://yoursite.com.com
🔒 SSL redirect: True
📊 Debug mode: False
✅ Build completed successfully
🌟 Starting Mbugani Luxe Adventures web server...
```

### 2. Test Website Access

- **Homepage:** https://www.yoursite.com.com
- **Admin Panel:** https://yoursite.com/admin
- **Packages:** https://yoursite.com/packages
- **Blog:** https://yoursite.com/blog

### 3. Test Critical Functionality

#### Test Database Connection
- Log in to admin panel
- Verify packages, destinations, and blog posts are visible
- Create a test entry

#### Test Email Sending
- Submit a quote request form
- Verify confirmation email is received
- Check admin notification email

#### Test Image Uploads
- Upload an image in admin panel
- Verify it displays correctly on the frontend
- Check Uploadcare dashboard for the upload

### 4. Verify Security Headers

Use https://securityheaders.com to check:
- ✅ HSTS enabled
- ✅ SSL/TLS configured
- ✅ Content Security Policy
- ✅ X-Frame-Options

---

## 🔄 Updating the Application

### For Code Changes

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Your commit message"
   git push origin mailltrapapi
   ```

2. **Automatic Deployment:**
   - Render automatically deploys when you push to the `mailltrapapi` branch
   - Monitor deployment in Render dashboard

3. **Manual Deployment:**
   - Go to Render dashboard
   - Click **Manual Deploy** → **Deploy latest commit**

### For Environment Variable Changes

1. Go to Render dashboard → Environment tab
2. Update the variable
3. Click **Save**
4. Render will automatically redeploy

### For Database Migrations

Migrations run automatically during deployment via `render.yaml`.

To run manually:
```bash
# In Render Shell (Dashboard → Shell)
python manage.py migrate --settings=tours_travels.settings_prod
```

---

## 🔍 Troubleshooting

### Issue: "ImproperlyConfigured: Set the SECRET_KEY environment variable"

**Solution:**
- Verify `SECRET_KEY` is set in Render dashboard
- Check for typos in the variable name
- Ensure the value is not empty

### Issue: "could not connect to server: Connection refused"

**Solution:**
- Verify `DATABASE_URL` is correct
- Check Supabase database is running
- Ensure password includes special characters (e.g., `!`)
- Test connection from Render Shell

### Issue: "Mailtrap API error" or emails not sending

**Solution:**
- Verify `MAILTRAP_API_TOKEN` is correct
- Check token hasn't expired in Mailtrap dashboard
- Review Render logs for specific error messages

### Issue: "Uploadcare: Invalid public key"

**Solution:**
- Verify both `UPLOADCARE_PUBLIC_KEY` and `UPLOADCARE_SECRET_KEY` are set
- Check keys are correct in Uploadcare dashboard
- Ensure no extra spaces in the values

### Issue: "DisallowedHost at /"

**Solution:**
- Verify `ALLOWED_HOSTS` includes your domain
- Check custom domain is properly configured in Render
- Ensure DNS records are correct

### Issue: Static files not loading

**Solution:**
- Check `collectstatic` ran successfully in build logs
- Verify `STATIC_ROOT` and `STATIC_URL` are configured
- Clear browser cache
- Check Render logs for 404 errors

---

## 🔒 Security Best Practices

### 1. Credential Management

- ✅ **Never commit** `.env` or `.env.secrets` to version control
- ✅ **Use strong passwords** for database and admin accounts
- ✅ **Enable 2FA** on Render, GitHub, Supabase, Mailtrap, Uploadcare

### 2. Regular Maintenance

- ✅ **Update dependencies** monthly: `pip list --outdated`
- ✅ **Review security logs** in Render dashboard
- ✅ **Monitor error rates** and performance
- ✅ **Backup database** regularly (Supabase automatic backups)

### 3. Access Control

- ✅ **Limit admin access** to authorized personnel only
- ✅ **Use strong admin passwords** (minimum 16 characters)
- ✅ **Review user permissions** regularly
- ✅ **Monitor login attempts** in Django admin

### 4. Monitoring

- ✅ **Set up alerts** in Render for deployment failures
- ✅ **Monitor uptime** using external service (e.g., UptimeRobot)
- ✅ **Review logs** daily for errors or suspicious activity
- ✅ **Track email delivery** in Mailtrap dashboard

---

## 📞 Support Resources

### Documentation
- **Django:** https://docs.djangoproject.com/
- **Render:** https://render.com/docs
- **Supabase:** https://supabase.com/docs
- **Mailtrap:** https://mailtrap.io/docs
- **Uploadcare:** https://uploadcare.com/docs

### Dashboards
- **Render:** https://dashboard.render.com
- **Supabase:** https://supabase.com/dashboard
- **Mailtrap:** https://mailtrap.io/signin
- **Uploadcare:** https://uploadcare.com/

### Internal Documentation

- **Environment Secrets:** `.env.secrets` (not in version control)


---

## 🎯 Quick Reference

### Common Commands

**Run migrations:**
```bash
python manage.py migrate --settings=tours_travels.settings_prod
```

**Create superuser:**
```bash
python manage.py createsuperuser --settings=tours_travels.settings_prod
```

**Collect static files:**
```bash
python manage.py collectstatic --noinput --settings=tours_travels.settings_prod
```

**Check deployment:**
```bash
python manage.py check --deploy --settings=tours_travels.settings_prod
```

### Important URLs

- **Production Site:** https://www.mbuganiluxeadventures.com
- **Admin Panel:** https://www.mbuganiluxeadventures.com/admin
- **Render Dashboard:** https://dashboard.render.com
- **GitHub Repository:** [Your repository URL]

---

**Last Updated:** November 7, 2025  
**Maintained By:** Mbugani Luxe Adventures Development Team



## 📄 License

This project is proprietary software owned by Mbugani Luxe Adventures.
All rights reserved.

---

## 🙏 Acknowledgments

- **Django Community** - For the excellent web framework
- **Unfold Admin** - For the modern admin interface
- **Uploadcare** - For reliable CDN services
- **Mailtrap** - For email delivery infrastructure
- **Render** - For hosting platform

---

**Built with ❤️ by the Kipekee studio Team**

**Last Updated:** November 7, 2025
