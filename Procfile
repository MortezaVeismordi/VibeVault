release: bash build.sh
web: cd proshop && gunicorn proshop.wsgi:application --bind 0.0.0.0:$PORT
