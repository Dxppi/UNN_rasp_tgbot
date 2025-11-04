"""Вспомогательные функции для работы с расписанием"""

import time
from datetime import datetime, timedelta
from bot.config import MAX_MESSAGE_SIZE, MESSAGE_DELAY
from parser.parseData import fetch_schedule, make_schedule, split_schedule_by_size


def get_moscow_time():
    """Получает текущее время в часовом поясе Москвы"""
    return datetime.now() + timedelta(hours=3)


def send_schedule_to_user(
    messenger,
    chat_id: int,
    group_id: str,
    start_date: datetime.date,
    end_date: datetime.date,
):
    """Отправляет расписание пользователю"""
    if not group_id:
        messenger.send_message(chat_id, "Группа не установлена. Используйте /start.")
        return

    try:
        start_date_str = start_date.strftime("%Y.%m.%d")
        end_date_str = end_date.strftime("%Y.%m.%d")

        schedules = fetch_schedule(group_id, start_date_str, end_date_str)
        schedule = make_schedule(schedules)
        messages = split_schedule_by_size(schedule, max_size=MAX_MESSAGE_SIZE)

        for message in messages:
            messenger.send_message(chat_id, message, parse_mode="Markdown")
            time.sleep(MESSAGE_DELAY)
    except Exception as e:
        messenger.send_message(chat_id, f"Ошибка: {str(e)}")
