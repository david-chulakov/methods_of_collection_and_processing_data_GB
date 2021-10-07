from pymongo import MongoClient
import pymongo.errors
from bs4 import BeautifulSoup
import requests
from pprint import pprint
import re

client = MongoClient('127.0.0.1', 27017)
db = client['headhunter']

URL = "https://hh.ru/search/vacancy?clusters=true&area=1&enable_snippets=true&salary=&st=searchVacancy&"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"}


def get_salary(vacancy_type ,info, type_sal):
    if "от" in vacancy_type:
        vacancy_salary_min = re.sub('[^0-9]+', ' ', info).split()[0] + \
                             re.sub('[^0-9]+', ' ', info).split()[1]
        salary = {'type': type_sal,
                          'value_min': int(vacancy_salary_min),
                          'value_max': None}
    elif "до" in vacancy_type:
        vacancy_salary_max = re.sub('[^0-9]+', ' ', info).split()[0] + \
                             re.sub('[^0-9]+', ' ', info).split()[1]
        salary = {'type': type_sal,
                          'value_min': None,
                          'value_max': int(vacancy_salary_max)}
    else:
        vacancy_salary_min = re.sub('[^0-9]+', ' ', info).split()[0] + \
                                 re.sub('[^0-9]+', ' ', info).split()[1]
        vacancy_salary_max = re.sub('[^0-9]+', ' ', info).split()[2] + \
                                 re.sub('[^0-9]+', ' ', info).split()[3]
        salary = {'type': type_sal,
                              'value_min': int(vacancy_salary_min),
                              'value_max': int(vacancy_salary_max)}

    return salary


id_counter = 0
params = {'page': 0}
result = {}


def parse(id_count):
    vacancies = input("Введите название вакансии для поиска: ")
    vacancies = vacancies.replace(" ", "+")

    while True:
        req = requests.get(URL + "&text=" + vacancies, params=params, headers=HEADERS)

        soup = BeautifulSoup(req.text, 'html.parser')
        vacancy_list = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})
        if not vacancy_list or not req.ok:
            break
        for vacancy in vacancy_list[:]:
            vacancy_name = vacancy.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
            vacancy_url = vacancy.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
            try:
                vacancy_company = vacancy.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
            except AttributeError:
                vacancy_company = None
            vacancy_city = vacancy.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text
            vacancy_cite = 'HeadHunter'
            try:
                vacancy_salary_info = vacancy.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'}).text
                vacancy_salary_type = re.sub(r'[^\w\s]+|[\d]+', r"", vacancy_salary_info).replace(" ", "")
                if "руб" in vacancy_salary_type:
                    vacancy_salary = get_salary(vacancy_salary_type, vacancy_salary_info, "руб")

                elif "USD" in vacancy_salary_type:
                    vacancy_salary = get_salary(vacancy_salary_type, vacancy_salary_info, "USD")

                else:
                    vacancy_salary = get_salary(vacancy_salary_type, vacancy_salary_info, "EUR")

                result[vacancy_name] = {
                                        "_id": id_count,
                                        'name': vacancy_name,
                                        'salary': vacancy_salary,
                                        'url': vacancy_url,
                                        'company': vacancy_company,
                                        'city': vacancy_city,
                                        'resource': vacancy_cite}

            except AttributeError:
                vacancy_salary = "Не указана"
                result[vacancy_name] = {
                                        "_id": id_count,
                                        'name': vacancy_name,
                                        'salary': vacancy_salary,
                                        'url': vacancy_url,
                                        'company': vacancy_company,
                                        'city': vacancy_city,
                                        'resource': vacancy_cite}

            id_count += 1
        params['page'] += 1


def add_to_db(cursor, data):
    try:
        cursor.insert_one(data)
    except pymongo.errors.DuplicateKeyError:
        print("Already exists")


def find_more_than(cursor, type_val, value):
    for i in cursor.find({"salary": {"$ne": "Не указана"}}):
        if i["salary"]["type"] == type_val:
            min_salary = i["salary"]["value_min"]
            max_salary = i["salary"]["value_max"]
            if min_salary is not None and min_salary > value or max_salary is not None and max_salary < value and min_salary is None:
                print(i)


if __name__ == "__main__":
    # parse(id_counter)
    # for key, _ in result.items():
    #     add_to_db(db.vacancy, result[key])
    find_more_than(db.vacancy, "руб", 100000)




