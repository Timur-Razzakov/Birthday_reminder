import os
import sys
import time

import django
import dotenv
from pyrogram.errors import FloodWait

dotenv.load_dotenv('.env')

proj = os.path.dirname(os.path.abspath('../manage.py'))
sys.path.append(proj)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reminder_service.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
# # ---------------------------------------------------------------------------------
import asyncio

import datetime
from reminder.models import Result
from accounts.models import Client as cl

from pyrogram import Client

app = Client('account')


def get_data():
    """Получаем данные с бд"""
    data = Result.objects.filter(sending_status=False).values('id', 'client', 'process_date', 'message',
                                                              'sending_status')
    client_phones = []

    for item in data:
        all_phones = cl.objects.filter(id=item['client']).values('phone_number', 'first_name')
        for phone in all_phones:
            client = {
                'id': item['id'],
                'name': phone['first_name'],
                'phone_number': phone['phone_number'],
                'message': item['message'],
            }
            client_phones.append(client)
    return client_phones


today = datetime.datetime.today()


def update_result(client_id):
    """Обновляем модель Result, Sending_status=True и process_date=today"""
    client = Result.objects.get(id=client_id)
    client.sending_status = True
    client.process_date = today
    client.save()


async def send_message(client_data: list, admin_username):
    """Получаем chart_id пользователя и рассылаем сообщения из модели Result"""
    async with app:
        client_count = len(client_data)
        client_name = []
        try:
            for client in client_data:
                client_name.append(client['name'])
                # сохраняем пользователей и получаем chat_id, если даже он есть, сохраняем (без циклов)
                new_contact = await app.add_contact(client['phone_number'].split("+")[-1], client['name'])
                await app.send_message(new_contact.id, client['message'])
                time.sleep(5)
                update_result(client['id'])
            if client_count < 10:
                await app.send_message(admin_username,
                                       f"<b>Сегодня день рождения у пользователей:</b>\n{client_name} ")
                time.sleep(5)
            else:
                await app.send_message(admin_username,
                                       f"<b>Сегодня мы поздравили:</b> {client_count} пользователей!!")
        except FloodWait as e:
            print(e.value)
            await asyncio.sleep(e.value)


app.run(send_message(get_data(), 'Razzakov_Timur'))
