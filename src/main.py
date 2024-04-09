from src.db_creator import DBVacanciesCreator
from src.db_manager import DBManager
from src.hh_parser import HHParser
from src.vacancy import Vacancy

employers = {
    'ICL Service': '156424',
    'ICL Soft': '10647164',
    'Maxima': '2048653',
    'Miles&Miles': '5819349',
    'Ак Барс Цифровые Технологии': '1741901',
    'БАРС Груп': '72977',
    'ООО ТТК Диджитал': '6137125',
    'Татнефть цифровые технологии': '3154691',
    'ТАТТЕЛЕКОМ': '672459',
    'Яндекс': '9991404'
}


def user_interaction():
    """Функция взаимодействия с пользователем"""
    print("В базе содержится информация по актуальным вакансиям hh.ru следующих компаний:")
    for key in employers.keys():
        print(key)
    info = ("\nКакую информацию о вакансиях Вы хотите получить?\n"
            "1 - названия компаний и количество открытых вакансий\n"
            "2 - список всех вакансий с указанием названия компании, вакансии, зарплаты и ссылки на вакансию\n"
            "3 - средняя зарплата по вакансиям\n"
            "4 - список вакансий c зарплатой выше средней по вакансиям данных компаний\n"
            "5 - список вакансий, в названии которых содержится заданное слово\n"
            "0 - выход")
    print(info)
    action = input()
    while action != '0':
        if action == '1':
            for company in companies_and_vacancies_count:
                print(*company, sep=':')
        elif action == '2':
            for vacancy in all_vacancies:
                print(*vacancy, sep=', ')
        elif action == '3':
            print(str(avg_salary), 'рублей')
        elif action == '4':
            for vacancy in vacancies_with_higher_salary:
                print(*vacancy, sep=', ')
        elif action == '5':
            keyword = input("Введите слово для поиска:\n")
            vacancies_with_keyword = db_manager.get_vacancies_with_keyword(keyword)
            if not vacancies_with_keyword:
                print("Отсутствуют вакансии, удовлетворяющие запросу")
            else:
                for vacancy in vacancies_with_keyword:
                    print(*vacancy, sep=', ')
        else:
            print("Запрос не определен.")
        print(info)
        action = input()


# Создание и заполнение базы данных
hh_parser = HHParser(employers)
hh_parser.load_vacancies()
vacancies_list = Vacancy.cast_to_object_list(hh_parser.vacancies)
db_creator = DBVacanciesCreator('parser')
db_creator.create_database()
vacancies = db_creator.get_vacancies_params(vacancies_list)
db_creator.save_data_to_database(hh_parser.employers, vacancies)

# Выборка по базе данных
db_manager = DBManager('parser')
companies_and_vacancies_count = db_manager.get_companies_and_vacancies_count()
all_vacancies = db_manager.get_all_vacancies()
avg_salary = db_manager.get_avg_salary()
vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()

user_interaction()
