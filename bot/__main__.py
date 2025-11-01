from bot.config import BOT_TOKEN
from bot.telegram_api import TelegramAPI
from bot.dispatcher import Dispatcher, State
from bot.longpolling import LongPolling
from bot.handlers.commands import (
    start_command,
    change_command,
    today_command,
    tomorrow_command,
    week_command,
    handle_group_input,
    cancel,
    set_database,
)
from bot.handlers.text_actions import handle_button_text
from db.sqlite_database import SQLiteDatabase


def main() -> None:
    db = SQLiteDatabase()
    set_database(db)

    telegram_api = TelegramAPI(BOT_TOKEN)
    dispatcher = Dispatcher(telegram_api)

    dispatcher.register_command("start", start_command)
    dispatcher.register_command("change", change_command)
    dispatcher.register_command("today", today_command)
    dispatcher.register_command("tomorrow", tomorrow_command)
    dispatcher.register_command("week", week_command)
    dispatcher.register_command("cancel", cancel)
    dispatcher.register_state_handler(State.WAITING_FOR_GROUP, handle_group_input)
    dispatcher.register_message_handler(handle_button_text)

    long_polling = LongPolling(telegram_api, dispatcher)
    long_polling.start()


if __name__ == "__main__":
    main()
