import os

from celery import Celery
from celery.schedules import crontab

# Установили переменную окружения с именем вашего проекта Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reminder_service.settings')

# Создайте экземпляр Celery для нашего проекта
app = Celery('reminder_service')

# Загрузите конфигурацию из настроек Django
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'run-every-day-at-5': {
        'task': 'tasks.check_holiday_task',
        'schedule': crontab(hour=5, minute=0),
    },
}

app.conf.beat_schedule = {
    'run-every-day-at-7': {
        'task': 'tasks.check_birthday',
        'schedule': crontab(hour=7, minute=0),
    },
}

app.conf.beat_schedule = {
    'run-every-day-at-9': {
        'task': 'tasks.send_congratulation_task',
        'schedule': crontab(hour=9, minute=0),
    },
}

app.conf.beat_schedule = {
    'run-every-week-at-9': {
        'task': 'tasks.delete_old_task',
        'schedule': crontab(day_of_week=1, hour=9, minute=0),
    },
}
app.conf.timezone = 'Asia/Tashkent'
# Загрузите задачи из всех файлов tasks.py в приложениях Django
app.autodiscover_tasks()
