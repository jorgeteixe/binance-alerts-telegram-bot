import os
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")
client = Client(API_KEY, SECRET_KEY)


def get_balance():
    my_balances = []
    msg = ""
    all_balances = client.get_account()['balances']
    for b in all_balances:
        if float(b['free']) > 0:
            data = {'asset': b['asset'], 'value': float(b['free']), 'btc': 0, 'eur': 0, 'change': ''}
            if data['asset'] == 'BTC':
                data['change'] = str(
                    round(float(client.get_ticker(symbol='BTCEUR')['priceChangePercent']), 2))
                price = 1
            elif data['asset'] == 'USDT':
                continue
            else:
                price = float(client.get_avg_price(symbol=str(data['asset']) + 'BTC')['price'])
                data['change'] = str(
                    round(float(client.get_ticker(symbol=str(data['asset']) + 'BTC')['priceChangePercent']), 2))
            data['btc'] = price * float(data['value'])
            btceur = float(client.get_avg_price(symbol='BTCEUR')['price'])
            data['eur'] = btceur * data['btc']
            my_balances.append(data)
    for b in sorted(my_balances, key=lambda x: x['btc'], reverse=True):
        msg += str(b['asset']) + ': ' + str(b['value']) + ' (' + str(round(b['eur'], 2)) + ' €) [' + b[
            'change'] + '%]\n'
    return msg


def get_short_balance():
    pass


def get_asset_balance(asset):
    pass
