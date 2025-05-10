import json
import os
from pathlib import Path
from typing import Dict, List, Any

from src.abstract_storage import AbstractStorage


class JSONStorage(AbstractStorage):
    """Класс для работы с JSON-файлом"""

    def __init__(self, filename: str = "user_vacancies.json"):
        self.__filename = Path("data") / filename
        self.__ensure_data_dir_exists()
        self.__ensure_file_exists()

    def __ensure_data_dir_exists(self) -> None:
        """Создает директорию data, если она не существует"""
        self.__filename.parent.mkdir(exist_ok=True)

    def __ensure_file_exists(self) -> None:
        """Создает файл с пустым списком, если он не существует или пуст"""
        if not self.__filename.exists() or os.path.getsize(self.__filename) == 0:
            with open(self.__filename, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def __read_file(self) -> Any:
        """Чтение данных из файла с обработкой ошибок"""
        try:
            with open(self.__filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            # Если файл поврежден или не читается, создаем новый
            self.__ensure_file_exists()
            return []

    def __write_file(self, data: List[Dict]) -> None:
        """Запись данных в файл"""
        with open(self.__filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_vacancy(self, vacancy: Dict) -> None:
        """Добавление вакансии в файл (без дубликатов)"""
        vacancies = self.__read_file()

        # Проверка на дубликаты по URL
        if not any(v.get("url") == vacancy.get("url") for v in vacancies):
            vacancies.append(vacancy)
            self.__write_file(vacancies)

    def get_vacancies(self, criteria: Dict) -> Any:
        """
        Получение вакансий по критериям

        :param criteria: Словарь с критериями фильтрации
        :return: Список отфильтрованных вакансий
        """
        vacancies = self.__read_file()

        if not criteria:
            return vacancies

        filtered_vacancies = []
        for vacancy in vacancies:
            match = True
            for key, value in criteria.items():
                if key == "keyword" and value.lower() not in vacancy.get("description", "").lower():
                    match = False
                    break
                elif key == "salary_from" and vacancy.get("salary_from", 0) < value:
                    match = False
                    break
                elif key == "salary_to" and vacancy.get("salary_to", 0) > value:
                    match = False
                    break
            if match:
                filtered_vacancies.append(vacancy)

        return filtered_vacancies

    def delete_vacancy(self, vacancy: Dict) -> None:
        """Удаление вакансии из файла"""
        vacancies = self.__read_file()
        vacancies = [v for v in vacancies if v.get("url") != vacancy.get("url")]
        self.__write_file(vacancies)
