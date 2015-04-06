#!/usr/bin/env python

import sqlite3
from src.lib.db_handler import DBHandler

class Meta:

    db = DBHandler()

    setting = ""
    value = ""

    def set(self, setting, value):
        data = (setting, value)

        cursor = self.db.conn.cursor()
        cursor.execute(
            "INSERT INTO meta "
            "(`setting`, `value`)"
            "VALUES"
            "(?, ?)",
            data
        )
        result = self.db.conn.commit()
        cursor.close()
        return result

    def get(self, setting):
        conditions = (setting,)
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM `meta` WHERE `setting` = ?", conditions)
        result = cursor.fetchone()
        cursor.close()

        if result != None:
            return {"setting": result[0], "value": result[1]}

    def create_table(self):
        cursor = self.db.conn.cursor()
        cursor.execute('''CREATE TABLE meta
             (setting text, value text)''')
        self.db.conn.commit()
        cursor.close()

    def __init__(self):
        self.db.make_sure_table_exists("meta", self.create_table)