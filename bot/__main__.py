from bot.dispatcher import Dispatcher
from bot.longpolling import start_long_polling
from infrastructure.db_sqlite import DbSqlite
from infrastructure.messenger_telegram import MessengerTelegram
from bot.handlers import get_handlers


def main():
    db = DbSqlite()
    messenger = MessengerTelegram()
    dispatcher = Dispatcher(db, messenger)
    dispatcher.add_handlers(*get_handlers())
    start_long_polling(dispatcher, messenger)


if __name__ == "__main__":
    main()
