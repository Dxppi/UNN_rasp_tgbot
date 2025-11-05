import os
from dotenv import load_dotenv

load_dotenv(override=False)

BOT_TOKEN = os.getenv("TOKEN")
if not BOT_TOKEN:
    raise ValueError("Не найден токен в переменных окружения")

DB_PATH = os.getenv("DB_PATH", "database.sqlite")
MESSAGE_DELAY = 0.1
MAX_MESSAGE_SIZE = 1000
