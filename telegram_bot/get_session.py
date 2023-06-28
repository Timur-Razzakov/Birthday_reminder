import asyncio
import os
import sys

import django
import dotenv
from pyrogram import Client

dotenv.load_dotenv('.env')

proj = os.path.dirname(os.path.abspath('../manage.py'))
sys.path.append(proj)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reminder_service.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

# # -----------------------------------------------------

workdir = os.environ.get('SESSIONS_FOLDER')


async def get_string_session():
    """Получаем string_session, чтобы отправлять сообщение без задержек,
    так как pyrogram исп sqlite """
    api_id = os.environ.get('API_ID')
    api_hash = os.environ.get('API_HASH')
    async with Client(workdir, api_id, api_hash) as app:
        string_session = await app.export_session_string()
    return string_session
