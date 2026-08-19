release: python manage.py migrate --no-input
web: python manage.py migrate --no-input 2>/dev/null; gunicorn auto.wsgi:application --bind 0.0.0.0:$PORT
