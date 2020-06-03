from random import choice, randint

from emoji import emojize
from telegram import ReplyKeyboardMarkup, KeyboardButton

import settings


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


def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Image', KeyboardButton('My coordinates', request_location=True)]
        ])