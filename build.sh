#!/bin/bash

# Comprehensive Build Script for Mbugani Luxe Adventures Django Application
# Render.com Production Deployment
#
# This script handles all essential Django deployment steps with proper error handling

set -o errexit   # Exit on any error
set -o pipefail  # Exit on pipe failures
set -o nounset   # Exit on undefined variables

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}ℹ️  INFO: $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ SUCCESS: $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  WARNING: $1${NC}"
}

log_error() {
    echo -e "${RED}❌ ERROR: $1${NC}"
}

log_step() {
    echo -e "${BLUE}🔄 STEP: $1${NC}"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check environment variables
check_environment() {
    log_step "Checking environment variables"

    # Required environment variables
    required_vars=(
        "DATABASE_URL"
        "SECRET_KEY"
        "DJANGO_SETTINGS_MODULE"
    )

    missing_vars=()

    for var in "${required_vars[@]}"; do
        if [[ -z "${!var:-}" ]]; then
            missing_vars+=("$var")
        else
            log_info "$var is set"
        fi
    done

    if [[ ${#missing_vars[@]} -gt 0 ]]; then
        log_error "Missing required environment variables: ${missing_vars[*]}"
        exit 1
    fi

    log_success "All required environment variables are set"
}

# Function to install dependencies
install_dependencies() {
    log_step "Installing Python dependencies"

    if [[ ! -f "requirements.txt" ]]; then
        log_error "requirements.txt not found"
        exit 1
    fi

    # Upgrade pip first
    log_info "Upgrading pip"
    python -m pip install --upgrade pip

    # Install requirements
    log_info "Installing requirements from requirements.txt"
    pip install -r requirements.txt

    log_success "Dependencies installed successfully"
}

# Function to run database migrations
run_migrations() {
    log_step "Running database migrations"

    # Check database connectivity first
    log_info "Testing database connectivity"
    python manage.py check --database default --settings=tours_travels.settings_prod

    # Create migrations if needed (for development, usually not needed in production)
    log_info "Checking for new migrations"
    python manage.py makemigrations --noinput --settings=tours_travels.settings_prod || {
        log_warning "No new migrations to create"
    }

    # Apply migrations
    log_info "Applying database migrations"
    python manage.py migrate --noinput --settings=tours_travels.settings_prod

    log_success "Database migrations completed successfully"
}

# Function to collect static files
collect_static_files() {
    log_step "Collecting static files"

    # Clear any existing static files
    log_info "Preparing static files directory"

    # Collect static files
    log_info "Running collectstatic"
    python manage.py collectstatic --noinput --settings=tours_travels.settings_prod

    log_success "Static files collected successfully"
}

# Function to create cache table
create_cache_table() {
    log_step "Creating cache table"

    # Create cache table for database caching
    log_info "Creating database cache table"
    python manage.py createcachetable --settings=tours_travels.settings_prod || {
        log_warning "Cache table creation failed or already exists"
    }

    log_success "Cache table setup completed"
}

# Function to create superuser
create_superuser() {
    log_step "Creating superuser account"

    # Set default superuser credentials if not provided
    export DJANGO_SUPERUSER_USERNAME="${DJANGO_SUPERUSER_USERNAME:-mbuganiluxeadventures}"
    export DJANGO_SUPERUSER_EMAIL="${DJANGO_SUPERUSER_EMAIL:-admin@mbuganiluxeadventures.com}"
    export DJANGO_SUPERUSER_PASSWORD="${DJANGO_SUPERUSER_PASSWORD:-mbuganiluxeadventurespassword}"

    log_info "Creating superuser with username: $DJANGO_SUPERUSER_USERNAME"
    python manage.py createsu --settings=tours_travels.settings_prod

    log_success "Superuser setup completed"
}

# Function to run Django system checks
run_system_checks() {
    log_step "Running Django system checks"

    log_info "Performing comprehensive system check"
    python manage.py check --settings=tours_travels.settings_prod

    log_success "System checks passed"
}

# Function to verify deployment
verify_deployment() {
    log_step "Verifying deployment readiness"

    # Check if manage.py exists
    if [[ ! -f "manage.py" ]]; then
        log_error "manage.py not found"
        exit 1
    fi

    # Verify settings module
    log_info "Verifying Django settings"
    python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tours_travels.settings_prod')
import django
django.setup()
from django.conf import settings
print(f'✅ Django settings loaded: {settings.SETTINGS_MODULE}')
print(f'✅ Debug mode: {settings.DEBUG}')
print(f'✅ Database engine: {settings.DATABASES[\"default\"][\"ENGINE\"]}')
print(f'✅ Static URL: {settings.STATIC_URL}')
"

    log_success "Deployment verification completed"
}

# Main execution function
main() {
    echo "🚀 Starting Mbugani Luxe Adventures Django Application Build"
    echo "================================================================"
    echo "📅 Build started at: $(date)"
    echo "🌍 Environment: Production (Render.com)"
    echo "🐍 Python version: $(python --version)"
    echo "📦 Pip version: $(pip --version)"
    echo "================================================================"

    # Execute deployment steps in order
    local start_time=$(date +%s)

    # Step 1: Environment verification
    check_environment

    # Step 2: Install dependencies
    install_dependencies

    # Step 3: Run system checks
    run_system_checks

    # Step 4: Database migrations
    run_migrations

    # Step 5: Create cache table
    create_cache_table

    # Step 6: Collect static files
    collect_static_files

    # Step 7: Create superuser
    create_superuser

    # Step 8: Final verification
    verify_deployment

    # Calculate build time
    local end_time=$(date +%s)
    local build_time=$((end_time - start_time))

    echo "================================================================"
    echo "🎉 BUILD COMPLETED SUCCESSFULLY!"
    echo "================================================================"
    echo "⏱️  Total build time: ${build_time} seconds"
    echo "📅 Build completed at: $(date)"
    echo "🌐 Application: Mbugani Luxe Adventures"
    echo "🚀 Ready for deployment on Render.com"
    echo "================================================================"

    log_success "Mbugani Luxe Adventures is ready for production!"
}

# Error handling function
handle_error() {
    local exit_code=$?
    local line_number=$1

    echo "================================================================"
    log_error "Build failed at line $line_number with exit code $exit_code"
    echo "================================================================"
    echo "📅 Build failed at: $(date)"
    echo "🔍 Check the logs above for detailed error information"
    echo "💡 Common issues:"
    echo "   - Missing environment variables"
    echo "   - Database connectivity problems"
    echo "   - Missing dependencies in requirements.txt"
    echo "   - Static files collection errors"
    echo "================================================================"

    exit $exit_code
}

# Set up error handling
trap 'handle_error $LINENO' ERR

# Execute main function
main "$@"