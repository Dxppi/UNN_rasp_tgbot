import logging
from bot.config import create_application, CommandHandler, filters, WAITING_FOR_GROUP, MessageHandler, ConversationHandler
from bot.handlers.commands import start_command, today_command, tomorrow_command, week_command, handle_group_input, cancel

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def main() -> None:
    application = create_application()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            WAITING_FOR_GROUP: [
                MessageHandler(filters.TEXT & ~filters.COMMAND,
                               handle_group_input)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("today", today_command))
    application.add_handler(CommandHandler("tomorrow", tomorrow_command))
    application.add_handler(CommandHandler("week", week_command))

    print("Бот запущен!")
    application.run_polling()


if __name__ == '__main__':
    main()
