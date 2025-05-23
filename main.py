# main.py
from src.api.hh_api import HeadHunterAPI
from src.models.vacancy import Vacancy
from src.storage.json_storage import JSONStorage
from src.utils.filters import (
    filter_vacancies,
    get_vacancies_by_salary,
    sort_vacancies,
    get_top_vacancies
)


def user_interaction():
    """Функция для взаимодействия с пользователем"""
    print("Добро пожаловать в программу для работы с вакансиями HeadHunter!")

    # Инициализация API и хранилища
    hh_api = HeadHunterAPI()
    storage = JSONStorage()

    # Получение данных от пользователя
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий (через пробел): ").split()
    salary_range = input("Введите диапазон зарплат (например: 100000-150000): ")

    # Получение вакансий с HH
    print("\nПолучаем вакансии с HeadHunter...")
    vacancies_data = hh_api.get_vacancies(search_query)
    vacancies = Vacancy.cast_to_object_list(vacancies_data)

    # Сохранение вакансий в файл
    print(f"Найдено {len(vacancies)} вакансий. Сохраняем в файл...")
    for vacancy in vacancies:
        storage.add_vacancy({
            'name': vacancy.name,
            'url': vacancy.url,
            'salary_from': vacancy.salary_from,
            'salary_to': vacancy.salary_to,
            'currency': vacancy.currency,
            'description': vacancy.description,
            'requirements': vacancy.requirements
        })

    # Фильтрация и сортировка вакансий
    print("\nФильтруем и сортируем вакансии...")
    filtered_vacancies = filter_vacancies(vacancies, ' '.join(filter_words))
    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
    sorted_vacancies = sort_vacancies(ranged_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

    # Вывод результатов
    print(f"\nРезультаты поиска ({len(top_vacancies)} вакансий):")
    for i, vacancy in enumerate(top_vacancies, 1):
        print(f"\nВакансия #{i}")
        print(vacancy)

    print("\nРабота программы завершена. Данные сохранены в data/user_vacancies.json")


if __name__ == "__main__":
    user_interaction()
