from web_scrapper import webscrapper

PATH_TO_MAIN_PAGE_SOURCE = 'tmp/main_page_source.html'
PATH_TO_ARTICLE_SOURCE = 'tmp/article_source.html'

scrapper = webscrapper()

scrapper.get_main_page_source(PATH_TO_MAIN_PAGE_SOURCE)
links = scrapper.get_links_article(PATH_TO_MAIN_PAGE_SOURCE)
data = []
for l in links:
    d = {'link': l}
    scrapper.get_article_source(l)
    d['article'] = scrapper.get_article(PATH_TO_ARTICLE_SOURCE)
    d['tickers'] = scrapper.get_tickers(PATH_TO_ARTICLE_SOURCE)
    d['date'] = scrapper.get_date(PATH_TO_ARTICLE_SOURCE)

scrapper.get_article(links.pop())