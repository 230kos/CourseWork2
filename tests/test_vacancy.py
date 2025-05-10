import unittest
from src.vacancy import Vacancy


class TestVacancy(unittest.TestCase):
    def setUp(self) -> None:
        self.vacancy1 = Vacancy(
            name="Python Developer",
            url="https://hh.ru/vacancy/123",
            salary_from=100000,
            salary_to=150000,
            currency="RUR",
            description="Разработка на Python",
            requirements="Опыт работы 3+ года",
        )

        self.vacancy2 = Vacancy(
            name="Java Developer",
            url="https://hh.ru/vacancy/456",
            salary_from=120000,
            salary_to=180000,
            currency="RUR",
            description="Разработка на Java",
            requirements="Опыт работы 5+ лет",
        )

        self.vacancy3 = Vacancy(
            name="DevOps Engineer",
            url="https://hh.ru/vacancy/789",
            salary_from=150000,
            salary_to=0,
            currency="RUR",
            description="Настройка CI/CD",
            requirements="Знание Docker, Kubernetes",
        )

    def test_avg_salary(self) -> None:
        self.assertEqual(self.vacancy1.avg_salary, 125000)
        self.assertEqual(self.vacancy2.avg_salary, 150000)
        self.assertEqual(self.vacancy3.avg_salary, 150000)

    def test_str(self) -> None:
        self.assertIn("Python Developer", str(self.vacancy1))
        self.assertIn("100000", str(self.vacancy1))
        self.assertIn("150000", str(self.vacancy1))
        self.assertIn("RUR", str(self.vacancy1))

    def test_cast_with_missing_data(self) -> None:
        test_data = [
            {
                "name": "Test",
                "alternate_url": "https://test.com",
                "salary": None,
                "snippet": {"responsibility": None, "requirement": None},
            }
        ]
        vacancies = Vacancy.cast_to_object_list(test_data)
        self.assertEqual(vacancies[0].description, "")
        self.assertEqual(vacancies[0].requirements, "")


if __name__ == "__main__":
    unittest.main()
