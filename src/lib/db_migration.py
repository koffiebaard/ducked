#!/usr/bin/env python

import json
from src.lib.db_handler import DBHandler
from src.lib.os_handler import OSHandler
from src.models.web_search_plugin import WebSearchPlugin
from src.models.meta import Meta

class DBMigration:

    DB = DBHandler()
    OS = OSHandler()
    Meta = Meta()
    WebSearchPlugin = WebSearchPlugin()

    def load_settings(self):

        # Load app meta info
        meta_json = open(self.OS.cwd() + "/meta.json", "r")
        self.app = json.load(meta_json)

        # Setup app version for matching & migrating
        self.app_version = self.app["version"]

        # Setup DB version for matching & migrating
        if self.app_version == None:
            self.db_version = None
        else:
            self.db_version = self.Meta.get("version")


    def check_if_migration_is_needed(self):
        self.load_settings()

        if self.db_version < self.app_version or self.db_version == None:
            self.migrate()


    def migrate(self):

        cursor = self.DB.conn.cursor()
        # First time setup
        if self.db_version == None:
            print "Fresh install! Updating to " + self.app_version

            # Meta table
            cursor.execute('''create table meta
                         (setting text, value text)''')
            self.DB.conn.commit()

            # Meta info
            self.Meta.set("initial_sync_completed", 0)
            self.Meta.set("version", self.app_version)
            self.Meta.set("app_name", self.app["name"])


            # App table
            cursor.execute('''CREATE TABLE apps
                         (icon text, name text, command text, selected int, source text)''')
            self.DB.conn.commit()


            # Web Search Plugin table
            cursor.execute('''create table web_search_plugin
                         (match text, match_shorthand text, name text, url text, icon text)''')
            self.DB.conn.commit()

            # Web Search Plugin info
            self.WebSearchPlugin.create("^github ", "^gh ", "Github to {query}", "https://github.com/search?q={query}", "resources/icons/github.png")
            self.WebSearchPlugin.create("^maps ", "", "Search Maps for \"{query}\"", "https://www.google.com/maps/search/{query}", "resources/icons/google.png")
            self.WebSearchPlugin.create("^wiki ", "", "Search Wiki for \"{query}\"", "https://en.wikipedia.org/w/index.php?search={query}", "resources/icons/wiki.png")
            self.WebSearchPlugin.create("^youtube ", "^yt ", "Search YouTube for \"{query}\"", "https://www.youtube.com/results?search_query={query}", "resources/icons/youtube.png")
            self.WebSearchPlugin.create("^twitter ", "^twit ", "Search The Twits for \"{query}\"", "https://twitter.com/search?q={query}", "resources/icons/twitter.png")
            self.WebSearchPlugin.create("^gmail ", "", "Search Gmail for \"{query}\"", "https://mail.google.com/mail/#search/{query}", "resources/icons/gmail.png")
            self.WebSearchPlugin.create("^torrentz ", "^tz ", "Search Torrentz for \"{query}\"", "https://torrentz.eu/search?q={query}", "resources/icons/torrentz.png")
            self.WebSearchPlugin.create("^py2ref ", "", "Search Python 2 ref for \"{query}\"", "https://docs.python.org/2/search.html?q={query}", "resources/icons/python.png")
            self.WebSearchPlugin.create("^py3ref ", "", "Search Python 3 ref for \"{query}\"", "https://docs.python.org/3/search.html?q={query}", "resources/icons/python.png")
            self.WebSearchPlugin.create("^phpref ", "", "Search PHP ref for \"{query}\"", "http://php.net/manual-lookup.php?pattern={query}", "resources/icons/php.png")
            self.WebSearchPlugin.create("", "", "{query}", "{query}", "")
            self.WebSearchPlugin.create("", "", "{query}", "{query}", "")
            self.WebSearchPlugin.create("", "", "{query}", "{query}", "")
            self.WebSearchPlugin.create("", "", "{query}", "{query}", "")
            self.WebSearchPlugin.create("", "", "{query}", "{query}", "")
            self.WebSearchPlugin.create("", "", "{query}", "{query}", "")
            self.WebSearchPlugin.create("", "", "{query}", "{query}", "")



        cursor.close()