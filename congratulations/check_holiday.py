import os
import sys
import time

import django

proj = os.path.dirname(os.path.abspath('../manage.py'))
sys.path.append(proj)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reminder_service.settings")

django.setup()
# ---------------------------------------------------------------------------------
from jinja2 import Template
import datetime
from reminder.models import Holiday, TemplateForChannel, Result
from accounts.models import Client
from schedule import every, repeat, run_pending

today = datetime.date.today()
print(today)


@repeat(every().day.at("08:30"))
def holiday():
    get_holiday = Holiday.objects.filter(date=today).values('image', 'congratulation',
                                                            'name')
    for item in get_holiday:
        res_for_send = Result.objects.create()
        if '8 марта' in item['name']:
            clients = Client.objects.filter(gender='Женщина').values('pk', 'first_name', 'father_name',
                                                                     'channel')
        elif '14 Февраля' in item['name']:
            clients = Client.objects.filter(gender='Мужчина').values('pk', 'first_name', 'father_name',
                                                                     'channel')
        else:
            clients = Client.objects.all().values('pk', 'first_name', 'father_name',
                                                  'channel')
        for client in clients:
            res_for_send.client.add(client['pk'])
            template = TemplateForChannel.objects.get(id=client['channel'])
            tm_message = Template(template.templates_for_massage)
            msg = tm_message.render(first_name=client['first_name'],
                                    father_name=client['father_name'],
                                    message=item['congratulation'],
                                    image=item['image'])
            res_for_send.message = msg
            res_for_send.save()
            print("Данные сохранены")


while True:
    run_pending()
    time.sleep(1)
