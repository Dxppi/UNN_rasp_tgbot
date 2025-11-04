import sqlite3
from domain.database import DatabaseInterface
from bot.config import DB_PATH


class DbSqlite(DatabaseInterface):
    """Реализация интерфейса БД на SQLite"""

    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self._create_table()

    def _create_table(self):
        """Создает таблицу если её нет"""
        connection = sqlite3.connect(self.db_path, timeout=5)
        with connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS user_groups (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER UNIQUE NOT NULL,
                    group_number TEXT NOT NULL,
                    group_id TEXT NOT NULL
                )
            """
            )

    def get_user_group(self, user_id):
        try:
            connection = sqlite3.connect(self.db_path, timeout=5)
            with connection:
                cursor = connection.cursor()
                cursor.execute(
                    "SELECT group_number, group_id FROM user_groups WHERE user_id = ?",
                    (user_id,),
                )
                result = cursor.fetchone()
                if result:
                    return {"group_number": result[0], "group_id": result[1]}
                return None
        except Exception as e:
            raise Exception(f"Ошибка при получении группы пользователя: {e}")

    def save_user_group(self, user_id, group_number, group_id):
        connection = sqlite3.connect(self.db_path, timeout=5)
        with connection:
            connection.execute(
                "INSERT OR REPLACE INTO user_groups (user_id, group_number, group_id) VALUES (?, ?, ?)",
                (user_id, group_number, group_id),
            )
