from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
import time

class webscrapper:

    _YAHOO_MAIN_PAGE = "https://finance.yahoo.com/news/"

    # Collect the main page of yahoo finance news HTML
    def get_main_page_source(self):
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
            time.sleep(1)
            lastScroll = currentScroll
            driver.execute_script("window.scrollBy(0, 1000)")
            currentScroll = driver.execute_script("return document.body.scrollHeight")


        #save the html source
        source = driver.page_source
        file = open('tmp/main_page_source.html', 'w+', encoding='utf-8')
        file.write(source)
        file.close()

        driver.close()

