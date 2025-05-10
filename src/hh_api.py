from typing import Any, Dict, List, Union
import requests
from src.abstract_api import AbstractAPI


class HeadHunterAPI(AbstractAPI):
    """Класс для работы с API HeadHunter"""

    def __init__(self) -> None:
        self.__base_url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params: Dict[str, Union[str, int, bool]] = {
            "text": "",
            "page": 0,
            "per_page": 100,
            "area": 113,
            "only_with_salary": True
        }

    def connect(self) -> None:
        """Реализация абстрактного метода для проверки подключения к API"""
        try:
            response = requests.get(self.__base_url, headers=self.__headers)
            response.raise_for_status()  # Проверка на ошибки HTTP
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Ошибка подключения к API HH: {str(e)}")

    def get_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Получение вакансий по ключевому слову

        :param keyword: Ключевое слово для поиска вакансий
        :return: Список вакансий в формате словарей
        """
        self.connect()  # Проверяем подключение перед запросом
        self.__params["text"] = keyword
        self.__params["page"] = 0
        vacancies: List[Dict[str, Any]] = []

        while True:
            response = requests.get(
                self.__base_url,
                headers=self.__headers,
                params={k: str(v) for k, v in self.__params.items()}  # Конвертируем все значения в строки
            )
            response.raise_for_status()

            data = response.json()
            vacancies.extend(data["items"])

            if int(self.__params["page"]) >= int(data["pages"]) - 1:  # Явное преобразование типов
                break

            self.__params["page"] = int(self.__params["page"]) + 1  # Явное преобразование типов

        return vacancies
