import requests


from abc import ABC, abstractmethod


class Parser(ABC):
    """
    Абстрактный класс для работы с API сервиса с вакансиями
    """

    @abstractmethod
    def load_vacancies(self):
        """
        Получает данные о вакансиях с сайта
        """
        pass


class HHParser(Parser):
    """
    Класс для работы с API HeadHunter
    """

    def __init__(self, employers):
        """Создает объект класса HHParser"""
        self.vacancies_url = 'https://api.hh.ru/vacancies'
        self.employers_url = 'https://api.hh.ru/employers'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'page': 0, 'per_page': 100}
        self.vacancies = []
        self.employers = employers

    def load_vacancies(self):
        """
        Получает данные о вакансиях с сайта hh.ru
        """
        self.params['employer_id'] = self.employers.values()
        while self.params.get('page') != 20:
            response = requests.get(self.vacancies_url, headers=self.headers, params=self.params)
            if response.status_code == 200:
                vacancies = response.json()['items']
                self.vacancies.extend(vacancies)
                self.params['page'] += 1
            else:
                print('Возникла ошибка при обращении к сайту hh.ru')
