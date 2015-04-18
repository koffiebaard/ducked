#!/usr/bin/env python

from src.lib.db_handler import DBHandler

class Meta:

    db = DBHandler()

    setting = ""
    value = ""

    def set(self, setting, value):

        setting_in_db = self.get(setting)

        if setting_in_db == None:
            data = (setting, value)
            cursor = self.db.conn.cursor()
            cursor.execute(
                "insert into `meta` "
                "(`setting`, `value`)"
                "values"
                "(?, ?)",
                data
            )
            result = self.db.conn.commit()
            cursor.close()
        else:
            data = (value, setting)
            cursor = self.db.conn.cursor()
            cursor.execute(
                "update `meta` "
                "set `value` = ?"
                "where `setting` = ?",
                data
            )
            result = self.db.conn.commit()
            cursor.close()

        return result

    def get(self, setting):
        try:
            conditions = (setting,)
            cursor = self.db.conn.cursor()

            cursor.execute("select * from `meta` where `setting` = ?", conditions)
            result = cursor.fetchone()
            cursor.close()

            if result != None:
                return {"setting": result[0], "value": result[1]}
        except:
            return None