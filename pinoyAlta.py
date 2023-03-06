# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 23:22:32 2023

@author: HabonV
"""

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import timeit
import re
# Time starts now
start = timeit.default_timer()

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver_path = r"C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(executable_path=driver_path, options=options)

links = pd.read_csv(r'C:\Users\User\PycharmProjects\Thinkingpinoy\url1.csv')  # Link

data_list = []
for index, row in links.iterrows():
    # Visit the product page
    driver.get(row["url"])
    time.sleep(2)

    brand = "Pinoy Trending Altervista"
    author = 'pinoytrending'
    title = driver.find_element_by_css_selector(
        'h1.entry-title').text  # if header use this "driver.find_element_by_css_selector"
    date_element = driver.find_element_by_css_selector('time.entry-date')
    date = date_element.get_attribute('datetime').split('T')[0] # if header use this "driver.find_element_by_css_selector"
    content = driver.find_element_by_xpath(
        '//div[@class="entry-content"]')  # if it uses div then use xpath "driver.find_element_by_xpath"
    sources_index = content.text.find("PUBLISHED BY PINOYTRENDING")
    if sources_index != -1:
        content = content.text[:sources_index]
    else:
        content = content.text
    label = "Fake"

    data = {'Headline': title,
            'Content': content,
            'Author': author,
            'Date': date,
            'URL': row['url'],
            'Brand': brand,
            'Label': label}

    data_list.append(data)

driver.quit()

df = pd.DataFrame(data_list)

df.to_csv(r'C:\Users\User\PycharmProjects\Thinkingpinoy\pinoy_trending_altervista.csv', index=False)

end = timeit.default_timer()
print("Time: ", end - start)

