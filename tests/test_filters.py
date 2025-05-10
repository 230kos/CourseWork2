import unittest
from src.vacancy import Vacancy
from src.filters import filter_vacancies, get_vacancies_by_salary, sort_vacancies, get_top_vacancies


class TestFilters(unittest.TestCase):
    def setUp(self) -> None:
        # Создаем тестовые вакансии
        self.vacancies = [
            Vacancy(
                name="Python Developer",
                url="https://hh.ru/vacancy/1",
                salary_from=120000,
                salary_to=150000,
                description="Разработка на Python в Москве",
                requirements="Опыт работы 3+ года",
            ),
            Vacancy(
                name="Java Developer",
                url="https://hh.ru/vacancy/2",
                salary_from=100000,
                salary_to=130000,
                description="Разработка на Java",
                requirements="Опыт работы 5+ лет",
            ),
            Vacancy(
                name="DevOps Engineer",
                url="https://hh.ru/vacancy/3",
                salary_from=150000,
                salary_to=0,
                description="Настройка CI/CD в Москве",
                requirements="Знание Docker, Kubernetes",
            ),
            Vacancy(
                name="Frontend Developer",
                url="https://hh.ru/vacancy/4",
                salary_from=80000,
                salary_to=120000,
                description="Разработка интерфейсов",
                requirements=None,  # Тестируем None в требованиях
            ),
            Vacancy(
                name="Data Scientist",
                url="https://hh.ru/vacancy/5",
                salary_from=0,
                salary_to=0,
                description=None,  # Тестируем None в описании
                requirements="Python, Machine Learning",
            ),
        ]

    def test_filter_vacancies_with_empty_keyword(self) -> None:
        """Тест фильтрации с пустым ключевым словом"""
        filtered = filter_vacancies(self.vacancies, "")
        self.assertEqual(len(filtered), len(self.vacancies))

    def test_filter_vacancies_with_none_fields(self) -> None:
        """Тест фильтрации с None в описании/требованиях"""
        filtered = filter_vacancies(self.vacancies, "Python")
        self.assertEqual(len(filtered), 2)
        self.assertEqual(filtered[0].name, "Python Developer")
        self.assertEqual(filtered[1].name, "Data Scientist")

    def test_filter_vacancies_no_matches(self) -> None:
        """Тест фильтрации без совпадений"""
        filtered = filter_vacancies(self.vacancies, "PHP")
        self.assertEqual(len(filtered), 0)

    def test_get_vacancies_by_salary_invalid_range(self) -> None:
        """Тест с некорректным диапазоном зарплат"""
        filtered = get_vacancies_by_salary(self.vacancies, "invalid-range")
        self.assertEqual(len(filtered), len(self.vacancies))

    def test_get_vacancies_by_salary_empty_range(self) -> None:
        """Тест с пустым диапазоном зарплат"""
        filtered = get_vacancies_by_salary(self.vacancies, "")
        self.assertEqual(len(filtered), len(self.vacancies))

    def test_sort_vacancies(self) -> None:
        """Тест сортировки вакансий по зарплате"""
        sorted_list = sort_vacancies(self.vacancies)
        self.assertEqual(sorted_list[0].name, "DevOps Engineer")
        self.assertEqual(sorted_list[1].name, "Python Developer")
        self.assertEqual(sorted_list[2].name, "Java Developer")
        self.assertEqual(sorted_list[3].name, "Frontend Developer")
        self.assertEqual(sorted_list[4].name, "Data Scientist")

    def test_get_top_vacancies_more_than_exists(self) -> None:
        """Тест получения большего количества, чем есть"""
        top = get_top_vacancies(self.vacancies, 10)
        self.assertEqual(len(top), len(self.vacancies))


if __name__ == "__main__":
    unittest.main()
