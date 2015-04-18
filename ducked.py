#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
from src.gui.search import Search
from src.gui.indexing import Indexing
from src.lib.indexer import Indexer
from src.lib.db_migration import DBMigration
import sys
from src.lib.log import Log

class Ducked:

    Index = Indexer()

    def __init__(self):

        CustomLog = Log()
        CustomLog.setup_custom_logger('ducked')

        # API stuff, no GUI
        if "--reindex" in sys.argv:
            self.Index.index_apps()
            sys.exit(0)
        if "--migrate" in sys.argv:
            Migrate = DBMigration()
            Migrate.check_if_migration_is_needed()
            self.Index.index_apps()
            sys.exit(0)
        # No API stuff, so do the GUI
        else:

            IndexingWindow = Indexing()
            SearchWindow = Search()

            if self.Index.needs_synchronization():
                IndexingWindow.draw()

                self.Index.index_apps()

                IndexingWindow.remove()
                SearchWindow.draw()
            else:
                SearchWindow.draw()

    def main(self):
        gtk.main()


ThisIsSoDucked = Ducked()
ThisIsSoDucked.main()
