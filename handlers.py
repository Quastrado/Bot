from glob import glob
import os
from random import choice

from db import db, get_or_create_user, subscribe_user, unsubscribe_user
from jobs import alarm
from utils import play_random_numbers, main_keyboard, is_cat, cat_rating_inline_keyboard


def greet_user(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    print('Start triggered')
    update.message.reply_text(
        f'Hey!{user["emoji"]}',
        reply_markup=main_keyboard()
        )


def talk_to_me(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat_id)
    text = update.message.text
    print(text)
    update.message.reply_text(
        f'{text} {user["emoji"]}',
        reply_markup=main_keyboard())


def guess_number(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat_id)
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except (TypeError, ValueError):
            message = 'Enter an integer'
    else:
        message = 'Enter the number'
    update.message.reply_text(
        message,
        reply_markup=main_keyboard()
        )


def send_picture(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat_id)
    picture_list = glob('images/pic*.jpg')
    picture = choice(picture_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(
        chat_id=chat_id,
        photo=open(picture, 'rb'),
        reply_markup=cat_rating_inline_keyboard(picture)
    )


def user_coordinates(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat_id)
    coords = update.message.location
    update.message.reply_text(
        f'Your coordinates {coords} {user["emoji"]}!',
        reply_markup=main_keyboard()
    )


def check_user_photo(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat_id)
    update.message.reply_text('Process image')
    os.makedirs('downloads', exist_ok=True)
    user_photo = context.bot.getFile(update.message.photo[-1].file_id)
    file_name = os.path.join('downloads', f'{user_photo.file_id}.jpg')
    user_photo.download(file_name)
    update.message.reply_text('Image saved')
    if is_cat(file_name):
        update.message.reply_text('Cat detected!')
        new_filename = os.path.join('images', f'{user_photo.file_id}.jpg')
        os.rename(file_name, new_filename)
    else:
        update.message.reply_text('Cat not found')
        os.remove(file_name)


def subscribe(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    subscribe_user(db, user)
    update.message.reply_text('You have successfully subscribed')


def unsubscribe(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    unsubscribe_user(db, user)
    update.message.reply_text('You have successfully unsubscribed')

def set_alarm(update, context):
    try:
        alarm_seconds = abs(int(context.args[0]))
        context.job_queue.run_once(alarm, alarm_seconds, context=update.message.chat.id)
        update.message.reply_text(f'Notification after {alarm_seconds} seconds')
    except (ValueError, TypeError):
        update.message.reply_text(f'Enter an integer number of seconds after the command')


def cat_picture_rating(update, context):
    update.callback_query.answer()
    text = f"Your choice: {update.callback_query.data}"
    update.callback_query.edit_message_caption(caption=text)