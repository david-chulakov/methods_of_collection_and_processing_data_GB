# text=Data+scientist+junior&from=suggest_post
from bs4 import BeautifulSoup
import requests
from pprint import pprint
import re
import json

URL = "https://hh.ru/search/vacancy?clusters=true&area=1&enable_snippets=true&salary=&st=searchVacancy&"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"}

vacancyINP = input("Введите название вакансии для поиска: ")
vacancyINP = vacancyINP.replace(" ", "+")


params = {'page': 0}
result = {}
while True:
    req = requests.get(URL + "&text=" + vacancyINP, params=params, headers=HEADERS)

    soup = BeautifulSoup(req.text, 'html.parser')
    vacancy_list = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})
    if not vacancy_list or not req.ok:
        break
    for vacancy in vacancy_list[:]:
        vacancy_name = vacancy.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
        vacancy_url = vacancy.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
        vacancy_company = vacancy.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
        vacancy_city = vacancy.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text
        vacancy_cite = 'HeadHunter'
        try:
            vacancy_salary_info = vacancy.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'}).text
            vacancy_salary_type = re.sub(r'[^\w\s]+|[\d]+', r"", vacancy_salary_info).replace(" ", "")
            if "руб" in vacancy_salary_type:
                if "от" in vacancy_salary_type:
                    vacancy_salary_min = re.sub('[^0-9]+', ' ', vacancy_salary_info).split()[0] + \
                                         re.sub('[^0-9]+', ' ', vacancy_salary_info).split()[1]
                    vacancy_salary_max = f">{vacancy_salary_min}"
                    vacancy_salary = {'type': "руб",
                                      'value_min': vacancy_salary_min,
                                      'value_max': vacancy_salary_max}
                elif "до" in vacancy_salary_type:
                    vacancy_salary_max = re.sub('[^0-9]+', ' ', vacancy_salary_info).split()[0] + \
                                         re.sub('[^0-9]+', ' ', vacancy_salary_info).split()[1]
                    vacancy_salary_min = f"<{vacancy_salary_max}"
                    vacancy_salary = {'type': "руб",
                                      'value_min': vacancy_salary_min,
                                      'value_max': vacancy_salary_max}
                else:
                    vacancy_salary_min = re.sub('[^0-9]+', ' ', vacancy_salary_info).split()[0] + \
                                         re.sub('[^0-9]+', ' ', vacancy_salary_info).split()[1]
                    vacancy_salary_max = re.sub('[^0-9]+', ' ', vacancy_salary_info).split()[2] + \
                                         re.sub('[^0-9]+', ' ', vacancy_salary_info).split()[3]
                    vacancy_salary = {'type': "руб",
                                      'value_min': vacancy_salary_min,
                                      'value_max': vacancy_salary_max}

            elif "USD" in vacancy_salary_type:
                if "от" in vacancy_salary_type:
                    vacancy_salary_min = re.sub('[^0-9]+', ' ', vacancy_salary_info).split()[0] + \
                                         re.sub('[^0-9]+', ' ', vacancy_salary_info).split()[1]
                    vacancy_salary_max = f">{vacancy_salary_min}"
                    vacancy_salary = {'type': "USD",
                                      'value_min': vacancy_salary_min,
                                      'value_max': vacancy_salary_max}
                elif "до" in vacancy_salary_type:
                    vacancy_salary_max = re.sub('[^0-9]+', ' ', vacancy_salary_info).split()[0] + \
                                         re.sub('[^0-9]+', ' ', vacancy_salary_info).split()[1]
                    vacancy_salary_min = f"<{vacancy_salary_max}"
                    vacancy_salary = {'type': "USD",
                                      'value_min': vacancy_salary_min,
                                      'value_max': vacancy_salary_max}
                else:
                    vacancy_salary_min = re.sub('[^0-9]+', ' ', vacancy_salary_info).split()[0] + \
                                         re.sub('[^0-9]+', ' ', vacancy_salary_info).split()[1]
                    vacancy_salary_max = re.sub('[^0-9]+', ' ', vacancy_salary_info).split()[2] + \
                                         re.sub('[^0-9]+', ' ', vacancy_salary_info).split()[3]
                    vacancy_salary = {'type': "USD",
                                      'value_min': vacancy_salary_min,
                                      'value_max': vacancy_salary_max}

            else:
                vacancy_salary_type = "EUR"
                if "от" in vacancy_salary_type:
                    vacancy_salary_min = re.sub('[^0-9]+', ' ', vacancy_salary_info).split()[0] + \
                                         re.sub('[^0-9]+', ' ', vacancy_salary_info).split()[1]
                    vacancy_salary_max = f">{vacancy_salary_min}"
                    vacancy_salary = {'type': "EUR",
                                      'value_min': vacancy_salary_min,
                                      'value_max': vacancy_salary_max}
                elif "до" in vacancy_salary_type:
                    vacancy_salary_max = re.sub('[^0-9]+', ' ', vacancy_salary_info).split()[0] + \
                                         re.sub('[^0-9]+', ' ', vacancy_salary_info).split()[1]
                    vacancy_salary_min = f"<{vacancy_salary_max}"
                    vacancy_salary = {'type': "EUR",
                                      'value_min': vacancy_salary_min,
                                      'value_max': vacancy_salary_max}
                else:
                    try:
                        vacancy_salary_min = re.sub('[^0-9]+', ' ', vacancy_salary_info).split()[0] + \
                                             re.sub('[^0-9]+', ' ', vacancy_salary_info).split()[1]
                        vacancy_salary_max = re.sub('[^0-9]+', ' ', vacancy_salary_info).split()[2] + \
                                             re.sub('[^0-9]+', ' ', vacancy_salary_info).split()[3]
                        vacancy_salary = {'type': "EUR",
                                          'value_min': vacancy_salary_min,
                                          'value_max': vacancy_salary_max}
                    except IndexError:
                        continue

            result[vacancy_name] = {'name': vacancy_name,
                                    'salary': vacancy_salary,
                                    'url': vacancy_url,
                                    'company': vacancy_company,
                                    'city': vacancy_city,
                                    'resource': vacancy_cite}

        except AttributeError:
            vacancy_salary = "Не указана"
            result[vacancy_name] = {'name': vacancy_name,
                                    'salary': vacancy_salary,
                                    'url': vacancy_url,
                                    'company': vacancy_company,
                                    'city': vacancy_city,
                                    'resource': vacancy_cite}

    params['page'] += 1

with open(f"{vacancyINP}.json", "w", encoding='utf-8') as f_obj:
    json.dump(result, f_obj, ensure_ascii=False)


