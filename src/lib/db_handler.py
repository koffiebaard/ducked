#!/usr/bin/env python

import sqlite3
from src.lib.os_handler import OSHandler

class DBHandler:

    cursor = {}
    conn = {}

    def table_exists(self, name):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='" + name + "';")
        return self.cursor.fetchone()

    def make_sure_table_exists(self, name, callback):
        if self.table_exists(name) == None:
            callback()

    def __init__(self):
        OS = OSHandler()
        cwd = OS.cwd()
        self.conn = sqlite3.connect(cwd + '/../../ducked.db', check_same_thread=False)
        self.cursor = self.conn.cursor()