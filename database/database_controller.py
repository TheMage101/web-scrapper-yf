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
        cur = cur.execute(sql, link)
        if cur.fetchone() == 1:
            return True
        return False
        