"""Хендлер для команды /change"""

from bot.handlers.handle import Handler
from bot.handler_result import HandlerStatus
from bot.telegram_api import send_message


class ChangeHandler(Handler):
    """Обрабатывает команду /change для изменения группы"""

    def can_handle(self, update: dict, state, data: dict):
        """Проверяет, является ли сообщение командой /change"""
        return (
            "message" in update
            and "text" in update["message"]
            and update["message"]["text"].strip().startswith("/change")
        )

    def handle(self, update: dict, state, data: dict, dispatcher):
        """Обрабатывает команду /change"""
        chat_id = update["message"]["chat"]["id"]

        data["state"] = "WAITING_FOR_GROUP"
        send_message(chat_id, "Введите новый номер группы")

        return HandlerStatus.STOP
