#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import pango
from src.lib.search import Search

class DuckedUI:

    def destroy(self, widget, data=None):
        """Destroy all the things"""
        print "destroy all the things!"
        gtk.main_quit()

    def shortcut_destroy(self, widget, AccelGroup, i, control_mask):
        """Destroy app through shortcut"""
        gtk.main_quit()

    def signal_changed(self,widget):
        """Signal on change for text entry"""
        DuckedSearch = Search()
        DuckedSearch.signal_changed(self, widget)

    def add_accelerator(self, widget, accelerator, callback):
        """Adds a keyboard shortcut"""
        if accelerator is not None:
            key, mod = gtk.accelerator_parse(accelerator)
            #widget.add_accelerator(signal, self.my_accelerators, key, mod, gtk.ACCEL_VISIBLE)
            self.my_accelerators.connect_group(key, mod, gtk.ACCEL_VISIBLE, callback)
            self.window.add_accel_group(self.my_accelerators)

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        self.window.connect("destroy", self.destroy)

        self.window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#f0f0f0"))
        self.window.set_border_width(10)
        self.window.set_size_request(650,100)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_title("Ducked")
        self.window.set_decorated(False)

        # input box
        self.entry = gtk.Entry()
        self.entry.set_size_request(450,100)

        self.entry.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#f0f0f0"))
        self.entry.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#f0f0f0"))
        self.entry.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse("#22352c"))
        self.entry.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#22352c"))

        font_description = pango.FontDescription('Lucida Sans %s' % 36)
        self.entry.modify_font(font_description)
        self.entry.set_inner_border(None);
        self.entry.set_has_frame(0);

        # Wrap input box for styling
        self.entry_box = gtk.EventBox()
        self.entry_box.add(self.entry)
        self.window.add(self.entry_box)

        # Shortcuts & Signals
        self.my_accelerators = gtk.AccelGroup()
        self.add_accelerator(self.window, "Escape", self.shortcut_destroy)

        # on change for text entry
        self.entry.connect("changed", self.signal_changed)

        # Show the app
        self.window.show_all()

    def main(self):
        gtk.main()

if __name__ == "__main__":
    arr= DuckedUI()
    arr.main()
