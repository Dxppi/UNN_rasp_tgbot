import json
import urllib.request
from bot.config import BOT_TOKEN


def get_telegram_base_uri():
    """Возвращает базовый URI для Telegram Bot API"""
    return f"https://api.telegram.org/bot{BOT_TOKEN}"


def make_request(method: str, **kwargs):
    json_data = json.dumps(kwargs).encode("utf-8")
    request = urllib.request.Request(
        method="POST",
        url=f"{get_telegram_base_uri()}/{method}",
        data=json_data,
        headers={
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode("utf-8")
        response_json = json.loads(response_body)
        assert response_json["ok"]
        return response_json["result"]


def get_updates(**kwargs):
    """Получает обновления от Telegram API"""
    return make_request("getUpdates", **kwargs)


def send_message(chat_id, text, **kwargs):
    """Отправляет сообщение в чат"""
    return make_request("sendMessage", chat_id=chat_id, text=text, **kwargs)
