from web_scrapper import webscrapper
from database.database_controller import database_controller
import stock_controller
import time
import pandas as pd

PATH_TO_MAIN_PAGE_SOURCE = 'tmp/main_page_source.html'
PATH_TO_ARTICLE_SOURCE = 'tmp/article_source.html'

scrapper = webscrapper()
db = database_controller()
db.connect()

""" #scrapper.get_main_page_source(PATH_TO_MAIN_PAGE_SOURCE)
links = scrapper.get_links_article(PATH_TO_MAIN_PAGE_SOURCE)

#gets all the data from a link
for l in links:
    if(not db.is_in_db(l)):
        print(l)
        data = {'link': l}
        scrapper.get_article_source(l)
        data['article'] = scrapper.get_article(PATH_TO_ARTICLE_SOURCE)
        data['tickers'] = scrapper.get_tickers(PATH_TO_ARTICLE_SOURCE)
        data['date'] = scrapper.get_date(PATH_TO_ARTICLE_SOURCE)
        if data['article'] != None and data['tickers'] != None and data['date'] != None:
            db.add_article(data) 
 """

# get the stock from 5 days old news
curr_date = int(time.time())
articles = db.get_articles_from_prev_date(curr_date)
start_time = curr_date - 5*24*60*60  # recupere 5 jours en avance
for article_link in articles:
    print(article_link)
    tickers = db.get_tickers(article_link=article_link)
    for ticker in tickers:
        values = stock_controller.get_prices(ticker=ticker[0],
                                    start_time=start_time,
                                    end_time=curr_date)
        for value in values.itertuples():
            db.add_ticker_value(ticker[0], value.Timestamps, value.Close)
db.close()