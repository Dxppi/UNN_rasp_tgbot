import time
from bot.telegram_api import TelegramAPI
from bot.dispatcher import Dispatcher, Update


class LongPolling:
    def __init__(self, telegram_api: TelegramAPI, dispatcher: Dispatcher):
        self.telegram_api = telegram_api
        self.dispatcher = dispatcher
        self.last_update_id = 0
        self.running = False

    def start(self):
        """Запускает Long Polling"""
        self.running = True
        print("Бот запущен!")

        while self.running:
            try:
                offset = self.last_update_id + 1 if self.last_update_id > 0 else None
                updates = self.telegram_api.get_updates(offset=offset, timeout=5)

                for update_data in updates:
                    try:
                        update = Update(update_data)
                        self.dispatcher.process_update(update)
                        self.last_update_id = max(self.last_update_id, update.update_id)
                    except Exception as e:
                        print(f"Ошибка при обработке обновления: {e}")
                        if "update_id" in update_data:
                            self.last_update_id = max(
                                self.last_update_id, update_data["update_id"]
                            )
            except KeyboardInterrupt:
                print("\nОстановка бота...")
                self.stop()
                break
            except Exception as e:
                print(f"Ошибка при получении обновлений: {e}")
                time.sleep(2)

    def stop(self):
        """Останавливает Long Polling"""
        self.running = False
