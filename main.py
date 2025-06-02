from web_scrapper import webscrapper
from database import database_controller

PATH_TO_MAIN_PAGE_SOURCE = 'tmp/main_page_source.html'
PATH_TO_ARTICLE_SOURCE = 'tmp/article_source.html'

scrapper = webscrapper()

scrapper.get_main_page_source(PATH_TO_MAIN_PAGE_SOURCE)
links = scrapper.get_links_article(PATH_TO_MAIN_PAGE_SOURCE)

#gets all the data from a link
for l in links:
    data = {'link': l}
    scrapper.get_article_source(l)
    data['article'] = scrapper.get_article(PATH_TO_ARTICLE_SOURCE)
    data['tickers'] = scrapper.get_tickers(PATH_TO_ARTICLE_SOURCE)
    data['date'] = scrapper.get_date(PATH_TO_ARTICLE_SOURCE)
    

scrapper.get_article(links.pop())