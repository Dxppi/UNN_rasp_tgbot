"""Хендлер для загрузки данных пользователя и проверки группы"""

from bot.handlers.handle import Handler
from bot.handler_result import HandlerStatus


class UserDataHandler(Handler):
    """Загружает данные пользователя из БД и проверяет наличие группы"""

    def can_handle(self, update: dict, state, data: dict):
        return True

    def handle(self, update: dict, state, data: dict, messenger, database):
        """Загружает данные пользователя из БД и проверяет группу"""
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

        if state == "WAITING_FOR_GROUP":
            return HandlerStatus.CONTINUE

        group_id = data.get("group_id")
        if group_id is None:
            if "message" in update and "text" in update["message"]:
                text = update["message"]["text"].strip()
                
                allowed_commands = ["/start", "/change", "/cancel", "/help"]
                commands_requiring_group = ["/today", "/tomorrow", "/week"]
                buttons_requiring_group = ["Сегодня", "Завтра", "Неделя"]
                
                is_command_requiring_group = any(
                    text.startswith(cmd) for cmd in commands_requiring_group
                )
                is_button_requiring_group = text in buttons_requiring_group
                is_allowed_command = any(
                    text.startswith(cmd) for cmd in allowed_commands
                )
                
                if is_command_requiring_group or is_button_requiring_group:
                    chat_id = update["message"]["chat"]["id"]
                    messenger.send_message(
                        chat_id,
                        "Сначала введите номер группы в /start"
                    )
                    return HandlerStatus.STOP
                elif not is_allowed_command and not text.startswith("/"):
                    chat_id = update["message"]["chat"]["id"]
                    messenger.send_message(
                        chat_id,
                        "Вас приветствует бот расписания ННГУ, введите номер группы",
                    )
                    data["state"] = "WAITING_FOR_GROUP"
                    return HandlerStatus.STOP

        return HandlerStatus.CONTINUE
