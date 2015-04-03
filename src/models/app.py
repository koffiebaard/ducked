#!/usr/bin/env python

import sqlite3
from src.lib.db_handler import DBHandler

class App:

    db = DBHandler()

    icon = ""
    name = ""
    command = ""
    selected = 0
    source = ""

    def get_all(self):
        self.db.cursor.execute("select * from `apps`")
        tuple_list = self.db.cursor.fetchall()

        resultset = []
        for tuple in tuple_list:
            resultset.append({
                "icon": tuple[0],
                "name": tuple[1],
                "command": tuple[2],
                "selected": tuple[3],
                "source": tuple[4],
            })

        return resultset

    def get_by_name(self, name):
        conditions = (name,)

        self.db.cursor.execute("select * from `apps` where `name` = ?", conditions)
        result = self.db.cursor.fetchone()

        if result != None:
            return {
                "icon": result[0],
                "name": result[1],
                "command": result[2],
                "selected": result[3],
                "source": result[4],
            }

    def save(self):
        data = (
            self.icon,
            self.name,
            self.command,
            str(self.selected),
            self.source
        )

        self.db.cursor.execute(
            "INSERT INTO apps "
            "(`icon`, `name`, `command`, `selected`, `source`)"
            "VALUES"
            "(?, ?, ?, ?, ?)",
            data
        )
        return self.db.conn.commit()

    def app_is_selected(self, name):
        conditions = (
            name,
        )

        self.db.cursor.execute(
            "update apps set `selected` = `selected` + 1 where `name` = ?",
            conditions
        )
        return self.db.conn.commit()

    def create_table(self):
        self.db.cursor.execute('''CREATE TABLE apps
             (icon text, name text, command text, selected int, source text)''')
        self.db.conn.commit()

    def __init__(self):
        self.db.make_sure_table_exists("apps", self.create_table)