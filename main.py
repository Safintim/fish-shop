import os
import logging
import redis

from telegram.ext import Filters, Updater
from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler

DATABASE = None


def start(bot, update):
    update.message.reply_text(text='Привет!')
    return "ECHO"


def echo(bot, update):
    users_reply = update.message.text
    update.message.reply_text(users_reply)
    return "ECHO"


def handle_users_reply(bot, update):
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
    global DATABASE
    if DATABASE is None:
        DATABASE = redis.Redis(
            host=os.getenv("REDIS_HOST"),
            port=os.getenv("REDIS_PORT"),
            password=os.getenv("REDIS_PASSWORD"),
            decode_responses=True,
            charset='utf-8')
    return DATABASE


def error_callback(bot, update, error):
    try:
        logging.error(str(update))
        update.message.reply_text(text='Простите, возникла ошибка.')
    except Exception as err:
        logging.critical(err)


if __name__ == '__main__':
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    updater = Updater(token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CallbackQueryHandler(handle_users_reply))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_users_reply))
    dispatcher.add_handler(CommandHandler('start', handle_users_reply))
    dispatcher.add_error_handler(error_callback)
    updater.start_polling()
