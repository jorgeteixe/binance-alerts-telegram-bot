import logging
import threading

from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater, CommandHandler

from crypto import get_balance
from data import start_user_db


def log_command(command, eff_chat, params=''):
    logging.info('/' + command + ' from id=' + str(eff_chat.id) + ' (' + str(eff_chat.username) + ') ' + params)


def balance_background(update, context, seconds):
    threading.Timer(float(seconds), balance_background, [update, context, seconds]).start()
    msg = get_balance()
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
    log_command('balance', update.effective_chat, 'BACKGROUND')


def start_bot(TELEGRAM_TOKEN):
    updater = Updater(token=TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('balance', balance))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    dispatcher.add_handler(MessageHandler(Filters.text, messages))
    updater.start_polling()


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='No entiendo ese comando...')


def messages(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='No te entiendo meu, solo entiendo los comandos...')


def start(update, context):
    log_command('start', update.effective_chat)
    if start_user_db(update.effective_chat.id) == 0:
        msg = "¡Bienvenido! Me llamo teixeBOT, creo que nos vamos a llevar bien."
    else:
        msg = "¡Tranquilo! Aún me acuerdo de ti..."
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


def balance(update, context):
    params = 'DENIED'
    if update.effective_chat.id == 678104316 or update.effective_chat.id == 1537367308:
        params = 'ACCEPTED'
        if not context.args:
            msg = get_balance()
            context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
        elif context.args[0] == 'background':
            try:
                if float(context.args[1]) > 10:
                    timer = context.args[1]
                else:
                    timer = 3600
            except ValueError:
                timer = 3600
            balance_background(update, context, timer)
            return
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Mi dinero no lo puedes ver, socio.')
    log_command('balance', update.effective_chat, params)
