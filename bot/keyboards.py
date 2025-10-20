from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove


def main_menu_keyboard():
    keyboard = [
        ["Сегодня", "Завтра"],
        ["Неделя"]
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )


def remove_keyboard():
    return ReplyKeyboardRemove()
