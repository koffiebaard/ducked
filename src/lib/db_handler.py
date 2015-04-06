#!/usr/bin/env python

import sqlite3
from src.lib.os_handler import OSHandler

class DBHandler:

    conn = {}

    def table_exists(self, name):

        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='" + name + "';")
        result = cursor.fetchone()
        cursor.close()
        return result

    def make_sure_table_exists(self, name, callback):
        if self.table_exists(name) == None:
            callback()

    def unlock_db(self):

        OS = OSHandler()
        cwd = OS.cwd()
        db_location = cwd + "/ducked.db"

        OS.run_command(cwd + "/bin/unlock_db " + db_location)

    def __init__(self):
        OS = OSHandler()
        cwd = OS.cwd()
        self.conn = sqlite3.connect(cwd + '/ducked.db')