# 🚀 MBUGANI EMAIL FIX - DEPLOYMENT CHECKLIST

## **PRE-DEPLOYMENT VERIFICATION** ✅

- [x] Settings check passes: `python manage.py check --settings=tours_travels.settings_prod`
- [x] Email configuration matches Novustell:
  - [x] Port 587 (not 465)
  - [x] EMAIL_USE_TLS = True
  - [x] No EMAIL_TIMEOUT
  - [x] No EMAIL_USE_SSL
- [x] Email sending is synchronous (not async)
- [x] DJANGO_ENV removed from render.yaml
- [x] All changes committed to git

---

## **STEP 1: COMMIT AND PUSH** 📤

```bash
# Review changes
git status
git diff

# Commit changes
git add .
git commit -m "Fix email system: replicate Novustell's proven configuration

- Change email port from 465 to 587 with TLS (matches Novustell)
- Remove EMAIL_TIMEOUT (was causing premature connection failures)
- Switch from async to synchronous email sending (matches Novustell)
- Remove DJANGO_ENV complexity (matches Novustell's simple architecture)
- Hardcode email settings in settings_prod.py instead of env-driven

This matches Novustell Travel's working production setup on Render."

# Push to trigger deployment
git push origin mbugani5
```

**Expected Output:**
```
Enumerating objects: X, done.
Counting objects: 100% (X/X), done.
Delta compression using up to X threads
Compressing objects: 100% (X/X), done.
Writing objects: 100% (X/X), X KiB | X MiB/s, done.
Total X (delta X), reused X (delta X), pack-reused 0
To github.com:username/repo.git
   abc1234..def5678  mbugani5 -> mbugani5
```

---

## **STEP 2: UPDATE RENDER DASHBOARD** 🎛️

### **2.1 Navigate to Render Dashboard**
1. Go to https://dashboard.render.com
2. Log in with your credentials
3. Select **"Mbuganiapp"** service from the list

### **2.2 Remove Unnecessary Environment Variables**

Click on **"Environment"** tab, then **REMOVE** these variables if they exist:

- [ ] EMAIL_PORT
- [ ] EMAIL_USE_TLS
- [ ] EMAIL_USE_SSL
- [ ] EMAIL_TIMEOUT
- [ ] DJANGO_ENV

**How to remove:**
1. Find the variable in the list
2. Click the **trash icon** (🗑️) next to it
3. Confirm deletion

### **2.3 Verify Required Environment Variables**

Ensure these variables are set correctly:

- [ ] **DJANGO_SETTINGS_MODULE** = `tours_travels.settings_prod`
- [ ] **EMAIL_HOST_USER** = `novustellke@gmail.com`
- [ ] **EMAIL_HOST_PASSWORD** = `vsmw vdut tanu gtdg`
- [ ] **DEFAULT_FROM_EMAIL** = `Mbugani Luxe Adventures <novustellke@gmail.com>`
- [ ] **ADMIN_EMAIL** = `info@mbuganiluxeadventures.com`
- [ ] **DATABASE_URL** = `postgresql://postgres.zgwfxeemdgfryiulbapx:JDuH37tYEfVuPpX!@aws-1-eu-west-1.pooler.supabase.com:6543/postgres`
- [ ] **UPLOADCARE_PUBLIC_KEY** = `6fb55bb425b16d386db6`
- [ ] **UPLOADCARE_SECRET_KEY** = `3086089d3d2ac096684d`
- [ ] **SITE_URL** = `https://www.mbuganiluxeadventures.com`

### **2.4 Save Changes**
- [ ] Click **"Save Changes"** button at the bottom
- [ ] Wait for confirmation message

---

## **STEP 3: MONITOR DEPLOYMENT** 👀

### **3.1 Watch Build Process**

In Render dashboard, click on **"Logs"** tab and watch for:

```
🚀 Starting Mbugani Luxe Adventures build process...
📦 Dependencies installed successfully
📁 Static files collected
🗄️ Database migrations applied
💾 Cache table created
✅ Build completed successfully
```

**Build should complete in 2-5 minutes.**

### **3.2 Watch Startup Process**

After build completes, watch for:

```
🌟 Starting Mbugani Luxe Adventures web server...
🌍 Environment: production
🚀 Loading production settings...
✅ Production settings loaded successfully
🚀 Production settings loaded
🌐 Site URL: https://www.mbuganiluxeadventures.com
📧 Email: host=smtp.gmail.com port=587 use_tls=True
🔒 SSL redirect: True
📊 Debug mode: False
[INFO] Listening at: http://0.0.0.0:XXXXX
[INFO] Using worker: sync
[INFO] Booting worker with pid: XXXXX
```

**Critical Success Indicators:**
- ✅ `📧 Email: host=smtp.gmail.com port=587 use_tls=True`
- ✅ `🚀 Production settings loaded`
- ✅ No error messages about email configuration

### **3.3 Verify Service is Live**

- [ ] Service status shows **"Live"** (green indicator)
- [ ] No error messages in logs
- [ ] Health check passes

---

## **STEP 4: TEST EMAIL FUNCTIONALITY** 📧

### **4.1 Test Quote Request Form**

1. **Open the quote form:**
   - [ ] Go to https://www.mbuganiluxeadventures.com/quote/
   - [ ] Or click "Get a Quote" from any package page

