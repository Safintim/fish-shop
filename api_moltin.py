import os
import requests


def get_headers():
    return {
        'Authorization': f'Bearer {os.getenv("ACCESS_TOKEN_MOLTIN")}',
    }


def get_products():
    url = 'https://api.moltin.com/v2/products'
    response = requests.get(url, headers=get_headers())
    return response.json()['data']


def get_cart():
    url = 'https://api.moltin.com/v2/carts/:reference'
    response = requests.get(url, headers=get_headers())

    return response.json()


def put_product_to_cart(product_id):
    headers = get_headers()
    headers.update({'Content-Type': 'application/json'})

    payload = {
        'data': {
            'id': product_id,
            'type': 'cart_item',
            'quantity': 1
        }
    }
    url = 'https://api.moltin.com/v2/carts/:reference/items'
    response = requests.post(url, headers=headers, json=payload)

    return response
