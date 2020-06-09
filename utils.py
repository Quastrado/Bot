from pprint import PrettyPrinter
from random import choice, randint

from clarifai.rest import ClarifaiApp 
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
        ['Image', KeyboardButton('My coordinates', request_location=True), 'Fill out a form']
        ])


def is_cat(file_name):
    app = ClarifaiApp(api_key=settings.CLARIFAI_API_KEY)
    model = app.public_models.general_model
    response = model.predict_by_filename(file_name, max_concepts=5)
    if response['status']['code'] == 10000:
        for concept in response['outputs'][0]['data']['concepts']:
            if concept['name'] == 'cat':
                return True
    return False


if __name__ == '__main__':
    print(is_cat('images/cat1.jpg'))
    print(is_cat('images/cat2.jpg'))