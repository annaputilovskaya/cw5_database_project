from abc import ABC, abstractmethod

import psycopg2

from config import config


class DBCreator(ABC):
    """Класс для создания и заполнения базы данных"""
    @abstractmethod
    def create_database(self):
        """Создает базу данных и таблицы для сохранения данных"""

    @abstractmethod
    def save_data_to_database(self, *args):
        """Сохраняет информацию в базу данных"""


class DBVacanciesCreator(DBCreator):
    """Класс для создания и заполнения базы данных о вакансиях в разрезе работодателей"""

    def __init__(self, db_name):
        """Создает объект класса DBVacanciesCreator"""
        self.name = db_name
        self.params = config()

    def create_database(self):
        """Создает базу данных и таблицы для сохранения данных о работодателях и вакансиях"""
        conn = psycopg2.connect(dbname='postgres', **self.params)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f'DROP DATABASE IF EXISTS {self.name}')
        cur.execute(f'CREATE DATABASE {self.name}')
        cur.close()
        conn.close()

        conn = psycopg2.connect(dbname=self.name, **self.params)
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(
                """CREATE TABLE employers (
                employer_id INTEGER PRIMARY KEY,
                employer_name VARCHAR NOT NULL)"""
            )

        with conn.cursor() as cur:
            cur.execute(
                """CREATE TABLE vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                employer_id INTEGER REFERENCES employers(employer_id),
                title VARCHAR NOT NULL,
                url VARCHAR,
                salary INTEGER,
                requirements VARCHAR,
                area VARCHAR(100))"""
            )

        conn.close()

    def save_data_to_database(self, employers, vacancies_list):
        """Сохраняет информацию о работодателях и вакансиях в базу данных"""

        conn = psycopg2.connect(dbname=self.name, **self.params)
        conn.autocommit = True

        with conn.cursor() as cur:
            for key, value in employers.items():
                cur.execute("""INSERT INTO employers VALUES (%s, %s)""", (int(value), key))

            for vacancy in vacancies_list:
                cur.execute(
                    """
                    INSERT INTO vacancies (employer_id, title, url, salary, requirements, area)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (vacancy['employer_id'],
                     vacancy['title'],
                     vacancy['url'],
                     vacancy['salary'],
                     vacancy['requirements'],
                     vacancy['area'])
                     )

        conn.close()

    @staticmethod
    def get_vacancies_params(vacancies_list):
        """
        Возвращает параметры вакансий из списка в виде списка словарей
        """
        vacancies_params_list = []
        for vacancy in vacancies_list:
            vacancies_params_list.append({
                'employer_id': vacancy.employer_id,
                'title': vacancy.title,
                'url': vacancy.url,
                'salary': vacancy.salary,
                'requirements': vacancy.requirements,
                'area': vacancy.area
            })
        return vacancies_params_list
