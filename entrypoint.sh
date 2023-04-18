#!/bin/sh

python manage.py migrate --no-input
python manage.py collectstatic --no-input

# create superuser
#DJANGO_SUPERUSER_PASSWORD=$SUPER_USER_PASSWORD python manage.py createsuperuser --email $SUPER_USER_EMAIL --user_name $SUPER_USER_NAME --noinput

## run celery worker
#celery -A reminder_service worker -l info
## run schedule
#celery -A reminder_service beat -l info

# run project
gunicorn reminder_service.wsgi:application --bind 0.0.0.0:8000
#python manage.py runserver 127.0.0.1:8000