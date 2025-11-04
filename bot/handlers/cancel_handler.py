"""Хендлер для команды /cancel"""

from bot.handlers.handle import Handler
from bot.handler_result import HandlerStatus
from bot.keyboards import remove_keyboard


class CancelHandler(Handler):
    """Обрабатывает команду /cancel"""

    def can_handle(self, update: dict, state, data: dict):
        """Проверяет, является ли сообщение командой /cancel"""
        return (
            "message" in update
            and "text" in update["message"]
            and update["message"]["text"].strip().startswith("/cancel")
        )

    def handle(self, update: dict, state, data: dict, dispatcher):
        """Обрабатывает команду /cancel"""
        chat_id = update["message"]["chat"]["id"]

        dispatcher.messenger.send_message(
            chat_id,
            "Диалог отменен. Используй /start чтобы начать заново.",
            reply_markup=remove_keyboard(),
        )
        data["state"] = None

        return HandlerStatus.STOP
