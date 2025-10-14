import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, ConversationHandler, CommandHandler, filters, MessageHandler

load_dotenv()

BOT_TOKEN = os.getenv("TOKEN")
if not BOT_TOKEN:
    raise "Не найден токен в переменных окружения"

WAITING_FOR_GROUP = 1


def create_application():
    return Application.builder().token(BOT_TOKEN).build()
