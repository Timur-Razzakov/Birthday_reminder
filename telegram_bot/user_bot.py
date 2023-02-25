import os

import dotenv
from pyrogram import Client, enums

dotenv.load_dotenv('.env')

# api_id = os.environ.get('API_ID')
# api_hash = os.environ.get('API_HASH')

api_id = 2040
api_hash = 'b18441a1ff607e10a989891a5462e627'
#
# app = Client('account', api_id=api_id, api_hash=api_hash)
with Client('account', api_id=api_id, api_hash=api_hash) as app:
    app.send_message('me', 'hi, it good')


# async def main():
#     async with app:
#         id_ = await app.get_me()
#
#         a = await app.send_message(chat_id='me',
#                                    text=f'<a href="tg://user?id=123456789">{id_.id}inline mention of a user</a>',
#                                    parse_mode=enums.ParseMode.HTML)
#
# app.run(main())