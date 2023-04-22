#!/bin/sh
python manage.py collectstatic --no-input --clear
python manage.py migrate --no-input

# create superuser
#DJANGO_SUPERUSER_PASSWORD='4525' python manage.py createsuperuser --email 'razzakov443@gmail.com' --user_name 'RT' --noinput
#DJANGO_SUPERUSER_PASSWORD=$SUPER_USER_PASSWORD python manage.py createsuperuser --email $SUPER_USER_EMAIL--user_name $SUPER_USER_NAME --noinput


# run project
#gunicorn reminder_service.wsgi:application --bind 0.0.0.0:8000
python manage.py runserver 0.0.0.0:8000
# run celery worker
celery -A reminder_service worker -l info
# run schedule
celery -A reminder_service beat -l info
