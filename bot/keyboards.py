def main_menu_keyboard() -> dict:
    """Создает клавиатуру главного меню"""
    keyboard = {
        "keyboard": [["Сегодня", "Завтра", "Неделя"], ["Помощь"]],
        "resize_keyboard": True,
        "one_time_keyboard": False,
    }
    return keyboard


def remove_keyboard() -> dict:
    """Создает пустую клавиатуру для удаления"""
    return {"remove_keyboard": True}
