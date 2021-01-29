import logging
from telegram.ext import Updater, CommandHandler
from telegram.ext import MessageHandler, Filters


def start_bot(TELEGRAM_TOKEN):
    updater = Updater(token=TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('doge', doge))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    dispatcher.add_handler(MessageHandler(Filters.text, messages))
    updater.start_polling()


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='No entiendo ese comando...')


def messages(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='No te entiendo meu, solo entiendo los comandos...')


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Soy teixeBOT, en que puedo ayudarte!")
    logging.info('/start from id=' + str(update.effective_chat.id) + ' (' + str(update.effective_chat.username) + ')')


def doge(update, context):
    pass
