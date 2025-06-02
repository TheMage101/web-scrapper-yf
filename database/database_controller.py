import sqlite3
from sqlite3 import Connection

class database_controller:
    _PATH_TO_DB = 'tmp/database.db'

    _con: Connection

    def connect(self):
        self._con = sqlite3.connect(self._PATH_TO_DB)

    def close(self):
        self._con.close()


    def create_tables(self):
        file = open('scrips/CREATE_DATABASE.sql')
        cur = self._con.cursor()

        cur.executescript(file.read())  
        self._con.commit()
        cur.close() 


    def add_article(self, data):
        cur = self._con.cursor()
        cur.execute('INSERT INTO News')