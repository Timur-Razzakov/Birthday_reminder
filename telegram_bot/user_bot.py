import asyncio
import datetime
import logging
import os
import sys

import django
import dotenv
from pyrogram import Client
from pyrogram.errors import FloodWait
from pyrogram.raw.base.contacts import ImportedContacts
from pyrogram.types import InputPhoneContact, InputMediaPhoto, InputMediaVideo

dotenv.load_dotenv('.env')

proj = os.path.dirname(os.path.abspath('../manage.py'))
sys.path.append(proj)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reminder_service.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
# # ---------------------------------------------------------------------------------

logger = logging.getLogger(__name__)
from reminder.models import Result, MailingCommerceOffer, Holiday

today = datetime.datetime.today()


async def get_string_session():
    """Получаем string_session, чтобы отправлять сообщение без задержек,
    так как pyrogram исп sqlite """
    api_id = os.environ.get('API_ID')
    api_hash = os.environ.get('API_HASH')
    async with Client('account', api_id, api_hash) as app:
        string_session = await app.export_session_string()
    return string_session


#
# #
# asyncio.run(get_string_session())


def update_result(result_id):
    """Обновляем модель Result, Sending_status=True и process_date=today"""
    client = Result.objects.get(id=result_id)
    client.sending_status = True
    client.process_date = today
    client.save()


async def send_message_holiday(client_data: list, admin_username):
    """Получаем chart_id пользователя и рассылаем сообщения из модели Result"""
    string_session = await get_string_session()
    api_id = os.environ.get('API_ID')
    api_hash = os.environ.get('API_HASH')
    async with Client('account', api_id, api_hash, string_session) as app:
        client_count = set()
        client_name = []
        error_list = []
        try:
            for client in client_data:
                client_count.add(client['phone_number'])
                get_image = Holiday.objects.get(id=client['images'])
                client_name.append(client['name'])
                # сохраняем пользователей и получаем chat_id, если даже он есть, сохраняем (без циклов)
                contact: ImportedContacts = await app.import_contacts(
                    [InputPhoneContact(phone=client['phone_number'], first_name=client['name'])]
                )
                if contact.users:
                    user_id = contact.users[0].id
                    await app.send_photo(user_id, photo=f'media/{get_image.image}', caption=client['message'])
                    await asyncio.sleep(5)
                    update_result(client['id'])
                else:
                    error_list.append(client['phone_number'])
            if len(error_list) != 0:
                await app.send_message(admin_username,
                                       f"К сожалению, пользователи с этими номерами телефона: "
                                       f"\n{error_list}\n "
                                       f"пока не пользуется Telegram или он скрыл свой номер телефона")
            if len(client_count) < 10:
                await app.send_message(admin_username,
                                       f"<b>Сегодня мы поздравили:</b>\n{client_name} ")
                await asyncio.sleep(5)
            else:
                await app.send_message(admin_username,
                                       f"<b>Сегодня мы поздравили:</b> {len(client_count)} пользователей!!")
        except FloodWait as e:
            logger.exception("FloodWait", e.value)
            await asyncio.sleep(e.value)


#
# asyncio.run(send_message_holiday(get_data_from_result(), 'Razzakov_Timur'))


# ------------------------Отправляем по телеграмму Коммерческие предложения-------------------------

def update_mailing(mailing_id):
    """Обновляем модель MailingCommerceOffer, Sending_status=True и process_date=today"""
    mailing = MailingCommerceOffer.objects.get(id=mailing_id)
    mailing.sending_status = True
    mailing.save()


async def send_message_mailing(video_data: list, image_data: list, mailing_id: int, client_list,
                               commercial_offer: str,
                               admin_username: str):
    api_id = os.environ.get('API_ID')
    api_hash = os.environ.get('API_HASH')
    string_session = await get_string_session()
    """Получаем chart_id пользователя и рассылаем сообщения"""
    error_list = []  # список номеров, которым не смогли отправить сообщение

    async with Client('account', api_id, api_hash, session_string=string_session) as app:
        client_count = set()
        try:
            for client in client_list:
                client_count.add(client.phone_number)
                # сохраняем пользователей и получаем chat_id, если даже он есть, сохраняем (без циклов)
                contact: ImportedContacts = await app.import_contacts(
                    [InputPhoneContact(phone=client.phone_number, first_name=client.first_name)]
                )
                if contact.users:
                    user_id = contact.users[0].id
                    # проверяем есть ли фото, если да, то рассылаем их первыми
                    if len(image_data or video_data) != 0:
                        # собирает все изображения и отправляет в 1 сообщении
                        media = []
                        for item in image_data:
                            media.append(InputMediaPhoto(f'media/{item}'))

                        for item in video_data:
                            media.append(InputMediaVideo(f'media/{item}'))
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
                                           f"К сожалению, пользователи с этими номерами телефона: "
                                           f"\n{error_list}\n "
                                           f"пока не пользуется Telegram или они скрыли свой номер телефона")
            await app.send_message(admin_username,
                                   f"<b>Было отправлено:</b> {len(client_count)} пользователям!!")
        except FloodWait as e:
            await asyncio.sleep(e.value)
