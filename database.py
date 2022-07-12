import enum
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Boolean, Text, String, DateTime, Enum, ForeignKey, select, func, update
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
import datetime
import preprocessing
import copy


# engine = create_engine('sqlite:///:memory:', echo=False)
engine = create_engine('sqlite:///db.db', echo=True)
Base = declarative_base()


class Status(enum.Enum):
   dont_remind_me_again = 0
   remind_me_later = 1
   for_next_session = 2


class User(Base):
   __tablename__ = 'user'

   id = Column(Integer, primary_key=True, autoincrement=True)
   username = Column(String(128))


class Word(Base):
   __tablename__ = 'word'

   id = Column(Integer, primary_key=True, autoincrement=True)
   word = Column(String(128))
   pronunciation = Column(String(128))
   translation = Column(Text)
   example = Column(Text)
   details = Column(Text)
   level = Column(String(10))


class Progress(Base):
   __tablename__ = 'progress'

   id = Column(Integer, primary_key=True, autoincrement=True)
   user_id = Column(Integer, ForeignKey('user.id'))
   word_id = Column(Integer, ForeignKey('word.id'))
   status = Column(Enum(Status))
   date = Column(DateTime, default=datetime.datetime.now)
   stage = Column(Integer)
   permit = Column(Boolean)
   level = Column(String(10))
   user = relationship('User')
   word = relationship('Word')


Base.metadata.create_all(engine)


def get_date(days=0):
   d = datetime.datetime.now()
   d += datetime.timedelta(days=days)
   return d


def fill_word_table():
    data = preprocessing.main()
    session = sessionmaker(bind=engine)()

    for d in data:
        word = d
        translation = data[d]

        _ = Word(word=word, translation=translation)
        session.add(_)
    session.commit()
    session.close()


def add_word(word, translation, level):
    session = sessionmaker(bind=engine)()

    _ = Word(word=word, translation=translation, level=level)
    session.add(_)
    session.commit()
    session.close()


def fill_word_table_2():
    data = preprocessing.main2()
    session = sessionmaker(bind=engine)()

    columns = data.columns

    for index, row in data.iterrows():
        try:

            # A2, B2
            word = row[columns[2]]
            pronunciation = ''
            translation = row[columns[0]]
            example = ''
            level = 'B2'
            details = ''

            # B1
            # word = row[columns[6]]
            # pronunciation = ''
            # translation = row[columns[0]]
            # example = ''
            # level = 'B1'
            # details = ''

            print('&' * 10000)
            print(word)
            print(pronunciation)
            print(translation)
            print(example)

            _ = Word(word=word, pronunciation=pronunciation, translation=translation, example=example, details=details,
                     level=level)
            session.add(_)
        except:
            pass
    session.commit()
    session.close()


def create_user():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    u = User(username='sina')
    session.add(u)
    session.commit()
    user = u.id
    session.close()

    return user


def fill_progress_table():
    status = Status.remind_me_later
    current_date = get_date()
    next_date = get_date(days=3)

    u = create_user()

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    all_words = session.query(Word).all()

    for i in all_words:
        p = Progress(user_id=u, word_id=i.id, status=status, current_date=current_date, next_date=next_date)
        session.add(p)

    session.commit()
    session.close()


def read_words_yield():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    all_words = session.query(Word).all()

    for i in all_words:
        yield i.word

    session.close()


def make_decision(user_id, word_id, new_status):
    session = sessionmaker(bind=engine)()

    session.query(Progress).filter(Progress.word_id == word_id, Progress.user_id == user_id).\
        update({"status": Status(int(new_status))}, synchronize_session="fetch")
    session.commit()
    # print('1' * 1000)
    # _ = select(Progress).where(Progress.word_id == word_id)
    # _ = session.execute(_).fetchall()
    # print(_[0][0].status)

    session.close()


