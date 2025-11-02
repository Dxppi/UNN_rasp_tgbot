"""Хендлер для команды /week"""

from datetime import timedelta
from bot.handlers.handle import Handler
from bot.handler_result import HandlerStatus
from bot.handlers.schedule_helpers import get_moscow_time, send_schedule_to_user


class WeekHandler(Handler):
    """Обрабатывает команду /week"""

    def can_handle(self, update: dict, state, data: dict):
        """Проверяет, является ли сообщение командой /week или текстом кнопки"""
        return (
            "message" in update
            and "text" in update["message"]
            and (
                update["message"]["text"].strip() == "Неделя"
                or update["message"]["text"].strip().startswith("/week")
            )
        )

    def handle(self, update: dict, state, data: dict, dispatcher):
        """Обрабатывает команду /week"""
        chat_id = update["message"]["chat"]["id"]
        group_id = data["group_id"]

        current_date = get_moscow_time().date()
        end_date = current_date + timedelta(days=7)
        send_schedule_to_user(
            chat_id,
            group_id,
            current_date,
            end_date,
        )

        return HandlerStatus.STOP
