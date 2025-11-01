import urllib.request
import urllib.parse
import json
from typing import Optional, Dict, Any


class TelegramAPI:
    BASE_URL = "https://api.telegram.org/bot"

    def __init__(self, token: str):
        self.token = token
        self.api_url = f"{self.BASE_URL}{token}"

    def _make_request(
        self, method: str, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        url = f"{self.api_url}/{method}"

        if data:
            data_bytes = json.dumps(data).encode("utf-8")
            req = urllib.request.Request(
                url, data=data_bytes, headers={"Content-Type": "application/json"}
            )
        else:
            req = urllib.request.Request(url)

        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            if result.get("ok"):
                return result.get("result")
            raise Exception(result.get("description", "API Error"))

    def get_updates(self, offset: Optional[int] = None, timeout: int = 30) -> list:
        params = {"timeout": timeout}
        if offset:
            params["offset"] = offset

        url = f"{self.api_url}/getUpdates?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url)

        with urllib.request.urlopen(req, timeout=timeout + 10) as response:
            result = json.loads(response.read().decode("utf-8"))
            if result.get("ok"):
                return result.get("result", [])
            raise Exception(result.get("description", "API Error"))

    def send_message(
        self,
        chat_id: int,
        text: str,
        reply_markup: Optional[Dict] = None,
        parse_mode: Optional[str] = None,
    ) -> Dict[str, Any]:
        data = {"chat_id": chat_id, "text": text}
        if reply_markup:
            data["reply_markup"] = reply_markup
        if parse_mode:
            data["parse_mode"] = parse_mode
        return self._make_request("sendMessage", data)
