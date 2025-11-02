from abc import ABC, abstractmethod


class Handler(ABC):
    @abstractmethod
    def can_handle(self, update: dict, state, data: dict):
        """Определяет, может ли хендлер обработать данное обновление"""
        pass

    @abstractmethod
    def handle(self, update: dict, state, data: dict, dispatcher):
        """Обрабатывает обновление и возвращает статус (CONTINUE или STOP)"""
        pass
