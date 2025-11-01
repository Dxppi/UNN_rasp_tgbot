from datetime import timedelta
from bot.dispatcher import Update, Context
from bot.handlers.commands import get_moscow_time, send_schedule, get_user_group_from_db


def _build_help_text(group_number: str = None) -> str:
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


def handle_help_command(update: Update, context: Context):
    user_id = update.user_id
    chat_id = update.chat_id
    user_data = context.get_user_data(user_id)
    group_number = user_data.get("group_number")

    if not group_number:
        group_data = get_user_group_from_db(user_id)
        if group_data:
            group_number = group_data["group_number"]

    help_text = _build_help_text(group_number)
    context.telegram_api.send_message(chat_id, help_text, parse_mode="Markdown")


def handle_button_text(update: Update, context: Context):
    text = update.text.strip()
    chat_id = update.chat_id
    user_id = update.user_id
    user_data = context.get_user_data(user_id)

    if "group_id" not in user_data:
        group_data = get_user_group_from_db(user_id)
        if group_data:
            user_data["group_number"] = group_data["group_number"]
            user_data["group_id"] = group_data["group_id"]
        else:
            context.telegram_api.send_message(
                chat_id, "Сначала установите группу с помощью команды /start"
            )
            return

    current_time = get_moscow_time()

    if text == "Сегодня":
        date = current_time.date()
        send_schedule(update, context, date, date)
    elif text == "Завтра":
        tomorrow = (current_time + timedelta(days=1)).date()
        send_schedule(update, context, tomorrow, tomorrow)
    elif text == "Неделя":
        current_date = current_time.date()
        send_schedule(update, context, current_date, current_date + timedelta(days=7))
    elif text == "Помощь":
        handle_help_command(update, context)
    else:
        context.telegram_api.send_message(chat_id, "Неизвестная команда")
