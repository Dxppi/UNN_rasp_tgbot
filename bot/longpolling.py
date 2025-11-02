from bot.telegram_api import get_updates
from bot.dispatcher import Dispatcher


def start_long_polling(dispatcher: Dispatcher):
    """Запускает Long Polling"""
    print("Бот запущен!")
    next_update_offset = 0

    try:
        while True:
            offset = next_update_offset if next_update_offset > 0 else None
            updates = get_updates(offset=offset, timeout=5)

            for update in updates:
                dispatcher.dispatch(update)
                next_update_offset = max(
                    next_update_offset, update.get("update_id", 0) + 1
                )
                print(".", end="", flush=True)
    except KeyboardInterrupt:
        print("\nОстановка бота...")
