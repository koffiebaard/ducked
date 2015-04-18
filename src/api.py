
import sys
from src.lib.indexer import Indexer
from src.lib.db_migration import DBMigration
from src.lib.os_handler import OSHandler
from src.models.meta import Meta
from src.models.app import App
from src.models.web_search_plugin import WebSearchPlugin

class API:

    OS = OSHandler()

    def run(self):

        if "--help" in sys.argv:

            MetaModel = Meta()
            url = MetaModel.get("app_url")["value"]

            print "Usage: ducked <flags>"
            print ""
            print("{: >20} {: >5} {: >10}".format(*["--version", "", "Version of the app"]))
            print("{: >20} {: >5} {: >10}".format(*["--reindex", "", "Reindex the apps and plugins"]))
            print("{: >20} {: >5} {: >10}".format(*["--migrate", "", "Update the DB to the newest version"]))
            print("{: >20} {: >5} {: >10}".format(*["--focus <title>", "", "Set focus to a window (part of window title)"]))
            print("{: >20} {: >5} {: >10}".format(*["--list-apps", "", "List all apps"]))
            print("{: >20} {: >5} {: >10}".format(*["--list-web", "", "List all web search plugins"]))
            print ""
            print "Report bugs through GitHub: " + url

        if "--reindex" in sys.argv:
            Index = Indexer()
            Index.index_apps()

        if "--migrate" in sys.argv:
            Migrate = DBMigration()
            Index = Indexer()
            Migrate.check_if_migration_is_needed()
            Index.index_apps()

        if "--version" in sys.argv or "-v" in sys.argv:

            MetaModel = Meta()
            name = MetaModel.get("app_name")["value"]
            version = MetaModel.get("version")["value"]
            description = MetaModel.get("app_description")["value"]
            author = MetaModel.get("author")["value"]
            author_email = MetaModel.get("author_email")["value"]
            url = MetaModel.get("app_url")["value"]

            if "--dude" in sys.argv:
                print version
            else:
                print name + " v" + version
                print description
                print ""
                print "Created by " + author + " (" + author_email + ")"
                print url

        if "--focus" in sys.argv and sys.argv[1] == "--focus" and len(sys.argv) > 2:
            window_name = sys.argv[2]
            self.OS.focus_to_window(window_name)

        if "--list-apps" in sys.argv:
            AppModel = App()

            apps = AppModel.get_all()

            for Application in apps:
                print Application["name"]

        if "--list-web" in sys.argv:
            WebSearchPluginModel = WebSearchPlugin()

            apps = WebSearchPluginModel.get_all()

            for Plugin in apps:
                row = [Plugin["match"], Plugin["match_shorthand"], Plugin["url"]]
                print("{: >15} {: >15} {: >20}".format(*row))

        # Done; finish up
        sys.exit(0)