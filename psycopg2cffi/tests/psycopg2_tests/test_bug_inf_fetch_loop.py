#!/usr/bin/env python
#
# bug_info_fetch_loop.py - test for bug with infinite loop, when 
# result size exceeds cursor.itersize

import psycopg2
from testconfig import dsn
from testutils import unittest


class CursorTests(unittest.TestCase):

    def setUp(self):
        self.conn = psycopg2.connect(dsn)

    def tearDown(self):
        self.conn.close()

    def _test(self):
        curs = self.conn.cursor()
        curs.itersize = 10
        curs.execute('create table inf_fetch_loop (id integer)')

        for i in xrange(curs.itersize * 2):
            curs.execute('insert into inf_fetch_loop values (%s)', (2 * i,))

        curs.execute('select * from inf_fetch_loop')
        result = list(curs)
        self.assertEqual(
                result, 
                [(2 * i,) for i in xrange(curs.itersize * 2)])

