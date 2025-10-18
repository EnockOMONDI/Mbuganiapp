# 🚀 Render.com Deployment Steps - Mbugani Luxe Adventures

## Complete Step-by-Step Guide for Mailtrap HTTP API Migration

---

## 📋 **PRE-DEPLOYMENT CHECKLIST**

Before you start, make sure you have:

- [x] Code pushed to `mailltrapapi` branch on GitHub
- [x] Supabase database credentials ready
- [x] Uploadcare credentials ready
- [x] Mailtrap account set up
- [x] Custom domain DNS configured (if using)

---

## 🔧 **STEP 1: GENERATE DJANGO SECRET KEY**

Run this command on your local machine:

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

**Copy the output** - you'll need it in Step 3.

Example output:
```
django-insecure-abc123xyz789!@#$%^&*()_+-=[]{}|;:,.<>?
```

---

## 🗄️ **STEP 2: GET SUPABASE DATABASE URL**

1. Go to: https://supabase.com/dashboard
2. Select your project: **Mbuganiapp**
3. Click **Settings** (gear icon) in the left sidebar
4. Click **Database**
5. Scroll to **Connection Pooling** section
6. Copy the **Connection string** (should use port **6543**)

Example format:
```
postgresql://postgres.PROJECT_ID:PASSWORD@aws-0-REGION.pooler.supabase.com:6543/postgres
```

Your actual URL:
```
postgresql://postgres.zgwfxeemdgfryiulbapx:YOUR_PASSWORD@aws-0-eu-central-1.pooler.supabase.com:6543/postgres
```

---

## 🌐 **STEP 3: ADD ENVIRONMENT VARIABLES TO RENDER**

### **3.1 Access Render Dashboard**

1. Go to: https://dashboard.render.com
2. Click on your **Mbuganiapp** web service
3. Click **"Environment"** in the left sidebar
4. You'll see a list of existing environment variables

### **3.2 Add/Update Variables**

Click **"Add Environment Variable"** for each of these:

#### **Required Variables:**

| Key | Value | Notes |
|-----|-------|-------|
| `DJANGO_SECRET_KEY` | `[Your generated key from Step 1]` | Keep this secret! |
| `DATABASE_URL` | `[Your Supabase URL from Step 2]` | Include password |
| `ALLOWED_HOSTS` | `www.mbuganiluxeadventures.com,mbuganiluxeadventures.com,YOUR_APP.onrender.com` | Replace YOUR_APP |
| `CSRF_TRUSTED_ORIGINS` | `https://www.mbuganiluxeadventures.com,https://mbuganiluxeadventures.com,https://YOUR_APP.onrender.com` | Must have https:// |
| `UPLOADCARE_PUBLIC_KEY` | `6fb55bb425b16d386db6` | Already provided |
| `UPLOADCARE_SECRET_KEY` | `3086089d3d2ac096684d` | Already provided |
| `DJANGO_ENV` | `production` | Important! |
| `DEBUG` | `False` | Must be False |
| `SITE_URL` | `https://www.mbuganiluxeadventures.com` | Your primary domain |

#### **Email Variables:**

| Key | Value |
|-----|-------|
| `DEFAULT_FROM_EMAIL` | `Mbugani Luxe Adventures <info@mbuganiluxeadventures.com>` |
| `ADMIN_EMAIL` | `info@mbuganiluxeadventures.com` |
| `JOBS_EMAIL` | `careers@mbuganiluxeadventures.com` |
| `NEWSLETTER_EMAIL` | `news@mbuganiluxeadventures.com` |

#### **Security Variables:**

| Key | Value |
|-----|-------|
| `SECURE_SSL_REDIRECT` | `True` |
| `SESSION_COOKIE_SECURE` | `True` |
| `CSRF_COOKIE_SECURE` | `True` |

### **3.3 Save Changes**

After adding all variables, click **"Save Changes"** at the bottom.

⚠️ **This will trigger a new deployment automatically!**

---

## 🔄 **STEP 4: CONFIGURE DEPLOYMENT BRANCH**

### **Option A: Deploy from `mailltrapapi` branch (Recommended for testing)**

