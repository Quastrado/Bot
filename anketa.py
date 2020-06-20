from telegram import ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler
from db import db, get_or_create_user, save_anketa
from utils import main_keyboard

def anketa_start(update, context):
    update.message.reply_text(
        'What is your name?',
        reply_markup=ReplyKeyboardRemove()
    )
    return 'name'


def anketa_name(update, context):
    user_name = update.message.text
    if len(user_name.split()) < 2:
        update.message.reply_text('Please enter first and last name')
        return 'name'
    else:
        context.user_data['anketa'] = {'name': user_name}
        reply_keyboard = ['1', '2', '3', '4', '5']
        update.message.reply_text(
            'Rate the LazyBoy from 1 to 5',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        )
        return 'rating'


def anketa_rating(update, context):
    context.user_data['anketa']['rating'] = int(update.message.text)
    update.message.reply_text('Write a comment or press "/skip" to skip')
    return 'comment'


def anketa_comment(update, context):
    context.user_data['anketa']['comment'] = update.message.text
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    save_anketa(db, user['user_id'], context.user_data['anketa'])
    user_text = format_anketa(context.user_data['anketa'])
    update.message.reply_text(user_text, reply_markup=main_keyboard(), parse_mode=ParseMode.HTML)
    return ConversationHandler.END


def anketa_skip(update, context):
    user = get_or_create_user(db, update.effective_user, update.message.chat.id)
    save_anketa(db, user['user_id'], context.user_data['anketa'])
    user_text = format_anketa(context.user_data['anketa'])
    update.message.reply_text(user_text, reply_markup=main_keyboard(), parse_mode=ParseMode.HTML)
    return ConversationHandler.END


def format_anketa(anketa):
    user_text = f"""<b>Name Surname</b>: {anketa['name']}
<b>Rating</b>: {anketa['rating']}
"""
    if 'comment' in anketa:
        user_text += f"\n<b>Comment</b>: {anketa['comment']}"
    return user_text


def anketa_dontknow(update, context):
    update.message.reply_text('I do not understand')
