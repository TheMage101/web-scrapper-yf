import sqlite3
from sqlite3 import Connection

class database_controller:
    _PATH_TO_DB = 'database/database.db'

    _con: Connection

    def connect(self):
        self._con = sqlite3.connect(self._PATH_TO_DB)

    def close(self):
        self._con.close()


    def create_tables(self):
        file = open('database/scripts/CREATE_DATABASE.sql')
        cur = self._con.cursor()

        cur.executescript(file.read())
        self._con.commit()
        cur.close() 

    def drop_tables(self):
        file = open('database/scripts/DROP_DATABASE.sql')
        cur = self._con.cursor()

        cur.executescript(file.read())
        self._con.commit()
        cur.close() 


    def add_article(self, data):
        cur = self._con.cursor()
        sql = 'INSERT INTO News(Link, Article, ArticleTime) VALUES(?, ?, ?)'
        cur.execute(sql, (data['link'], data['article'], data['date']))
        self._con.commit()

        sql = 'INSERT INTO Company(Ticker, NewsLink) VALUES(?, ?)'
        for ticker in data['tickers']:
            cur.execute(sql, (ticker, data['link']))
        self._con.commit()
        cur.close()

    def save_count(self):
        cur = self._con.cursor()
        cur = cur.execute('SELECT COUNT(*) FROM News')
        amount = cur.fetchall()

    def is_in_db(self, link: str) -> bool:
        cur = self._con.cursor()
        sql = 'SELECT COUNT(Link) FROM News WHERE Link = ?'
        cur = cur.execute(sql, (link,))
        if cur.fetchone()[0] == 1:
            return True
        return False
    
    def get_articles_from_prev_date(self, date: int):
        request = f"""
            SELECT Link FROM NEWS WHERE ArticleTime < {date}
        """

        cur = self._con.cursor()
        cur.execute(request)
        articles = cur.fetchall()
        cur.close()
        if len(articles) > 0:
            return articles[0]
        return None
    
    def get_tickers(self, article_link: str):
        request = f"""
        SELECT Ticker FROM Company WHERE NewsLink = "{article_link}"
        """
        cur = self._con.cursor()
        cur.execute(request)
        tickers = cur.fetchall()
        cur.close()
        return tickers
    
    def add_ticker_value(self, ticker: str, time, price):
        request = """
        INSERT INTO CompanyValues (Ticker, ValueTime, ValuePrice) VALUES (?, ?, ?)
        """

        cur = self._con.cursor()
        cur.execute(request, (ticker, time, float(price),))
        cur.close()
        self._con.commit()