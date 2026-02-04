#!/bin/bash
set -e

echo "🔨 Building frontend..."
cd frontend
npm install
npm run build

echo "📁 Copying frontend build to Django..."
rm -rf ../proshop/static/dist 2>/dev/null || true
cp -r dist ../proshop/static/dist/

echo "📦 Collecting Django static files..."
cd ../proshop
python manage.py collectstatic --noinput

echo "🗄️  Running migrations..."
python manage.py migrate

echo "✅ Build complete!"

