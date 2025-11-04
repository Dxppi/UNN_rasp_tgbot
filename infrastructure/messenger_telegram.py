"""Реализация интерфейса Messenger через Telegram Bot API"""

import json
import urllib.request
from domain.messenger import Messenger
from bot.config import BOT_TOKEN


class MessengerTelegram(Messenger):
    def _base_uri(self) -> str:
        return f"https://api.telegram.org/bot{BOT_TOKEN}"

    def _request(self, method: str, **kwargs) -> dict:
        payload = json.dumps(kwargs).encode("utf-8")
        req = urllib.request.Request(
            method="POST",
            url=f"{self._base_uri()}/{method}",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode("utf-8")
            data = json.loads(body)
            assert data.get("ok") is True
            return data["result"]

    def send_message(self, chat_id, text, **kwargs) -> None:
        self._request("sendMessage", chat_id=chat_id, text=text, **kwargs)

    def get_updates(self, **kwargs) -> dict:
        return self._request("getUpdates", **kwargs)
