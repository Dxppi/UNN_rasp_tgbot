from bot.handlers.handle import Handler
from bot.handler_result import HandlerStatus
from db.database_interface import DatabaseInterface


class Dispatcher:
    def __init__(self, database: DatabaseInterface):
        """Инициализирует диспетчер с базой данных"""
        self.database = database
        self._handlers = []
        self._user_states = {}

    def add_handlers(self, *handlers: Handler):
        """Добавляет хендлеры в цепочку обработки"""
        for handler in handlers:
            self._handlers.append(handler)

    def dispatch(self, update: dict):
        """Обрабатывает обновление через цепочку хендлеров"""
        telegram_id = None
        if "message" in update:
            telegram_id = update["message"]["from"]["id"]
        elif "callback_query" in update:
            telegram_id = update["callback_query"]["from"]["id"]

        if not telegram_id:
            return

        user_state = self._user_states.get(telegram_id)
        user_data = {}

        for handler in self._handlers:
            if handler.can_handle(update, user_state, user_data):
                result = handler.handle(update, user_state, user_data, self)

                if "state" in user_data:
                    new_state = user_data["state"]
                    if new_state is None:
                        self._user_states.pop(telegram_id, None)
                    else:
                        self._user_states[telegram_id] = new_state

                if result == HandlerStatus.STOP:
                    break