1. In Render dashboard, go to **Settings**
2. Scroll to **Build & Deploy** section
3. Find **Branch** setting
4. Change from `main` to `mailltrapapi`
5. Click **Save Changes**

### **Option B: Merge to `main` and deploy (Recommended for production)**

On your local machine:

```bash
# Switch to main branch
git checkout main

# Merge mailltrapapi branch
git merge mailltrapapi

# Push to GitHub
git push origin main
```

Render will automatically deploy from `main` branch.

---

## 📊 **STEP 5: MONITOR DEPLOYMENT**

### **5.1 Watch Build Logs**

1. In Render dashboard, click **"Logs"** tab
2. Watch the deployment progress
3. Look for these success indicators:

```
✅ Installing dependencies...
✅ Collecting static files...
✅ Build successful
✅ Starting service...
🌍 Environment: production
🚀 Loading production settings...
📧 Email: Mailtrap HTTP API (synchronous)
✅ Production settings loaded successfully
```

### **5.2 Check for Errors**

If you see errors, common issues:

**Database Connection Error:**
```
django.db.utils.OperationalError: could not connect to server
```
→ Check DATABASE_URL is correct

**Static Files Error:**
```
ValueError: Missing staticfiles manifest entry
```
→ Check ALLOWED_HOSTS includes your domain

**Import Error:**
```
ModuleNotFoundError: No module named 'mailtrap'
```
→ Check requirements.txt includes `mailtrap>=2.0.0`

---

## ✅ **STEP 6: VERIFY DEPLOYMENT**

### **6.1 Check Website is Live**

1. Open your browser
2. Go to: https://YOUR_APP.onrender.com
3. Verify the homepage loads correctly
4. Check that images load (Uploadcare working)
5. Check that styles load (static files working)

### **6.2 Test Email Functionality**

**Test Quote Request:**
1. Go to your website
2. Fill out the quote request form
3. Submit the form
4. **Expected:** Form submits in 1-4 seconds
5. **Expected:** Success message appears
6. Go to: https://mailtrap.io/inboxes
7. **Expected:** See 2 emails (admin + user)

**Test Newsletter Subscription:**
1. Subscribe to newsletter on your website
2. **Expected:** Form submits in 1-4 seconds
3. Check Mailtrap inbox
4. **Expected:** See 2 emails (admin + subscriber)

### **6.3 Check Logs for Email Sending**

In Render logs, look for:

```
INFO Sending email via Mailtrap API: subject='New Quote Request from...'
INFO Email sent successfully via Mailtrap API: {'success': True, 'message_ids': [...]}
```

---

## 🌐 **STEP 7: CONFIGURE CUSTOM DOMAIN (Optional)**

If you want to use `www.mbuganiluxeadventures.com`:

### **7.1 Add Custom Domain in Render**

1. In Render dashboard, go to **Settings**
2. Scroll to **Custom Domains** section
3. Click **"Add Custom Domain"**
4. Enter: `www.mbuganiluxeadventures.com`
5. Click **"Save"**
6. Render will show you DNS records to add

### **7.2 Update DNS Records**

Go to your domain registrar (e.g., Namecheap, GoDaddy) and add:

**CNAME Record:**
```
Type: CNAME
Name: www
Value: YOUR_APP.onrender.com
TTL: 3600
```

**A Record (for root domain):**
```
Type: A
Name: @
Value: [IP provided by Render]
TTL: 3600
```

### **7.3 Wait for DNS Propagation**

- DNS changes can take 1-48 hours
- Check status: https://dnschecker.org
- Render will automatically provision SSL certificate

---

## 🔒 **STEP 8: ENABLE SSL CERTIFICATE**

Render automatically provisions SSL certificates for custom domains.

**To verify:**
1. Go to Render dashboard > Settings
2. Scroll to **Custom Domains**
3. Check that SSL status shows **"Active"**
4. Visit your site with `https://` - should work without warnings

---

## 🚫 **STEP 9: SHUT DOWN RAILWAY WORKER**

⚠️ **IMPORTANT: Wait 24-48 hours before doing this!**

After confirming emails are working correctly:

