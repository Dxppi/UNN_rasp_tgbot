import urllib.request
import json


class TelegramAPI:
    BASE_URL = "https://api.telegram.org/bot"

    def __init__(self, token):
        self.api_url = f"{self.BASE_URL}{token}"

    def _read_json(self, req):
        """Открывает URL, читает ответ и возвращает result или ошибку."""
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            if result.get("ok"):
                return result["result"]
            raise Exception(result.get("description", "API Error"))

    def _post(self, method, data=None):
        url = f"{self.api_url}/{method}"
        data_bytes = json.dumps(data or {}).encode("utf-8")

        req = urllib.request.Request(
            url,
            data=data_bytes,
            headers={"Content-Type": "application/json"},
        )
        return self._read_json(req)

    def get_updates(self, offset=None, timeout=30):
        data = {"timeout": timeout}
        if offset is not None:
            data["offset"] = offset
        return self._post("getUpdates", data)

    def send_message(self, chat_id, text, reply_markup=None, parse_mode=None):
        data = {"chat_id": chat_id, "text": text}
        if reply_markup:
            data["reply_markup"] = reply_markup
        if parse_mode:
            data["parse_mode"] = parse_mode
        return self._post("sendMessage", data)
