from datetime import datetime

from telegram.error import BadRequest

from db import db, get_subscribed


def send_updates(context):
    now = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    for user in get_subscribed(db):
        try:
            context.bot.send_message(chat_id=555825427, text=f'Exact time: {now}')
        except BadRequest:
            print(f"Chat {user['chat_id']} not found")