from lxml import html
import requests
from pprint import pprint
from pymongo import MongoClient
import pymongo.errors

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"}

client = MongoClient('127.0.0.1', 27017)
db = client['news']

url = "https://yandex.ru/news/"
response = requests.get(url, headers=headers)
dom = html.fromstring(response.text)
items = dom.xpath("//article[contains(@class, 'mg-card')]")

all_news = []

for item in items:
    news = {}
    name = item.xpath(".//h2[contains(@class, 'mg-card__title')]/text()")
    link = item.xpath(".//a[contains(@class, 'mg-card__link')]/@href")
    descriprion = item.xpath(".//div[contains(@class, 'mg-card__annotation')]/text()")
    source = item.xpath(".//a[contains(@class, 'mg-card__source-link')]/text()")
    time = item.xpath(".//span[contains(@class, 'mg-card-source__time')]/text()")

    news["Заголовок"] = name[0].replace("\xa0", " ");
    news["Ссылка"] = link
    news["Описание"] = descriprion[0].replace("\xa0", " ")
    news["Ресурс"] = source[0].replace("\xa0", " ")
    news["Время публикации"] = time[0]

    all_news.append(news)


def add_to_db(cursor, data):
    try:
        cursor.insert_one(data)
    except pymongo.errors.DuplicateKeyError:
        print("Already exists")


for d in all_news:
    add_to_db(db.news, d)

