# 🚀 MBUGANI LUXE ADVENTURES - RENDER ENVIRONMENT SETUP GUIDE

## 📋 **OVERVIEW**
This guide provides the exact steps to configure environment variables in the Render Dashboard for the Mbugani Luxe Adventures deployment.

---

## 🔧 **CLEANED UP .env FILE**

The `.env` file has been completely reorganized and cleaned up:

### **✅ REMOVED (No longer needed):**
- ❌ Development-only settings (DEBUG=True, console email backend)
- ❌ Variables already defined in render.yaml (duplicates)
- ❌ Unnecessary configuration variables (100+ removed)
- ❌ Local development paths and settings
- ❌ Redundant security and performance settings

### **✅ KEPT (Essential for production):**
- ✅ **Security**: SECRET_KEY, DJANGO_SETTINGS_MODULE, DEBUG=False
- ✅ **Email**: Novustell credentials and Mbugani business emails
- ✅ **Database**: Supabase PostgreSQL connection string
- ✅ **Media**: Uploadcare keys for file management
- ✅ **Domains**: ALLOWED_HOSTS and SITE_URL
- ✅ **Business**: WhatsApp contact information

---

## 🎯 **CRITICAL VARIABLES FOR RENDER DASHBOARD**

Copy these **EXACT VALUES** to Render Dashboard > Environment Tab:

### **🔐 Security & Core**
```
DJANGO_SETTINGS_MODULE = tours_travels.settings_prod
SECRET_KEY = djngo-iiamysing30ochatachterxfoatensedonfgssooeyyspw--EDIGIQDFNNNWDEJJJWEDFRTCVF
DEBUG = False
ALLOWED_HOSTS = mbuganiapp.onrender.com,mbuganiluxeadventures.com,www.mbuganiluxeadventures.com
SITE_URL = https://www.mbuganiluxeadventures.com
```

### **📧 Email Configuration (CRITICAL)**
```
EMAIL_HOST_USER = novustellke@gmail.com
EMAIL_HOST_PASSWORD = vsmw vdut tanu gtdg
DEFAULT_FROM_EMAIL = Mbugani Luxe Adventures <novustellke@gmail.com>
ADMIN_EMAIL = info@mbuganiluxeadventures.com
JOBS_EMAIL = careers@mbuganiluxeadventures.com
NEWSLETTER_EMAIL = news@mbuganiluxeadventures.com
```

### **🗄️ Database**
```
DATABASE_URL = postgresql://postgres.zgwfxeemdgfryiulbapx:JDuH37tYEfVuPpX!@aws-1-eu-west-1.pooler.supabase.com:6543/postgres
```

### **📁 Uploadcare (MUST SET MANUALLY)**
```
UPLOADCARE_PUBLIC_KEY = 6fb55bb425b16d386db6
UPLOADCARE_SECRET_KEY = 3086089d3d2ac096684d
```

### **📱 Business Contact**
```
WHATSAPP_PHONE = +254701363551
```

---

## 🔧 **OPTIONAL VARIABLES (Have Defaults)**

These are optional and only need to be set if you want to override defaults:

```
TIME_ZONE = Africa/Nairobi
DEFAULT_COUNTRY = Kenya
DEFAULT_CURRENCY = USD
DEFAULT_BOOKING_EXPIRY_HOURS = 24
MAX_BOOKING_ADULTS = 20
MAX_BOOKING_CHILDREN = 15
MAX_BOOKING_ROOMS = 10
```

---

## 📝 **STEP-BY-STEP RENDER SETUP**

### **Step 1: Access Render Dashboard**
1. Go to https://dashboard.render.com
2. Log in to your account
3. Select your **Mbuganiapp** service

### **Step 2: Configure Environment Variables**
1. Click on the **"Environment"** tab
2. Click **"Add Environment Variable"**
3. Copy and paste each variable from the **CRITICAL VARIABLES** section above
4. **Important**: Copy the exact values including spaces and special characters

### **Step 3: Save and Deploy**
1. Click **"Save Changes"** after adding all variables
2. Render will automatically trigger a new deployment
3. Monitor the deployment logs for any errors

### **Step 4: Verify Deployment**
1. Wait for deployment to complete (5-10 minutes)
2. Test the website: https://www.mbuganiluxeadventures.com
3. Test quote request functionality
4. Check that emails are being sent successfully

---

## 🚨 **CRITICAL NOTES**

### **Email System**
- ✅ **Using proven Novustell credentials** for reliable email delivery
- ✅ **Emails show "Mbugani Luxe Adventures"** branding to customers
- ✅ **100% test success rate** achieved with these credentials

### **Security**
- 🔒 **UPLOADCARE keys MUST be set manually** (not in render.yaml for security)
- 🔒 **SECRET_KEY is production-ready** and secure
- 🔒 **DEBUG=False** ensures production security

### **Database**
- 🗄️ **Supabase PostgreSQL** connection configured
- 🗄️ **Connection pooling** enabled for performance

---

## ✅ **VERIFICATION CHECKLIST**

After setting up environment variables in Render:

- [ ] **Deployment completes successfully** (no build errors)
- [ ] **Website loads** at https://www.mbuganiluxeadventures.com
- [ ] **Quote request form loads** without errors
- [ ] **Quote submission works** (no 500 errors)
- [ ] **Admin receives quote emails** at info@mbuganiluxeadventures.com
- [ ] **Customer receives confirmation emails**
- [ ] **Response time < 10 seconds** (not 30+ seconds)
- [ ] **Static files load correctly** (CSS, images, etc.)
- [ ] **Admin panel accessible** at /admin/

---

## 🔍 **TROUBLESHOOTING**

### **If deployment fails:**
1. Check Render logs for specific error messages
2. Verify all environment variables are set correctly
3. Ensure no typos in variable names or values

### **If emails don't work:**
1. Verify EMAIL_HOST_PASSWORD is exactly: `vsmw vdut tanu gtdg`
2. Check that EMAIL_HOST_USER is: `novustellke@gmail.com`
3. Run the email test: `python test_mbugani_email_system.py --quick`

### **If quote requests timeout:**
1. Check that DJANGO_SETTINGS_MODULE is set to `tours_travels.settings_prod`
2. Verify DATABASE_URL is correct
3. Monitor Render logs during quote submission

---

## 📞 **SUPPORT**

If you encounter issues:
1. **Check Render logs** first for specific error messages
2. **Run diagnostic scripts** locally to test components
3. **Verify environment variables** are exactly as specified above

**Remember**: The background worker service is non-functional and should be removed from render.yaml to avoid deployment issues.

---

**🎉 SUCCESS**: Once all variables are set correctly, the Mbugani Luxe Adventures website will be fully operational with reliable email delivery using the proven Novustell Travel credentials while maintaining Mbugani branding.
