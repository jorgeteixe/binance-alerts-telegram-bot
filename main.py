import os
import signal
from dotenv import load_dotenv
import logging
from data import init_db
from bot import start_bot


def exit_bot(s, f):
    exit(0)


load_dotenv()
signal.signal(signal.SIGINT, exit_bot)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")


def main():
    init_db()
    start_bot(TELEGRAM_TOKEN)


if __name__ == '__main__':
    main()

