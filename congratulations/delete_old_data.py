"""
Функция для удаления старых записей
"""

import os
import sys
import time

import django

proj = os.path.dirname(os.path.abspath('../manage.py'))
sys.path.append(proj)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reminder_service.settings")

django.setup()
# ---------------------------------------------------------------------------------
from datetime import datetime, timedelta
from reminder.models import Result, MailingCommerceOffer
from django.core.management.base import BaseCommand
from schedule import every, repeat, run_pending


class Command(BaseCommand):
    help = 'Delete objects older than 5 days'

    @repeat(every().sunday.at("15:45"))
    def handle(*args, **options):
        Result.objects.filter(sending_status=True,
                              created_at__lte=datetime.now() - timedelta(days=10)).delete()
        # Result.objects.filter(created_at__gte=datetime.now() - timedelta(days=5)).delete()

    @repeat(every().sunday.at("16:45"))
    def handle(*args, **options):
        MailingCommerceOffer.objects.filter(sending_status=True,
                                            created_at__lte=datetime.now() - timedelta(days=10)).delete()


while 1:
    run_pending()
    time.sleep(1)
