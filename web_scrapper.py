from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from bs4 import BeautifulSoup
import time
import datetime

class webscrapper:



    _YAHOO_MAIN_PAGE = "https://finance.yahoo.com/news/"
    # Collect the main page of yahoo finance news HTML
    def get_main_page_source(self, path_source_file):
        driver = webdriver.Firefox()

        driver.get(self._YAHOO_MAIN_PAGE)

        self._click_cookie(driver)


        #load in the entire page by scrolling
        self._load_entire_page(driver)


        #save the html source
        source = driver.page_source
        file = open(path_source_file, 'w+', encoding='utf-8')
        file.write(source)
        file.close()

        driver.close()

    def get_links_article(self, path_source_file):
        file = open(path_source_file, encoding='utf-8')
        source = file.read()
        soup = BeautifulSoup(source, "html.parser")
        
        #finds all articles that contain a ticker
        #makes sure there is no duplicate
        links = set()
        tickers = soup.find_all("a", class_='ticker')
        for t in tickers: 
            parent = t.find_parent('div', class_='content')
            links.add(parent.find('a')["href"])
        return links

    #gets the html source of an article  
    def get_article_source(self, url: str):
        driver = webdriver.Firefox()
        driver.get(url)
        
        self._click_cookie(driver)
        self._load_entire_page(driver)

        source = driver.page_source
        file = open('tmp/article_source.html', 'w+', encoding='utf-8')
        file.write(source)
        file.close()

        driver.close()

    _ARTICLE_PARENT_CLASS = 'yf-1ir6o1g' 
    #returns the content of the article
    def get_article(self, path):
        f = open(path, encoding='utf-8')
        soup = BeautifulSoup(f.read(), 'html.parser')

        parent = soup.find('div', class_ = self._ARTICLE_PARENT_CLASS)
        paragraph = parent.find_all('p')
        article = ""
        for p in paragraph:
            article = article + p.get_text()
        return article

    _TICKER_PARENT_CLASS = 'yf-pqeumq'
    def get_tickers(self, path):
        f = open(path, encoding='utf-8')
        soup = BeautifulSoup(f.read(), 'html.parser')

        parent = soup.find('div', class_ = self._TICKER_PARENT_CLASS)
        ticker_containers = parent.find_all('a', class_='ticker')
        tickers = []
        for t in ticker_containers:
            tickers.append(t['title'])
        return tickers


    _TIME_CLASS = 'byline-attr-meta-time'
    def get_date(self, path):
        f = open(path, encoding='utf-8')
        soup = BeautifulSoup(f.read(), 'html.parser')

        time_container = soup.find('time', class_ = self._TIME_CLASS)
        return self._time_to_timestamp(time_container['datetime'])
    #--------PRIVATE METHODS--------#
    
    #adjust wait time depending on internet speed
    _WAIT_TIME = 2
    def _load_entire_page(self, driver):
        lastScroll = -1
        currentScroll = 0
        while(lastScroll != currentScroll):
            lastScroll = currentScroll
            driver.execute_script("window.scrollBy(0, 10000)")
            time.sleep(self._WAIT_TIME)
            currentScroll = driver.execute_script("return document.body.scrollHeight")

    def _click_cookie(self, driver):
        time.sleep(self._WAIT_TIME)
        try:
            cookie_button = driver.find_element(by=By.NAME, value="agree")
            cookie_button.click()
        except NoSuchElementException:
            print("Cookie not found")
        except ElementNotInteractableException:
            print("No button")

    #2025-06-01T22:09:29.000Z
    def _time_to_timestamp(self, time_str):
        time_str = time_str.split('T')
        date = time_str[0].split('-')
        hour = time_str[1].split(':')
        dt = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(hour[0]), int(hour[1]), 0)
        return dt.timestamp()