import os
import sys
import time

import django
import dotenv
from pyrogram.errors import FloodWait
from pyrogram.raw.base.contacts import ImportedContacts

dotenv.load_dotenv('.env')

proj = os.path.dirname(os.path.abspath('../manage.py'))
sys.path.append(proj)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reminder_service.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
# # ---------------------------------------------------------------------------------
import asyncio

import datetime
from reminder.models import Result, MailingCommerceOffer
from accounts.models import Client as cl

from pyrogram import Client
from pyrogram.types import InputPhoneContact, InputMediaPhoto
import logging

logger = logging.getLogger(__name__)


def get_data():
    """Получаем данные """
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


def update_result(result_id):
    """Обновляем модель Result, Sending_status=True и process_date=today"""
    client = Result.objects.get(id=result_id)
    client.sending_status = True
    client.process_date = today
    client.save()


def update_mailing(mailing_id):
    """Обновляем модель MailingCommerceOffer, Sending_status=True и process_date=today"""
    mailing = MailingCommerceOffer.objects.get(id=mailing_id)
    mailing.sending_status = True
    mailing.save()


async def send_message_holiday(api_id, api_hash, client_data: list, admin_username):
    """Получаем chart_id пользователя и рассылаем сообщения из модели Result"""
    string_session = os.environ.get('STRING_SESSION')
    async with Client('account', api_id, api_hash, string_session) as app:
        client_count = len(client_data)
        client_name = []
        error_list = []
        try:
            for client in client_data:
                client_name.append(client['name'])
                # сохраняем пользователей и получаем chat_id, если даже он есть, сохраняем (без циклов)
                contact: ImportedContacts = await app.import_contacts(
                    [InputPhoneContact(phone=client['phone_number'], first_name=client['name'])]
                )
                if contact.users:
                    user_id = contact.users[0].id
                    await app.send_message(user_id, client['message'])
                    time.sleep(5)
                    update_result(client['id'])
                else:
                    error_list.append(client['phone_number'])
            if len(error_list) != 0:
                await app.send_message(admin_username,
                                       f"К сожалению, пользователи с этими номерами телефона: \n{error_list}\n "
                                       f"пока не пользуется Telegram или он скрыл свой номер телефона")
            if client_count < 10:
                await app.send_message(admin_username,
                                       f"<b>Сегодня мы поздравили:</b>\n{client_name} ")
                time.sleep(5)
            else:
                await app.send_message(admin_username,
                                       f"<b>Сегодня мы поздравили:</b> {client_count} пользователей!!")
        except FloodWait as e:
            logger.exception("FloodWait", e.value)
            await asyncio.sleep(e.value)


async def send_message_mailing(image_data: list, mailing_id: int, client_list, commercial_offer: str,
                               admin_username: str):
    api_id = os.environ.get('API_ID')
    api_hash = os.environ.get('API_HASH')
    string_session = os.environ.get('STRING_SESSION')
    """Получаем chart_id пользователя и рассылаем сообщения"""
    error_list = []  # список номеров, которым не смогли отправить сообщение

    async with Client('account', api_id, api_hash, session_string=string_session) as app:
        client_count = len(client_list)
        try:
            for client in client_list:
                # сохраняем пользователей и получаем chat_id, если даже он есть, сохраняем (без циклов)
                contact: ImportedContacts = await app.import_contacts(
                    [InputPhoneContact(phone=client.phone_number, first_name=client.first_name)]
                )
                if contact.users:
                    user_id = contact.users[0].id
                    # проверяем есть ли фото, если да, то рассылаем их первыми
                    if len(image_data) != 0:
                        # собирает все изображения и отправляет в 1 сообщении
                        media = [InputMediaPhoto(f'media/{item}') for item in image_data]
                        await app.send_media_group(user_id,
                                                   media=media)
                        await asyncio.sleep(3)
                    await app.send_message(user_id, commercial_offer)
                    update_mailing(mailing_id)
                    await asyncio.sleep(3)
                else:
                    error_list.append(client.phone_number)

                if len(error_list) != 0:
                    await app.send_message(admin_username,
                                           f"К сожалению, пользователи с этими номерами телефона: \n{error_list}\n "
                                           f"пока не пользуется Telegram или они скрыли свой номер телефона")
            await app.send_message(admin_username,
                                   f"<b>Было отправлено:</b> {client_count} пользователям!!")
        except FloodWait as e:
            await asyncio.sleep(e.value)
