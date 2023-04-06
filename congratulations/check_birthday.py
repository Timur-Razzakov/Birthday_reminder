import datetime
import logging
import os
import sys

import django
from jinja2 import Template

proj = os.path.dirname(os.path.abspath('../manage.py'))
sys.path.append(proj)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reminder_service.settings")

django.setup()
# ---------------------------------------------------------------------------------
from accounts.models import Client, Channel
from reminder.models import Holiday, TemplateForChannel, Result

today = datetime.date.today()
times = datetime.time()
logger = logging.getLogger(__name__)


def birthday():
    get_client = Client.objects.filter(date_of_birth=today).values(
        'phone_number',
        'first_name',
        'last_name',
        'father_name',
        'gender',
        'channel',
        'pk')
    if get_client.exists():
        get_congrats = Holiday.objects.get(name__icontains='День рождения')
        if get_congrats:
            message = get_congrats.congratulation
            for item in get_client:
                res_for_send = Result.objects.create()
                res_for_send.client.add(item['pk'])
                res_for_send.image = Holiday.objects.get(id=get_congrats.id)
                res_for_send.channels = Channel.objects.get(id=item['channel'])
                template = TemplateForChannel.objects.get(gender=item['gender'],
                                                          name__icontains=get_congrats.name)
                tm_message = Template(template.templates_for_massage)
                finished_message = tm_message.render(first_name=item['first_name'],
                                                     father_name=item['father_name'],
                                                     message=message, )
                res_for_send.message = finished_message
                res_for_send.save()
                logger.info("data to model 'Result' saved")
        else:
            logger.warning('holiday, with the name "День рождения" is missing')
        return 'Нет соответствующего праздника'
