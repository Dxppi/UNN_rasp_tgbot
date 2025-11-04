"""Хендлер для проверки наличия группы и блокировки команд"""

from bot.handlers.handle import Handler
from bot.handler_result import HandlerStatus


class GroupGuardHandler(Handler):
    """Проверяет наличие группы и блокирует команды без группы"""

    _COMMANDS_WITHOUT_GROUP = {"/start", "/change", "/cancel", "/help"}
    _SCHEDULE_BUTTONS = {"Сегодня", "Завтра", "Неделя"}
    _ALLOWED_BUTTONS = {"Помощь"}

    def can_handle(self, update: dict, state, data: dict):
        return True

    def handle(self, update: dict, state, data: dict, messenger, database):
        """Проверяет группу и блокирует команды без группы"""
        group_id = data.get("group_id")

        if group_id is not None:
            return HandlerStatus.CONTINUE

        if "message" not in update or "text" not in update["message"]:
            return HandlerStatus.CONTINUE

        text = update["message"]["text"].strip()
        chat_id = update["message"]["chat"]["id"]

        is_command = text.startswith("/")
        is_allowed_command = any(
            text.startswith(cmd) for cmd in self._COMMANDS_WITHOUT_GROUP
        )
        is_schedule_button = text in self._SCHEDULE_BUTTONS
        is_allowed_button = text in self._ALLOWED_BUTTONS

        if is_schedule_button or (is_command and not is_allowed_command):
            messenger.send_message(chat_id, "Сначала введите номер группы в /start")
            return HandlerStatus.STOP

        if state != "WAITING_FOR_GROUP" and not is_command and not is_allowed_button:
            messenger.send_message(
                chat_id,
                "Вас приветствует бот расписания ННГУ, введите номер группы",
            )
            data["state"] = "WAITING_FOR_GROUP"
            return HandlerStatus.STOP

        return HandlerStatus.CONTINUE
