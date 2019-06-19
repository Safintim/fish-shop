import re
import os
import redis
import logging
from logs_conf import LogsHandler
from api_moltin import (get_products, get_product_by_id,
                        delete_product_from_cart, get_img_by_id, push_product_to_cart_by_id,
                        get_cart, get_total_amount_from_cart, create_customer)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Filters, Updater
from telegram.ext import CallbackQueryHandler, CommandHandler, MessageHandler
from dotenv import load_dotenv


logger = logging.getLogger(__name__)


DATABASE = None


def handle_start(bot, update):
    keyboard = generate_buttons_for_all_products_from_shop()
    keyboard.append([InlineKeyboardButton('Корзина', callback_data='Корзина')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Пожалуйста, выберете товар:', reply_markup=reply_markup)
    return 'MENU'


def handle_menu(bot, update):
    product_id = update.callback_query.data
    product = get_product_by_id(product_id)

    img_id = product['data']['relationships']['main_image']['data']['id']
    url_img_product = get_img_by_id(img_id)

    keyboard = generate_buttons_for_description(product_id)
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_photo(
        chat_id=update.callback_query.message.chat_id,
        photo=url_img_product,
        caption=make_text_description_product(product),
        reply_markup=reply_markup)
    bot.delete_message(
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id)

    return 'DESCRIPTION'


def handle_description(bot, update):
    client_id = update.callback_query.message.chat_id
    if update.callback_query.data == 'В меню':
        handle_start(bot, update.callback_query)
        return 'MENU'
    elif re.match(r'^\d{1,2}/[0-9a-f]{8}\-[0-9a-f]{4}\-[0-9a-f]{4}\-[0-9a-f]{4}\-[0-9a-f]{12}',
                  update.callback_query.data):  # Нужна ли эта проверка
        amount, product = update.callback_query.data.split('/')
        push_product_to_cart_by_id(product, client_id, amount)
        return 'DESCRIPTION'


def handle_cart(bot, update):
    client_id = update.callback_query.message.chat_id

    if update.callback_query.data == 'В меню':
        handle_start(bot, update.callback_query)
        return 'START'
    elif update.callback_query.data == 'Оплата':
        handle_waiting_phone_number(bot, update)
        update.callback_query.message.reply_text('\nПришлите, пожалуйста, ваш номер')
        return 'WAITING_PHONE_NUMBER'
    else:
        product_id = update.callback_query.data
        delete_product_from_cart(client_id, product_id)

    cart = get_cart(client_id)
    total_amount = get_total_amount_from_cart(client_id)

    text = make_text_description_cart(cart, total_amount)

    keyboard = generate_buttons_for_all_products_from_cart(client_id)
    keyboard.append([InlineKeyboardButton('В меню', callback_data='В меню')])
    keyboard.append([InlineKeyboardButton('Оплата', callback_data='Оплата')])

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text(text, reply_markup=reply_markup)
    return 'CART'


def handle_waiting_phone_number(bot, update):

    if update.message:
        phone_number = update.message.text
        update.message.reply_text(f'Вы прислали мне этот номер: {phone_number}\n'
                                  f'В скором времени я свяэусь с вами')
        create_customer(update.message.chat_id, phone_number)
        handle_start(bot, update)
        return 'MENU'
    return 'WAITING_PHONE_NUMBER'


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
    elif user_reply == 'Корзина':
        user_state = 'CART'
        DATABASE.set(chat_id, user_state)
    else:
        user_state = DATABASE.get(chat_id)

    states_functions = {
        'START': handle_start,
        'MENU': handle_menu,
        'DESCRIPTION': handle_description,
        'CART': handle_cart,
        'WAITING_PHONE_NUMBER': handle_waiting_phone_number
    }

    state_handler = states_functions[user_state]
    next_state = state_handler(bot, update)
    DATABASE.set(chat_id, next_state)


def get_database_connection():
    global DATABASE
    if DATABASE is None:
        DATABASE = redis.Redis(
            host=os.environ.get("REDIS_HOST"),
            port=os.environ.get("REDIS_PORT"),
            password=os.environ.get("REDIS_PASSWORD"),
            decode_responses=True,
            charset='utf-8')
    return DATABASE


def make_text_description_cart(cart, total_amount):
    text = ''
    for product in cart['data']:

        name = product['name']
        description = product['description']
        price = product['meta']['display_price']['with_tax']['unit']['formatted']
        quantity = product['quantity']
        total_amount_product = product['value']['amount'] // 100

        text += f'{name}\n'\
                f'{description}\n'\
                f'{price} per kg\n'\
                f'{quantity}kg in cart for {total_amount_product}\n\n'

    total_amount = total_amount['data']['meta']['display_price']['with_tax']['formatted']
    text += f'Total: {total_amount}'
    return text


def make_text_description_product(product):

    product = product['data']
    name = product['name']
    price = product['meta']['display_price']['with_tax']['formatted']
    description = product['description']
    stock = product['meta']['stock']['level']

    text = f'{name}\n\n' \
           f'{price} per kg\n{stock}kg on stock\n\n'\
           f'{description}'

    return text


def generate_buttons_for_all_products_from_shop():
    keyboard = []
    for product in get_products()['data']:
        keyboard.append([InlineKeyboardButton(product['name'], callback_data=product['id'])])
    return keyboard


def generate_buttons_for_all_products_from_cart(client_id):
    keyboard = []
    for product in get_cart(client_id)['data']:
        keyboard.append([InlineKeyboardButton(f'Убрать из корзины {product["name"]}',
                                              callback_data=product['id'])])

    return keyboard


def generate_buttons_for_description(product_id):
    keyboard = [
        [
            InlineKeyboardButton('5', callback_data=f'5/{product_id}'),
            InlineKeyboardButton('10', callback_data=f'10/{product_id}'),
            InlineKeyboardButton('15', callback_data=f'15/{product_id}')
        ],
        [InlineKeyboardButton('Корзина', callback_data='Корзина')],
        [InlineKeyboardButton('В меню', callback_data='В меню')]
      ]

    return keyboard


def error_callback(bot, update, error):
    try:
        logging.error(f'(fish-shop) {update}')
        update.message.reply_text(text='Простите, возникла ошибка.')
    except Exception as err:
        logging.critical(f'(fish-shop) {err}')


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO,
                        handlers=[LogsHandler()])

    logger.info('(fish-shop) DeniskaShopTest запущен')

    load_dotenv()

    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    updater = Updater(token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CallbackQueryHandler(handle_users_reply))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_users_reply))
    dispatcher.add_handler(CommandHandler('start', handle_users_reply))
    dispatcher.add_error_handler(error_callback)
    updater.start_polling()
