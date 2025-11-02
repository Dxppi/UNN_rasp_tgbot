from bot.dispatcher import Dispatcher
from bot.longpolling import start_long_polling
from db.sqlite_database import SQLiteDatabase
from bot.handlers import get_handlers


def main():
    db = SQLiteDatabase()
    dispatcher = Dispatcher(db)
    dispatcher.add_handlers(*get_handlers())
    start_long_polling(dispatcher)


if __name__ == "__main__":
    main()
