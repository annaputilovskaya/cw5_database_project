import psycopg2

from config import config


class DBManager:
    """Класс для выборки информации из базы данных """

    def __init__(self, db_name):
        """Создает объект класса DBManager"""
        self.name = db_name
        self.params = config()

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        conn = psycopg2.connect(dbname=self.name, **self.params)
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute("""
            SELECT employer_name, COUNT(vacancies.employer_id) AS vacancies_amount
            FROM employers
            LEFT JOIN vacancies USING(employer_id)
            GROUP BY employer_id
            ORDER BY vacancies_amount DESC""")
            result = cur.fetchall()
        conn.close()
        return result

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии, зарплаты и ссылки на вакансию.
        """
        conn = psycopg2.connect(dbname=self.name, **self.params)
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute("""
            SELECT employers.employer_name, title, salary, url
            FROM vacancies
            LEFT JOIN employers USING(employer_id)
            ORDER BY employers.employer_name""")
            result = cur.fetchall()
        conn.close()
        return result

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям,
        исключая вакансии без указания заработной платы
        """
        conn = psycopg2.connect(dbname=self.name, **self.params)
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute("""
             SELECT AVG(salary) AS average_salary
             FROM vacancies
             WHERE salary != 0""")
            result = cur.fetchall()
        conn.close()
        return int(result[0][0])

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        conn = psycopg2.connect(dbname=self.name, **self.params)
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute("""
             SELECT employers.employer_name, title, salary, url
             FROM vacancies LEFT JOIN employers USING(employer_id)
             WHERE salary > (SELECT AVG(salary) AS average_salary
             FROM vacancies WHERE salary != 0)
             ORDER BY salary DESC""")
            result = cur.fetchall()
        conn.close()
        return result

    def get_vacancies_with_keyword(self, keyword):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
        """
        conn = psycopg2.connect(dbname=self.name, **self.params)
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(f"""
                     SELECT employers.employer_name, title, salary, url, requirements, area 
                     FROM vacancies LEFT JOIN employers USING(employer_id)
                     WHERE title LIKE '%{keyword}%'""")
            result = cur.fetchall()
        conn.close()
        return result
