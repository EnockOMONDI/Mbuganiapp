#!/bin/bash

set -o errexit  # exit on error

echo "🚀 Starting Mbugani Luxe Adventures build process..."

pip install -r requirements.txt
echo "📦 Dependencies installed successfully"

python manage.py collectstatic --noinput --settings=tours_travels.settings_prod
echo "📁 Static files collected"

python manage.py check_database_writable --settings=tours_travels.settings_prod
echo "🗄️ Database write access verified"

python manage.py migrate --noinput --settings=tours_travels.settings_prod
echo "🗄️ Database migrations applied"

python manage.py createcachetable --settings=tours_travels.settings_prod || true
echo "💾 Cache table ready"

python manage.py createsu --settings=tours_travels.settings_prod
echo "✅ Build completed successfully"
