
import os

import django
from celery import Celery
from celery.schedules import crontab

# Установили переменную окружения с именем вашего проекта Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reminder_service.settings')
django.setup()
# ---------------------------------------------------------------------------------
# Создайте экземпляр Celery для нашего проекта
app = Celery('reminder_service')

# Загрузите конфигурацию из настроек Django
app.config_from_object('django.conf:settings', namespace='CELERY')

CELERY_BEAT_SCHEDULE = {
    'run-every-day-at-5': {
        'task': 'reminder.tasks.check_holiday_task',
        'schedule': crontab(hour=13, minute=40),
    },

    'run-every-day-at-7': {
        'task': 'reminder.tasks.check_birthday_task',
        'schedule': crontab(hour=13, minute=50),
    },
    'run-every-day-at-9': {
        'task': 'reminder.tasks.send_congratulation_task',
        'schedule': crontab(hour=14, minute=0),
    },
    'run-every-week-at-9': {
        'task': 'reminder.tasks.delete_old_task',
        'schedule': crontab(day_of_week=1, hour=9, minute=0),
    },
}
app.conf.beat_schedule = CELERY_BEAT_SCHEDULE
app.conf.timezone = 'Asia/Tashkent'
# Загрузите задачи из всех файлов tasks.py в приложениях Django
app.autodiscover_tasks()
