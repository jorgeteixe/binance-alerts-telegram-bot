import logging
import os

from dotenv import load_dotenv
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater, CommandHandler

from crypto import create_watchpair, generate_watchpair_msg
from data import start_user_db, make_admin_db, save_watchpair, delete_watchpair, get_watchpairs_from_user

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
