#!/bin/bash

set -e

echo "Starting VibeVault E-Commerce Platform..."

# Wait for database to be ready (using Python instead of nc)
echo "Checking database connection..."
python << END
import sys
import time
import psycopg2
from urllib.parse import urlparse
import os

max_retries = 30
retry_count = 0

# Parse DATABASE_URL if available, otherwise use individual settings
database_url = os.environ.get('DATABASE_URL')
if database_url:
    url = urlparse(database_url)
    db_config = {
        'dbname': url.path[1:],
        'user': url.username,
        'password': url.password,
        'host': url.hostname,
        'port': url.port or 5432
    }
else:
    db_config = {
        'dbname': os.environ.get('DB_NAME', 'vibevault_db'),
        'user': os.environ.get('DB_USER', 'postgres'),
        'password': os.environ.get('DB_PASSWORD', 'postgres'),
        'host': os.environ.get('DB_HOST', 'localhost'),
        'port': int(os.environ.get('DB_PORT', 5432))
    }

while retry_count < max_retries:
    try:
        conn = psycopg2.connect(**db_config)
        conn.close()
        print("✓ Database connection successful!")
        sys.exit(0)
    except psycopg2.OperationalError as e:
        retry_count += 1
        print(f"Database not ready yet (attempt {retry_count}/{max_retries})...")
        time.sleep(1)

print("✗ Failed to connect to database after {max_retries} attempts")
sys.exit(1)
END

if [ $? -ne 0 ]; then
    echo "ERROR: Could not connect to database"
    exit 1
fi

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create superuser if it doesn't exist
echo "Checking for superuser..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('✓ Superuser created: admin / admin123')
    print('⚠️  IMPORTANT: Change the admin password immediately!')
else:
    print('✓ Superuser already exists')
END

echo "========================================="
echo "VibeVault is starting on port 8000..."
echo "========================================="

# Start Gunicorn
exec gunicorn proshop.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --threads 4 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info

