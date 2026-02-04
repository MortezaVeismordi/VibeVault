release: bash build.sh
web: cd proshop && DJANGO_ENV=production gunicorn proshop.wsgi:application --bind 0.0.0.0:$PORT