1. Go to: https://railway.app
2. Select your Django-Q worker service
3. Click **"Settings"**
4. Click **"Stop Service"** (don't delete yet!)
5. Monitor for 1 week
6. If everything works, delete the service

---

## 📊 **STEP 10: POST-DEPLOYMENT MONITORING**

### **First 24 Hours:**
- [ ] Check Render logs every few hours
- [ ] Monitor Mailtrap dashboard for email delivery
- [ ] Test all forms (quote, newsletter, job application)
- [ ] Check website performance
- [ ] Monitor error rates in Sentry (if configured)

### **First Week:**
- [ ] Review Mailtrap delivery statistics
- [ ] Check for any user complaints about slow forms
- [ ] Monitor database performance
- [ ] Check static file loading times
- [ ] Review Render resource usage

### **After 1 Week:**
- [ ] Stop Railway worker (if not already done)
- [ ] Continue monitoring for another week
- [ ] If stable, delete Railway service
- [ ] Update documentation

---

## 🆘 **TROUBLESHOOTING GUIDE**

### **Problem: Deployment Failed**

**Check:**
1. Build logs for specific error
2. requirements.txt includes all dependencies
3. Python version matches (3.12)
4. All environment variables are set

**Solution:**
```bash
# Trigger manual deploy
git commit --allow-empty -m "Trigger rebuild"
git push origin mailltrapapi
```

---

### **Problem: Database Connection Failed**

**Error:**
```
django.db.utils.OperationalError: could not connect to server
```

**Check:**
1. DATABASE_URL is correct
2. Supabase database is running
3. Password doesn't have special characters that need escaping
4. Using port 6543 (connection pooling)

**Solution:**
- Copy DATABASE_URL directly from Supabase dashboard
- Test connection locally first

---

### **Problem: Static Files Not Loading**

**Error:**
```
ValueError: Missing staticfiles manifest entry
```

**Check:**
1. ALLOWED_HOSTS includes your domain
2. STATIC_ROOT is configured
3. collectstatic ran successfully in build logs

**Solution:**
- Check build logs for `Collecting static files...`
- Verify ALLOWED_HOSTS in environment variables

---

### **Problem: Emails Not Sending**

**Error:**
```
Failed to send email via Mailtrap API
```

**Check:**
1. MAILTRAP_API_TOKEN is correct
2. Email addresses are valid
3. Mailtrap account is active
4. Check Mailtrap dashboard for errors

**Solution:**
- Test locally: `python test_mailtrap_email.py`
- Check Mailtrap API token: https://mailtrap.io/api-tokens
- Review Render logs for detailed error messages

---

### **Problem: CSRF Verification Failed**

**Error:**
```
CSRF verification failed. Request aborted.
```

**Check:**
1. CSRF_TRUSTED_ORIGINS includes `https://` prefix
2. All domains are listed
3. Cookies are enabled in browser

**Solution:**
```
CSRF_TRUSTED_ORIGINS=https://www.mbuganiluxeadventures.com,https://mbuganiluxeadventures.com,https://YOUR_APP.onrender.com
```

---

## 📞 **SUPPORT RESOURCES**

**Render Documentation:**
- https://render.com/docs

**Mailtrap Documentation:**
- https://api-docs.mailtrap.io/

**Django Documentation:**
- https://docs.djangoproject.com/

**Supabase Documentation:**
- https://supabase.com/docs

---

## ✅ **DEPLOYMENT COMPLETE CHECKLIST**

- [ ] All environment variables added to Render
- [ ] Deployment successful (check logs)
- [ ] Website loads correctly
- [ ] Static files loading
- [ ] Images loading (Uploadcare)
- [ ] Quote request form works
- [ ] Newsletter subscription works
- [ ] Emails received in Mailtrap
- [ ] Custom domain configured (if applicable)
- [ ] SSL certificate active
- [ ] Railway worker stopped (after 24-48 hours)
- [ ] Monitoring set up
- [ ] Documentation updated

---

**Deployment Date:** _____________  
**Deployed By:** _____________  
**Branch:** mailltrapapi  
**Version:** 1.0 (Mailtrap HTTP API Migration)

---

🎉 **Congratulations! Your deployment is complete!** 🎉

