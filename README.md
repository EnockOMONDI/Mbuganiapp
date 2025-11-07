# 🌍 Mbugani Luxe Adventures

**Premium Safari & Adventure Tourism Platform**

A comprehensive Django-based web application for luxury safari tours, adventure packages, and travel experiences across East Africa.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
- [Environment Setup](#environment-setup)
- [Deployment](#deployment)
- [Security](#security)
- [Documentation](#documentation)
- [Support](#support)

---

## 🎯 Overview

Mbugani Luxe Adventures is a full-featured travel and tourism platform offering:

- **Safari Packages:** Multi-day bush safaris, Nairobi excursions, and outbound packages
- **Destination Management:** Hierarchical destination system (Countries → Cities → Places)
- **Accommodation Booking:** Integration with luxury lodges and hotels
- **Blog Platform:** Travel stories, guides, and destination insights
- **Quote System:** Custom quote requests with email notifications
- **Admin Dashboard:** Comprehensive management interface with Django Unfold

---

## ✨ Features

### Customer-Facing Features
- 🏞️ **Package Browsing:** Filter by category, destination, duration, and price
- 📧 **Quote Requests:** Custom travel planning with email confirmations
- 🏨 **Accommodation Listings:** Detailed hotel and lodge information
- 📝 **Travel Blog:** Engaging content with categories and tags
- 📱 **Responsive Design:** Mobile-first approach with modern UI
- 🔍 **Search & Filters:** Advanced filtering for packages and destinations

### Admin Features
- 🎨 **Modern Admin Interface:** Django Unfold with custom branding
- 📊 **Dashboard Analytics:** Booking statistics and performance metrics
- 🖼️ **Image Management:** Uploadcare CDN integration
- ✉️ **Email System:** Mailtrap API for reliable email delivery
- 🔐 **Security:** CSRF protection, SSL/TLS, HSTS headers
- 📦 **Package Management:** Create and manage travel packages with itineraries

---

## 🛠️ Technology Stack

### Backend
- **Framework:** Django 5.0.14
- **Language:** Python 3.12
- **Database:** PostgreSQL (Supabase)
- **Server:** Gunicorn with sync workers

### Frontend
- **Template Engine:** Django Templates
- **CSS Framework:** Custom CSS with responsive design
- **JavaScript:** Vanilla JS with modern ES6+
- **Fonts:** TAN-Garland-Regular (custom brand font)

### Third-Party Services
- **CDN:** Uploadcare (image/file hosting)
- **Email:** Mailtrap HTTP API
- **Hosting:** Render.com
- **Database:** Supabase PostgreSQL

### Key Dependencies
- `django==5.0.14` - Web framework
- `psycopg2-binary==2.9.10` - PostgreSQL adapter
- `gunicorn==23.0.0` - WSGI HTTP server
- `django-unfold==0.42.0` - Modern admin interface
- `django-ckeditor-5==0.2.15` - Rich text editor
- `pyuploadcare==5.1.0` - Uploadcare integration
- `mailtrap==2.0.1` - Email API client
- `python-decouple==3.8` - Environment variable management

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- PostgreSQL (or use Supabase)
- Git
- Virtual environment tool (venv, virtualenv, or conda)

### Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Mbuganiapp
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   # Create .env file (see Environment Setup section below)
   cp .env.example .env
   # Edit .env with your local configuration
   ```

5. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files:**
   ```bash
   python manage.py collectstatic --noinput
   ```

8. **Run development server:**
   ```bash
   python manage.py runserver
   ```

9. **Access the application:**
   - Frontend: http://localhost:8000
   - Admin: http://localhost:8000/admin

---

## 🔐 Environment Setup

### Required Environment Variables

Create a `.env` file in the project root with these variables:

```bash
# Django Core
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (for local development, use SQLite or local PostgreSQL)
# DATABASE_URL is only needed for production
# DATABASE_URL=postgresql://user:password@host:port/database

# Email Configuration (optional for local development)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=Your Name <your-email@gmail.com>

# Uploadcare (optional for local development)
UPLOADCARE_PUBLIC_KEY=your-public-key
UPLOADCARE_SECRET_KEY=your-secret-key

# Site Configuration
SITE_URL=http://localhost:8000
WHATSAPP_PHONE=+254701363551
```

### Development vs Production

- **Development:** Uses SQLite database by default, simpler email backend
- **Production:** Uses PostgreSQL (Supabase), Mailtrap API, Uploadcare CDN

**⚠️ IMPORTANT:** Never commit `.env` files to version control!

---

## 📦 Deployment

### Deploying to Render.com

See **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** for comprehensive deployment instructions.

**Quick Steps:**

1. **Set up environment variables** in Render dashboard (see `.env.secrets`)
2. **Connect GitHub repository** to Render
3. **Select branch:** `mailltrapapi`
4. **Deploy** - Render will use `render.yaml` configuration

**Critical Environment Variables for Production:**
- `SECRET_KEY` - Django secret key
- `DATABASE_URL` - PostgreSQL connection string
- `MAILTRAP_API_TOKEN` - Email API token
- `UPLOADCARE_PUBLIC_KEY` - CDN public key
- `UPLOADCARE_SECRET_KEY` - CDN secret key

---

## 🔒 Security

### Security Features

✅ **HTTPS/SSL:** Enforced SSL redirect in production
✅ **HSTS:** HTTP Strict Transport Security enabled
✅ **CSRF Protection:** Django CSRF middleware active
✅ **Secure Cookies:** HTTPOnly and Secure flags set
✅ **Content Security Policy:** CSP headers configured
✅ **XSS Protection:** Template auto-escaping enabled
✅ **SQL Injection Protection:** Django ORM parameterized queries

### Security Best Practices

1. **Never commit secrets** to version control
2. **Rotate credentials** if exposed (see `SECURITY_AUDIT_REPORT.md`)
3. **Use strong passwords** for admin accounts (16+ characters)
4. **Enable 2FA** on all third-party services
5. **Keep dependencies updated** regularly
6. **Monitor logs** for suspicious activity
7. **Backup database** regularly

### Security Documentation

- **[SECURITY_AUDIT_REPORT.md](SECURITY_AUDIT_REPORT.md)** - Comprehensive security audit
- **[IMMEDIATE_ACTION_REQUIRED.md](IMMEDIATE_ACTION_REQUIRED.md)** - Emergency response guide
- **`.env.secrets`** - Production credentials reference (not in version control)

**⚠️ If credentials are exposed, follow the rotation guide in `SECURITY_AUDIT_REPORT.md` immediately!**

---

## 📚 Documentation

### Project Documentation

- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Deployment instructions
- **[SECURITY_AUDIT_REPORT.md](SECURITY_AUDIT_REPORT.md)** - Security audit and best practices
- **[IMMEDIATE_ACTION_REQUIRED.md](IMMEDIATE_ACTION_REQUIRED.md)** - Security incident response
- **[docs/hero_slider_management.md](docs/hero_slider_management.md)** - Hero slider configuration

### External Documentation

- **Django:** https://docs.djangoproject.com/
- **Django Unfold:** https://unfoldadmin.com/
- **Uploadcare:** https://uploadcare.com/docs/
- **Mailtrap:** https://mailtrap.io/docs/
- **Render:** https://render.com/docs

---

## 🧪 Testing

### Run Tests

```bash
# Run all tests
python run_tests.py

# Run specific app tests
python manage.py test adminside
python manage.py test users
python manage.py test blog

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### Test Coverage

- Unit tests for models, views, and forms
- Integration tests for email sending
- Admin interface tests
- API endpoint tests

---

## 🤝 Contributing

### Development Workflow

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Run tests: `python run_tests.py`
4. Commit changes: `git commit -m "Description of changes"`
5. Push to branch: `git push origin feature/your-feature`
6. Create Pull Request

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused
- Write tests for new features

---

## 📞 Support

### Getting Help

- **Issues:** Create an issue in the GitHub repository
- **Email:** info@mbuganiluxeadventures.com
- **WhatsApp:** +254701363551

### Dashboards

- **Render:** https://dashboard.render.com
- **Supabase:** https://supabase.com/dashboard
- **Mailtrap:** https://mailtrap.io/signin
- **Uploadcare:** https://uploadcare.com/

---

## 📄 License

This project is proprietary software owned by Mbugani Luxe Adventures.
All rights reserved.

---

## 🙏 Acknowledgments

- **Django Community** - For the excellent web framework
- **Unfold Admin** - For the modern admin interface
- **Uploadcare** - For reliable CDN services
- **Mailtrap** - For email delivery infrastructure
- **Render** - For hosting platform

---

**Built with ❤️ by the Mbugani Luxe Adventures Development Team**

**Last Updated:** November 7, 2025
