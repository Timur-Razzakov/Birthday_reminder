"""
Функция для удаления старых записей
"""

import logging
import os
import sys
from datetime import datetime, timedelta

import django
from django.core.management.base import BaseCommand

proj = os.path.dirname(os.path.abspath('../manage.py'))
sys.path.append(proj)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reminder_service.settings")

django.setup()
# ---------------------------------------------------------------------------------

from reminder.models import Result, MailingCommerceOffer

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Delete objects older than 5 days'

    def handle(*args, **options):
        Result.objects.filter(sending_status=True,
                              created_at__lte=datetime.now() - timedelta(days=10)).delete()
        MailingCommerceOffer.objects.filter(sending_status=True,
                                            created_at__lte=datetime.now() - timedelta(days=10)).delete()
        logger.info("data removed from Result and MailingCommerceOffer")
