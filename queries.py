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
