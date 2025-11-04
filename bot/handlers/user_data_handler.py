"""Хендлер для загрузки данных пользователя"""

from bot.handlers.handle import Handler
from bot.handler_result import HandlerStatus


class UserDataHandler(Handler):
    """Загружает данные пользователя из БД"""

    def can_handle(self, update: dict, state, data: dict):
        return True

    def handle(self, update: dict, state, data: dict, messenger, database):
        """Загружает данные пользователя из БД"""
        telegram_id = None
        if "message" in update:
            telegram_id = update["message"]["from"]["id"]
        elif "callback_query" in update:
            telegram_id = update["callback_query"]["from"]["id"]

        if not telegram_id:
            return HandlerStatus.STOP

        if database:
            group_data = database.get_user_group(telegram_id)
            if group_data:
                data["group_number"] = group_data["group_number"]
                data["group_id"] = group_data["group_id"]

        return HandlerStatus.CONTINUE