def update_translation(word_id, details):
    session = sessionmaker(bind=engine)()

    session.query(Word).filter(Word.id == word_id).\
        update({"details": details}, synchronize_session="fetch")
    session.commit()

    session.close()


def get_translation(word_id):
    session = sessionmaker(bind=engine)()

    std = select(Word.translation).where(Word.id == word_id)
    _ = session.execute(std).fetchall()

    session.close()

    return _[0][0]


def get_all_words():
    session = sessionmaker(bind=engine)()
    std = select(Word)
    words = session.execute(std).fetchall()
    session.close()

    return words


def get_count(user_id=1):

    date = datetime.datetime.now()

    session = sessionmaker(bind=engine)()
    count = session.query(func.count(Progress.id)).filter(Progress.user_id == user_id, Progress.date < date).all()

    count = count[0][0]
    session.close()

    return count


def get_stage(user_id, word_id):
    session = sessionmaker(bind=engine)()
    stage = session.query(Progress.stage).filter(Progress.user_id == user_id, Progress.word_id == word_id).all()

    stage = stage[0][0]

    session.close()

    return stage


def set_stage(user_id, word_id, stage):
    session = sessionmaker(bind=engine)()

    session.query(Progress).filter(Progress.user_id == user_id, Progress.word_id == word_id). \
        update({"stage": stage}, synchronize_session="fetch")
    session.commit()

    session.close()


def set_date_progress(user_id, word_id, date):
    session = sessionmaker(bind=engine)()

    session.query(Progress).filter(Progress.user_id == user_id, Progress.word_id == word_id). \
        update({"date": date}, synchronize_session="fetch")
    session.commit()

    session.close()


def revert_backup():
    engine_old = create_engine('sqlite:///backup/db.db', echo=True)
    session_old = sessionmaker(bind=engine_old)()

    std = select(Word)
    words = session_old.execute(std).fetchall()

    print(words[0][0].translation)

    session = sessionmaker(bind=engine)()

    for word in words:
        w = word[0].word
        t = word[0].translation
        l = word[0].level

        _ = Word(word=w, pronunciation='', translation=t, example='', details='', level=l)
        session.add(_)

    session.commit()

    session.close()
    session_old.close()


def fill_word_date(user_id):
    session = sessionmaker(bind=engine)()

    date = datetime.datetime.now()

    session.query(Progress).filter(Progress.user_id == user_id).update({"date": date}, synchronize_session="fetch")
    session.commit()
    # print('1' * 1000)
    # _ = select(Progress).where(Progress.word_id == word_id)
    # _ = session.execute(_).fetchall()
    # print(_[0][0].status)

    session.close()


def fill_progress_table_2(user_id):

    date = datetime.datetime.now()

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    all_words = session.query(Word).all()

    for i in all_words:
        p = Progress(user_id=user_id, word_id=i.id, date=date, stage=0, level=i.level)
        session.add(p)

    session.commit()
    session.close()


def check_new(user_id):
    session = sessionmaker(bind=engine)()

    status = session.query(Progress).filter(Progress.user_id == user_id).first()
    if status is None:
        fill_progress_table_2(user_id)


def set_level(user_id, level):
    session = sessionmaker(bind=engine)()

    # session.query(Progress).join(Progress.word).join(Word).filter(Progress.user_id == user_id, Progress.word.level == level). \
    #     update({"permit": True}, synchronize_session="fetch")

    session.query(Progress).filter(Progress.user_id == user_id, Progress.level == level). \
        update({"permit": True}, synchronize_session="fetch")

    # session.query(Progress).join(Progress.word).join(Word).filter(Progress.user_id == user_id,
    #                                                               Progress.word.level == level)

    session.commit()


def main():
    fill_word_table()
    fill_progress_table()


def main2():
    #preprocessing.main2()
    #fill_word_table_2()
    pass


if __name__ == '__main__':
    main2()
    revert_backup()
    # fill_word_date()
    pass