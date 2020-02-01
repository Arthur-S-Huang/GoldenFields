from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager



def scrapeData(location):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    #driver = webdriver.Chrome('/Users/arthurhuang/agco/GoldenFields/goldenfields/forecaster/chromedriver.exe')
    driver.get("https://www.wunderground.com/history/daily/us/il/champaign/date/2019-3-1")
    html = driver.page_source
    tables = pd.read_html(html)
    data = tables[0]
    driver.close()

    print(data)

scrapeData("bob")
