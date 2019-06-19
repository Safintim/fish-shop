import os
import re
import requests
from datetime import datetime
from pprint import pprint
from dotenv import load_dotenv


PROXIES = {
    'http': 'http://213.211.146.13:3128',
}


def create_customer(client_id, phone_number):
    url = 'https://api.moltin.com/v2/customers'

    headers = get_headers()
    headers.update({'Content-Type': 'application/json'})
    time = str(datetime.now().replace(second=0, microsecond=0))
    unique_email = re.sub(r'[\s\-:]', '_', time) + '@m.ru'
    payload = {
        'data': {
            'type': 'customer',
            'name': str(phone_number),
            'email': unique_email
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()


def delete_product_from_cart(client_id, product_id):
    url = f'https://api.moltin.com/v2/carts/{client_id}/items/{product_id}'
    response = requests.delete(url, headers=get_headers())
    return response.json()


def get_access_token():
    payload = {
        'client_id': os.environ.get('CLIENT_ID_MOLTIN'),
        'client_secret': os.environ.get('CLIENT_SECRET_MOLTIN'),
        'grant_type': 'client_credentials'
    }
    url = 'https://api.moltin.com/oauth/access_token'
    response = requests.post(url, data=payload, proxies=PROXIES)
    return response.json()['access_token']


def get_cart(client_id):
    url = f'https://api.moltin.com/v2/carts/{client_id}/items'
    response = requests.get(url, headers=get_headers(), proxies=PROXIES)

    return response.json()


def get_headers():
    return {
        'Authorization': f'Bearer {os.environ.get("ACCESS_TOKEN_MOLTIN")}',
    }


def get_customer(client_id):
    url = f'https://api.moltin.com/v2/customers/{client_id}'
    response = requests.get(url, headers=get_headers())
    return response.json()


def get_img_by_id(id):
    url = f'https://api.moltin.com/v2/files/{id}'
    response = requests.get(url, headers=get_headers(), proxies=PROXIES)
    return response.json()['data']['link']['href']


def get_products():
    url = 'https://api.moltin.com/v2/products'
    response = requests.get(url, headers=get_headers(), proxies=PROXIES)
    return response.json()


def get_product_by_id(id):
    url = f'https://api.moltin.com/v2/products/{id}'
    response = requests.get(url, headers=get_headers(), proxies=PROXIES)
    return response.json()


def get_total_amount_from_cart(client_id):
    url = f'https://api.moltin.com/v2/carts/{client_id}'
    response = requests.get(url, headers=get_headers(), proxies=PROXIES)

    return response.json()


def push_product_to_cart_by_id(product_id, client_id, amount):
    headers = get_headers()
    headers.update({'Content-Type': 'application/json'})

    payload = {
        'data': {
            'id': product_id,
            'type': 'cart_item',
            'quantity': int(amount)
        }
    }
    url = f'https://api.moltin.com/v2/carts/{client_id}/items'
    response = requests.post(url, headers=headers, json=payload, proxies=PROXIES)

    return response


def main():
    load_dotenv()
    pprint(get_access_token())
    # pprint(get_products())


if __name__ == '__main__':
    main()
