
import sys
from src.lib.indexer import Indexer
from src.lib.db_migration import DBMigration
from src.lib.os_handler import OSHandler
from src.models.meta import Meta

class API:

    OS = OSHandler()

    def run(self):

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

        sys.exit(0)