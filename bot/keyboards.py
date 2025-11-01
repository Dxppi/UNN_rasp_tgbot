from typing import Dict, Any


def main_menu_keyboard() -> Dict[str, Any]:
    """Создает клавиатуру главного меню"""
    keyboard = {
        "keyboard": [["Сегодня", "Завтра", "Неделя"], ["Помощь"]],
        "resize_keyboard": True,
        "one_time_keyboard": False,
    }
    return keyboard


def remove_keyboard() -> Dict[str, Any]:
    """Создает пустую клавиатуру для удаления"""
    return {"remove_keyboard": True}
