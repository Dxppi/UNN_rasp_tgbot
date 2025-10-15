import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()


def recreateDatabase() -> None:
    con = sqlite3.connect(os.getenv("DB_PATH"), timeout=5)
    with con:
        con.execute("DROP TABLE IF EXISTS user_groups")
        con.execute("""
            CREATE TABLE IF NOT EXISTS user_groups
            (
                id INTEGER PRIMARY KEY,
                user_id INTEGER UNIQUE NOT NULL,
                group_number TEXT NOT NULL,
                group_id TEXT NOT NULL
            )
        """)


def persistUpdates(updates: list) -> None:
    connection = sqlite3.connect(os.getenv("DB_PATH"), timeout=5)

    with connection:
        data = []
        for update in updates:
            data.append(
                (update['user_id'], update['group_number'], update['group_id']))

        connection.executemany(
            "INSERT INTO user_groups (user_id, group_number, group_id) VALUES (?, ?, ?)", data)
