"""Хендлер для команды /today"""

from bot.handlers.handle import Handler
from bot.handler_result import HandlerStatus
from bot.handlers.schedule_helpers import get_moscow_time, send_schedule_to_user


class TodayHandler(Handler):
    """Обрабатывает команду /today"""

    def can_handle(self, update: dict, state, data: dict):
        """Проверяет, является ли сообщение командой /today или текстом кнопки"""
        return (
            "message" in update
            and "text" in update["message"]
            and (
                update["message"]["text"].strip() == "Сегодня"
                or update["message"]["text"].strip().startswith("/today")
            )
        )

    def handle(self, update: dict, state, data: dict, dispatcher):
        """Обрабатывает команду /today"""
        chat_id = update["message"]["chat"]["id"]
        group_id = data["group_id"]

        current_date = get_moscow_time().date()
        send_schedule_to_user(
            dispatcher.messenger,
            chat_id,
            group_id,
            current_date,
            current_date,
        )

        return HandlerStatus.STOP
