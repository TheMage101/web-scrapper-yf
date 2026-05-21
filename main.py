from web_scrapper import webscrapper
from database.database_controller import database_controller
import stock_controller
import time
import pandas as pd
from tqdm import tqdm

PATH_TO_MAIN_PAGE_SOURCE = 'tmp/main_page_source.html'
PATH_TO_ARTICLE_SOURCE = 'tmp/article_source.html'

scrapper = webscrapper()
db = database_controller()
db.connect()
# db.create_tables()  # TODO: Create tables if not created yet otherwise do nothing

#scrapper.get_main_page_source(PATH_TO_MAIN_PAGE_SOURCE)
links = scrapper.get_links_article(PATH_TO_MAIN_PAGE_SOURCE)

#gets all the data from a link
print("===== GOING THROUGH LINKS =====")
for l in tqdm(links):
    if(not db.is_in_db(l)):
        data = {'link': l}
        scrapper.get_article_source(l)
        data['article'] = scrapper.get_article(PATH_TO_ARTICLE_SOURCE)
        data['tickers'] = scrapper.get_tickers(PATH_TO_ARTICLE_SOURCE)
        data['date'] = scrapper.get_date(PATH_TO_ARTICLE_SOURCE)
        if data['article'] != None and data['tickers'] != None and data['date'] != None:
            db.add_article(data) 

# get the stock from 5 days old news
print("===== COLLECTING PRICES =====")
curr_time = int(time.time())
start_time = curr_time - 5*24*60*60  # get from 5 days back
articles = db.get_articles_from_prev_date(start_time)
#  If no articles 5 days 
if articles:
    for article_link in tqdm(articles):
        tickers = db.get_tickers(article_link=article_link)
        for ticker in tickers:
            values = stock_controller.get_prices(ticker=ticker[0],
                                        start_time=start_time,
                                        end_time=curr_time)
            for value in values.itertuples():
                db.add_ticker_value(ticker[0], value.Timestamps, value.Close)
else:
    tqdm([])  # Just so the prints are a bit prettier
db.close()