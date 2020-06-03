from glob import glob
import logging
from random import choice, randint

from emoji import emojize
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings

logging.basicConfig(filename='bot.log', level=logging.INFO)

PROXY = {'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}


def greet_user(update, context):
    print('Start triggered')
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(
        f'Hey!{context.user_data["emoji"]}',
        reply_markup=main_keyboard()
        )


def talk_to_me(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    text = update.message.text
    print(text)
    update.message.reply_text(
        f'{text} {context.user_data["emoji"]}',
        reply_markup=main_keyboard())


def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, use_aliases=True)
    return user_data['emoji']


def play_random_numbers(user_number):
    bot_number = randint(user_number-10, user_number+10)
    if user_number > bot_number:
        message = f'You made {user_number}, I made {bot_number}, you won!'
    elif user_number == bot_number:
        message = f'You made {user_number}, I made {bot_number}, draw!'
    else:
        message = f'You made {user_number}, I made {bot_number}, I won!'
    return message


def guess_number(update, context):
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
    picture_list = glob('images/pic*.jpg')
    picture = choice(picture_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(
        chat_id=chat_id,
        photo=open(picture, 'rb'),
        reply_markup=main_keyboard()
        ) 


def main_keyboard():
    return ReplyKeyboardMarkup([['Image']])


def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('guess', guess_number))
    dp.add_handler(CommandHandler('pic', send_picture))
    dp.add_handler(MessageHandler(Filters.regex('^(Image)$'), send_picture))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    logging.info('LazyBoy was start')
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()