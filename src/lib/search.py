#!/usr/bin/env python

from src.lib.os_handler import OSHandler
from src.lib.indexer import Indexer
from src.models.app import App
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from operator import itemgetter, attrgetter, methodcaller
import re
import urllib
import random
import logging
import json
logger = logging.getLogger('ducked')

class Search:

    OS = OSHandler()
    App = App()
    search_results = []

    def signal_changed(self, Window, widget):
        """Signal on change for text entry"""
        query = Window.entry.get_text()

        if len(query) > 0:
            Window.redraw_listview()

            search_results = self.search(query)

            for index in range(0,6):
                if index < len(search_results):
                    app = search_results[index]

                    Window.append_to_listview(app["name"], app["icon"], "", app["command"])
        else:
            Window.clear_listview()

    def signal_goto_first_result(self, query):
        """Go to result"""
        self.search(query)

        if len(self.search_results) > 0:
            app = self.search_results[0]
            Application = App()
            Application.app_is_selected(app["name"])
            self.OS.goto_app(app["command"])

    def signal_goto_app_name(self, app_name):
        Application = App()
        app = Application.get_by_name(app_name)

        if app:
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
                "icon": self.OS.cwd() + "/icons/4chan.png"
            }]
        # is a dir/file kind of syntaxy goodness?
        elif re.search('^[~]*[/]+', query):
            self.search_results = [{
                "name": "Open " + query,
                "command": self.OS.cwd() + "/bin/open_file " + query,
                "icon": self.OS.cwd() + "/icons/dir.png"
            }]
        # does this search query look particularly calculatey?
        elif re.search('^[\(\)0-9\. ]{1}[\(\)0-9\. +\/%\^\*\-]+[\(\)0-9\. ]{1}$', query):

            fallback_search_results = self.search_apps("calculator")
            if len(fallback_search_results) > 0:
                fallback_command = fallback_search_results[0]
            else:
                fallback_command = ""

            self.search_results = [{
                "name": self.OS.run_command('echo "scale=10; ' + query + '" | bc'),
                "command": fallback_command,
                "icon": ""
            }]
        elif re.search('^github ', query) or re.search('^gh ', query):
            query = re.sub("^github ", "", query)
            query = re.sub("^gh ", "", query)
            self.search_results = [{
                "name": "Github to \"" + query + "\"",
                "command": self.OS.cwd() + "/bin/open_file https://github.com/search?q=" + urllib.quote_plus(query),
                "icon": self.OS.cwd() + "/icons/github.png"
            }]
        elif re.search('^maps ', query):
            query = re.sub("^maps ", "", query)
            self.search_results = [{
                "name": "Search Maps for \"" + query + "\"",
                "command": self.OS.cwd() + "/bin/open_file https://www.google.com/maps/search/" + urllib.quote_plus(query),
                "icon": self.OS.cwd() + "/icons/google.png"
            }]
        elif re.search('^wiki ', query):
            query = re.sub("^wiki ", "", query)
            self.search_results = [{
                "name": "Search Wiki for \"" + query + "\"",
                "command": self.OS.cwd() + "/bin/open_file https://en.wikipedia.org/w/index.php?search=" + urllib.quote_plus(query),
                "icon": self.OS.cwd() + "/icons/wiki.png"
            }]
        elif re.search('^youtube ', query) or re.search('^yt ', query):
            query = re.sub("^youtube ", "", query)
            query = re.sub("^yt ", "", query)
            self.search_results = [{
                "name": "Search YouTube for \"" + query + "\"",
                "command": self.OS.cwd() + "/bin/open_file https://www.youtube.com/results?search_query=" + urllib.quote_plus(query),
                "icon": self.OS.cwd() + "/icons/youtube.png"
            }]
        elif re.search('^twitter ', query) or re.search('^twit ', query):
            query = re.sub("^twit ", "", query)
            query = re.sub("^twitter ", "", query)
            self.search_results = [{
                "name": "Search The Twits for \"" + query + "\"",
                "command": self.OS.cwd() + "/bin/open_file https://twitter.com/search?q=" + urllib.quote_plus(query),
                "icon": self.OS.cwd() + "/icons/twitter.png"
            }]
        elif re.search('^gmail ', query):
            query = re.sub("^gmail ", "", query)
            self.search_results = [{
                "name": "Search Gmail for \"" + query + "\"",
                "command": self.OS.cwd() + "/bin/open_file https://mail.google.com/mail/#search/" + urllib.quote_plus(query),
                "icon": self.OS.cwd() + "/icons/gmail.png"
            }]
        elif re.search('^torrentz ', query) or re.search('^tz ', query):
            query = re.sub("^tz ", "", query)
            query = re.sub("^torrentz ", "", query)
            self.search_results = [{
                "name": "Search Torrentz for \"" + query + "\"",
                "command": self.OS.cwd() + "/bin/open_file https://torrentz.eu/search?q=" + urllib.quote_plus(query),
                "icon": self.OS.cwd() + "/icons/torrentz.png"
            }]
        elif re.search('^py2 ', query):
            query = re.sub("^py2 ", "", query)
            query = re.sub("^python ", "", query)
            self.search_results = [{
                "name": "Search Python 2 ref for \"" + query + "\"",
                "command": self.OS.cwd() + "/bin/open_file https://docs.python.org/2/search.html?q=" + urllib.quote_plus(query),
                "icon": self.OS.cwd() + "/icons/python.png"
            }]
        elif re.search('^py3 ', query):
            query = re.sub("^py3 ", "", query)
            self.search_results = [{
                "name": "Search Python 3 ref for \"" + query + "\"",
                "command": self.OS.cwd() + "/bin/open_file https://docs.python.org/3/search.html?q=" + urllib.quote_plus(query),
                "icon": self.OS.cwd() + "/icons/python.png"
            }]
        elif re.search('^phpref ', query):
            query = re.sub("^phpref ", "", query)
            self.search_results = [{
                "name": "Search PHP ref for \"" + query + "\"",
                "command": self.OS.cwd() + "/bin/open_file http://php.net/manual-lookup.php?pattern=" + urllib.quote_plus(query),
                "icon": self.OS.cwd() + "/icons/php.png"
            }]
        elif re.search('^http[s]{0,1}:\/\/.+', query):
            query = re.sub("^php ", "", query)
            self.search_results = [{
                "name": "goto " + query + "",
                "command": self.OS.cwd() + "/bin/open_file " + query,
                "icon": self.OS.cwd() + "/icons/web.png"
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
                "https://en.wikipedia.org/wiki/Archelon"
            ]

            self.search_results = [{
                "name": "Press enter.",
                "command": self.OS.cwd() + "/bin/open_file " + random.choice(possible_time_spendature),
                "icon": ""
            }]
        else:
            app_results = self.search_apps(query)

            if len(app_results) > 0:
                self.search_results = app_results
            else:
                self.search_results = [{
                   "name": "Search for \"" + query + "\"",
                   "command": self.OS.cwd() + "/bin/open_file https://www.google.com/search?q=" + urllib.quote_plus(query),
                   "icon": self.OS.cwd() + "/icons/google.png"
                }]

        return self.search_results

    def search_apps(self, query):

        apps = self.App.get_all()

        app_names = []
        app_findables = {}

        for app in apps:
            app_names.append(app["name"])
            app_findables[app["name"]] = app

        # just a list of names
        fuzzy_results = process.extract(query, app_names, limit=7)
        print fuzzy_results
        # convert the list of names into a list of objects
        search_results = []

        ratio_best_hit = None

        for result in fuzzy_results:
            found_app_name = result[0]
            ratio = result[1]

            if ratio_best_hit == None:
                ratio_best_hit = ratio

            if ratio > 60 and ratio > (ratio_best_hit - (ratio_best_hit / 3)) and (not " " in query or found_app_name[0:len(query)].lower() == query.lower()):
                search_results.append(app_findables[found_app_name])

        search_results = sorted(search_results, key=itemgetter('selected'), reverse=True)
        return search_results