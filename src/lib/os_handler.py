#!/usr/bin/env python

import os,json

class OSHandler:

    installed_apps = [];

    def get_installed_apps(self):

        if len(self.installed_apps) == 0:
            self.installed_apps = os.popen("bin/get_installed_apps").read()

            if len(self.installed_apps) > 0:
                self.installed_apps = json.loads(self.installed_apps)

        return self.installed_apps