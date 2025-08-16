# 🚀 Build Script Documentation - Mbugani Luxe Adventures

## **📋 Overview**

The `build.sh` script is a comprehensive Django deployment script designed specifically for Render.com production deployment of the Mbugani Luxe Adventures application. It handles all essential Django deployment steps with proper error handling and logging.

## **✨ Features**

### **🔧 Core Functionality**
- **Environment Verification**: Checks required environment variables
- **Dependency Installation**: Installs Python packages from requirements.txt
- **Database Migrations**: Applies pending database migrations
- **Static Files Collection**: Collects and prepares static files for production
- **Cache Table Creation**: Sets up database caching tables
- **Superuser Creation**: Creates admin user account
- **System Checks**: Validates Django configuration
- **Deployment Verification**: Confirms deployment readiness

### **🛡️ Error Handling**
- **Comprehensive Error Trapping**: Exits on any command failure
- **Detailed Error Messages**: Provides specific error information
- **Build Time Tracking**: Reports total build duration
- **Colored Output**: Easy-to-read console output with color coding

### **📊 Logging & Monitoring**
- **Step-by-Step Progress**: Clear indication of current build step
- **Success/Warning/Error Messages**: Categorized output messages
- **Build Statistics**: Start time, end time, and duration tracking
- **Environment Information**: Python version, pip version, etc.

## **🔧 Configuration**

### **Required Environment Variables**
```bash
# Essential variables that must be set
DATABASE_URL=postgresql://...           # Database connection string
SECRET_KEY=your-secret-key             # Django secret key
DJANGO_SETTINGS_MODULE=tours_travels.settings_prod  # Settings module
```

### **Optional Environment Variables**
```bash
# Superuser configuration (with defaults)
DJANGO_SUPERUSER_USERNAME=mbuganiluxeadventures
DJANGO_SUPERUSER_EMAIL=admin@mbuganiluxeadventures.com
DJANGO_SUPERUSER_PASSWORD=mbuganiluxeadventurespassword
```

## **📝 Build Steps Executed**

### **1. Environment Verification**
- Checks for required environment variables
- Validates Django settings module
- Ensures database connectivity

### **2. Dependency Installation**
- Upgrades pip to latest version
- Installs all packages from requirements.txt
- Verifies successful installation

### **3. System Checks**
- Runs Django's built-in system checks
- Validates configuration integrity
- Identifies potential issues

### **4. Database Migrations**
- Tests database connectivity
- Creates new migrations if needed
- Applies all pending migrations

### **5. Cache Table Creation**
- Creates database cache tables
- Handles existing table scenarios
- Configures caching infrastructure

### **6. Static Files Collection**
- Collects static files from all apps
- Processes and compresses files
- Prepares files for production serving

### **7. Superuser Creation**
- Creates admin user account
- Uses environment variables for credentials
- Skips if user already exists

### **8. Deployment Verification**
- Validates Django setup
- Confirms all components working
- Reports deployment readiness

## **🚀 Usage**

### **Local Testing**
```bash
# Make script executable
chmod +x build.sh

# Test script syntax
bash -n build.sh

# Run with environment variables
export DATABASE_URL="your-database-url"
export SECRET_KEY="your-secret-key"
export DJANGO_SETTINGS_MODULE="tours_travels.settings_prod"
./build.sh
```

### **Render.com Deployment**
The script is automatically executed by Render.com during deployment when specified in `render.yaml`:

```yaml
buildCommand: ./build.sh
```

## **📊 Output Examples**

