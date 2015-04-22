#!/usr/bin/env python

import re
import urllib
import random
import json
import time
from src.lib.os_handler import OSHandler
from src.models.app import App
from src.models.web_search_plugin import WebSearchPlugin
from src.models.searchables_plugin import SearchablesPlugin
from operator import itemgetter, attrgetter, methodcaller

import logging
logger = logging.getLogger('ducked')

class Search:

    OS = OSHandler()
    App = App()
    WebSearchPlugin = WebSearchPlugin()
    SearchablesPlugin = SearchablesPlugin()
    search_results = []

    def signal_input_changed(self, Window, widget):
        """Signal on change for text entry"""
        query = Window.entry.get_text()

        if len(query) > 0:

            search_results = self.search(query)

            if type(search_results) is dict:
                Window.switch_to_web(search_results["content"])
            else:

                Window.ensure_list_visibility()

                for index in range(0,6):
                    if index < len(search_results):
                        app = search_results[index]

                        Window.append_to_listview(app["name"], app["icon"], "", app["command"])
        else:
            Window.clear_listview()

    def signal_goto_first_result(self, query, ctrl_pressed):
        """Pressed enter on the input box, so go to first result"""
        self.search(query)

        # One result or a list?
        if type(self.search_results) is dict:
            self.launch_app(self.search_results, ctrl_pressed)

        # If it's a list, pick the first
        elif len(self.search_results) > 0:
            self.launch_app(self.search_results[0], ctrl_pressed)

    def signal_goto_app_name(self, app_name, ctrl_pressed):
        """Pressed enter on one of the listview items, so we've got an app name"""
        Application = App()
        app = Application.get_by_name(app_name)

        if app:
            self.launch_app(app, ctrl_pressed)

    def launch_app(self, app, ctrl_pressed):
        """The actual launching of the app"""

        if app and type(app) is dict:

            # Log usage to improve the search
            Application = App()
            Application.app_is_selected(app["name"])

            # Try to bring focus to the window, otherwise just launch it
            if ctrl_pressed == True or "source" not in app or app["source"] != "installed" or self.OS.focus_to_window(app["name"]) == "narp":
                self.OS.goto_app(app["command"])

    def search(self, query):
        """Search for anything the user wants"""

        # 4Channey?
        if query in ["/a/","/c/","/w/","/m/","/cgl/","/cm/","/f/","/n/","/jp/","/vp/","/v/","/vg/","/vr/","/co/","/g/","/tv/","/k/","/o/","/an/","/tg/","/sp/","/asp/","/sci/","/int/","/out/","/toy/","/biz/","/i/","/po/","/p/","/ck/","/ic/","/wg/","/mu/","/fa/","/3/","/gd/","/diy/","/wsg/","/trv/","/fit/","/x/","/lit/","/adv/","/lgbt/","/mlp/","/b/","/r/","/r9k/","/pol/","/soc/","/s4s/","/s/","/hc/","/hm/","/h/","/e/","/u/","/d/","/y/","/t/","/hr/","/gif/"]:
            self.search_results = self.search_4chan(query)

        # Dir/file kind of syntaxy goodness?
        elif re.search('^[~]*[/]+', query):
            self.search_results = self.search_dir(query)

        # Calculatey?
        elif re.search('^[\(\)0-9\. ]{1}[\(\)0-9\. +\/%\^\*\-]+[\(\)0-9\. ]{1}$', query):
            self.search_results = self.search_calculator(query)

        # Goto website
        elif re.search('^http[s]{0,1}:\/\/.+|[a-zA-Z]+\.[a-zA-Z]{2,5}', query):
            self.search_results = self.search_goto_website(query)

        # wotd
        elif re.search('^wotd$', query):

            self.search_results = {
                "content": "Wotd wotd?",
                "command": ""
            }
        elif re.search('^time\(\)$', query):
            self.search_results = self.search_unix_timestamp(query)

        # anti-boredom feature
        elif re.search('^b[o]+red$', query):
            self.search_results = self.search_anti_boredom(query)
        else:

            # Can we match on a web plugin?
            if self.match_for_web_plugin(query) == True:
                self.search_results = self.search_web_plugin(query)

            # Can we match on a searchable plugin?
            elif self.match_for_searchable_plugin(query) == True:
                self.search_results = self.search_searchable_plugin(query)

            # No match on plugins. Search for apps.
            else:
                # Have we found any apps?
                app_results = self.search_apps(query)
                if len(app_results) > 0:
                    self.search_results = app_results

                # No apps, so fallback to Google Search
                else:
                    self.search_results = self.search_fallback(query)

        return self.search_results

    def search_apps(self, query):

        apps = self.App.get_all()

        app_names = []
        app_findables = {}

        for app in apps:
            app_names.append(app["name"])
            app_findables[app["name"]] = app

        # Is it regexy?
        if re.search("^\^|^\[|\$$|\.[\*|+]|\|", query):

            app_results = []
            for app_name in app_names:
                if re.search(query.lower(), app_name.lower()):
                    result = (app_name,100)
                    app_results.append(result)
        # Otherwise do fuzzy search
        else:
            app_results = self.custom_search_extract(query, app_names, limit=7)

        # convert the list of names into a list of objects
        search_results = []

        ratio_best_hit = None

        for result in app_results:
            found_app_name = result[0]

            search_results.append(app_findables[found_app_name])

        search_results = sorted(search_results, key=itemgetter('selected'), reverse=True)
        return search_results

    def custom_search_algorithm(self, query, string):

        regular_search_regex = ".*"
        for character in query:
            regular_search_regex += character + ".*"

        word_search_regex = ".*"
        for character in query:
            word_search_regex += "[ \-_]+[" + character + "]+"
        word_search_regex += ".*"

        initials = "".join(re.findall("[A-Z]+", string))

        if re.match("^" + query, string, flags=re.IGNORECASE) != None:
            return 99
        if re.match(regular_search_regex, initials, flags=re.IGNORECASE) != None:
            return 85
        if query in string.lower():
            return 70
        if re.match(word_search_regex, string, flags=re.IGNORECASE) != None:
            return 60
        if re.match(regular_search_regex, string, flags=re.IGNORECASE) != None:
            return 50

        return 0

    def custom_search_extract(self, query, strings, limit):

        search_results = []

        for string in strings:
            ratio = self.custom_search_algorithm(query, string)
            if ratio > 0:
                search_results.append((string, ratio))

        search_results = sorted(search_results, key=itemgetter(1), reverse=True)

        return search_results[:limit]

    def match_for_web_plugin(self, query):
        self.web_plugin = self.WebSearchPlugin.search(query)
        if self.web_plugin != None:
            return True

        return False

    def search_web_plugin(self, query):
        query = re.sub(self.web_plugin["match"], "", query)
        query = re.sub(self.web_plugin["match_shorthand"], "", query)

        return [{
            "name": self.web_plugin["name"].replace("{query}", query),
            "command": self.OS.cwd() + "/bin/open_file " + self.web_plugin["url"].replace("{query}", urllib.quote_plus(query)),
            "icon": self.OS.cwd() + "/" + self.web_plugin["icon"]
        }]

    def match_for_searchable_plugin(self, query):
        self.searchable_plugin = self.SearchablesPlugin.search(query)
        if self.searchable_plugin != None:
            return True

        return False

    def search_searchable_plugin(self, query):
        query = re.sub(self.searchable_plugin["match"], "", query)
        query = re.sub(self.searchable_plugin["match_shorthand"], "", query)

        command = self.searchable_plugin["command"].replace("{query}", query)
        plugin_search_results = self.OS.run_command(self.OS.cwd() + "/" + command)
        return json.loads(plugin_search_results)

    def search_anti_boredom(self, query):
        logger.info("Awesooooome. Someone is bored! ^^")
        possible_time_spendature = [
            "https://en.wikipedia.org/wiki/List_of_common_misconceptions",
            "https://en.wikipedia.org/wiki/Out-of-place_artifact",
            "https://en.wikipedia.org/wiki/Category:Anomalous_weather",
            "https://en.wikipedia.org/wiki/List_of_people_who_disappeared_mysteriously",
            "https://boards.4chan.org/b/",
            "https://en.wikipedia.org/wiki/Turritopsis_dohrnii",
            "https://en.wikipedia.org/wiki/Ophiocordyceps_unilateralis",
            "https://www.youtube.com/watch?v=HEheh1BH34Q",
            "https://en.wikipedia.org/wiki/Megatherium",
            "https://en.wikipedia.org/wiki/Largest_organisms",
            "https://en.wikipedia.org/wiki/Largest_prehistoric_animals",
            "https://en.wikipedia.org/wiki/List_of_longest-living_organisms",
            "https://en.wikipedia.org/wiki/Common_misunderstandings_of_genetics",
            "https://xkcd.com",
            "https://en.wikipedia.org/wiki/List_of_backmasked_messages",
            "https://en.wikipedia.org/wiki/Spongiforma_squarepantsii",
            "https://en.wikipedia.org/wiki/Berlin_Gold_Hat",
            "https://en.wikipedia.org/wiki/Timeline_of_the_evolutionary_history_of_life",
            "https://en.wikipedia.org/wiki/Solid_oxygen",
            "http://m.space.com/19865-how-to-make-a-peanut-butter-and-honey-sandwich-in-space-video.html",
            "https://en.wikipedia.org/wiki/Alpheidae",
            "https://en.wikipedia.org/wiki/Scolopendra_gigantea",
            "http://hubblesite.org/gallery/album/",
            "http://space-facts.com/mars-panorama/",
            "https://en.wikipedia.org/wiki/Microraptor",
            "https://en.wikipedia.org/wiki/Archelon",
            "http://www.thesillywalk.com/",
            "http://planetarynames.wr.usgs.gov/Page/Planets"
        ]

        return [{
            "name": "Press enter.",
            "command": self.OS.cwd() + "/bin/open_file " + random.choice(possible_time_spendature),
            "icon": ""
        }]

    def search_goto_website(self, query):

        if re.search('^http[s]{0,1}:\/\/.+', query) == None:
            query = "http://" + query

        return [{
            "name": "goto " + query + "",
            "command": self.OS.cwd() + "/bin/open_file " + query,
            "icon": self.OS.cwd() + "/resources/icons/web.png"
        }]

    def search_calculator(self, query):
        fallback_search_results = self.search_apps("calculator")
        if len(fallback_search_results) > 0:
            fallback_command = fallback_search_results[0]
        else:
            fallback_command = ""

        return [{
            "name": self.OS.run_command('echo "scale=10; ' + query + '" | bc').strip(),
            "command": fallback_command,
            "icon": self.OS.cwd() + "/resources/icons/calc.png"
        }]

    def search_dir(self, query):
        return [{
            "name": "Open " + query,
            "command": self.OS.cwd() + "/bin/open_file " + query,
            "icon": self.OS.cwd() + "/resources/icons/dir.png"
        }]

    def search_4chan(self, query):
        return [{
             "name": "Go to " + query,
             "command": self.OS.cwd() + "/bin/open_file https://boards.4chan.org" + query,
             "icon": self.OS.cwd() + "/resources/icons/4chan.png"
         }]

    def search_unix_timestamp(self, query):

        return [{
            "name": int(time.time()),
            "command": "",
            "icon": ""
        }]

    def search_fallback(self, query):
        return [{
             "name": "Search for \"" + query + "\"",
             "command": self.OS.cwd() + "/bin/open_file https://www.google.com/search?q=" + urllib.quote_plus(query),
             "icon": self.OS.cwd() + "/resources/icons/google.png"
         }]