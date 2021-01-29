import os
from dotenv import load_dotenv
import logging
from bot import start_bot
from crypto import setup_crypto

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")


def main():
    binance_client = setup_crypto(API_KEY, SECRET_KEY)
    start_bot(TELEGRAM_TOKEN)


if __name__ == '__main__':
    main()

