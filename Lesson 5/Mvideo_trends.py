from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

from pprint import pprint
from bs4 import BeautifulSoup

import time

from pymongo import MongoClient
import pymongo.errors

client = MongoClient('127.0.0.1', 27017)
db = client['mvideo']

chrome_options = Options()
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("start-maximized")

driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)
driver.get('https://www.mvideo.ru/')
actions = ActionChains(driver)
actions.move_by_offset(10, 100)
time.sleep(3)
actions.click().perform()


result = []
wait = WebDriverWait(driver, 10)
driver.execute_script('window.scrollTo(0, 1600);')

time.sleep(3)
buttons = driver.find_elements(By.CLASS_NAME, 'tab-button')
buttons[1].click()

elem = driver.find_element(By.XPATH, "//*")
source_code = elem.get_attribute("outerHTML")

soup = BeautifulSoup(source_code, 'lxml')

items = soup.find('mvid-product-cards-group')
names = items.find_all('div', {'class': 'product-mini-card__name ng-star-inserted'})
titles = [name.text for name in names]

prices = items.find_all('span', {'class': 'price__main-value'})
price_list = [price.text for price in prices]

links = items.find_all('a', {'class': 'img-with-badge'})
link_list = [link['href'] for link in links]

for i in range(16):
    result.append({'title': titles[i],
                    'link': 'https://www.mvideo.ru' + link_list[i],
                    'price': int(price_list[0].replace(u'\xa0', "").replace(" ", ""))})

driver.close()


def add_to_db(cursor, data):
    try:
        cursor.insert_one(data)
    except pymongo.errors.DuplicateKeyError:
        print("Already exists")


for d in result:
    add_to_db(db.mvideo_trends, d)
