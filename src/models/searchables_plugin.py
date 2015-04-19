#!/usr/bin/env python

from src.lib.db_handler import DBHandler

class SearchablesPlugin:

    db = DBHandler()

    match = ""
    match_shorthand = ""
    name = ""
    command = ""
    icon = ""

    def get_all(self):
        cursor = self.db.conn.cursor()
        cursor.execute("select * from `searchables_plugin`")
        tuple_list = cursor.fetchall()
        cursor.close()

        resultset = []
        for tuple in tuple_list:
            resultset.append({
                "match": tuple[0],
                "match_shorthand": tuple[1],
                "name": tuple[2],
                "command": tuple[3],
                "icon": tuple[4]
            })

        return resultset

    def get_by_match(self, match):
        conditions = (match,match)

        cursor = self.db.conn.cursor()
        cursor.execute("select * from `searchables_plugin` where `match` = ? or `match_shorthand` = ?", conditions)
        result = cursor.fetchone()
        cursor.close()

        if result != None:
            return {
                "match": result[0],
                "match_shorthand": result[1],
                "name": result[2],
                "command": result[3],
                "icon": result[4]
            }

    def search(self, query):
        conditions = (query,query)

        cursor = self.db.conn.cursor()
        cursor.execute(
           "select * "
           "from `searchables_plugin` "
           "where ( `match` != '' and ? REGEXP `match` )"
           "or ( `match_shorthand` != '' and ? REGEXP `match_shorthand` )",
           conditions
        )
        result = cursor.fetchone()
        cursor.close()

        if result != None:
            return {
                "match": result[0],
                "match_shorthand": result[1],
                "name": result[2],
                "command": result[3],
                "icon": result[4]
            }

    def save(self):
        data = (
            self.match,
            self.match_shorthand,
            self.name,
            self.command,
            self.icon
        )

        cursor = self.db.conn.cursor()

        plugin = self.get_by_match(self.match)

        if plugin == None:
            cursor = self.db.conn.cursor()
            cursor.execute(
                "INSERT INTO `searchables_plugin` "
                "(`match`, `match_shorthand`, `command`, `icon`)"
                "VALUES"
                "(?, ?, ?, ?, ?)",
                data
            )
        else:
            cursor.execute(
                "update `searchables_plugin` "
                "set `match` = ?, `match_shorthand` = ?, `name` = ?, `command` = ?, `icon` = ?)",
                data
            )

        result = self.db.conn.commit()
        cursor.close()

        return result

    def create(self, match, match_shorthand, name, command, icon):
        data = (
            match,
            match_shorthand,
            name,
            command,
            icon
        )

        cursor = self.db.conn.cursor()
        cursor.execute(
            "INSERT INTO `searchables_plugin` "
            "(`match`, `match_shorthand`, `name`, `command`, `icon`)"
            "VALUES"
            "(?, ?, ?, ?, ?)",
            data
        )

        result = self.db.conn.commit()
        cursor.close()

        return result
