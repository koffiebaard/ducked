#!/usr/bin/env python

class Search:

    def signal_changed(self, Widget, widget):
        """Signal on change for text entry"""
        query = Widget.entry.get_text()
        print query