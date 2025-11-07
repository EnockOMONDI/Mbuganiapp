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
🌐 Site URL: https://www.mbuganiluxeadventures.com
🔒 SSL redirect: True
📊 Debug mode: False
✅ Build completed successfully
🌟 Starting Mbugani Luxe Adventures web server...
```

### 2. Test Website Access

- **Homepage:** https://www.mbuganiluxeadventures.com
- **Admin Panel:** https://www.mbuganiluxeadventures.com/admin
- **Packages:** https://www.mbuganiluxeadventures.com/packages
- **Blog:** https://www.mbuganiluxeadventures.com/blog

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
- ✅ **Rotate credentials** if exposed (see `SECURITY_AUDIT_REPORT.md`)
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
- **Security Audit:** `SECURITY_AUDIT_REPORT.md`
- **Immediate Actions:** `IMMEDIATE_ACTION_REQUIRED.md`
- **Environment Secrets:** `.env.secrets` (not in version control)
- **Hero Slider Management:** `docs/hero_slider_management.md`

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

For security issues, see `SECURITY_AUDIT_REPORT.md` and `IMMEDIATE_ACTION_REQUIRED.md`.

