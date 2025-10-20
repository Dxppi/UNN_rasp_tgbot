from telegram import Update
from telegram.ext import ContextTypes
from datetime import timedelta
from bot.handlers.commands import get_moscow_time, send_schedule, require_group


@require_group
async def handle_button_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text == "Сегодня":
        current_date = get_moscow_time().date()
        await send_schedule(update, context, current_date, current_date)

    elif text == "Завтра":
        tomorrow = (get_moscow_time() + timedelta(days=1)).date()
        await send_schedule(update, context, tomorrow, tomorrow)

    elif text == "Неделя":
        current_date = get_moscow_time().date()
        week_later = current_date + timedelta(days=7)
        await send_schedule(update, context, current_date, week_later)

    else:
        await update.message.reply_text("Неизвестная команда. Используйте кнопки в меню")
