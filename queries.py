# USER TABLE

create_user_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        chat_id INTEGER PRIMARY KEY,
        is_admin INTEGER NOT NULL DEFAULT 0
    );
"""

insert_user_sql = """
    INSERT INTO users(chat_id) VALUES (?);
"""

make_admin_sql = """
    UPDATE users SET is_admin = 1 WHERE chat_id = ?;
"""

select_user_sql = """
    SELECT chat_id, is_admin FROM users WHERE chat_id = ?;
"""

# WATCHPAIR TABLE

create_watchpair_table_sql = """
    CREATE TABLE IF NOT EXISTS watchpair (
        chat_id INTEGER,
        pair TEXT NOT NULL,
        refresh INTEGER NOT NULL,
        last_price REAL NOT NULL,
        last_send INTEGER NOT NULL,
        PRIMARY KEY (chat_id, pair),
        FOREIGN KEY(chat_id) REFERENCES users(chat_id)
    );
"""

insert_watchpair_sql = """
    INSERT INTO watchpair(chat_id, pair, refresh, last_price, last_send) VALUES (?,?,?,?,?);
"""

select_watchpair_sql = """
    SELECT chat_id, pair, refresh, last_price, last_send FROM watchpair WHERE chat_id = ? AND pair = ?;
"""

select_watchpairs_sql = """
    SELECT chat_id, pair, refresh, last_price, last_send FROM watchpair;
"""

select_watchpairs_from_user_sql = """
    SELECT chat_id, pair, refresh, last_price, last_send FROM watchpair WHERE chat_id = ?;
"""

delete_watchpair_sql = """
    DELETE FROM watchpair WHERE chat_id = ? AND pair = ?;
"""

update_watchpair_sql = """
    UPDATE watchpair SET last_price = ?, last_send = ? WHERE chat_id = ? AND pair = ?;
"""

# WATCHTRADE TABLE

create_watchtrade_table_sql = """
    CREATE TABLE IF NOT EXISTS watchtrade (
        chat_id INTEGER,
        pair TEXT NOT NULL,
        refresh INTEGER NOT NULL,
        last_price REAL NOT NULL,
        last_send INTEGER NOT NULL,
        enter_price REAL NOT NULL,
        last_warning REAL NOT NULL DEFAULT 1,
        alerts INTEGER NOT NULL DEFAULT 0,
        PRIMARY KEY (chat_id, pair),
        FOREIGN KEY(chat_id) REFERENCES users(chat_id)
    );
"""

insert_watchtrade_sql = """
    INSERT INTO watchtrade(chat_id, pair, refresh, last_price, last_send, enter_price) 
    VALUES (?,?,?,?,?,?);
"""

select_watchtrade_sql = """
    SELECT chat_id, pair, refresh, last_price, last_send, enter_price, last_warning, alerts
    FROM watchtrade WHERE chat_id = ? AND pair = ?;
"""

select_watchtrades_sql = """
    SELECT chat_id, pair, refresh, last_price, last_send, enter_price, last_warning, alerts FROM watchtrade;
"""

select_watchtrades_from_user_sql = """
    SELECT chat_id, pair, refresh, last_price, last_send, enter_price, last_warning, alerts 
    FROM watchtrade WHERE chat_id = ?;
"""

delete_watchtrade_sql = """
    DELETE FROM watchtrade WHERE chat_id = ? AND pair = ?;
"""

update_watchtrade_sql = """
    UPDATE watchtrade SET last_price = ?, last_send = ? WHERE chat_id = ? AND pair = ?;
"""


update_watchtrade_warning_sql = """
    UPDATE watchtrade SET last_warning = ? WHERE chat_id = ? AND pair = ?;
"""

update_watchtrade_alert_sql = """
    UPDATE watchtrade SET alerts = ? WHERE chat_id = ? AND pair = ?;
"""