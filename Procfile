release: python manage.py migrate && python manage.py collectstatic --noinput
web: gunicorn auto.wsgi:application --bind 0.0.0.0:$PORT
