import os
from time import time

from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")
client = Client(API_KEY, SECRET_KEY)


def generate_watchpair_msg(watchpair):
    ticker = client.get_ticker(symbol=watchpair[1])
    last_price = float(ticker['lastPrice'])
    change = float(ticker['priceChangePercent'])
    if last_price > watchpair[3]:
        arrow = '↑'
    elif last_price < watchpair[3]:
        arrow = '↓'
    else:
        arrow = '→'
    if last_price > 1:
        formatted_price = f'{"%.2f" % last_price}'
    else:
        formatted_price = f'{"%.8f" % last_price}'
    return f'{arrow} {watchpair[1]} {formatted_price} ({"%+.1f" % change}%)', last_price


def create_watchpair(chat_id, args):
    if len(args) != 2:
        return False, 'Usage:\n/watch <pair> <interval>'
    refresh = int(args[1])
    if not 1 <= refresh <= 1440:
        return False, 'Invalid interval.'
    pair = args[0]
    try:
        price = client.get_ticker(symbol=pair)['lastPrice']
    except BinanceAPIException:
        return False, 'Invalid pair.'
    return [[chat_id, pair, refresh, float(price), int(time())], None]


def create_watchtrade(chat_id, args):
    if len(args) != 3:
        return False, 'Usage:\n/wtrade <pair> <interval> <enterPrice>'
    try:
        refresh = int(args[1])
        if not 1 <= refresh <= 1440:
            raise ValueError
    except ValueError:
        return False, 'Invalid interval.'
    pair = args[0]
    try:
        price = client.get_ticker(symbol=pair)['lastPrice']
    except BinanceAPIException:
        return False, 'Invalid pair.'
    try:
        enterprice = float(args[2])
        if enterprice < 0:
            raise ValueError
    except ValueError:
        return False, 'Invalid enterPrice.'
    return [[chat_id, pair, refresh, float(price), int(time()), enterprice], None]


def generate_tradeposition_msg(enterprice, actualprice):
    change = actualprice / enterprice
    return f'[{"%.2f" % change}]'
