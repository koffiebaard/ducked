#!/usr/bin/env python

import os,json
from subprocess import Popen, PIPE

cwd = os.path.dirname(os.path.realpath(__file__))

class OSHandler:

    installed_apps = []

    def get_all_apps(self):

        if len(self.installed_apps) == 0:
            self.get_installed_apps()
            self.get_apps_from_plugin("phpstorm")

        return self.installed_apps


    def get_installed_apps(self):
        if len(self.installed_apps) == 0:
            self.installed_apps = os.popen(cwd + "/../../bin/get_installed_apps").read()

            if len(self.installed_apps) > 0:
                self.installed_apps = json.loads(self.installed_apps)

        return self.installed_apps

    def get_apps_from_plugin(self, plugin):

        plugin_apps = os.popen(cwd + "/../../plugins/" + plugin).read()

        plugin_apps = json.loads(plugin_apps)
        self.installed_apps.extend(plugin_apps)
        return plugin_apps

    def goto_app(self, command):
        command += " &"
        print command
        os.popen(command)

    def run_command(self, command):
        print command
        return os.popen(command).read()

    def cwd(self):
        return os.path.dirname(os.path.realpath(__file__))