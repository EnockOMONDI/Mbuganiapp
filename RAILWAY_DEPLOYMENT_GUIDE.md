# 🚂 Railway.app Django-Q Worker Deployment Guide

This guide walks you through deploying your Django-Q background worker to Railway.app while keeping your web app on Render.

## 📋 Prerequisites

- ✅ Django-Q implemented and working locally
- ✅ Render web service running successfully
- ✅ GitHub repository with `railwayapp` branch
- ✅ Railway.app account (free tier)

## 🚀 Step 1: Create Railway Project

1. **Go to Railway.app**
   - Visit https://railway.app
   - Sign in with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `Mbuganiapp` repository
   - Select `railwayapp` branch

3. **Configure Service Type**
   - Railway will auto-detect as Python app
   - It will use the `Procfile` and `railway.json` we created

## ⚙️ Step 2: Set Environment Variables

Copy these environment variables from your Render dashboard to Railway:

### 🔐 Sensitive Variables (Copy from Render)
```
SECRET_KEY=<COPY_FROM_RENDER>
DATABASE_URL=<COPY_FROM_RENDER>
EMAIL_HOST_PASSWORD=<COPY_FROM_RENDER>
```

### 📝 Standard Variables (Copy as-is)
```
DJANGO_SETTINGS_MODULE=tours_travels.settings_prod
DEBUG=False
EMAIL_HOST_USER=mbuganiluxeadventures@gmail.com
DEFAULT_FROM_EMAIL=Mbugani Luxe Adventures <mbuganiluxeadventures@gmail.com>
ADMIN_EMAIL=info@mbuganiluxeadventures.com
JOBS_EMAIL=careers@mbuganiluxeadventures.com
NEWSLETTER_EMAIL=news@mbuganiluxeadventures.com
SITE_URL=https://www.mbuganiluxeadventures.com
ALLOWED_HOSTS=www.mbuganiluxeadventures.com,mbuganiluxeadventures.com
RAILWAY_ENVIRONMENT=production
```

### 📍 How to Add Variables in Railway
1. Go to Railway dashboard → Your project
2. Click on your service
3. Go to "Variables" tab
4. Add each variable above
5. Click "Deploy" to restart with new variables

## 🔍 Step 3: Verify Deployment

### ✅ Check Railway Logs
1. Go to Railway dashboard → Your service → "Logs"
2. Look for these success messages:
   ```
   🚀 Production settings loaded
   INFO Q Cluster starting.
   INFO Q Cluster [mbugani_luxe_prod] running.
   INFO Process ready for work
   ```

### ✅ Test Email Processing
1. Submit a quote request on your website
2. Check Railway logs for task processing
3. Verify email delivery
4. Check Django admin: `/admin/django_q/`

## 📊 Step 4: Monitor & Optimize

### 🔍 Monitoring
- **Railway Logs**: Real-time worker activity
- **Django Admin**: Task queue status at `/admin/django_q/`
- **Email Delivery**: Check inbox for test emails

### ⚡ Free Tier Optimization
- **Memory**: Set to 512MB minimum
- **CPU**: Set to 0.25 vCPU minimum
- **Auto-scaling**: Disable to control costs
- **Sleep Mode**: Worker sleeps when no tasks (automatic)

### 💰 Usage Monitoring
- Railway dashboard shows credit usage
- ~$5/month free credit
- Worker uses minimal resources when idle

## 🔧 Troubleshooting

### ❌ Worker Won't Start
**Check Railway logs for:**
- Missing environment variables
- Database connection errors
- Import/dependency errors

**Solutions:**
- Verify all environment variables are set
- Check DATABASE_URL is correct
- Ensure `requirements.txt` includes `django-q2`

### ❌ Tasks Not Processing
**Check:**
- Railway service is running (not sleeping)
- Database connection working
- Tasks appear in Django admin queue

**Solutions:**
- Restart Railway service
- Check DATABASE_URL matches Render exactly
- Verify Django-Q configuration

### ❌ Emails Not Sending
**Check:**
- EMAIL_HOST_USER and EMAIL_HOST_PASSWORD set correctly
- Gmail SMTP settings correct
- Railway logs for SMTP errors

**Solutions:**
- Verify Gmail app password is correct
- Check firewall/network restrictions
- Test email settings locally

## 🎯 Expected Behavior

### ✅ Normal Operation
1. **User submits quote** → Render web app responds instantly
2. **Task queued** → Stored in PostgreSQL database
3. **Railway picks up task** → Within 5-10 seconds
4. **Email sent** → Via Gmail SMTP
5. **Task completed** → Removed from queue

### 📈 Performance Metrics
- **Response time**: <2 seconds (Render web app)
- **Task processing**: 5-10 seconds (Railway worker)
- **Email delivery**: 10-30 seconds total
- **Resource usage**: <10% of Railway free tier

## 🔄 Maintenance

### 🔄 Updates
- Push changes to `railwayapp` branch
- Railway auto-deploys on git push
- Worker restarts automatically

### 🔄 Scaling
- Free tier: 1 worker instance
- Paid tier: Multiple workers possible
- Current setup handles 100+ emails/hour

## ✅ Success Checklist

- [ ] Railway project created and deployed
- [ ] All environment variables configured
- [ ] Worker logs show "ready for work"
- [ ] Test quote request processes successfully
- [ ] Email delivered to inbox
- [ ] Django admin shows completed tasks
- [ ] Render web service still working normally

## 🆘 Support

If you encounter issues:

1. **Check Railway logs** for error messages
2. **Verify environment variables** match Render exactly
3. **Test locally** with same settings
4. **Check database connectivity** from Railway
5. **Monitor resource usage** in Railway dashboard

---

🎉 **Congratulations!** Your Django-Q worker is now running on Railway.app, processing background email tasks while your web app continues running on Render.

**Benefits achieved:**
- ✅ No more worker timeouts on Render
- ✅ Instant response times for users
- ✅ Reliable background email processing
- ✅ Cost-effective free tier usage
- ✅ Automatic restarts and monitoring
