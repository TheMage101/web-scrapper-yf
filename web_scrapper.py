from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from bs4 import BeautifulSoup
import time

class webscrapper:

    _WAIT_TIME = 2

    _YAHOO_MAIN_PAGE = "https://finance.yahoo.com/news/"

    # Collect the main page of yahoo finance news HTML
    def get_main_page_source(self, path_source_file):
        """ options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-error")
        options.add_argument("--ignore-ssl-errors") """
        driver = webdriver.Firefox()

        driver.get(self._YAHOO_MAIN_PAGE)

        #find the accept cookie and clicks
        try:
            cookie_button = driver.find_element(by=By.NAME, value="agree")
            cookie_button.click()
        except NoSuchElementException:
            print("Cookie not found")
        except ElementNotInteractableException:
            print("No button")


        #load in the entire page by scrolling
        lastScroll = -1
        currentScroll = 0
        while(lastScroll != currentScroll):
            time.sleep(self._WAIT_TIME)
            lastScroll = currentScroll
            driver.execute_script("window.scrollBy(0, 1000)")
            currentScroll = driver.execute_script("return document.body.scrollHeight")


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
        parents = set()
        tickers = soup.find_all("a", class_='ticker')
        for t in tickers: 
            parent = t.find_parent('div', class_='content')
            parents.add(parent.find('a')["href"])
        print(parents)
        