### **Successful Build**
```
🚀 Starting Mbugani Luxe Adventures Django Application Build
================================================================
📅 Build started at: Mon Jan 15 10:30:00 UTC 2024
🌍 Environment: Production (Render.com)
🐍 Python version: Python 3.12.0
📦 Pip version: pip 24.0
================================================================

🔄 STEP: Checking environment variables
ℹ️  INFO: DATABASE_URL is set
ℹ️  INFO: SECRET_KEY is set
ℹ️  INFO: DJANGO_SETTINGS_MODULE is set
✅ SUCCESS: All required environment variables are set

🔄 STEP: Installing Python dependencies
ℹ️  INFO: Upgrading pip
ℹ️  INFO: Installing requirements from requirements.txt
✅ SUCCESS: Dependencies installed successfully

🔄 STEP: Running Django system checks
ℹ️  INFO: Performing comprehensive system check
✅ SUCCESS: System checks passed

🔄 STEP: Running database migrations
ℹ️  INFO: Testing database connectivity
ℹ️  INFO: Checking for new migrations
ℹ️  INFO: Applying database migrations
✅ SUCCESS: Database migrations completed successfully

🔄 STEP: Creating cache table
ℹ️  INFO: Creating database cache table
✅ SUCCESS: Cache table setup completed

🔄 STEP: Collecting static files
ℹ️  INFO: Preparing static files directory
ℹ️  INFO: Running collectstatic
✅ SUCCESS: Static files collected successfully

🔄 STEP: Creating superuser account
ℹ️  INFO: Creating superuser with username: mbuganiluxeadventures
✅ SUCCESS: Superuser setup completed

🔄 STEP: Verifying deployment readiness
ℹ️  INFO: Verifying Django settings
✅ SUCCESS: Deployment verification completed

================================================================
🎉 BUILD COMPLETED SUCCESSFULLY!
================================================================
⏱️  Total build time: 45 seconds
📅 Build completed at: Mon Jan 15 10:30:45 UTC 2024
🌐 Application: Mbugani Luxe Adventures
🚀 Ready for deployment on Render.com
================================================================
✅ SUCCESS: Mbugani Luxe Adventures is ready for production!
```

### **Error Handling**
```
================================================================
❌ ERROR: Build failed at line 156 with exit code 1
================================================================
📅 Build failed at: Mon Jan 15 10:30:30 UTC 2024
🔍 Check the logs above for detailed error information
💡 Common issues:
   - Missing environment variables
   - Database connectivity problems
   - Missing dependencies in requirements.txt
   - Static files collection errors
================================================================
```

## **🔍 Troubleshooting**

### **Common Issues**

#### **Missing Environment Variables**
```bash
❌ ERROR: Missing required environment variables: DATABASE_URL SECRET_KEY
```
**Solution**: Set all required environment variables in Render.com dashboard

#### **Database Connectivity**
```bash
❌ ERROR: Database connection failed
```
**Solution**: Verify DATABASE_URL format and database accessibility

#### **Static Files Collection**
```bash
❌ ERROR: Static files collection failed
```
**Solution**: Check static files configuration and file permissions

#### **Migration Errors**
```bash
❌ ERROR: Migration failed
```
**Solution**: Review migration files and database schema

## **🔧 Customization**

### **Adding Custom Steps**
To add custom deployment steps, create a new function and call it in the `main()` function:

```bash
# Custom function
custom_deployment_step() {
    log_step "Running custom deployment step"
    
    # Your custom logic here
    
    log_success "Custom step completed"
}

# Add to main() function
main() {
    # ... existing steps ...
    custom_deployment_step
    # ... remaining steps ...
}
```

### **Environment-Specific Configuration**
Modify environment variable checks for different deployment environments:

```bash
# Add environment-specific variables
if [[ "$ENVIRONMENT" == "staging" ]]; then
    required_vars+=("STAGING_DATABASE_URL")
elif [[ "$ENVIRONMENT" == "production" ]]; then
    required_vars+=("PRODUCTION_DATABASE_URL")
fi
```

## **📋 Best Practices**

1. **Always test locally** before deploying to production
2. **Set environment variables** in Render.com dashboard, not in code
3. **Monitor build logs** for warnings and errors
4. **Keep dependencies updated** in requirements.txt
5. **Test database migrations** in staging environment first
6. **Verify static files** are properly collected and served

## **🔗 Related Files**

- `render.yaml` - Render.com deployment configuration
- `requirements.txt` - Python dependencies
- `tours_travels/settings_prod.py` - Production Django settings
- `users/management/commands/createsu.py` - Custom superuser creation command

## **📞 Support**

For issues with the build script:
1. Check the build logs for specific error messages
2. Verify all environment variables are set correctly
3. Test the script locally with production settings
4. Review Django documentation for deployment best practices
