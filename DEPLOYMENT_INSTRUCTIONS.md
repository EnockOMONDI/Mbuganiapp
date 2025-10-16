# 🚀 DEPLOYMENT INSTRUCTIONS - Quote Request Fix

## **Issue Summary**
- Quote request submissions are failing with HTTP 500 errors
- Response time is 30+ seconds, indicating email timeout
- Service ID: `srv-d3i3gfre5dus738prjb0`

## **Fix Applied**
Updated `users/views.py` to handle email sending timeouts gracefully:
- Added try-catch around email sending
- Quote requests will succeed even if email fails
- Proper error logging for debugging

## **Deployment Steps**

### **1. Commit and Push Changes**
```bash
git add .
git commit -m "Fix quote request email timeout issue - handle email failures gracefully"
git push origin main2
```

### **2. Monitor Deployment**
1. Go to Render Dashboard: https://dashboard.render.com
2. Select service: `Mbuganiapp` (srv-d3i3gfre5dus738prjb0)
3. Watch the deployment progress
4. Check for any build errors

### **3. Verify Environment Variables**
**CRITICAL: Check these are set in Render Dashboard:**
- ✅ `UPLOADCARE_PUBLIC_KEY`: `6fb55bb425b16d386db6`
- ✅ `UPLOADCARE_SECRET_KEY`: `3086089d3d2ac096684d`
- ✅ `EMAIL_HOST_USER`: `mbuganiluxeadventures@gmail.com`
- ✅ `EMAIL_HOST_PASSWORD`: `grdg fofh myne wdpf`
- ✅ `DEFAULT_FROM_EMAIL`: `Mbugani Luxe Adventures <mbuganiluxeadventures@gmail.com>`
- ✅ `ADMIN_EMAIL`: `info@mbuganiluxeadventures.com`

### **4. Test After Deployment**
```bash
# Run the diagnostic script
python render_diagnostics.py
```

### **5. Check Render Logs**
1. Go to Render Dashboard
2. Select `Mbuganiapp` service
3. Click "Logs" tab
4. Submit a test quote request
5. Watch for any errors in real-time

## **Expected Results After Fix**
- ✅ Quote requests complete in 5-10 seconds (not 30+)
- ✅ Users see success message even if email is delayed
- ✅ Quote data is saved to database
- ✅ Emails are sent (may take up to 30 seconds)
- ✅ No more HTTP 500 errors

## **Manual Render Dashboard Steps**

### **Add Missing Environment Variables:**
1. Go to https://dashboard.render.com
2. Select "Mbuganiapp" service
3. Go to "Environment" tab
4. Click "Add Environment Variable"
5. Add these if missing:
   - `UPLOADCARE_PUBLIC_KEY` = `6fb55bb425b16d386db6`
   - `UPLOADCARE_SECRET_KEY` = `3086089d3d2ac096684d`

### **Check Service Status:**
1. Verify service is "Live"
2. Check recent deployments
3. Review any error messages

## **Troubleshooting**

### **If Quote Requests Still Fail:**
1. Check Render logs for specific error messages
2. Verify all environment variables are set
3. Test email configuration separately
4. Check database connectivity

### **Common Error Patterns to Look For:**
- `SMTPAuthenticationError` - Gmail credentials issue
- `socket.timeout` - Network timeout
- `TemplateDoesNotExist` - Missing email templates
- `DatabaseError` - Supabase connection issue

### **Email Testing:**
```python
# Test email configuration
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Test message', 'mbuganiluxeadventures@gmail.com', ['test@example.com'])
```

## **Success Verification**
After deployment, verify:
1. ✅ Website loads: https://www.mbuganiluxeadventures.com
2. ✅ Quote form loads: https://www.mbuganiluxeadventures.com/quote/
3. ✅ Quote submission works (test with real data)
4. ✅ Success message appears
5. ✅ Admin receives notification email
6. ✅ User receives confirmation email

## **Contact Support**
If issues persist:
- Check Render documentation: https://render.com/docs
- Review Django error logs
- Test individual components (database, email, templates)
