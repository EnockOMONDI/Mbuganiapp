# 🔧 Railway Email Port Configuration Update

## 🎯 Issue: SMTP Connection Timeout

**Problem**: Railway's network appears to be blocking or limiting outbound connections to Gmail SMTP on port 587 (TLS).

**Solution**: Switch to port 465 (SSL) which often has better compatibility with cloud platforms.

---

## ✅ Code Changes Applied

### 1. **Updated Email Configuration** (settings_prod.py)
- Changed default port from 587 (TLS) to 465 (SSL)
- Made port configurable via environment variable
- Reduced timeout from 120s to 30s per attempt
- Added proper SSL/TLS switching based on port

### 2. **Optimized Retry Logic** (users/tasks.py)
- Reduced retries from 3 to 2 attempts
- Added explicit connection management
- Reduced wait time between retries to 2 seconds
- Added 30-second timeout per attempt
- Total max time per email: ~64 seconds (2 attempts × 30s + 2s wait)

---

## 🚀 Railway Environment Variable Update

### **Option 1: Use Port 465 (SSL) - RECOMMENDED**

Add this environment variable in Railway dashboard:

```bash
EMAIL_PORT=465
```

**Why Port 465?**
- ✅ Uses SSL (more secure handshake)
- ✅ Better compatibility with cloud platforms
- ✅ Less likely to be blocked by firewalls
- ✅ Faster connection establishment

### **Option 2: Keep Port 587 (TLS)**

If you prefer to keep using port 587:

```bash
EMAIL_PORT=587
```

**Note**: Port 587 may continue to have timeout issues on Railway.

---

## 📝 How to Update Railway Environment Variables

### **Method 1: Railway Dashboard (Recommended)**

1. Go to Railway dashboard: https://railway.app/
2. Select your project
3. Click on your worker service
4. Go to **Variables** tab
5. Click **+ New Variable**
6. Add:
   - **Variable**: `EMAIL_PORT`
   - **Value**: `465`
7. Click **Add**
8. Railway will automatically redeploy

### **Method 2: Railway CLI**

```bash
railway variables set EMAIL_PORT=465
```

---

## 🧪 Testing After Update

### **Step 1: Wait for Deployment**
Railway will automatically redeploy after you add the environment variable. Wait for:
```
✅ Build successful
✅ Deployment successful
✅ Service running
```

### **Step 2: Clear Old Failed Tasks**
```bash
python clear_all_queued_tasks.py
```

### **Step 3: Submit Test Quote Request**
1. Go to your website
2. Submit a quote request
3. Monitor Railway logs

### **Expected Railway Logs (Success)**
```
INFO Starting async email sending for quote request 93
INFO Attempting to send email (attempt 1/2)
INFO Email sent successfully on attempt 1
INFO Admin notification sent for quote request 93
INFO Attempting to send email (attempt 1/2)
INFO Email sent successfully on attempt 1
INFO User confirmation sent for quote request 93
```

### **If Still Timing Out**
```
ERROR Task exceeded maximum timeout value (60 seconds)
```

This means Railway is blocking SMTP entirely. See **Alternative Solutions** below.

---

## 🔄 Alternative Solutions (If Port 465 Doesn't Work)

### **Option A: Use SendGrid (Free Tier)**

SendGrid offers 100 emails/day free and works well with Railway.

1. **Sign up**: https://sendgrid.com/
2. **Get API Key**
3. **Install package**:
   ```bash
   pip install sendgrid
   ```
4. **Update settings_prod.py**:
   ```python
   EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'
   SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
   ```
5. **Add to Railway**:
   ```bash
   SENDGRID_API_KEY=your_api_key_here
   ```

### **Option B: Use Mailgun (Free Tier)**

Mailgun offers 5,000 emails/month free.

1. **Sign up**: https://www.mailgun.com/
2. **Get API credentials**
3. **Install package**:
   ```bash
   pip install django-mailgun
   ```
4. **Update settings_prod.py**:
   ```python
   EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
   MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY')
   MAILGUN_DOMAIN_NAME = os.getenv('MAILGUN_DOMAIN')
   ```

### **Option C: Use Resend (Modern Alternative)**

Resend offers 3,000 emails/month free with excellent deliverability.

1. **Sign up**: https://resend.com/
2. **Get API Key**
3. **Install package**:
   ```bash
   pip install resend
   ```
4. **Create custom backend** or use their API directly

### **Option D: Move Worker Back to Render**

If Railway's network restrictions are too limiting:

1. Move Django-Q worker back to Render
2. Use Render's background worker service
3. Render may have better SMTP connectivity

---

## 📊 Current Configuration Summary

### **Email Settings**
```python
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465  # SSL (default, configurable)
EMAIL_USE_SSL = True  # For port 465
EMAIL_USE_TLS = False  # For port 587
EMAIL_TIMEOUT = 30  # seconds per attempt
```

### **Retry Settings**
```python
max_retries = 2  # 2 attempts per email
wait_time = 2  # seconds between retries
timeout_per_attempt = 30  # seconds
total_max_time = 64  # seconds (2×30 + 2)
```

### **Django-Q Settings**
```python
timeout = 180  # 3 minutes (allows for retries)
retry = 300  # 5 minutes (retry failed tasks)
max_attempts = 5  # total task retry attempts
```

---

## 🎯 Recommended Next Steps

1. **Add `EMAIL_PORT=465` to Railway** ✅
2. **Wait for automatic redeployment** ⏳
3. **Clear old failed tasks** 🧹
4. **Test with new quote request** 🧪
5. **Monitor Railway logs** 👀

### **If Port 465 Works**
✅ Problem solved! Continue using Gmail SMTP.

### **If Port 465 Still Times Out**
❌ Railway is blocking SMTP entirely.
➡️ Switch to SendGrid, Mailgun, or Resend (recommended)

---

## 📞 Support

**Current Status**: Testing port 465 (SSL) for better Railway compatibility

**Next Update**: After testing port 465, we'll know if we need to switch to a transactional email service.

**Files Modified**:
- `tours_travels/settings_prod.py` - Email configuration
- `users/tasks.py` - Retry logic optimization

**Deployment**: Pushed to `railwayapp` branch, waiting for Railway auto-deploy

---

**Last Updated**: October 16, 2025  
**Status**: 🧪 Testing port 465 (SSL)
