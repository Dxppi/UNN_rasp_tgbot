import sqlite3
import os

from telegram import Update
from telegram.ext import ContextTypes
from telegram import ReplyKeyboardRemove

from functools import wraps
from bot.config import ConversationHandler, WAITING_FOR_GROUP
from parser.parseData import fetch_group_id, make_schedule, print_schedule, fetch_schedule
from datetime import datetime, timedelta


def get_user_group_from_db(user_id: int) -> dict:
    """Получает данные группы пользователя из базы данных"""
    try:
        connection = sqlite3.connect(os.getenv("DB_PATH"), timeout=5)
        cursor = connection.cursor()
        cursor.execute(
            "SELECT group_number, group_id FROM user_groups WHERE user_id = ?",
            (user_id,)
        )
        result = cursor.fetchone()

        if result:
            return {
                'group_number': result[0],
                'group_id': result[1]
            }
        return None
    except Exception as e:
        print(f"Ошибка при получении группы из БД: {e}")
        return None


def require_group(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.effective_user.id

        if 'group_id' in context.user_data:
            return await func(update, context, *args, **kwargs)

        group_data = get_user_group_from_db(user_id)
        if group_data:
            context.user_data['group_number'] = group_data['group_number']
            context.user_data['group_id'] = group_data['group_id']
            return await func(update, context, *args, **kwargs)

        await update.message.reply_text(
            "Сначала установите группу с помощью команды /start\n"
            "Введите /start и затем номер вашей группы"
        )
        return

    return wrapper


def get_moscow_time() -> datetime:
    return datetime.now() + timedelta(hours=3)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    welcome_text = f"""
Привет, {user.first_name}! 👋

Я бот с расписанием института.
Введите номер группы!

    """
    await update.message.reply_text(welcome_text)

    return WAITING_FOR_GROUP


async def handle_group_input(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    group_number = update.message.text.strip()
    group_id = fetch_group_id(group_number)
    context.user_data['group_number'] = group_number
    context.user_data['group_id'] = group_id

    connection = sqlite3.connect(os.getenv("DB_PATH"), timeout=5)
    with connection:
        connection.execute(
            "INSERT OR REPLACE INTO user_groups (user_id, group_number, group_id) VALUES (?, ?, ?)",
            (user_id, group_number, group_id)
        )

    await update.message.reply_text(
        f"Номер группы '{group_number}' сохранен!\n"
    )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработчик отмены"""
    await update.message.reply_text(
        "Диалог отменен. Используй /start чтобы начать заново.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


@require_group
async def today_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_date = get_moscow_time().date()
    await send_schedule(update, context, current_date, current_date)


@require_group
async def tomorrow_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tomorrow_date = (get_moscow_time() + timedelta(days=1)).date()
    await send_schedule(update, context, tomorrow_date, tomorrow_date)


@require_group
async def week_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_date = get_moscow_time().date()
    week_later = current_date + timedelta(days=7)
    await send_schedule(update, context, current_date, week_later)


async def send_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE,
                        start_date: datetime.date, end_date: datetime.date):
    schedules = fetch_schedule(
        context.user_data['group_id'], start_date, end_date)
    schedule = make_schedule(schedules)
    text = print_schedule(schedule)
    await update.message.reply_text(text, parse_mode='Markdown')
