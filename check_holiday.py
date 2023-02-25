import os
import sys
from abc import ABC

import django

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reminder_service.settings")

django.setup()
# ---------------------------------------------------------------------------------
from jinja2 import Template
import datetime
from reminder.models import Holiday, TemplateForChannel, Result
from accounts.models import Client, Channel
from django.core.management.base import BaseCommand

today = datetime.date.today()

print(today)


def holiday():
    get_holiday = Holiday.objects.get(date=today)

    print()
    if get_holiday.exists():
        clients = Client.objects.all().values('phone_number', 'chart_id')
        print(clients.pk)


holiday()
