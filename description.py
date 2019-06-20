from api_moltin import get_product_from_cart


def make_text_description_cart(cart, total_amount):
    text = ''
    for product in cart['data']:

        name = product['name']
        description = product['description']
        price = product['meta']['display_price']['with_tax']['unit']['formatted']
        quantity = product['quantity']
        total_amount_product = product['value']['amount'] // 100

        text += f'*{name}*\n'\
                f'_{description}_\n'\
                f'*{price} per kg*\n'\
                f'*{quantity}kg in cart for ${total_amount_product:.2f}*\n\n'

    total_amount = total_amount['data']['meta']['display_price']['with_tax']['formatted']
    text += f'*Total: {total_amount}*'
    return text


def make_text_description_product(product, client):
    product = product['data']

    product_from_cart = get_product_from_cart(product['id'], client)

    quantity_product_in_cart = 0
    total_amount_product_in_cart = 0
    if product_from_cart:
        quantity_product_in_cart = product_from_cart['quantity']
        total_amount_product_in_cart = product_from_cart['value']['amount'] // 100

    name = product['name']
    price = product['meta']['display_price']['with_tax']['formatted']
    description = product['description']
    stock = product['meta']['stock']['level']

    text = f'*{name}*\n\n' \
           f'*{price} per kg*\n*{stock}kg on stock*\n\n'\
           f'_{description}_\n\n'\
           f'_{quantity_product_in_cart}kg in cart for ${total_amount_product_in_cart:.2f}_\n\n'

    return text
