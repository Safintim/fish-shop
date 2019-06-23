import os
import requests
from pprint import pprint
from dotenv import load_dotenv


PROXIES = {
    'http': 'http://213.211.146.13:3128',
}

TOKEN = os.environ.get('ACCESS_TOKEN_MOLTIN')


def is_token_works(func):

    def decorator(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
        except requests.HTTPError as error:
            response = None
            if error.response.status_code == 401:
                global TOKEN
                TOKEN = get_access_token()
                response = func(*args, **kwargs)
        return response
    return decorator


@is_token_works
def create_customer(name, email):
    url = 'https://api.moltin.com/v2/customers'

    headers = get_headers()
    headers.update({'Content-Type': 'application/json'})
    payload = {
        'data': {
            'type': 'customer',
            'name': name,
            'email': email
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()


@is_token_works
def delete_product_from_cart(client_id, product_id):
    url = f'https://api.moltin.com/v2/carts/{client_id}/items/{product_id}'
    response = requests.delete(url, headers=get_headers())
    response.raise_for_status()
    return response.json()


def get_access_token():
    payload = {
        'client_id': os.environ.get('CLIENT_ID_MOLTIN'),
        'client_secret': os.environ.get('CLIENT_SECRET_MOLTIN'),
        'grant_type': 'client_credentials'
    }
    url = 'https://api.moltin.com/oauth/access_token'
    response = requests.post(url, data=payload, proxies=PROXIES)
    response.raise_for_status()
    return response.json()['access_token']


@is_token_works
def get_cart(client_id):
    url = f'https://api.moltin.com/v2/carts/{client_id}/items'
    response = requests.get(url, headers=get_headers(), proxies=PROXIES)
    response.raise_for_status()
    return response.json()


def get_headers():
    return {
        'Authorization': f'Bearer {TOKEN}',
    }


@is_token_works
def get_customer(client_id):
    url = f'https://api.moltin.com/v2/customers/{client_id}'
    response = requests.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()


@is_token_works
def get_customers():
    url = 'https://api.moltin.com/v2/customers/'
    response = requests.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()


@is_token_works
def get_img_by_id(id):
    url = f'https://api.moltin.com/v2/files/{id}'
    response = requests.get(url, headers=get_headers(), proxies=PROXIES)
    response.raise_for_status()
    return response.json()['data']['link']['href']


@is_token_works
def get_products():
    url = 'https://api.moltin.com/v2/products'
    response = requests.get(url, headers=get_headers(), proxies=PROXIES)
    response.raise_for_status()
    return response.json()


@is_token_works
def get_product_by_id(id):
    url = f'https://api.moltin.com/v2/products/{id}'
    response = requests.get(url, headers=get_headers(), proxies=PROXIES)
    response.raise_for_status()
    return response.json()


def get_product_from_cart(product_id, client_id):
    for pr in get_cart(client_id)['data']:
        if pr['product_id'] == product_id:
            return pr


@is_token_works
def get_total_amount_from_cart(client_id):
    url = f'https://api.moltin.com/v2/carts/{client_id}'
    response = requests.get(url, headers=get_headers(), proxies=PROXIES)
    response.raise_for_status()
    return response.json()


@is_token_works
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
    response.raise_for_status()
    return response.json()


def main():
    load_dotenv()
    pprint(get_access_token())


if __name__ == '__main__':
    main()
