release: python manage.py makemigrations
release: python manage.py migrate
worker: celery -A config worker -l info -B
web: gunicorn config.wsgi --log-file -

#orderSystem is the name of the project folder