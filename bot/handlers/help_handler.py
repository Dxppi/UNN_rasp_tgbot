"""Хендлер для команды /help"""

from bot.handlers.handle import Handler
from bot.handler_result import HandlerStatus
from bot.telegram_api import send_message


def build_help_text(group_number=None):
    """Формирует текст справки"""
    help_text = "*Помощь*\n\n"

    if group_number:
        help_text += f"*Ваша группа:* {group_number}\n\n"
    else:
        help_text += "Группа не установлена. Используйте /start\n\n"

    commands = [
        "/start - установить или восстановить группу",
        "/change - изменить группу",
        "/today - расписание на сегодня",
        "/tomorrow - расписание на завтра",
        "/week - расписание на неделю",
        "/cancel - отменить операцию",
    ]

    help_text += "*Команды:*\n" + "\n".join(commands) + "\n\n"
    help_text += "*Кнопки:*\n"
    help_text += "• Сегодня, Завтра, Неделя - расписание\n"
    help_text += "• Помощь - эта справка"

    return help_text


class HelpHandler(Handler):
    """Обрабатывает команду /help"""

    def can_handle(self, update: dict, state, data: dict):
        """Проверяет, является ли сообщение командой /help или текстом кнопки"""
        return (
            "message" in update
            and "text" in update["message"]
            and (
                update["message"]["text"].strip() == "Помощь"
                or update["message"]["text"].strip().startswith("/help")
            )
        )

    def handle(self, update: dict, state, data: dict, dispatcher):
        """Обрабатывает команду /help"""
        chat_id = update["message"]["chat"]["id"]
        group_number = data.get("group_number")

        help_text = build_help_text(group_number)
        send_message(chat_id, help_text, parse_mode="Markdown")

        return HandlerStatus.STOP
