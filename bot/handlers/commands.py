import bot.config


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_text = f"""
Привет, {user.first_name}! 👋

Я бот с расписанием института.

Доступные команды:
/start - показать это сообщение
/help - помощь
/time - текущее время
    """
    await update.message.reply_text(welcome_text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    help_text = """
Доступные команды:
/start - начать работу
/help - помощь
    """
    await update.message.reply_text(help_text)
