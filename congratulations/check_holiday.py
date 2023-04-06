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
from accounts.models import Client, Gender
from reminder.models import Holiday, TemplateForChannel, Result

logger = logging.getLogger(__name__)
today = datetime.date.today()


def holiday():
    get_holiday = Holiday.objects.filter(date=today).values('id', 'congratulation',
                                                            'name', 'gender')
    if get_holiday.exists():
        for item in get_holiday:
            gender = Gender.objects.get(id=item['gender'])
            res_for_send = Result.objects.create()
            res_for_send.image = Holiday.objects.get(id=item['id'])
            if gender.name.lower() == 'женщина' and '8 марта' in item['name'].lower():
                clients = Client.objects.filter(gender=item['gender']).values('pk', 'gender')
            elif gender.name.lower() == 'мужчина' and '14 января' in item['name'].lower():
                clients = Client.objects.filter(gender=item['gender']).values('pk', 'gender')
            else:
                clients = Client.objects.all().values('pk', 'gender')
            try:
                template = TemplateForChannel.objects.get(gender=item['gender'],
                                                          name__icontains='праздники')
                tm_message = Template(template.templates_for_massage)
                for client in clients:
                    res_for_send.client.add(client['pk'])

                    finished_message = tm_message.render(message=item['congratulation'])
                res_for_send.message = finished_message

                res_for_send.save()
            except Exception as e:
                logger.error('Error with TemplateForChannel: %s', e)

        logger.info("data to model 'Result' saved")
    logger.info("There are no holidays today")
