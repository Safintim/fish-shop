import os
import logging
import redis

from api_moltin import get_products, get_product_by_id, get_img_by_id
from telegram.ext import Filters, Updater
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler
from dotenv import load_dotenv

DATABASE = None

def start(bot, update):
    keyboard = generate_keyboard()
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)
    update.message.reply_text(text='Привет!')
    return "ECHO"


def echo(bot, update):
    """
    Хэндлер для состояния ECHO.
    
    Бот отвечает пользователю тем же, что пользователь ему написал.
    Оставляет пользователя в состоянии ECHO.
    """
    users_reply = update.message.text
    update.message.reply_text(users_reply)
    return "ECHO"


def handle_users_reply(bot, update):
    """
    Функция, которая запускается при любом сообщении от пользователя и решает как его обработать.
    Эта функция запускается в ответ на эти действия пользователя:
        * Нажатие на inline-кнопку в боте
        * Отправка собщения боту
        * Отправка команды боту
    Она получает стейт пользователя из базы данных и запускает соответствующую функцию-обработчик (хэндлер).
    Функция-обработчик возвращает следующее состояние, которое записывается в базу данных.
    Если пользователь только начал пользоваться ботом, Telegram форсит его написать "/start",
    поэтому по этой фразе выставляется стартовое состояние.
    Если польхователь захочет начать общение с ботом заново, он также может воспользоваться этой командой.
    """
    DATABASE = get_database_connection()
    if update.message:
        user_reply = update.message.text
        chat_id = update.message.chat_id
    elif update.callback_query:
        user_reply = update.callback_query.data
        chat_id = update.callback_query.message.chat_id
    else:
        return
    if user_reply == '/start':
        user_state = 'START'
    else:
        user_state = DATABASE.get(chat_id)
    states_functions = {
        'START': start,
        'ECHO': echo
    }
    state_handler = states_functions[user_state]
    next_state = state_handler(bot, update)
    DATABASE.set(chat_id, next_state)

def get_database_connection():
    print('a')
    global DATABASE
    if DATABASE is None:
        DATABASE = redis.Redis(
            host=os.getenv("REDIS_HOST"),
            port=os.getenv("REDIS_PORT"),
            password=os.getenv("REDIS_PASSWORD"),
            decode_responses=True,
            charset='utf-8')
    return DATABASE

def generate_keyboard():
    keyboard = []
    for product in get_products():
        keyboard.append([InlineKeyboardButton(
            product['name'], callback_data=product['id'])])
    return keyboard


def error_callback(bot, update, error):
    """
    Перехватывает все ошибки, связанные с Telegram (TelegramError).
    """
    try:
        logging.error(str(update))
        update.message.reply_text(text='Простите, возникла ошибка.')
    except Exception as err:
        logging.critical(err)

if __name__ == '__main__':
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    updater = Updater(token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CallbackQueryHandler(handle_users_reply))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_users_reply))
    dispatcher.add_handler(CommandHandler('start', handle_users_reply))
    dispatcher.add_error_handler(error_callback)
    updater.start_polling()