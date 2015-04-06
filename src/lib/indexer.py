#!/usr/bin/env/python


from src.lib.os_handler import OSHandler
from src.models.app import App
from src.models.meta import Meta
import logging
logger = logging.getLogger('ducked')

class Indexer:

    OS = OSHandler()
    Meta = Meta()

    def check_synchronization(self):

        if self.needs_synchronization():
            self.index_apps()

    def needs_synchronization(self):

        initial_sync_completed = self.Meta.get("initial_sync_completed")
        if initial_sync_completed == None or initial_sync_completed["value"] == 0:
            logger.info("Initial sync required.")
            return True
        else:
            return False

    def index_apps(self):

        logger.info("Begin indexing apps.")
        self.index_installed_apps()
        self.index_plugin_apps()
        self.Meta.set("initial_sync_completed", 1)
        logger.info("Finish indexing apps.")
        self.OS.cleanup_logs()

    def index_installed_apps(self):
        installed_apps = self.OS.get_installed_apps()

        for app in installed_apps:
            Application = App()

            if Application.get_by_name(app["name"]) == None:
                Application.name = app["name"]
                Application.icon = app["icon"]
                Application.command = app["command"]
                Application.source = "installed"
                Application.save()

    def index_plugin_apps(self):
        plugin = "phpstorm"

        plugin_apps = self.OS.get_apps_from_plugin(plugin)

        if plugin_apps != None:
            for app in plugin_apps:
                Application = App()

                if Application.get_by_name(app["name"]) == None:
                    Application.name = app["name"]
                    Application.icon = app["icon"]
                    Application.command = app["command"]
                    Application.source = plugin
                    Application.save()