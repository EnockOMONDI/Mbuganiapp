# 🚀 Mailtrap SMTP Migration Guide

## ✅ Code Changes Completed

The following file has been updated to use Mailtrap SMTP:

### **File: `tours_travels/settings_prod.py`**

**Changes Made:**
- ✅ Changed `EMAIL_HOST` from `smtp.gmail.com` to `live.smtp.mailtrap.io`
- ✅ Changed `EMAIL_PORT` from `465` to `2525` (Railway-compatible)
- ✅ Set `EMAIL_USE_TLS = True` (required by Mailtrap)
- ✅ Set `EMAIL_USE_SSL = False` (not using SSL)
- ✅ Changed `EMAIL_HOST_USER` to hardcoded `'api'` (Mailtrap requirement)
- ✅ Changed `EMAIL_HOST_PASSWORD` to use `MAILTRAP_API_TOKEN` environment variable
- ✅ Updated `DEFAULT_FROM_EMAIL` to `info@mbuganiluxeadventures.com`

---

## 📋 Railway Environment Variables Configuration

### **Step 1: Add New Environment Variables**

Go to your Railway dashboard → Select your **Django-Q Worker** service → **Variables** tab → Add these variables:

```bash
# Mailtrap API Token (REQUIRED)
MAILTRAP_API_TOKEN=<YOUR_MAILTRAP_API_TOKEN>

# Email Port (Railway-compatible)
EMAIL_PORT=2525

# Default From Email (updated to use verified domain)
DEFAULT_FROM_EMAIL=Mbugani Luxe Adventures <info@mbuganiluxeadventures.com>
```

**How to Get Your Mailtrap API Token:**
1. Log in to https://mailtrap.io
2. Go to **Sending Domains** → Click on `mbuganiluxeadventures.com`
3. Click **Integrations** tab
4. Click **Integrate** under **Transactional Stream**
5. Toggle to **SMTP**
6. Copy the **Password** field - this is your API token
7. Paste it as the value for `MAILTRAP_API_TOKEN` in Railway

---

### **Step 2: Remove Old Gmail Environment Variables**

**Remove these variables from Railway** (no longer needed):

```bash
EMAIL_HOST_USER          # Was: mbuganiluxeadventures@gmail.com
EMAIL_HOST_PASSWORD      # Was: Gmail app password
```

**Note:** The new configuration uses:
- `EMAIL_HOST_USER = 'api'` (hardcoded in settings_prod.py)
- `EMAIL_HOST_PASSWORD = MAILTRAP_API_TOKEN` (from environment variable)

---

### **Step 3: Verify Other Email Variables (Optional)**

These variables should already exist in Railway. Verify they are set correctly:

```bash
ADMIN_EMAIL=info@mbuganiluxeadventures.com
JOBS_EMAIL=careers@mbuganiluxeadventures.com
NEWSLETTER_EMAIL=news@mbuganiluxeadventures.com
```

If they don't exist, add them. If they exist with different values, update them if needed.

---

## 🔄 Git Deployment Commands

### **Step 1: Check Current Status**

```bash
git status
```

### **Step 2: Add Changes**

```bash
git add tours_travels/settings_prod.py
git add MAILTRAP_MIGRATION_GUIDE.md
```

### **Step 3: Commit Changes**

```bash
git commit -m "Migrate from Gmail SMTP to Mailtrap for Railway compatibility

- Switch EMAIL_HOST to live.smtp.mailtrap.io
- Use port 2525 for Railway network compatibility
- Update EMAIL_HOST_USER to 'api' (Mailtrap requirement)
- Use MAILTRAP_API_TOKEN environment variable
- Update DEFAULT_FROM_EMAIL to info@mbuganiluxeadventures.com
- Maintain existing retry logic and timeout settings"
```

### **Step 4: Push to Railway Branch**

```bash
git push origin railwayapp
```

**Note:** Railway will automatically detect the push and redeploy the worker service.

---

## 📊 Complete Environment Variables Summary

### **Railway Environment Variables (After Migration)**

| Variable Name | Value | Notes |
|---------------|-------|-------|
| `MAILTRAP_API_TOKEN` | `<your_token>` | **NEW** - Get from Mailtrap dashboard |
| `EMAIL_PORT` | `2525` | **UPDATED** - Railway-compatible port |
| `DEFAULT_FROM_EMAIL` | `Mbugani Luxe Adventures <info@mbuganiluxeadventures.com>` | **UPDATED** - Verified domain |
| `ADMIN_EMAIL` | `info@mbuganiluxeadventures.com` | Existing (verify) |
| `JOBS_EMAIL` | `careers@mbuganiluxeadventures.com` | Existing (verify) |
| `NEWSLETTER_EMAIL` | `news@mbuganiluxeadventures.com` | Existing (verify) |
| `DATABASE_URL` | `<supabase_url>` | Existing (no change) |
| `DJANGO_COLORS` | `nocolor` | Existing (no change) |

### **Variables to Remove:**
- ❌ `EMAIL_HOST_USER` (now hardcoded as 'api')
- ❌ `EMAIL_HOST_PASSWORD` (replaced by MAILTRAP_API_TOKEN)

---

## 🧪 Testing Procedure

### **Step 1: Clear Old Tasks**

Before testing, clear any old failed tasks from the queue:

```bash
python clear_all_queued_tasks.py
```

### **Step 2: Monitor Railway Logs**

