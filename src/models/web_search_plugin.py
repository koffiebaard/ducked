#!/usr/bin/env python

from src.lib.db_handler import DBHandler

class WebSearchPlugin:

    db = DBHandler()

    match = ""
    match_shorthand = ""
    name = ""
    url = ""
    icon = ""

    def get_all(self):
        cursor = self.db.conn.cursor()
        cursor.execute("select * from `web_search_plugin`")
        tuple_list = cursor.fetchall()
        cursor.close()

        resultset = []
        for tuple in tuple_list:
            resultset.append({
                "match": tuple[0],
                "match_shorthand": tuple[1],
                "name": tuple[2],
                "url": tuple[3],
                "icon": tuple[4]
            })

        return resultset

    def get_by_match(self, match):
        conditions = (match,match)

        cursor = self.db.conn.cursor()
        cursor.execute("select * from `web_search_plugin` where `match` = ? or `match_shorthand` = ?", conditions)
        result = cursor.fetchone()
        cursor.close()

        if result != None:
            return {
                "match": result[0],
                "match_shorthand": result[1],
                "name": result[2],
                "url": result[3],
                "icon": result[4]
            }

    def search(self, query):
        conditions = (query,query)

        cursor = self.db.conn.cursor()
        cursor.execute(
           "select * "
           "from `web_search_plugin` "
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
                "url": result[3],
                "icon": result[4]
            }

    def save(self):
        data = (
            self.match,
            self.match_shorthand,
            self.name,
            self.url,
            self.icon
        )

        cursor = self.db.conn.cursor()

        plugin = self.get_by_match(self.match)

        if plugin == None:
            cursor = self.db.conn.cursor()
            cursor.execute(
                "INSERT INTO `web_search_plugin` "
                "(`match`, `match_shorthand`, `url`, `icon`)"
                "VALUES"
                "(?, ?, ?, ?, ?)",
                data
            )
        else:
            cursor.execute(
                "update `web_search_plugin` "
                "set `match` = ?, `match_shorthand` = ?, `name` = ?, `url` = ?, `icon` = ?)",
                data
            )

        result = self.db.conn.commit()
        cursor.close()

        return result

    def create(self, match, match_shorthand, name, url, icon):
        data = (
            match,
            match_shorthand,
            name,
            url,
            icon
        )

        cursor = self.db.conn.cursor()
        cursor.execute(
            "INSERT INTO `web_search_plugin` "
            "(`match`, `match_shorthand`, `name`, `url`, `icon`)"
            "VALUES"
            "(?, ?, ?, ?, ?)",
            data
        )

        result = self.db.conn.commit()
        cursor.close()

        return result
