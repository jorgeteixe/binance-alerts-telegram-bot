import logging
import sqlite3

from queries import *

DATABASE = 'data.db'


def create_user_table():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute(create_user_table_sql)
        conn.commit()


def create_watchpairs_table():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute(create_watchpair_table_sql)
        conn.commit()


def create_tables():
    create_watchpairs_table()
    create_user_table()


def init_db():
    create_tables()


def start_user_db(user_id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        value = cursor.execute(select_user_sql, (user_id,)).fetchone()
        if value is None:
            cursor.execute(insert_user_sql, (user_id,))
            logging.info('id=' + str(user_id) + ' added to database')
            return True
        return False


def make_admin_db(user_id):
    with sqlite3.connect(DATABASE) as conn:
        conn.execute(make_admin_sql, (user_id,))
        logging.info('id=' + str(user_id) + ' is now admin.')


def is_admin_db(user_id):
    with sqlite3.connect(DATABASE) as conn:
        value = conn.execute(select_user_sql, (user_id,)).fetchone()
        return bool(value[1])


def save_watchpair(watchpair):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        value = cursor.execute(select_watchpair_sql, (watchpair[0], watchpair[1])).fetchone()
        if value is None:
            cursor.execute(insert_watchpair_sql, watchpair)
            logging.info('id=' + str(watchpair[0]) + ' added ' + watchpair[1] + ' to his watchpairs')
            return True
        return False


def delete_watchpair(chat_id, pair):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        value = cursor.execute(select_watchpair_sql, (chat_id, pair)).fetchone()
        if value:
            cursor.execute(delete_watchpair_sql, (chat_id, pair))
            logging.info('id=' + str(chat_id) + ' deleted ' + str(pair) + ' from his watchpairs')
            return True
        return False


def get_watchpairs():
    with sqlite3.connect(DATABASE) as conn:
        return conn.execute(select_watchpairs_sql).fetchall()


def update_watchpair(w):
    with sqlite3.connect(DATABASE) as conn:
        conn.execute(update_watchpair_sql, (w[3], w[4], w[0], w[1]))


def get_watchpairs_from_user(user_id):
    with sqlite3.connect(DATABASE) as conn:
        return conn.execute(select_watchpairs_from_user_sql, (user_id,)).fetchall()
