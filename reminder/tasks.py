from celery import shared_task
from icecream import ic

from reminder_service.celery import app
from telegram_bot.user_bot import send_message_mailing
import asyncio


@app.task
def send_messages(api_id, api_hash, mailing_id,
                  clients, msg, admin_name):
    ic(api_id)
    ic(api_id)
    asyncio.run(send_message_mailing(api_id, api_hash, mailing_id,
                                     clients, msg, admin_name))
