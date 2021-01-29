from binance.client import Client


def setup_crypto(API_KEY, SECRET_KEY):
    return Client(API_KEY, SECRET_KEY)
