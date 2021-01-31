import logging
import os

from dotenv import load_dotenv
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater, CommandHandler

from crypto import create_watchpair, generate_watchpair_msg, generate_tradeposition_msg, create_watchtrade
from data import start_user_db, make_admin_db, save_watchpair, delete_watchpair, get_watchpairs_from_user, \
    get_watchtrades_from_user, delete_watchtrade, save_watchtrade, update_alerting_watchtrade

load_dotenv()
MY_CHAT_ID = os.getenv("MY_CHAT_ID")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")


def log_command(command, eff_chat, params=''):
    logging.info('id=' + str(eff_chat.id) + ' (' + str(eff_chat.username) + ') -> ' + '/' + command + params)


def start_bot():
    updater = Updater(token=TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('watch', watch))
    dispatcher.add_handler(CommandHandler('unwatch', unwatch))
    dispatcher.add_handler(CommandHandler('watching', watching))
    dispatcher.add_handler(CommandHandler('wtrade', wtrade))
    dispatcher.add_handler(CommandHandler('unwtrade', unwtrade))
    dispatcher.add_handler(CommandHandler('atrade', atrade))
    dispatcher.add_handler(CommandHandler('wtrades', wtrades))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    dispatcher.add_handler(MessageHandler(Filters.text, messages))
    updater.start_polling()


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Unrecognised command...')


def messages(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='I\'m not a person, try a command...')


def start(update, context):
    log_command('start', update.effective_chat)
    if start_user_db(update.effective_chat.id):
        msg = "Welcome! I\'m teixeBOT, we can be friends."
        if int(update.effective_chat.id) == int(MY_CHAT_ID):
            make_admin_db(update.effective_chat.id)
    else:
        msg = "Welco... you again, I still remember you!"
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


def watch(update, context):
    log_command('watch', update.effective_chat)
    rsp, err = create_watchpair(update.effective_chat.id, context.args)
    if not rsp:
        context.bot.send_message(chat_id=update.effective_chat.id, text=err)
        return
    else:
        watchpair = rsp
    if not save_watchpair(watchpair):
        context.bot.send_message(chat_id=update.effective_chat.id, text='Already watching that pair.')
        return
    msg, _ = generate_watchpair_msg(watchpair)
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


def unwatch(update, context):
    log_command('unwatch', update.effective_chat)
    if not context.args or len(context.args) != 1:
        msg = 'Usage:\n/unwatch <pair>'
    elif delete_watchpair(update.effective_chat.id, context.args[0]):
        msg = 'Successfully unwatched pair ' + context.args[0]
    else:
        msg = 'You\'re not watching this...'
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


def watching(update, context):
    log_command('watching', update.effective_chat)
    watchpairs = get_watchpairs_from_user(update.effective_chat.id)
    if len(watchpairs) == 0:
        msg = 'Your watchlist is empty.'
    else:
        msg = 'Watchlist:\n'
    for w in watchpairs:
        msg += f'{w[1]} ({w[2]} min)\n'
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


def wtrade(update, context):
    log_command('wtrade', update.effective_chat)
    rsp, err = create_watchtrade(update.effective_chat.id, context.args)
    if not rsp:
        context.bot.send_message(chat_id=update.effective_chat.id, text=err)
        return
    else:
        watchtrade = rsp
    if not save_watchtrade(watchtrade):
        context.bot.send_message(chat_id=update.effective_chat.id, text='Already watching that trade.')
        return
    msg, actual_price = generate_watchpair_msg(watchtrade)
    position = generate_tradeposition_msg(watchtrade[5], actual_price)
    msg = position + ' ' + msg
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


def unwtrade(update, context):
    log_command('unwtrade', update.effective_chat)
    if not context.args or len(context.args) != 1:
        msg = 'Usage:\n/unwtrade <pair>'
    elif delete_watchtrade(update.effective_chat.id, context.args[0]):
        msg = 'Successfully unwatched trade ' + context.args[0]
    else:
        msg = 'You\'re not watching this...'
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


def wtrades(update, context):
    log_command('wtrades', update.effective_chat)
    watchpairs = get_watchtrades_from_user(update.effective_chat.id)
    if len(watchpairs) == 0:
        msg = 'Your watchtrades-list is empty.'
    else:
        msg = 'Watchtrades-list:\n'
    for w in watchpairs:
        if w[7] == 1:
            alerts = 'ALERTS ON'
        else:
            alerts = 'ALERTS OFF'
        msg += f'{w[1]} ({w[2]} min) {alerts}\n'
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


def atrade(update, context):
    log_command('atrade', update.effective_chat)
    if len(context.args) != 2:
        msg = 'Usage:\n/atrade <pair> <value>'
    else:
        try:
            alerting = int(context.args[1])
            if alerting == 1 or alerting == 0:
                rsp, err = update_alerting_watchtrade(update.effective_chat.id, context.args[0], alerting)
                if rsp:
                    msg = f'Updated {context.args[0]} set alerting to {alerting}'
                else:
                    msg = err
            else:
                raise ValueError
        except ValueError:
            msg = 'Alerting value has to be 0 (OFF) or 1 (ON).'
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
