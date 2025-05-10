import unittest
import os
import json
from pathlib import Path
from src.json_storage import JSONStorage


class TestJSONStorage(unittest.TestCase):
    def setUp(self) -> None:
        self.test_file = Path("data") / "test_vacancies.json"
        if self.test_file.exists():
            os.remove(self.test_file)

        self.storage = JSONStorage("test_vacancies.json")
        self.vacancy = {
            "name": "Python Developer",
            "url": "https://hh.ru/vacancy/123",
            "salary_from": 100000,
            "salary_to": 150000,
            "currency": "RUR",
            "description": "Разработка на Python",
            "requirements": "Опыт работы 3+ года",
        }

    def tearDown(self) -> None:
        if self.test_file.exists():
            os.remove(self.test_file)

    def test_add_vacancy(self) -> None:
        self.storage.add_vacancy(self.vacancy)
        with open(self.test_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]["name"], "Python Developer")

    def test_no_duplicates(self) -> None:
        self.storage.add_vacancy(self.vacancy)
        self.storage.add_vacancy(self.vacancy)
        with open(self.test_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertEqual(len(data), 1)

    def test_get_vacancies(self) -> None:
        self.storage.add_vacancy(self.vacancy)

        # Тест без критериев (должен вернуть все вакансии)
        vacancies = self.storage.get_vacancies({})
        self.assertEqual(len(vacancies), 1)

        # Тест с критерием keyword
        filtered = self.storage.get_vacancies({"keyword": "Python"})
        self.assertEqual(len(filtered), 1)

        # Тест с критерием keyword (нет совпадений)
        filtered = self.storage.get_vacancies({"keyword": "Java"})
        self.assertEqual(len(filtered), 0)

        # Тест с критерием salary_from
        filtered = self.storage.get_vacancies({"salary_from": 90000})
        self.assertEqual(len(filtered), 1)

        # Тест с критерием salary_from (нет совпадений)
        filtered = self.storage.get_vacancies({"salary_from": 200000})
        self.assertEqual(len(filtered), 0)

    def test_delete_vacancy(self) -> None:
        self.storage.add_vacancy(self.vacancy)

        # Проверяем, что вакансия добавилась
        vacancies = self.storage.get_vacancies({})
        self.assertEqual(len(vacancies), 1)

        # Удаляем вакансию
        self.storage.delete_vacancy(self.vacancy)

        # Проверяем, что вакансия удалилась
        vacancies = self.storage.get_vacancies({})
        self.assertEqual(len(vacancies), 0)


if __name__ == "__main__":
    unittest.main()
