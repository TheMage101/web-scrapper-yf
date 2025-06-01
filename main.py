from web_scrapper import webscrapper

PATH_TO_MAIN_PAGE_SOURCE = 'tmp/main_page_source.html'

scrapper = webscrapper()

scrapper.get_main_page_source(PATH_TO_MAIN_PAGE_SOURCE)
scrapper.get_links_article(PATH_TO_MAIN_PAGE_SOURCE)