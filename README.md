# teixeBOT
Telegram bot for my personal things.

## Commands
#### watch / unwatch [cryptocurrency]
Receive scheduled updates on the selected pair each n minutes.
Use ```unwatch``` to stop.

Usage: 
```
/watch <pair> <interval>
    pair:       valid pair from Binance Exchange
    interval:   minutes between messages [min: 1  max: 1440 (day)]

/unwatch <pair>
    pair:       pair on your watchlist
```


### Telegram-like format command list
```
watch - add a cryptocurrency pair to your watchlist
unwatch - remove a pair from your watchlist
```