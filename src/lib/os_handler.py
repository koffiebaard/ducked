#!/usr/bin/env python

import os
import sys
import json
import re
from subprocess import Popen, PIPE

class OSHandler:

    installed_apps = []

    def get_all_apps(self):

        if len(self.installed_apps) == 0:
            self.get_installed_apps()
            self.get_apps_from_plugin("phpstorm")

        return self.installed_apps


    def get_installed_apps(self):
        if len(self.installed_apps) == 0:
            self.installed_apps = os.popen(self.cwd() + "/bin/get_installed_apps").read()

            if len(self.installed_apps) > 0:
                self.installed_apps = json.loads(self.installed_apps)

        return self.installed_apps

    def get_apps_from_plugin(self, plugin):

        plugin_apps = os.popen(self.cwd() + "/plugins/indexables/" + plugin).read()

        plugin_apps = json.loads(plugin_apps)
        self.installed_apps.extend(plugin_apps)
        return plugin_apps

    def focus_to_window(self, name):

        plugin_apps = os.popen(self.cwd() + "/bin/focus_to_window \"" + name + "\"").read()

        return plugin_apps.strip()

    def goto_app(self, command):
        command = re.sub(' %[a-zA-Z0-9]+', '', command)
        command += " &"

        if "--verbose" in sys.argv:
            print command

        os.popen(command)

    def run_command(self, command):

        if "--verbose" in sys.argv:
            print command

        return os.popen(command).read()

    def run_command_forked(self, command):
        command += " &"
        if "--verbose" in sys.argv:
            print command
        Popen(command, shell=True)

    def cwd(self):
        cwd = os.path.dirname(os.path.realpath(__file__)) + "/../.."
        return cwd

    def cleanup_logs(self):
        log_location = self.cwd() + "/message.log"
        last_n_lines = 3040
        self.run_command(self.cwd() + "/bin/cleanup_logs " + log_location + " " + str(last_n_lines))