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

print(today)
print(times)


@repeat(every().day.at("07:00"))
def birthday():
    print(today)
    get_client = Client.objects.filter(date_of_birth=today).values('phone_number',
                                                                   'first_name',
                                                                   'last_name',
                                                                   'father_name',
                                                                   'gender',
                                                                   'channel',
                                                                   'pk')
    if get_client.exists():
        get_congrats = Holiday.objects.get(name='День рождение')
        message = get_congrats.congratulation
        for item in get_client:
            res_for_send = Result.objects.create()
            res_for_send.client.add(item['pk'])
            res_for_send.channels = Channel.objects.get(id=item['channel'])
            template = TemplateForChannel.objects.get(gender=item['gender'], channel=item['channel'])
            tm_message = Template(template.templates_for_massage)

            msg = tm_message.render(first_name=item['first_name'],
                                    father_name=item['father_name'],
                                    message=message, )
            res_for_send.message = msg
            # Producer().produce(message=msg, routing_key='tr151199')
            res_for_send.save()
            print("Данные сохранены")


while True:
    run_pending()
    time.sleep(1)

