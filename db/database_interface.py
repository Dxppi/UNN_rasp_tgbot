from abc import ABC, abstractmethod
from typing import Optional, Dict


class DatabaseInterface(ABC):
    @abstractmethod
    def get_user_group(self, user_id: int) -> Optional[Dict[str, str]]:
        """Получает группу пользователя по user_id"""
        pass

    @abstractmethod
    def save_user_group(self, user_id: int, group_number: str, group_id: str) -> None:
        """Сохраняет группу пользователя"""
        pass
