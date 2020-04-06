from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import pandas as pd
import numpy as np
from random import randint

"""
Settings
----------
using filtered search: https://mediabiasfactcheck.com/filtered-search/

Bias: All Biases
Reporting: cycle through each option
Country: -- Select One --
"""

url = 'https://mediabiasfactcheck.com/filtered-search/'

# -------- get each option in "Reporting" --------
browser = webdriver.Safari()
browser.get(url)

# waiting for the browser to finish loading
time.sleep(3)
selectElem=browser.find_element_by_xpath('//*[@id="filter-reporting"]')

reporting_opt = []

for option in selectElem.find_elements_by_tag_name('option'):
    reporting_opt.append(option.text)
    # print(option.get_attribute("value"))
    # print(option.text)

browser.quit()
print(reporting_opt)

# just get rid of the first option, nothing under it
del reporting_opt[0]
print(reporting_opt)

# -------- get data --------
browser = webdriver.Safari()
browser.get(url)


data_dict = {}
news_source = []
news_link = []
bias = []
reporting = []
country = []
references = []

for r_item in reporting_opt:

    # set drop down menu options
    set_bias = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="filter-bias"]')))
    set_bias.click()
    set_bias_select = Select(set_bias)
    # set_bias_select.select_by_value("Right")
    set_bias_select.select_by_visible_text("All Biases")

    set_report = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="filter-reporting"]')))
    set_report.click()
    set_report_select = Select(set_report)
    set_report_select.select_by_visible_text(r_item)

    set_country = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="filter-country"]')))
    set_country.click()
    set_country_select = Select(set_country)
    set_country_select.select_by_visible_text("-- Select One --")


    # get soup
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    # print(soup.prettify())

    # find the data table
    table = soup.find('table', id="mbfc-table")
    rows = table.select('tbody tr')

    #parse data
    for row in rows:
        tds = row.find_all("td")

        news_source.append(tds[0].get_text())
        try:
            news_link.append(tds[0].select_one('a')['href'])
        except:
            news_link.append(np.nan)
        bias.append(tds[1].get_text())
        reporting.append(tds[2].get_text())
        country.append(tds[3].get_text())
        references.append(tds[4].get_text())

    time.sleep(3)

data_dict['name'] = news_source
data_dict['news_link'] = news_link
data_dict['bias_mbfc'] = bias
data_dict['reporting_mbfc'] = reporting
data_dict['country_mbfc'] = country
data_dict['references_mbfc'] = references


df = pd.DataFrame(data_dict)
df.to_csv('data/MBFC/MBFC_data.csv', index=False)
print('Saving csv...  ')
print(' ')




browser.quit()
