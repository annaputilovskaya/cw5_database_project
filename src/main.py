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

# Создание и заполнение базы данных
hh_parser = HHParser(employers)
hh_parser.load_vacancies()
vacancies_list = Vacancy.cast_to_object_list(hh_parser.vacancies)
db_creator = DBVacanciesCreator('parser')
db_creator.create_database()
vacancies = db_creator.get_vacancies_params(vacancies_list)
db_creator.save_data_to_database(hh_parser.employers, vacancies)

# Выборка по базе данных

