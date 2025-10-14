import logging
from bot.config import create_application, CommandHandler
from bot.handlers.commands import start_command, help_command

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def main():
    """Основная функция запуска бота"""
    try:
        application = create_application()

        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))

        print("Бот запущен!")
        application.run_polling()

    except Exception as e:
        logging.error(f"Ошибка при запуске бота: {e}")


if __name__ == '__main__':
    main()
