from abc import ABC, abstractmethod
from typing import Dict, List


class AbstractAPI(ABC):
    """Абстрактный класс для работы с API сервисов с вакансиями"""

    @abstractmethod
    def connect(self) -> None:
        """Метод для подключения к API"""
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str) -> List[Dict]:
        """Метод для получения вакансий по ключевому слову"""
        pass
