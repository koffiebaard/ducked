#!/usr/bin/env python

import sys
from src.lib.db_handler import DBHandler

class App:

    db = DBHandler()

    icon = ""
    name = ""
    command = ""
    selected = 0
    source = ""

    def get_all(self):
        cursor = self.db.conn.cursor()
        cursor.execute("select * from `apps`")
        tuple_list = cursor.fetchall()
        cursor.close()

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

        cursor = self.db.conn.cursor()
        cursor.execute("select * from `apps` where `name` = ?", conditions)
        result = cursor.fetchone()
        cursor.close()

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

        cursor = self.db.conn.cursor()
        cursor.execute(
            "INSERT INTO apps "
            "(`icon`, `name`, `command`, `selected`, `source`)"
            "VALUES"
            "(?, ?, ?, ?, ?)",
            data
        )

        result = self.db.conn.commit()
        cursor.close()

        return result

    def app_is_selected(self, name):
        conditions = (
            name,
        )

        try:
            cursor = self.db.conn.cursor()
            cursor.execute(
                "update apps set `selected` = `selected` + 1 where `name` = ?",
                conditions
            )
            result = self.db.conn.commit()
            cursor.close()
            return result
        except:
            print sys.exc_info()[0]
            print sys.exc_info()[1]
            self.db.unlock_db()
            pass

        return False

    def create_table(self):
        cursor = self.db.conn.cursor()
        cursor.execute('''CREATE TABLE apps
             (icon text, name text, command text, selected int, source text)''')
        self.db.conn.commit()
        cursor.close()

    def __init__(self):
        self.db.make_sure_table_exists("apps", self.create_table)