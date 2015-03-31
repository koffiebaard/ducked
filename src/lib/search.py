#!/usr/bin/env python

from src.lib.os_handler import OSHandler

class Search:

    OS = OSHandler()
    search_results = []

    def signal_changed(self, Window, widget):
        """Signal on change for text entry"""
        query = Window.entry.get_text()

        if len(query) > 0:
            Window.redraw_listview()

            print query
            search_results = self.search(query)
            print search_results

            for index in range(0,6):
                if index < len(search_results):
                    app = search_results[index]
                    Window.append_to_listview(app["name"], "/home/tim-en-bren/apps/intellij/bin/idea.png", "", app["command"])
        else:
            Window.remove_listview()

    def signal_goto(self, Widget, widget):
        """Go to result"""
        query = Widget.entry.get_text()
        self.search(query)

        print "Go to " + query

        if len(self.search_results) == 1:
            self.OS.goto_app(self.search_results[0]["command"])

    def search(self, query):
        """Search through apps"""

        query = query.lower()
        apps = self.OS.get_all_apps()
        self.search_results = []

        for app in apps:
            if app["name"][:len(query)].lower() == query:
                self.search_results.append(app)

        return self.search_results