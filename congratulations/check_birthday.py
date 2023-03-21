import os
import sys

import django

proj = os.path.dirname(os.path.abspath('../manage.py'))
sys.path.append(proj)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reminder_service.settings")

django.setup()
# ---------------------------------------------------------------------------------
from jinja2 import Template
import datetime
import time
from reminder.models import Holiday, TemplateForChannel, Result
from accounts.models import Client, Channel
from schedule import every, repeat, run_pending

today = datetime.date.today()
times = datetime.time()


# @repeat(every().day.at("06:00"))
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
                res_for_send.channels = Channel.objects.get(id=item['channel'])
                template = TemplateForChannel.objects.get(gender=item['gender'],
                                                          name__icontains=get_congrats.name)
                tm_message = Template(template.templates_for_massage)

                msg = tm_message.render(first_name=item['first_name'],
                                        father_name=item['father_name'],
                                        message=message, )
                res_for_send.message = msg
                res_for_send.save()
                print("Данные сохранены")
        return 'Нет соответствующего праздника'

#
# while True:
#     run_pending()
#     time.sleep(1)

birthday()