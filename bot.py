from glob import glob
import logging
from random import choice, randint
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings

logging.basicConfig(filename='bot.log', level=logging.INFO)

PROXY = {'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}


def greet_user(update, context):
    print('Start triggered')
    update.message.reply_text('Hey! You triggered a start')


def talk_to_me(update, context):
    text = update.message.text
    print(text)
    update.message.reply_text(text)


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
    update.message.reply_text(message)


def send_picture(update, context):
    picture_list = glob('images/pic*.jpg')
    picture = choice(picture_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(picture, 'rb')) 


def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('guess', guess_number))
    dp.add_handler(CommandHandler('pic', send_picture))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    logging.info('LazyBoy was start')
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()