1. Open Railway dashboard
2. Select your Django-Q Worker service
3. Go to **Deployments** → Click latest deployment → **View Logs**
4. Keep this window open

### **Step 3: Submit Test Quote Request**

1. Go to your production website: https://mbuganiluxeadventures.com
2. Navigate to a tour/package page
3. Fill out and submit a quote request form
4. Note the quote request ID (if visible)

### **Step 4: Verify Railway Logs**

**Expected Success Logs:**
```
INFO Process-XXXXXXXX processing quote_emails_XX 'users.tasks.send_quote_request_emails_async'
INFO Starting async email sending for quote request XX
INFO Attempting to send email (attempt 1/2)
INFO Email sent successfully on attempt 1
INFO Admin notification sent for quote request XX
INFO User confirmation sent for quote request XX
```

**What You Should NOT See:**
- ❌ `Task exceeded maximum timeout value (60 seconds)`
- ❌ `TimeoutException`
- ❌ `SMTPServerDisconnected`
- ❌ `Connection refused`

### **Step 5: Verify Email Delivery**

**Check Mailtrap Dashboard:**
1. Log in to https://mailtrap.io
2. Go to **Email Logs**
3. You should see 2 emails:
   - Admin notification to `info@mbuganiluxeadventures.com`
   - User confirmation to the email address used in the quote request

**Check Actual Inboxes:**
1. Check `info@mbuganiluxeadventures.com` inbox
2. Check the user's email inbox (the one used in the quote request)
3. Both should have received emails

**Email Tracking in Mailtrap:**
- Click on any email in Email Logs to see:
  - Delivery status
  - Open tracking
  - Click tracking
  - Full email content
  - SMTP conversation logs

---

## 🔍 Troubleshooting

### **Issue 1: "MAILTRAP_API_TOKEN is None" Error**

**Cause:** Environment variable not set in Railway

**Solution:**
1. Go to Railway dashboard → Variables
2. Add `MAILTRAP_API_TOKEN` with your token from Mailtrap
3. Railway will auto-redeploy

### **Issue 2: "Authentication failed" Error**

**Cause:** Invalid or expired API token

**Solution:**
1. Go to Mailtrap → Settings → API Tokens
2. Generate a new token
3. Update `MAILTRAP_API_TOKEN` in Railway
4. Railway will auto-redeploy

### **Issue 3: "Sender address rejected" Error**

**Cause:** Domain not verified or using wrong sender email

**Solution:**
1. Verify `mbuganiluxeadventures.com` is verified in Mailtrap
2. Check DNS records are properly configured
3. Ensure `DEFAULT_FROM_EMAIL` uses `@mbuganiluxeadventures.com` domain

### **Issue 4: Still Getting Timeout Errors**

**Cause:** Port 2525 might also be blocked by Railway

**Solution:**
Try alternative ports:
```bash
# In Railway, update EMAIL_PORT to:
EMAIL_PORT=587   # Try TLS port
# or
EMAIL_PORT=465   # Try SSL port
```

Then update `settings_prod.py` if needed.

### **Issue 5: Emails Not Appearing in Inbox**

**Cause:** Emails might be in spam or Mailtrap is in sandbox mode

**Solution:**
1. Check spam/junk folders
2. Verify domain is in **Sending Domains** (not Email Sandbox)
3. Check Mailtrap Email Logs for delivery status
4. Verify compliance check is complete

---

## 📈 Expected Improvements

### **Before (Gmail SMTP):**
- ❌ Port 587/465 blocked by Railway
- ❌ Timeout errors after 60 seconds
- ❌ No email delivery tracking
- ❌ "Less secure app" security concerns

### **After (Mailtrap SMTP):**
- ✅ Port 2525 designed for cloud platforms
- ✅ Fast, reliable connections
- ✅ Email delivery tracking and analytics
- ✅ Professional email infrastructure
- ✅ Better deliverability
- ✅ Webhook support for events
- ✅ Unsubscribe management

---

## 🎯 Success Criteria

**The migration is successful when:**

1. ✅ Railway worker starts without errors
2. ✅ Quote request emails are queued successfully
3. ✅ Railway logs show "Email sent successfully on attempt 1"
4. ✅ Emails appear in Mailtrap Email Logs
5. ✅ Emails are delivered to actual inboxes
6. ✅ No timeout errors in Railway logs
7. ✅ Email sending completes within 30-60 seconds

---

## 📞 Support

**If you encounter issues:**

1. **Check Railway Logs** - Most issues show up here
2. **Check Mailtrap Email Logs** - Shows delivery status
3. **Verify Environment Variables** - Ensure all variables are set correctly
4. **Check Domain Verification** - Ensure domain is verified in Mailtrap
5. **Contact Mailtrap Support** - support@mailtrap.io

---

## 🔐 Security Notes

- ✅ `MAILTRAP_API_TOKEN` is stored securely in Railway environment variables
- ✅ Token is never committed to Git
- ✅ Token can be rotated anytime in Mailtrap dashboard
- ✅ Each domain has separate credentials
- ✅ TLS encryption for all email transmission

---

**Migration Date:** 2025-10-17  
**Migrated From:** Gmail SMTP (smtp.gmail.com:465)  
**Migrated To:** Mailtrap SMTP (live.smtp.mailtrap.io:2525)  
**Reason:** Railway free tier blocks Gmail SMTP ports 465/587

