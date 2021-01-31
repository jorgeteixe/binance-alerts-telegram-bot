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


def create_watchtrades_table():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute(create_watchtrade_table_sql)
        conn.commit()


def create_tables():
    create_watchpairs_table()
    create_watchtrades_table()
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


def save_watchtrade(watchtrade):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        value = cursor.execute(select_watchtrade_sql, (watchtrade[0], watchtrade[1])).fetchone()
        if value is None:
            cursor.execute(insert_watchtrade_sql, watchtrade)
            logging.info('id=' + str(watchtrade[0]) + ' added ' + watchtrade[1] + ' to his watchtrades')
            return True
        return False


def delete_watchtrade(chat_id, pair):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        value = cursor.execute(select_watchtrade_sql, (chat_id, pair)).fetchone()
        if value:
            cursor.execute(delete_watchtrade_sql, (chat_id, pair))
            logging.info('id=' + str(chat_id) + ' deleted ' + str(pair) + ' from his watchtrades')
            return True
        return False


def get_watchtrades():
    with sqlite3.connect(DATABASE) as conn:
        return conn.execute(select_watchtrades_sql).fetchall()


def update_watchtrade(w):
    with sqlite3.connect(DATABASE) as conn:
        conn.execute(update_watchtrade_sql, (w[3], w[4], w[0], w[1]))


def update_watchtrade_warning(w):
    with sqlite3.connect(DATABASE) as conn:
        conn.execute(update_watchtrade_sql, (w[3], w[4], w[6], w[0], w[1]))


def get_watchtrades_from_user(user_id):
    with sqlite3.connect(DATABASE) as conn:
        return conn.execute(select_watchtrades_from_user_sql, (user_id,)).fetchall()


def update_alerting_watchtrade(chat_id, pair, alerting):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        value = cursor.execute(select_watchtrade_sql, (chat_id, pair)).fetchone()
        if value and value[7] != alerting:
            cursor.execute(update_watchtrade_alert_sql, (alerting, chat_id, pair))
            logging.info('id=' + str(chat_id) + ' deleted ' + str(pair) + ' from his watchtrades')
            return True
        return False
