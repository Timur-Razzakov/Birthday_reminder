import os

from celery import Celery

# Установили переменную окружения с именем вашего проекта Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reminder_service.settings')

# Создайте экземпляр Celery для нашего проекта
app = Celery('reminder_service')

# Загрузите конфигурацию из настроек Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Загрузите задачи из всех файлов tasks.py в приложениях Django
app.autodiscover_tasks()
