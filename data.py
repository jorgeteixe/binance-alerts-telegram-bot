import sqlite3
import logging
from queries import *


def create_user_table():
    with sqlite3.connect('data.db') as conn:
        conn.execute(create_user_table_sql)
        conn.commit()


def create_coin_table():
    pass


def create_tables():
    create_coin_table()
    create_user_table()


def init_db():
    create_tables()


def start_user_db(user_id):
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        value = cursor.execute(select_user_sql, (user_id,)).fetchone()
        if value is None:
            cursor.execute(insert_user_sql, (user_id,))
            logging.info('Added chat_id=' + str(user_id) + ' to data.db')
            return 0
        return 1
