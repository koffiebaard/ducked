#!/usr/bin/env python

from src.lib.os_handler import OSHandler

class Search:

    OS = OSHandler()

    def signal_changed(self, Widget, widget):
        """Signal on change for text entry"""
        query = Widget.entry.get_text()
        print query
        print self.search(query)


    def search(self, query):
        """Search through apps"""

        query = query.lower()
        apps = self.OS.get_installed_apps()
        search_results = []

        for app in apps:
            if app["name"][:len(query)].lower() == query:
                search_results.append(app)

        return search_results