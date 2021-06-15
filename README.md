# binance-alerts-telegram-bot
Telegram bot that alerts binance actions.

## Get it running

### Ubuntu:
```bash
git clone https://github.com/jorgeteixe/binance-alerts-telegram-bot.git bot
apt install build-essential python3.8 python3.8-dev
cd bot
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
nano .env                         # details below
python main.py
```

### .env file
```.env
BINANCE_API_KEY=
BINANCE_SECRET_KEY=
TELEGRAM_TOKEN=
MY_CHAT_ID=
```

1. Get your Binance API key and secret [here](https://accounts.binance.com/en/register).
2. Get your Telegram Token with [BotFather](https://t.me/BotFather).
3. Run the software without MY_CHAT_ID, start the conversation with the bot and paste the id shown in your shell.



## Commands

#### Cryptocurrency watchlist
Receive scheduled updates on the selected pair each n minutes.

Usage: 
```
/watch <pair> <interval>       >> Adds to watchlist
    pair:       valid pair from Binance Exchange
    interval:   minutes between messages [min: 1  max: 1440 (day)]

/unwatch <pair>                >> Removes from watchlist
    pair:       pair on your watchlist

/watching                      >> Shows watchlist
```


#### Trade cryptocyrrency watchlist
Receive scheduled updates on the selected pair each n minutes.
To receive special alerts when abrupt changes occur, toggle ALERTING.

Usage: 
```
/wtrade <pair> <interval> <enterPrice>      >> Adds to watchtrades-list
    pair:       valid pair from Binance Exchange
    interval:   minutes between messages [min: 1  max: 1440 (day)]
    enterPrice: base price to show actual position

/atrade <pair> <value>                      >> Change alerting value
    pair:       the pair to change the value
    value:      1 to activate, 0 to deactivate

/unwtrade <pair>                            >> Removes from watchtrades-list
    pair:       pair on your watchtrades-list

/wtrades                                    >> Shows watchtrades-list
```



### Telegram-like format command list
```
watch - add a cryptocurrency pair to your watchlist
unwatch - remove a pair from your watchlist
watching - show your watchlist
wtrade - add a trade to your watchtrades-list
atrade - set alerting for a specific watchtrade
unwtrade - remove a pair from your watchtrades-list
wtrades - show your watchtrades-list
```