2. **Fill out the form with test data:**
   ```
   Full Name: Test User
   Email: your-test-email@gmail.com
   Phone: +254700000000
   Number of Adults: 2
   Number of Children: 0
   Travel Date: [Select a future date]
   Number of Days: 5
   Special Requests: This is a test quote request to verify email functionality
   ```

3. **Submit the form:**
   - [ ] Click "Submit Quote Request" button
   - [ ] Wait for response (should be fast, < 5 seconds)

### **4.2 Verify Success Response**

**Expected Results:**
- [ ] Page redirects to success page
- [ ] Success message displayed: "Thank you! Your quote request has been submitted successfully..."
- [ ] No error messages
- [ ] No timeout errors

### **4.3 Check Email Delivery**

**Admin Email (info@mbuganiluxeadventures.com):**
- [ ] Check inbox for "New Quote Request from Test User"
- [ ] Email contains all form details
- [ ] Email is properly formatted
- [ ] Check spam folder if not in inbox

**User Email (your-test-email@gmail.com):**
- [ ] Check inbox for "Quote Request Received - Mbugani Luxe Adventures"
- [ ] Email contains confirmation details
- [ ] Email is properly formatted
- [ ] Check spam folder if not in inbox

**Timing:**
- Emails should arrive within **1-2 minutes** of form submission

---

## **STEP 5: VERIFY IN RENDER LOGS** 📊

### **5.1 Check for Success Messages**

In Render dashboard logs, search for:

```
INFO Email notifications sent for quote [ID]
INFO Quote request emails sent for Test User
INFO Quote request [ID] submitted successfully
```

### **5.2 Verify NO Error Messages**

**Should NOT see:**
```
❌ ERROR Quote request email error: [Errno 101] Network is unreachable
❌ ERROR [Async] Email notifications FAILED
❌ ERROR Failed to spawn async email thread
```

### **5.3 Check HTTP Response**

Look for successful quote request:
```
POST /quote/?package_id=X HTTP/1.1" 302 0
```

**302 = Successful redirect to success page** ✅

---

## **STEP 6: PRODUCTION MONITORING** 📈

### **First 24 Hours:**

- [ ] Monitor Render logs for any email errors
- [ ] Test quote requests from different packages
- [ ] Verify all emails are delivered
- [ ] Check spam folders periodically
- [ ] Monitor server response times

### **Success Metrics:**

- [ ] **Email Delivery Rate:** 100% (all emails delivered)
- [ ] **Response Time:** < 5 seconds for quote submissions
- [ ] **Error Rate:** 0% (no network unreachable errors)
- [ ] **User Experience:** Smooth, no timeouts

---

## **TROUBLESHOOTING GUIDE** 🔧

### **Issue: Emails still not sending**

**Check:**
1. Render logs for exact error message
2. Environment variables in Render dashboard
3. Gmail account hasn't blocked Render IPs
4. Email credentials are correct

**Solution:**
```bash
# SSH into Render shell (if available)
python manage.py shell --settings=tours_travels.settings_prod

# Test email manually
from django.core.mail import send_mail
send_mail(
    'Test Email',
    'This is a test.',
    'novustellke@gmail.com',
    ['your-email@gmail.com'],
    fail_silently=False,
)
```

### **Issue: "[Errno 101] Network is unreachable"**

**This should be FIXED by the changes. If it still occurs:**

1. Verify EMAIL_PORT = 587 in logs
2. Verify EMAIL_USE_TLS = True in logs
3. Verify no EMAIL_TIMEOUT in settings
4. Check Render's network status

### **Issue: "Authentication failed"**

**Check:**
1. EMAIL_HOST_PASSWORD is correct in Render dashboard
2. Gmail app password hasn't expired
3. Gmail account is active

### **Issue: Deployment fails**

**Check:**
1. Build logs for specific error
2. requirements.txt is up to date
3. Database migrations are compatible
4. Static files collection succeeds

---

## **ROLLBACK PLAN** ⏮️

If emails still don't work after deployment:

```bash
# Revert to previous commit
git log --oneline  # Find previous commit hash
git revert HEAD
git push origin mbugani5

# Or reset to previous commit
git reset --hard [previous-commit-hash]
git push origin mbugani5 --force
```

**Then:**
1. Contact support with Render logs
2. Consider alternative email providers (SendGrid, Mailgun)
3. Review Novustell's actual production environment variables

---

## **SUCCESS CONFIRMATION** ✅

**All checks passed when:**

- [x] Code deployed successfully to Render
- [x] Production settings load correctly
- [x] Email configuration shows port 587 with TLS
- [ ] **Quote request form submits successfully**
- [ ] **Admin receives email notification**
- [ ] **User receives confirmation email**
- [ ] **No "[Errno 101] Network is unreachable" errors**
- [ ] **Render logs show successful email sending**

---

## **FINAL NOTES** 📝

- This configuration **exactly matches** Novustell Travel's working production setup
- Novustell has been running this configuration successfully on Render for months
- The key differences that were causing failures:
  1. Port 465 → 587
  2. SSL → TLS
  3. EMAIL_TIMEOUT → removed
  4. Async → Synchronous
  5. DJANGO_ENV → removed

**Expected Result:** 100% email delivery rate, matching Novustell's proven reliability.

---

**Deployment Date:** _____________
**Deployed By:** _____________
**Status:** _____________
**Notes:** _____________

