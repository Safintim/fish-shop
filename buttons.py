from api_moltin import get_products, get_cart
from telegram import InlineKeyboardButton


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


def generate_buttons_for_confirm_personal_data():
    keyboard = [
                [InlineKeyboardButton('Верно', callback_data='Верно')],
                [InlineKeyboardButton('Неверно', callback_data='Неверно')]
            ]

    return keyboard
