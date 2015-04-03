#!/usr/bin/env python

import sqlite3
from src.lib.db_handler import DBHandler

class Meta:

    db = DBHandler()

    setting = ""
    value = ""

    def set(self, setting, value):
        data = (setting, value)

        self.db.cursor.execute(
            "INSERT INTO meta "
            "(`setting`, `value`)"
            "VALUES"
            "(?, ?)",
            data
        )
        return self.db.conn.commit()

    def get(self, setting):
        conditions = (setting,)
        self.db.cursor.execute("SELECT * FROM `meta` WHERE `setting` = ?", conditions)
        result = self.db.cursor.fetchone()

        if result != None:
            return {"setting": result[0], "value": result[1]}

    def create_table(self):
        self.db.cursor.execute('''CREATE TABLE meta
             (setting text, value text)''')
        self.db.conn.commit()

    def __init__(self):
        self.db.make_sure_table_exists("meta", self.create_table)