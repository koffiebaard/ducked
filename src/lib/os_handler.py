#!/usr/bin/env python

import os,json

class OSHandler:

    installed_apps = [];

    def get_all_apps(self):

        if len(self.installed_apps) == 0:
            self.get_installed_apps()
            self.get_apps_from_plugin("phpstorm")

        return self.installed_apps


    def get_installed_apps(self):

        if len(self.installed_apps) == 0:
            self.installed_apps = os.popen("bin/get_installed_apps").read()

            if len(self.installed_apps) > 0:
                self.installed_apps = json.loads(self.installed_apps)

        return self.installed_apps

    def get_apps_from_plugin(self, plugin):

            plugin_apps = os.popen("plugins/" + plugin).read()
            plugin_apps = json.loads(plugin_apps)
            self.installed_apps.extend(plugin_apps)

    def goto_app(self, command):
        command += " &"
        print command
        os.popen(command)