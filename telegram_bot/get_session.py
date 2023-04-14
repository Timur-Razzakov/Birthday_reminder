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
def get_session():
    """Входим в аккаунт телеграмма """
    api_id = os.environ.get('API_ID')
    api_hash = os.environ.get('API_HASH')
    app = Client('account', api_id, api_hash)
    return app


app = get_session()
app.run()
