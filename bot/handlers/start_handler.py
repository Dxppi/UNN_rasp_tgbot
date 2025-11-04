"""Хендлер для команды /start"""

from bot.handlers.handle import Handler
from bot.handler_result import HandlerStatus
from bot.keyboards import main_menu_keyboard


class StartHandler(Handler):
    """Обрабатывает команду /start"""

    def can_handle(self, update: dict, state, data: dict):
        """Проверяет, является ли сообщение командой /start"""
        return (
            "message" in update
            and "text" in update["message"]
            and update["message"]["text"].strip().startswith("/start")
        )

    def handle(self, update: dict, state, data: dict, messenger, database):
        """Обрабатывает команду /start"""
        chat_id = update["message"]["chat"]["id"]
        group_id = data.get("group_id")

        if group_id:
            group_number = data["group_number"]
            messenger.send_message(
                chat_id,
                f"Добро пожаловать! Ваша группа: {group_number}",
                reply_markup=main_menu_keyboard(),
            )
            data["state"] = None
        else:
            messenger.send_message(
                chat_id, "Вас приветствует бот расписания ННГУ, введите номер группы"
            )
            data["state"] = "WAITING_FOR_GROUP"

        return HandlerStatus.STOP
