from typing import List

from src.vacancy import Vacancy


def filter_vacancies(vacancies: List[Vacancy], keyword: str) -> List[Vacancy]:
    """
    Фильтрация вакансий по ключевому слову в описании

    :param vacancies: Список вакансий
    :param keyword: Ключевое слово для фильтрации
    :return: Отфильтрованный список вакансий
    """
    if not keyword:
        return vacancies

    keyword = keyword.lower()
    filtered = []

    for vacancy in vacancies:
        # Безопасная обработка возможных None значений
        desc = vacancy.description or ""
        reqs = vacancy.requirements or ""

        if (keyword in desc.lower()) or (keyword in reqs.lower()):
            filtered.append(vacancy)

    return filtered


def get_vacancies_by_salary(vacancies: List[Vacancy], salary_range: str) -> List[Vacancy]:
    """
    Фильтрация вакансий по диапазону зарплат

    :param vacancies: Список вакансий
    :param salary_range: Диапазон зарплат в формате "100000-150000"
    :return: Отфильтрованный список вакансий
    """
    if not salary_range:
        return vacancies

    try:
        min_salary, max_salary = map(int, salary_range.split("-"))
    except ValueError:
        return vacancies

    filtered = []
    for vacancy in vacancies:
        # Учитываем вакансии, где хотя бы одна граница зарплаты попадает в диапазон
        if (vacancy.salary_from and vacancy.salary_from >= min_salary) or (
            vacancy.salary_to and vacancy.salary_to <= max_salary
        ):
            filtered.append(vacancy)

    return filtered


def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """Сортировка вакансий по убыванию средней зарплаты"""
    return sorted(vacancies, key=lambda x: x.avg_salary, reverse=True)


def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    """
    Получение топ N вакансий

    :param vacancies: Список вакансий
    :param top_n: Количество вакансий для вывода
    :return: Список топ N вакансий
    """
    return vacancies[:top_n] if top_n > 0 else vacancies
