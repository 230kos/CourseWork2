import unittest
from unittest.mock import patch, Mock
from requests.exceptions import HTTPError
from src.hh_api import HeadHunterAPI


class TestHeadHunterAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.hh_api = HeadHunterAPI()
        self.mock_response = Mock()
        self.mock_response.json.return_value = {
            "items": [
                {
                    "name": "Python Developer",
                    "alternate_url": "https://hh.ru/vacancy/123",
                    "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                    "snippet": {"requirement": "Опыт работы 3+ года", "responsibility": "Разработка на Python"},
                }
            ],
            "pages": 1,
        }

    @patch("requests.get")
    def test_connect_success(self, mock_get) -> None:
        """Тест успешного подключения к API"""
        mock_get.return_value = self.mock_response
        self.mock_response.status_code = 200

        try:
            self.hh_api.connect()
        except ConnectionError:
            self.fail("connect() raised ConnectionError unexpectedly!")

    @patch("requests.get")
    def test_connect_failure(self, mock_get) -> None:
        """Тест ошибки подключения к API"""
        mock_get.return_value = self.mock_response
        self.mock_response.status_code = 404
        self.mock_response.raise_for_status.side_effect = HTTPError("404 Error")

        with self.assertRaises(ConnectionError):
            self.hh_api.connect()

    @patch("requests.get")
    def test_get_vacancies_empty_response(self, mock_get) -> None:
        """Тест пустого ответа от API"""
        mock_get.return_value = self.mock_response
        self.mock_response.json.return_value = {"items": [], "pages": 0}

        vacancies = self.hh_api.get_vacancies("Nonexistent")
        self.assertEqual(len(vacancies), 0)

    @patch("requests.get")
    def test_get_vacancies_with_none_salary(self, mock_get) -> None:
        """Тест обработки вакансий без указания зарплаты"""
        mock_get.return_value = self.mock_response
        self.mock_response.json.return_value = {
            "items": [
                {"name": "No Salary", "alternate_url": "https://hh.ru/vacancy/456", "salary": None, "snippet": None}
            ],
            "pages": 1,
        }

        vacancies = self.hh_api.get_vacancies("Test")
        self.assertEqual(len(vacancies), 1)
        self.assertIsNone(vacancies[0]["salary"])

    @patch("requests.get")
    def test_get_vacancies_api_error(self, mock_get) -> None:
        """Тест обработки ошибки API"""
        mock_get.return_value = self.mock_response
        self.mock_response.raise_for_status.side_effect = HTTPError("Server Error")

        with self.assertRaises(Exception):
            self.hh_api.get_vacancies("Python")


if __name__ == "__main__":
    unittest.main()
