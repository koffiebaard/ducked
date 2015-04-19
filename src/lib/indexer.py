#!/usr/bin/env/python


from src.lib.os_handler import OSHandler
from src.models.app import App
from src.models.meta import Meta
from os import listdir
from os.path import isfile, join
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

        # Mark all for deletion (update everything we can find, then delete the remainder)
        Application = App()
        Application.mark_all_for_deletion()

        # Index the installed apps
        self.index_installed_apps()

        # Index the indexable plugins
        self.index_plugin_apps()

        self.Meta.set("initial_sync_completed", 1)
        logger.info("Finish indexing apps.")

        # All done, remove the apps we didn't touch
        Application.mark_all_for_deletion()

        # Log can't grow too big, watch it for file size
        self.OS.cleanup_logs()

    def index_installed_apps(self):
        installed_apps = self.OS.get_installed_apps()

        for app in installed_apps:
            Application = App()
            Application.name = app["name"]
            Application.icon = app["icon"]
            Application.command = app["command"]
            Application.source = "installed"
            Application.marked_for_deletion = 0
            Application.save()

    def index_plugin_apps(self):
        plugin_path = self.OS.cwd() + "/plugins/indexables/"
        plugins = [ f for f in listdir(plugin_path) if isfile(join(plugin_path,f)) ]

        for plugin in plugins:
            plugin_apps = self.OS.get_apps_from_plugin(plugin)

            if plugin_apps != None:
                for app in plugin_apps:
                    Application = App()
                    Application.name = app["name"]
                    Application.icon = app["icon"]
                    Application.command = app["command"]
                    Application.source = plugin
                    Application.marked_for_deletion = 0
                    Application.save()