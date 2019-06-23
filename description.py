from api_moltin import get_product_from_cart


def make_text_description_cart(cart, total_amount):
    parts_text = []
    for product in cart['data']:

        name = product['name']
        description = product['description']
        price = product['meta']['display_price']['with_tax']['unit']['formatted']
        quantity = product['quantity']
        total_amount_product = product['value']['amount'] // 100

        parts_text.append(f'*{name}*')
        parts_text.append(f'_{description}_')
        parts_text.append(f'*{price} per kg*')
        parts_text.append(f'*{quantity}kg in cart for ${total_amount_product:.2f}*\n')

    total_amount = total_amount['data']['meta']['display_price']['with_tax']['formatted']
    parts_text.append(f'*Total: {total_amount}*')
    return '\n'.join(parts_text)


def make_text_description_product(product, client):
    product = product['data']

    product_from_cart = get_product_from_cart(product['id'], client)

    quantity_product_in_cart = 0
    total_amount_product_in_cart = 0
    parts_text = []
    if product_from_cart:
        quantity_product_in_cart = product_from_cart['quantity']
        total_amount_product_in_cart = product_from_cart['value']['amount'] // 100

    name = product['name']
    price = product['meta']['display_price']['with_tax']['formatted']
    description = product['description']
    stock = product['meta']['stock']['level']

    parts_text.append(f'*{name}*\n')
    parts_text.append(f'*{price} per kg*\n*{stock}kg on stock*\n')
    parts_text.append(f'_{description}_\n')
    parts_text.append(f'_{quantity_product_in_cart}kg in cart for ${total_amount_product_in_cart:.2f}_\n')

    return '\n'.join(parts_text)
