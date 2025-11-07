from bot.dispatcher import Dispatcher
from domain.messenger import Messenger


def start_long_polling(dispatcher: Dispatcher, messenger: Messenger):
    """Запускает Long Polling"""
    print("Бот запущен!")
    next_update_offset = 0

    try:
        while True:
            updates = messenger.get_updates(offset=next_update_offset, timeout=10)
            for update in updates:
                dispatcher.dispatch(update)
                next_update_offset = max(next_update_offset, update["update_id"]) + 1
                print(".", end="", flush=True)
    except KeyboardInterrupt:
        print("\nОстановка бота...")
