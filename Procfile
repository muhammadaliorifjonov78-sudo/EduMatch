release: python manage.py migrate
web: gunicorn auto.wsgi:application --bind 0.0.0.0:$PORT
