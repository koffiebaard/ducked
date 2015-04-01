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
            Window.clear_listview()

    def signal_goto_first_result(self, query):
        """Go to result"""
        self.search(query)

        if len(self.search_results) > 0:
            app = self.search_results[0]
            print "Go to " + app["name"]
            self.OS.goto_app(app["command"])

    def signal_goto_app_name(self, app_name):
        app = self.get_app_by_name(app_name)

        if app:
            self.OS.goto_app(app["command"])

    def search(self, query):
        """Search through apps"""

        query = query.lower()
        apps = self.OS.get_all_apps()
        self.search_results = []

        for app in apps:
            if app["name"][:len(query)].lower() == query:
                self.search_results.append(app)

        return self.search_results

    def get_app_by_name(self, app_name):

        apps = self.OS.get_all_apps()

        for app in apps:
            if app["name"] == app_name:
                return app