import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import KeyboardButton, ReplyKeyboardMarkup
import processing
import database
from sqlalchemy.sql.expression import func
from sqlalchemy import or_
from sqlalchemy.orm import sessionmaker
import database
from colorama import init, Fore, Back, Style
import processing
import variables
import Scheduler


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

levels = ['A1', 'A2', 'B1', 'B2', 'C1']


def start(update, context):
    user_id = update.message.from_user['id']
    database.check_new(user_id)

    msg = 'Please Choose a Level'
    btns = [[KeyboardButton('A1'), KeyboardButton('A2'), KeyboardButton('B1'), KeyboardButton('B2'), KeyboardButton('C1')]]

    context.bot.send_message(chat_id=update.effective_chat.id, text=msg, reply_markup=ReplyKeyboardMarkup(btns))


def help(update, context):
    update.message.reply_text('Help!')


def choose_1000():
    for i in range(500):
        processing.start(1)
        word_id = variables.active_words.get(1, -1)
        database.make_decision(1, word_id, 2)


def message(update, context):
    txt = update.message.text
    user_id = update.message.from_user['id']

    for level in levels:
        if txt == level:
            database.set_level(user_id, txt)

    btns = [[KeyboardButton('Never'), KeyboardButton('Again'), KeyboardButton('Next'), KeyboardButton('Show'), KeyboardButton('Counter')]]


    decision = -1

    if txt.lower() == 'never':
        decision = 0
    elif txt.lower() == 'again':
        decision = 1
    elif txt.lower() == 'next':
        decision = 2

    word_id = variables.active_words.get(user_id, -1)

    if word_id != -1:
        if txt.lower() == 'show':
            btns = [[KeyboardButton('.Continue'), KeyboardButton('.Next')]]
            word_id = variables.active_words.get(user_id, )
            translation = database.get_translation(word_id=word_id)
            context.bot.send_message(chat_id=update.effective_chat.id, text=translation, reply_markup=ReplyKeyboardMarkup(btns))
            return
        elif txt.lower() == 'counter':
            count = database.get_count(user_id)
            btns = [[KeyboardButton('Continue')]]
            context.bot.send_message(chat_id=update.effective_chat.id, text=count,
                                     reply_markup=ReplyKeyboardMarkup(btns))
            return
        elif txt.lower() == '.next':
            Scheduler.schedule(user_id, word_id)
        elif txt.lower() == 'never':
            Scheduler.never(1, word_id, decision)
    msg = processing.start(user_id)

    context.bot.send_message(chat_id=update.effective_chat.id, text=msg, reply_markup=ReplyKeyboardMarkup(btns))


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater("5196319726:AAFe6I8vXQo7vN8N_LHAxBjuM9aADAOgGVE", use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(MessageHandler(Filters.text, message))
    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
    # choose_1000()