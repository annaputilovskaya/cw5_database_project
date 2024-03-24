class Vacancy:
    """
    Класс для работы с вакансией
    """
    vacancies_list = []

    def __init__(self, employer_id, title, url, salary=0, requirements=None, area=None):
        """
        Создает объект класса Vacancy
        """
        self.employer_id = employer_id
        self.title = title
        self.url = url
        self.salary = salary
        self.requirements = requirements
        self.area = area

    def __str__(self) -> str:
        """
        Отображает информацию о ваканси для пользователей
        """
        return f'{self.title}: {self.salary}'

    def __repr__(self) -> str:
        """
        Отображает информацию о вакансии для разработчика
        """
        return (f'{self.__class__.__name__}({self.employer_id}, {self.title}, {self.url}, {self.salary}, '
               f'{self.requirements}, {self.area})')

    @property
    def salary(self):
        return self.__salary

    @salary.setter
    def salary(self, salary):
        """
        Устанавливает значение зарплаты.
        Если в вакансии не указан размер зарплаты или
        неизвестен курс перевода валюты, зарплата устанавливается  равной 0.
        """
        if isinstance(salary, dict):
            currency = salary.get('currency')
            if currency == 'RUR':
                salary = salary.get('from')
            else:
                salary = Vacancy.convert_to_rub(currency, salary.get('from'))

        if isinstance(salary, (int, float)):
            self.__salary = salary
        else:
            self.__salary = 0

    @staticmethod
    def convert_to_rub(currency, amount):
        """
        Переводит в рубли сумму в евро или долларах по заданному курсу
        """
        rates = {
           'EUR': 100,
           'USD': 90
        }
        rate = rates.get(currency)
        if rate is None:
            print('Нет информации о курсе валюты')
            return 0
        elif amount is None:
            return 0
        return amount * rate

    @classmethod
    def cast_to_object_list(cls, data) -> list:
        """
        Создает список объектов класса Vacancy по данным из JSON
        """
        for item in data:
            title = item.get('name')
            url = item.get('url')
            salary = item.get('salary')
            requirements = item.get('snippet').get('requirement')
            area = item.get('area').get('name')
            employer_id = item.get('employer').get('id')
            vacancy = Vacancy(employer_id, title, url, salary, requirements, area)
            Vacancy.vacancies_list.append(vacancy)
        return Vacancy.vacancies_list
