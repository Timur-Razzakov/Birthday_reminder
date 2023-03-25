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


class Command(BaseCommand):
    help = 'Delete objects older than 5 days'

    def handle(*args, **options):
        Result.objects.filter(sending_status=True,
                              created_at__lte=datetime.now() - timedelta(days=10)).delete()
        MailingCommerceOffer.objects.filter(sending_status=True,
                                            created_at__lte=datetime.now() - timedelta(days=10)).delete()
