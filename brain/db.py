# -*- coding: utf-8 -*-
import os
import sqlite3
from sqlite3 import Error

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


# For this exercise sqlite is utilize as it is fairly simple and easy to setup
# for future development sqlaclchemy is good option

# SQLITE REFERENCE
# http://www.sqlitetutorial.net/sqlite-python
class Database(object):
    def __init__(self, db_file=None):
        self.db_file = os.path.join(BASE_DIR, db_file)

        self.conn = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_file)

        except Error as e:
            print(e)

    def create_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY,
            timestamp DATETIME NOT NULL,
            hostname TEXT,
            status TEXT,
            component TEXT,
            value REAL,
            is_sent INTEGER DEFAULT 0 
            );
        """
        # BOOLEAN IS NOT IMPLEMENTED AS SEPARATE CLASS SO JUST USE INTEGER
        # http://www.sqlite.org/datatype3.html
        try:
            cr = self.conn.cursor()
            cr.execute(sql)
        except Error as e:
            print(e)

    def insert_logs(self, data):
        columns = ','.join(data.keys())
        markers = ','.join('?' * len(data))
        values = tuple(data.values())
        sql = f"""
            INSERT INTO logs ({columns}) VALUES ({markers})
        """
        try:
            cr = self.conn.cursor()
            cr.execute(sql, values)
        except Error as e:
            print(e)

    def get_logs(self, hostname):
        sql = f"""
            SELECT *
            FROM logs
            WHERE (is_sent = 0 AND hostname = '{hostname}')        
        """
        try:
            cr = self.conn.cursor()
            cr.execute(sql)
            return cr.fetchall()
        except Error as e:
            print(e)

    def update_sent_logs(self, ids):
        sql = f"""
            UPDATE logs 
            SET is_sent = 1
            WHERE id IN {tuple(ids)}        
        """
        try:
            cr = self.conn.cursor()
            cr.execute(sql)
            return cr.fetchall()
        except Error as e:
            print(e)

    def commit(self):
        self.conn.commit()


if __name__ == '__main__':
    db = Database('demo.db')
    db.connect()
    db.insert_logs({'timestamp': 1, 'status': 2, 'component': 3, 'value': 4})
    db.commit()
