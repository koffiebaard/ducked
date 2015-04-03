#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import pango
import os
from src.lib.os_handler import OSHandler

class Indexing:

    def destroy(self, widget, data=None):
        """Destroy all the things"""
        self.window.destroy()

    def shortcut_destroy(self, widget, AccelGroup, i, control_mask):
        """Destroy app through shortcut"""
        gtk.main_quit()

    def add_accelerator(self, widget, accelerator, callback):
        """Adds a keyboard shortcut"""
        if accelerator is not None:
            key, mod = gtk.accelerator_parse(accelerator)
            #widget.add_accelerator(signal, self.my_accelerators, key, mod, gtk.ACCEL_VISIBLE)
            self.my_accelerators.connect_group(key, mod, gtk.ACCEL_VISIBLE, callback)
            self.window.add_accel_group(self.my_accelerators)

    def draw(self):
        self.draw_window()
        self.draw_text()
        self.draw_logo()

        self.window.show_all()

    def remove(self):
        self.window.destroy()

    def draw_window(self):
        """Draw the indexing window"""
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        self.window.set_skip_taskbar_hint(True)

        self.window.connect("destroy", self.destroy)

        self.window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#ffffff"))
        self.window.set_border_width(10)
        self.window.set_size_request(350,100)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_title("Ducked")
        self.window.set_decorated(False)

        # We want the window at the top of the screen
        (x, y) = self.window.get_position()
        self.window.move(x, 150)

    def draw_text(self):

        self.indexing_buffer = gtk.TextBuffer()
        self.indexing_buffer.set_text("Sorry, we're indexing the apps installed on the system. Will take about 10-30 seconds.")

        self.indexing_textview = gtk.TextView()
        self.indexing_textview.set_buffer(self.indexing_buffer)
        self.indexing_textview.set_cursor_visible(False)
        self.indexing_textview.set_wrap_mode(gtk.WRAP_WORD)
        self.indexing_textview.set_editable(False)
        self.indexing_textview.set_justification(gtk.JUSTIFY_CENTER)

        # Taaaaable
        self.indexing_table = gtk.Table(2, 4, True)
        self.indexing_table.set_homogeneous(False)
        self.indexing_table.attach(self.indexing_textview, 0, 4, 1, 2)
        self.window.add(self.indexing_table)

    def draw_logo(self):

        OS = OSHandler()

        logo_pixbuf = gtk.gdk.pixbuf_new_from_file(OS.cwd() + "/../../icons/ducked.png")

        self.indexing_logo = gtk.Image()
        self.indexing_logo.set_from_pixbuf(logo_pixbuf)

        # Taaaaable
        self.indexing_table.attach(self.indexing_logo, 3, 4, 0, 1)

    def set_shortcuts_signals(self):
        """Set shortcuts & signals"""

        self.my_accelerators = gtk.AccelGroup()
        self.add_accelerator(self.window, "Escape", self.shortcut_destroy)
