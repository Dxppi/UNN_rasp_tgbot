from bot.dispatcher import Dispatcher
from domain.messenger import Messenger


def start_long_polling(dispatcher: Dispatcher, messenger: Messenger):
    """Запускает Long Polling"""
    print("Бот запущен!")
    next_update_offset = 0

    try:
        while True:
            offset = next_update_offset if next_update_offset > 0 else None
            updates = messenger.get_updates(offset=offset, timeout=5)

            for update in updates:
                dispatcher.dispatch(update)
                next_update_offset = max(
                    next_update_offset, update.get("update_id", 0) + 1
                )
                print(".", end="", flush=True)
    except KeyboardInterrupt:
        print("\nОстановка бота...")
