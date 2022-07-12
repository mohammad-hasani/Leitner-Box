from sqlalchemy.sql.expression import func
from sqlalchemy import or_
from sqlalchemy.orm import sessionmaker
import database
from colorama import init, Fore, Back, Style
from variables import active_words
import datetime


def start(user_id=1):
    session = sessionmaker(bind=database.engine)()

    date = datetime.datetime.now()

    data = session.query(database.Progress).filter(database.Progress.date < date, database.Progress.permit == True).order_by(func.random()).first()

    if not data:
        message = "Done"
    else:
        message = data.word.word + '\n'
        active_words[user_id] = data.word.id
    # message += '0: Don\' Remind Me Again \n'
    # message += '1: Remind Me Later \n'
    # message += '2: For Next \n'

    # print(Style.RESET_ALL)
    # print(data.word.word + ':')
    # print(Fore.GREEN + "0: " + Fore.WHITE + str(database.Status.dont_remind_me_again))
    # print(Fore.GREEN + "1: " + Fore.WHITE + str(database.Status.remind_me_later))
    # print(Fore.GREEN + "2: " + Fore.WHITE + str(database.Status.for_next_session))
    # x = input()
    # print(Fore.LIGHTBLACK_EX + data.word.translation)
    # print(Style.RESET_ALL + '-' * 100)

    return message


def set_level():
    pass


if __name__ == '__main__':
    start()




