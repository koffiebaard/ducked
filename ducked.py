#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
from src.gui.search import Search
from src.gui.indexing import Indexing
from src.lib.indexer import Indexer
import sys

class Ducked:

    IndexingWindow = Indexing()
    SearchWindow = Search()
    Index = Indexer()

    def switchGUI(self):
        self.IndexingWindow.remove()
        self.SearchWindow.draw()

    def __init__(self):

        if self.Index.needs_synchronization():
            self.IndexingWindow.draw()

            self.Index.index_apps()

            self.IndexingWindow.remove()
            self.SearchWindow.draw()
        else:

            if "--reindex" in sys.argv:
                self.Index.index_apps()

            self.SearchWindow.draw()

    def main(self):
        gtk.main()


ThisIsSoDucked = Ducked()
ThisIsSoDucked.main()
