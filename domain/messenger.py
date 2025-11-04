from abc import ABC, abstractmethod


class Messenger(ABC):
    @abstractmethod
    def send_message(self, chat_id, text, **kwargs) -> None: ...

    @abstractmethod
    def get_updates(self, **kwargs) -> list: ...
