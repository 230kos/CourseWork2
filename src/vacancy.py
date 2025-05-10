from dataclasses import dataclass
from typing import Dict, List


@dataclass(order=True)
class Vacancy:
    """Класс для представления вакансии"""

    name: str
    url: str
    salary_from: int = 0
    salary_to: int = 0
    currency: str = "RUR"
    description: str = ""
    requirements: str = ""

    def __post_init__(self) -> None:
        """Валидация данных после инициализации"""
        self._validate_salary()
        self._validate_url()

    def _validate_salary(self) -> None:
        """Приватный метод для валидации зарплаты"""
        if self.salary_from < 0:
            self.salary_from = 0
        if self.salary_to < 0:
            self.salary_to = 0

    def _validate_url(self) -> None:
        """Приватный метод для валидации URL"""
        if not self.url.startswith(("http://", "https://")):
            self.url = f"https://{self.url}"

    @property
    def avg_salary(self) -> float:
        """Средняя зарплата"""
        if self.salary_from and self.salary_to:
            return (self.salary_from + self.salary_to) / 2
        return self.salary_from or self.salary_to or 0

    @classmethod
    def cast_to_object_list(cls, vacancies_data: List[Dict]) -> List["Vacancy"]:
        """
        Преобразование списка словарей в список объектов Vacancy

        :param vacancies_data: Список словарей с данными о вакансиях
        :return: Список объектов Vacancy
        """
        vacancies = []
        for vacancy in vacancies_data:
            salary = vacancy.get("salary")
            if salary:
                salary_from = salary.get("from") or 0
                salary_to = salary.get("to") or 0
                currency = salary.get("currency", "RUR")
            else:
                salary_from = salary_to = 0
                currency = "RUR"

            snippet = vacancy.get("snippet", {})
            description = snippet.get("responsibility", "") or ""
            requirements = snippet.get("requirement", "") or ""

            vacancies.append(
                cls(
                    name=vacancy.get("name", ""),
                    url=vacancy.get("alternate_url", ""),
                    salary_from=salary_from,
                    salary_to=salary_to,
                    currency=currency,
                    description=description,
                    requirements=requirements,
                )
            )
        return vacancies

    def __str__(self) -> str:
        salary_info = f"от {self.salary_from}" if self.salary_from else ""
        if self.salary_to:
            salary_info += f" до {self.salary_to}" if salary_info else f"до {self.salary_to}"
        salary_info += f" {self.currency}" if salary_info else "Зарплата не указана"

        return (
            f"Вакансия: {self.name}\n"
            f"Зарплата: {salary_info}\n"
            f"Описание: {self.description[:100]}...\n"
            f"Требования: {self.requirements[:100]}...\n"
            f"Ссылка: {self.url}\n"
        )
