import requests
import json

BASE_URL = "https://portal.unn.ru/ruzapi/schedule/group"


def get_schedule(group_id: str, start_date: str, end_date: str) -> dict:
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


def print_schedule(schedules: dict) -> None:
    for i, schedule in enumerate(schedules):
        params = {
            "discipline": schedule.get("discipline"),
            "auditorium": schedule.get("auditorium"),
            "building": schedule.get("building"),
            "beginLesson": schedule.get("beginLesson"),
            "endLesson": schedule.get("endLesson"),
            "lecturer": schedule.get("lecturer")
        }
    print(params)


data = get_schedule("50345", "2025.10.15",
                    '2025.10.15')
print_schedule(data)
