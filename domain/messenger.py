"""Доменный интерфейс мессенджера"""
from abc import ABC, abstractmethod


class Messenger(ABC):
    @abstractmethod
    def send_message(self, chat_id, text, **kwargs) -> None:
        """Отправляет текстовое сообщение пользователю."""

    @abstractmethod
    def get_updates(self, **kwargs) -> list:
        """Возвращает новые апдейты (сообщения, события)."""
