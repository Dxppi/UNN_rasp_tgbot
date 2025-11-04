from abc import ABC, abstractmethod


class DatabaseInterface(ABC):
    """Интерфейс работы с базой данных"""

    @abstractmethod
    def get_user_group(self, user_id):
        """Получает группу пользователя по user_id"""
        pass

    @abstractmethod
    def save_user_group(self, user_id, group_number, group_id):
        """Сохраняет группу пользователя"""
        pass
