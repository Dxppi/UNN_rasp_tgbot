"""Хендлер для команды /tomorrow"""

from datetime import timedelta
from bot.handlers.handle import Handler
from bot.handler_result import HandlerStatus
from bot.handlers.schedule_helpers import get_moscow_time, send_schedule_to_user


class TomorrowHandler(Handler):
    """Обрабатывает команду /tomorrow"""

    def can_handle(self, update: dict, state, data: dict):
        """Проверяет, является ли сообщение командой /tomorrow или текстом кнопки"""
        return (
            "message" in update
            and "text" in update["message"]
            and (
                update["message"]["text"].strip() == "Завтра"
                or update["message"]["text"].strip().startswith("/tomorrow")
            )
        )

    def handle(self, update: dict, state, data: dict, messenger, database):
        """Обрабатывает команду /tomorrow"""
        chat_id = update["message"]["chat"]["id"]
        group_id = data["group_id"]

        tomorrow = (get_moscow_time() + timedelta(days=1)).date()
        send_schedule_to_user(
            messenger,
            chat_id,
            group_id,
            tomorrow,
            tomorrow,
        )

        return HandlerStatus.STOP
