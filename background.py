import logging
import os
from time import sleep, time

from dotenv import load_dotenv
from telegram import Bot

from crypto import generate_watchpair_msg
from data import get_watchpairs, update_watchpair

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def log_sent_watchpair(chat_id, pair):
    logging.info('id=' + str(chat_id) + ' watchpair=' + pair + ' sent')


def check_watchpairs(bot):
    now = int(time())
    watchpairs = get_watchpairs()
    for w in watchpairs:
        if now - w[4] > w[2] * 60:
            msg, new_price = generate_watchpair_msg(w)
            w = [w[0], w[1], w[2], new_price, int(time())]
            bot.send_message(w[0], msg)
            update_watchpair(w)
            log_sent_watchpair(w[0], w[1])


def background():
    bot = Bot(TELEGRAM_TOKEN)
    while True:
        check_watchpairs(bot)
        sleep(10)
