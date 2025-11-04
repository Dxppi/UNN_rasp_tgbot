from abc import ABC, abstractmethod
from domain.database import DatabaseInterface
from domain.messenger import Messenger


class Handler(ABC):
    @abstractmethod
    def can_handle(self, update: dict, state, data: dict):
        """Определяет, может ли хендлер обработать данное обновление"""
        pass

    @abstractmethod
    def handle(
        self,
        update: dict,
        state,
        data: dict,
        messenger: Messenger,
        database: DatabaseInterface,
    ):
        """Обрабатывает обновление и возвращает статус (CONTINUE или STOP)"""
        pass
