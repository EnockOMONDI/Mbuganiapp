"""
Production settings for Mbugani Luxe Adventures
Uses Supabase PostgreSQL for production
"""

# Force production environment before importing base settings
import os
os.environ['DJANGO_ENV'] = 'production'

from .settings import *
import dj_database_url
import logging

# Production-specific settings
print("🚀 Production settings loaded")
print("📧 Production mode: Using Mailtrap HTTP API (synchronous)")
print(f"🗄️ Database: {os.getenv('DATABASE_URL', 'Not set')[:50]}...")
print(f"🌐 Site URL: {os.getenv('SITE_URL', 'Not set')}")
print(f"🔒 SSL redirect: True")
print(f"📊 Debug mode: False")

# No longer using Railway for background workers - all email sending is synchronous

# Add CORS headers to installed apps
INSTALLED_APPS = INSTALLED_APPS + [
    'corsheaders',
]

# Force production settings
DEBUG = False
DJANGO_ENV = 'production'

# Production database - Supabase PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres.zgwfxeemdgfryiulbapx',
        'PASSWORD': 'JDuH37tYEfVuPpX!',
        'HOST': 'aws-1-eu-west-1.pooler.supabase.com',
        'PORT': '6543',
        'OPTIONS': {
            'sslmode': 'require',
        },
        'CONN_MAX_AGE': 600,
        'CONN_HEALTH_CHECKS': True,
    }
}

# Production email configuration - Mailtrap HTTP API
# Using Mailtrap HTTP API for synchronous email sending (no background worker needed)
MAILTRAP_API_TOKEN = os.getenv('MAILTRAP_API_TOKEN', '956b51c090fc5c1320bca0c26a394fd5')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'Mbugani Luxe Adventures <info@mbuganiluxeadventures.com>')

# Email addresses for different purposes
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'info@mbuganiluxeadventures.com')
JOBS_EMAIL = os.getenv('JOBS_EMAIL', 'careers@mbuganiluxeadventures.com')
NEWSLETTER_EMAIL = os.getenv('NEWSLETTER_EMAIL', 'news@mbuganiluxeadventures.com')


# Production allowed hosts
ALLOWED_HOSTS = [
    'mbuganiapp.onrender.com',
    'www.mbuganiluxeadventures.com',
    'mbuganiluxeadventures.com',
    '.onrender.com',
    os.getenv('RENDER_EXTERNAL_HOSTNAME', ''),
]

# Remove empty strings from ALLOWED_HOSTS
ALLOWED_HOSTS = [host for host in ALLOWED_HOSTS if host]

# Production static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Production media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Production logging - Railway-friendly configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'users': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'adminside': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Production cache - Redis (if available) or Database cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
        'TIMEOUT': 300,
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
        }
    }
}

# Production session configuration
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Production security settings
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Production Uploadcare settings
UPLOADCARE = {
    'pub_key': os.getenv('UPLOADCARE_PUBLIC_KEY'),
    'secret': os.getenv('UPLOADCARE_SECRET_KEY'),
}

# Production site URL
SITE_URL = os.getenv('SITE_URL', 'https://www.mbuganiluxeadventures.com')

# Production WhatsApp settings
WHATSAPP_PHONE = os.getenv('WHATSAPP_PHONE', '+254701363551')
WHATSAPP_MESSAGE_TEMPLATE = 'Hello! I have a question about my booking: {booking_reference}'

# Production performance settings
USE_TZ = True
TIME_ZONE = 'Africa/Nairobi'

# Production internationalization
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True

# Production file upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5MB

# Production CORS settings
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "https://mbuganiapp.onrender.com",
    "https://www.mbuganiluxeadventures.com",
    "https://mbuganiluxeadventures.com",
]
CORS_ALLOW_CREDENTIALS = True

# Production CSP settings
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "https://cdn.jsdelivr.net", "https://cdnjs.cloudflare.com")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net", "https://cdnjs.cloudflare.com")
CSP_IMG_SRC = ("'self'", "data:", "https:", "https://ucarecdn.com")
CSP_FONT_SRC = ("'self'", "https://cdn.jsdelivr.net", "https://cdnjs.cloudflare.com")
CSP_CONNECT_SRC = ("'self'", "https://api.uploadcare.com")

# Production error reporting
ADMINS = [
    ('Admin', os.getenv('ADMIN_EMAIL', 'info@mbuganiluxeadventures.com')),
]
MANAGERS = ADMINS

# Production database connection pooling (already configured above)

# Production middleware order (security first)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Production static files with WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = False

# Production compression
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Production template settings
TEMPLATES[0]['OPTIONS']['debug'] = False

# Production email error reporting
SERVER_EMAIL = DEFAULT_FROM_EMAIL
EMAIL_SUBJECT_PREFIX = '[Mbugani Luxe Adventures] '

# Production health check


# Production monitoring
SENTRY_DSN = os.getenv('SENTRY_DSN')
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.logging import LoggingIntegration
    
    sentry_logging = LoggingIntegration(
        level=logging.INFO,
        event_level=logging.ERROR
    )
    
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration(), sentry_logging],
        traces_sample_rate=0.1,
        send_default_pii=False,
        environment='production',
    )

print("🚀 Production settings loaded")
print(f"🌐 Site URL: {SITE_URL}")
print(f"📧 Email: Mailtrap HTTP API (synchronous)")
print(f"🔒 SSL redirect: {SECURE_SSL_REDIRECT}")
print(f"📊 Debug mode: {DEBUG}")
