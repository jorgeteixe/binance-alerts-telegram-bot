import logging
import os
import signal
from multiprocessing import Process

from dotenv import load_dotenv

from background import background
from bot import start_bot
from data import init_db


def exit_bot(s, f):
    exit(0)


load_dotenv()
signal.signal(signal.SIGINT, exit_bot)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")


def main():
    init_db()
    Process(target=background).start()
    start_bot(TELEGRAM_TOKEN)


if __name__ == '__main__':
    main()
