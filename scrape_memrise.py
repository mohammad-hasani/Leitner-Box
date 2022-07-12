import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Text, String, DateTime, Enum, ForeignKey, select
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
import database
import time
from database import add_word


# url = 'https://app.memrise.com/course/1385716/menschen-a11/%s/'
# url = 'https://app.memrise.com/course/1332514/german-a12-menschen-vocab/%s/'
# url = 'https://app.memrise.com/course/1310269/german-a21-menschen-vocab/%s/'
# url = 'https://app.memrise.com/course/774804/menschen-a22-4/%s/'
# url = 'https://app.memrise.com/course/1621566/menschen-b11/%s/'
# url = 'https://app.memrise.com/course/1320298/almanca-b12-kelime-ve-gramatik/%s/'

url = 'https://app.memrise.com/course/1797198/menschen-sicher-a1a2b1b2c1/%s/'


chrome_options = Options()

driver = webdriver.Chrome(ChromeDriverManager().install(),
                           chrome_options=chrome_options)

for i in range(109, 118):
    _url = url % i

    driver.get(_url)
    time.sleep(2)

    word = ''

    selector = "//div[contains(@class, 'col_a col text')]"

    try:
        word = driver.find_elements_by_xpath(selector)
        for j in word:
            parent = j.find_element_by_xpath('./..')
            translation = parent.find_element_by_xpath(".//div[contains(@class, 'col_b col text')]")
            add_word(j.text, translation.text, 'C1')
            print(j)

    except:
        pass
