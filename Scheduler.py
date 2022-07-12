from database import get_stage, set_stage, set_date_progress
import datetime
from dateutil.relativedelta import relativedelta


def schedule(user_id, word_id):
    stage = get_stage(user_id, word_id)

    # 1 3 7 15 30 365
    x = 100
    days = 0
    if stage == 0:
        x = 1
        days = 2
    elif stage == 1:
        x = 2
        days = 6
    elif stage == 2:
        x = 3
        days = 14
    elif stage == 3:
        x = 4
        days = 29
    elif stage == 4:
        x = 5
        days = 89
    elif stage == 5:
        x = 6
        days = 264
    set_stage(user_id, word_id, x)

    date = datetime.datetime.now()
    date = date + datetime.timedelta(days=days)

    set_date_progress(user_id, word_id, date)


def never(user_id, word_id):
    set_stage(user_id, word_id, 100)

    date = datetime.datetime.now()
    date = date + relativedelta(years=100)

    set_date_progress(user_id, word_id, date)