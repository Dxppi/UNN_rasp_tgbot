import time
from typing import Tuple
from datetime import datetime, timedelta
from bot.dispatcher import Update, Context, State
from bot.config import (
    CONVERSATION_END,
    MAX_MESSAGE_SIZE,
    MESSAGE_DELAY,
)
from parser.parseData import (
    fetch_group_id,
    make_schedule,
    fetch_schedule,
    split_schedule_by_size,
)
from bot.keyboards import main_menu_keyboard, remove_keyboard
from db.database_interface import DatabaseInterface


database: DatabaseInterface = None


def set_database(db: DatabaseInterface):
    """Устанавливает базу данных для использования в handlers"""
    global database
    database = db


def get_user_group_from_db(user_id: int):
    """Получает группу пользователя из БД"""
    return database.get_user_group(user_id) if database else None


def require_group(func):
    def wrapper(update: Update, context: Context, *args, **kwargs):
        user_id = update.user_id
        user_data = context.get_user_data(user_id)

        if "group_id" in user_data:
            return func(update, context, *args, **kwargs)

        group_data = get_user_group_from_db(user_id)
        if group_data:
            user_data["group_number"] = group_data["group_number"]
            user_data["group_id"] = group_data["group_id"]
            return func(update, context, *args, **kwargs)

        context.telegram_api.send_message(
            update.chat_id, "Сначала установите группу с помощью команды /start"
        )

    return wrapper


def get_moscow_time() -> datetime:
    """Получает текущее время в часовом поясе Москвы"""
    return datetime.now() + timedelta(hours=3)


def start_command(update: Update, context: Context):
    user_id = update.user_id
    chat_id = update.chat_id
    user_data = context.get_user_data(user_id)

    group_data = get_user_group_from_db(user_id)

    if group_data:
        user_data["group_number"] = group_data["group_number"]
        user_data["group_id"] = group_data["group_id"]

        context.telegram_api.send_message(
            chat_id,
            f"Добро пожаловать! Ваша группа: {group_data['group_number']}",
            reply_markup=main_menu_keyboard(),
        )
        return CONVERSATION_END
    else:
        context.telegram_api.send_message(
            chat_id, "Вас приветствует бот расписания ННГУ, введите номер группы"
        )
        context.set_user_state(user_id, State.WAITING_FOR_GROUP)
        return State.WAITING_FOR_GROUP


def handle_group_input(update: Update, context: Context):
    user_id = update.user_id
    chat_id = update.chat_id
    group_number = update.text.strip()

    try:
        group_id = fetch_group_id(group_number)
        user_data = context.get_user_data(user_id)
        user_data["group_number"] = group_number
        user_data["group_id"] = group_id

        if database:
            database.save_user_group(user_id, group_number, group_id)

        context.telegram_api.send_message(
            chat_id,
            f"Номер группы '{group_number}' сохранен!\n",
            reply_markup=main_menu_keyboard(),
        )

        context.clear_user_state(user_id)
        return CONVERSATION_END
    except Exception as e:
        context.telegram_api.send_message(
            chat_id, f"Ошибка: {str(e)}\nПопробуйте ввести группу снова."
        )
        return State.WAITING_FOR_GROUP


def change_command(update: Update, context: Context):
    """Позволяет пользователю изменить свою группу"""
    user_id = update.user_id
    chat_id = update.chat_id

    context.telegram_api.send_message(chat_id, "Введите новый номер группы")
    context.set_user_state(user_id, State.WAITING_FOR_GROUP)
    return State.WAITING_FOR_GROUP


def cancel(update: Update, context: Context):
    context.telegram_api.send_message(
        update.chat_id,
        "Диалог отменен. Используй /start чтобы начать заново.",
        reply_markup=remove_keyboard(),
    )
    context.clear_user_state(update.user_id)
    return CONVERSATION_END


def _get_date_range(period: str) -> Tuple[datetime.date, datetime.date]:
    """Возвращает диапазон дат для периода"""
    current_date = get_moscow_time().date()

    if period == "today":
        return current_date, current_date
    elif period == "tomorrow":
        tomorrow = current_date + timedelta(days=1)
        return tomorrow, tomorrow
    elif period == "week":
        return current_date, current_date + timedelta(days=7)
    return current_date, current_date


@require_group
def today_command(update: Update, context: Context):
    start_date, end_date = _get_date_range("today")
    send_schedule(update, context, start_date, end_date)


@require_group
def tomorrow_command(update: Update, context: Context):
    start_date, end_date = _get_date_range("tomorrow")
    send_schedule(update, context, start_date, end_date)


@require_group
def week_command(update: Update, context: Context):
    start_date, end_date = _get_date_range("week")
    send_schedule(update, context, start_date, end_date)


def send_schedule(
    update: Update, context: Context, start_date: datetime.date, end_date: datetime.date
):
    chat_id = update.chat_id
    user_data = context.get_user_data(update.user_id)
    group_id = user_data.get("group_id")

    if not group_id:
        context.telegram_api.send_message(
            chat_id, "Группа не установлена. Используйте /start."
        )
        return

    try:
        start_date_str = start_date.strftime("%Y.%m.%d")
        end_date_str = end_date.strftime("%Y.%m.%d")

        schedules = fetch_schedule(group_id, start_date_str, end_date_str)
        schedule = make_schedule(schedules)
        messages = split_schedule_by_size(schedule, max_size=MAX_MESSAGE_SIZE)

        for message in messages:
            context.telegram_api.send_message(chat_id, message, parse_mode="Markdown")
            time.sleep(MESSAGE_DELAY)
    except Exception as e:
        context.telegram_api.send_message(chat_id, f"Ошибка: {str(e)}")
