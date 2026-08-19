release: python manage.py migrate --no-input
web: python manage.py migrate --no-input; gunicorn auto.wsgi:application --bind 0.0.0.0:$PORT
worker: python bot.py
