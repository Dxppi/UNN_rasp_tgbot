import requests
import json

BASE_GROUP_URL = "https://portal.unn.ru/ruzapi/dictionary/groups"
BASE_URL = "https://portal.unn.ru/ruzapi/schedule/group"


def fetch_group_id(group_name: str) -> str:
    try:
        response = requests.get(BASE_GROUP_URL)
        response.raise_for_status()
        groups_data = response.json()
        for group in groups_data:
            if group["number"] == group_name:
                return group["groupOid"]
    except:
        raise "Айди группы невозможно получить"


def fetch_schedule(group_id: str, start_date: str, end_date: str) -> list:
    url = f"{BASE_URL}/{group_id}"
    params = {
        "start": start_date,
        "finish": end_date,
        "lng": 1
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return (response.json())
    except:
        raise "Описание невозможно получить"


def make_schedule(schedules: list) -> set:
    schedule_by_date = {}
    for schedule in schedules:
        date_parts = schedule.get("date").split("-")[::-1]
        date = "-".join(date_parts)
        params = {
            "discipline": schedule.get("discipline"),
            "auditorium": schedule.get("auditorium"),
            "building": schedule.get("building"),
            "beginLesson": schedule.get("beginLesson"),
            "endLesson": schedule.get("endLesson"),
            "lecturer": schedule.get("lecturer")
        }
        if date not in schedule_by_date:
            schedule_by_date[date] = []
        schedule_by_date[date].append(params)
    return schedule_by_date


def print_schedule(schedule_data: dict) -> str:
    output = ""
    for date_str, lessons in schedule_data.items():
        output += f"*Дата:*  {date_str}\n\n"

        for i, lesson in enumerate(lessons, 1):
            output += f"""{i}. *Дисциплина:* {lesson.get('discipline', '')}
 *Время проведения:* {lesson.get('beginLesson', '')}-{lesson.get('endLesson', '')}
 *Преподаватель:* {lesson.get('lecturer', '')}
 *Место проведения:* {lesson.get('building', '')}, ауд. {lesson.get('auditorium', '')}

"""
    return output.strip() if output else " Занятий нет"
