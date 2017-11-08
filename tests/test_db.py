# -*- coding: utf-8 -*-
import os

from brain.brain import BASE_DIR
from brain.db import Database

import unittest
from unittest import TestCase


class TestDatabase(TestCase):
    def setUp(self):
        self.db = Database('test.db')
        self.db.connect()
        self.cr = self.db.conn.cursor()

    def test_connect(self):
        # sqlite creates a db file when it connects
        db = Database('connect_test.db')
        db.connect()
        db.conn.close()

        self.assertTrue(os.path.isfile(db.db_file))
        os.remove(db.db_file)

    def test_create_table(self):
        self.db.create_table()

        sql = """
            SELECT * FROM logs
        """

        self.cr.execute(sql)
        res = self.cr.fetchall()

        self.assertTrue(isinstance(res, list))

    def tearDown(self):
        self.db.conn.close()
        db_path = os.path.join(BASE_DIR, self.db.db_file)
        if os.path.isfile(db_path):
            os.remove(db_path)


if __name__ == '__main__':
    unittest.main()
