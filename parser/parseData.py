import urllib.request
import urllib.parse
import json
from bot.config import MAX_MESSAGE_SIZE

BASE_GROUP_URL = "https://portal.unn.ru/ruzapi/dictionary/groups"
BASE_URL = "https://portal.unn.ru/ruzapi/schedule/group"


def fetch_group_id(group_name: str) -> str:
    """Получает ID группы по её номеру"""
    try:
        req = urllib.request.Request(BASE_GROUP_URL)
        with urllib.request.urlopen(req) as response:
            groups_data = json.loads(response.read().decode("utf-8"))
            for group in groups_data:
                if group["number"] == group_name:
                    return group["groupOid"]
        raise Exception("Группа не найдена")
    except Exception as e:
        raise Exception(f"Айди группы невозможно получить: {str(e)}")


def fetch_schedule(group_id: str, start_date: str, end_date: str) -> list:
    """Получает расписание для группы"""
    url = f"{BASE_URL}/{group_id}"
    params = {"start": start_date, "finish": end_date, "lng": 1}
    try:
        full_url = url + "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(full_url)
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        raise Exception(f"Описание невозможно получить: {str(e)}")


def make_schedule(schedules: list) -> dict:
    """Форматирует расписание по датам"""
    schedule_by_date = {}
    for schedule in schedules:
        date_parts = schedule.get("date").split("-")[::-1]
        date = "-".join(date_parts)
        lesson_data = {
            "discipline": schedule.get("discipline"),
            "auditorium": schedule.get("auditorium"),
            "building": schedule.get("building"),
            "beginLesson": schedule.get("beginLesson"),
            "endLesson": schedule.get("endLesson"),
            "lecturer": schedule.get("lecturer"),
        }
        if date not in schedule_by_date:
            schedule_by_date[date] = []
        schedule_by_date[date].append(lesson_data)
    return schedule_by_date


def print_day_schedule(date_str: str, lessons: list) -> str:
    """Форматирует расписание одного дня"""
    output = f"*Дата:*  {date_str}\n\n"

    for i, lesson in enumerate(lessons, 1):
        output += f"""{i}. *Дисциплина:* {lesson.get('discipline', '')}
 *Время проведения:* {lesson.get('beginLesson', '')}-{lesson.get('endLesson', '')}
 *Преподаватель:* {lesson.get('lecturer', '')}
 *Место проведения:* {lesson.get('building', '')}, ауд. {lesson.get('auditorium', '')}

"""
    return output


def print_schedule(schedule_data: dict) -> str:
    """Форматирует расписание в текст для отправки"""
    output = ""
    for date_str, lessons in sorted(schedule_data.items()):
        output += print_day_schedule(date_str, lessons)
    return output.strip() if output else " Занятий нет"


def split_schedule_by_size(
    schedule_data: dict, max_size: int = MAX_MESSAGE_SIZE
) -> list:
    """Разбивает расписание на части, не превышающие max_size символов
    Возвращает список строк, каждая строка содержит один или несколько дней,
    но дни не разрываются между сообщениями"""

    if not schedule_data:
        return [" Занятий нет"]

    messages = []
    current_message = ""

    for date_str, lessons in sorted(schedule_data.items()):
        day_text = print_day_schedule(date_str, lessons)

        if current_message and len(current_message) + len(day_text) > max_size:
            messages.append(current_message.strip())
            current_message = day_text
        else:
            current_message = (
                current_message + day_text if current_message else day_text
            )

    if current_message:
        messages.append(current_message.strip())

    return messages if messages else [" Занятий нет"]
