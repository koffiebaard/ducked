#!/usr/bin/env python

import re, urllib, random, json

from src.lib.os_handler import OSHandler
# from src.lib.indexer import Indexer
from src.models.app import App
from src.models.web_search_plugin import WebSearchPlugin
from operator import itemgetter, attrgetter, methodcaller

import logging
logger = logging.getLogger('ducked')

try:
    # from fuzzywuzzy import fuzz
    from fuzzywuzzy import process
except ImportError:
    pass

class Search:

    OS = OSHandler()
    App = App()
    WebSearchPlugin = WebSearchPlugin()
    search_results = []

    def signal_changed(self, Window, widget):
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
        """Go to result"""
        self.search(query)

        # One result or a list?
        if type(self.search_results) is dict:
            self.launch_app(self.search_results, ctrl_pressed)

        # If it's a list, pick the first
        elif len(self.search_results) > 0:
            self.launch_app(self.search_results[0], ctrl_pressed)

    def signal_goto_app_name(self, app_name, ctrl_pressed):
        Application = App()
        app = Application.get_by_name(app_name)

        if app:
            self.launch_app(app, ctrl_pressed)

    def launch_app(self, app, ctrl_pressed):

        if app and type(app) is dict:
            # Try to bring focus to the window, otherwise just launch it
            if ctrl_pressed == True or "source" not in app or app["source"] != "installed" or self.OS.focus_to_window(app["name"]) == "narp":
                Application = App()
                Application.app_is_selected(app["name"])
                self.OS.goto_app(app["command"])

    def search(self, query):
        """Search for anything the user wants"""

        # is it a direct match to a 4chan board?
        if query in ["/a/","/c/","/w/","/m/","/cgl/","/cm/","/f/","/n/","/jp/","/vp/","/v/","/vg/","/vr/","/co/","/g/","/tv/","/k/","/o/","/an/","/tg/","/sp/","/asp/","/sci/","/int/","/out/","/toy/","/biz/","/i/","/po/","/p/","/ck/","/ic/","/wg/","/mu/","/fa/","/3/","/gd/","/diy/","/wsg/","/trv/","/fit/","/x/","/lit/","/adv/","/lgbt/","/mlp/","/b/","/r/","/r9k/","/pol/","/soc/","/s4s/","/s/","/hc/","/hm/","/h/","/e/","/u/","/d/","/y/","/t/","/hr/","/gif/"]:
            self.search_results = [{
                "name": "Go to " + query,
                "command": self.OS.cwd() + "/bin/open_file https://boards.4chan.org" + query,
                "icon": self.OS.cwd() + "/resources/icons/4chan.png"
            }]
        # is a dir/file kind of syntaxy goodness?
        elif re.search('^[~]*[/]+', query):
            self.search_results = [{
                "name": "Open " + query,
                "command": self.OS.cwd() + "/bin/open_file " + query,
                "icon": self.OS.cwd() + "/resources/icons/dir.png"
            }]
        # does this search query look particularly calculatey?
        elif re.search('^[\(\)0-9\. ]{1}[\(\)0-9\. +\/%\^\*\-]+[\(\)0-9\. ]{1}$', query):

            fallback_search_results = self.search_apps("calculator")
            if len(fallback_search_results) > 0:
                fallback_command = fallback_search_results[0]
            else:
                fallback_command = ""

            self.search_results = [{
                "name": self.OS.run_command('echo "scale=10; ' + query + '" | bc').strip(),
                "command": fallback_command,
                "icon": self.OS.cwd() + "/resources/icons/calc.png"
            }]
        elif re.search('^http[s]{0,1}:\/\/.+|[a-zA-Z]+\.[a-zA-Z]{2,5}', query):
            query = re.sub("^php ", "", query)

            if re.search('^http[s]{0,1}:\/\/.+', query) == None:
                query = "http://" + query

            self.search_results = [{
                "name": "goto " + query + "",
                "command": self.OS.cwd() + "/bin/open_file " + query,
                "icon": self.OS.cwd() + "/resources/icons/web.png"
            }]
        elif re.search('^sup$', query):
            spotify_whats_playing = self.OS.run_command(self.OS.cwd() + "/plugins/searchables/spotify_whats_playing")
            self.search_results = [{
                "name": spotify_whats_playing.strip(),
                "command": "",
                "icon": "spotify-client"
            }]
        elif re.search('^cb ', query):
            query = re.sub("^cb ", "", query)

            results = self.OS.run_command(self.OS.cwd() + "/plugins/searchables/search_chrome_bookmarks " + query)
            print json.loads(results.strip())
            self.search_results = json.loads(results)
        elif re.search('^wotd$', query):

            self.search_results = {
                "content": "Wotd wotd?",
                "command": ""
            }

        elif re.search('^b[o]+red$', query):

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
                "http://www.thesillywalk.com/"
            ]

            self.search_results = [{
                "name": "Press enter.",
                "command": self.OS.cwd() + "/bin/open_file " + random.choice(possible_time_spendature),
                "icon": ""
            }]
        else:

            # Can we match on a web plugin?
            web_plugin = self.WebSearchPlugin.search(query)
            if web_plugin != None:
                query = re.sub(web_plugin["match"], "", query)
                query = re.sub(web_plugin["match_shorthand"], "", query)
                self.search_results = [{
                    "name": web_plugin["name"].replace("{query}", query),
                    "command": self.OS.cwd() + "/bin/open_file " + web_plugin["url"].replace("{query}", urllib.quote_plus(query)),
                    "icon": self.OS.cwd() + "/" + web_plugin["icon"]
                }]
            # No match on plugins. Search for apps.
            else:
                app_results = self.search_apps(query)

                # Have we found any apps?
                if len(app_results) > 0:
                    self.search_results = app_results
                # No apps, so fallback to Google Search
                else:
                    self.search_results = [{
                       "name": "Search for \"" + query + "\"",
                       "command": self.OS.cwd() + "/bin/open_file https://www.google.com/search?q=" + urllib.quote_plus(query),
                       "icon": self.OS.cwd() + "/resources/icons/google.png"
                    }]

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
            print "arr"
            app_results = []
            for app_name in app_names:
                if re.search(query.lower(), app_name.lower()):
                    result = (app_name,100)
                    app_results.append(result)
        # Otherwise do fuzzy search (if the module is present)
        elif process:
            # just a list of names
            app_results = process.extract(query, app_names, limit=7)
        else:
            for app_name in app_names:
                if query.lower() in app_name.lower():
                    result = (app_name,100)
                    app_results.append(result)

        # convert the list of names into a list of objects
        search_results = []

        ratio_best_hit = None

        for result in app_results:
            found_app_name = result[0]
            ratio = result[1]

            if ratio_best_hit == None:
                ratio_best_hit = ratio

            if ratio > 60 and ratio > (ratio_best_hit - (ratio_best_hit / 3)) and (not " " in query or found_app_name[0:len(query)].lower() == query.lower()):
                search_results.append(app_findables[found_app_name])

        search_results = sorted(search_results, key=itemgetter('selected'), reverse=True)
        return search_results