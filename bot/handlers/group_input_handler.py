"""Хендлер для ввода номера группы"""

from bot.handlers.handle import Handler
from bot.handler_result import HandlerStatus
from bot.keyboards import main_menu_keyboard
from bot.telegram_api import send_message
from parser.parseData import fetch_group_id


class GroupInputHandler(Handler):
    """Обрабатывает ввод номера группы пользователем"""

    def can_handle(self, update: dict, state, data: dict):
        """Проверяет, находится ли пользователь в состоянии ожидания группы"""
        return (
            state == "WAITING_FOR_GROUP"
            and "message" in update
            and "text" in update["message"]
            and not update["message"]["text"].strip().startswith("/")
        )

    def handle(self, update: dict, state, data: dict, dispatcher):
        """Обрабатывает ввод номера группы"""
        telegram_id = update["message"]["from"]["id"]
        chat_id = update["message"]["chat"]["id"]
        group_number = update["message"]["text"].strip()

        try:
            group_id = fetch_group_id(group_number)

            data["group_number"] = group_number
            data["group_id"] = group_id

            if dispatcher.database:
                dispatcher.database.save_user_group(telegram_id, group_number, group_id)

            send_message(
                chat_id,
                f"Номер группы '{group_number}' сохранен!\n",
                reply_markup=main_menu_keyboard(),
            )

            data["state"] = None

        except Exception as e:
            send_message(chat_id, f"Ошибка: {str(e)}\nПопробуйте ввести группу снова.")

        return HandlerStatus.STOP
