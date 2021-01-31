import logging
import signal
from multiprocessing import Process

from background import background
from bot import start_bot
from data import init_db


def exit_bot(s, f):
    exit(0)


signal.signal(signal.SIGINT, exit_bot)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def main():
    init_db()
    Process(target=background).start()
    start_bot()


if __name__ == '__main__':
    main()
