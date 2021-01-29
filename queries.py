create_user_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        chat_id INTEGER PRIMARY KEY
    );
"""

insert_user_sql = """
    INSERT INTO users(chat_id) VALUES (?);
"""

select_user_sql = """
    SELECT chat_id FROM users WHERE chat_id = ?;
"""