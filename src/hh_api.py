import requests
from typing import Dict, List
from src.abstract_api import AbstractAPI


class HeadHunterAPI(AbstractAPI):
    """Класс для работы с API HeadHunter"""

    def __init__(self):
        self.__base_url = "https://api.hh.ru/vacancies"
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.__params = {
            'text': '',
            'page': 0,
            'per_page': 100,
            'area': 113,  # Россия
            'only_with_salary': True
        }

    def __connect(self) -> None:
        """Приватный метод для проверки подключения к API"""
        response = requests.get(self.__base_url, headers=self.__headers)
        if response.status_code != 200:
            raise ConnectionError(f"Ошибка подключения к API HH: {response.status_code}")

    def get_vacancies(self, keyword: str) -> List[Dict]:
        """
        Получение вакансий по ключевому слову

        :param keyword: Ключевое слово для поиска вакансий
        :return: Список вакансий в формате словарей
        """
        self.__connect()
        self.__params['text'] = keyword
        self.__params['page'] = 0
        vacancies = []

        while True:
            response = requests.get(self.__base_url, headers=self.__headers, params=self.__params)
            if response.status_code != 200:
                break

            data = response.json()
            vacancies.extend(data['items'])

            if self.__params['page'] >= data['pages'] - 1:
                break

            self.__params['page'] += 1

        return vacancies
