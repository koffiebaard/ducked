#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import pango

class DuckedUI:

    def callback(self, widget, data=None):
        print "arrrrr"

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        print "destroy all the things!"
        gtk.main_quit()

    def shortcut_destroy(self, widget, AccelGroup, i, control_mask):
        gtk.main_quit()

    def add_accelerator(self, widget, accelerator, signal="activate"):
        """Adds a keyboard shortcut"""
        if accelerator is not None:
            key, mod = gtk.accelerator_parse(accelerator)
            #widget.add_accelerator(signal, self.my_accelerators, key, mod, gtk.ACCEL_VISIBLE)
            self.my_accelerators.connect_group(key, mod, gtk.ACCEL_VISIBLE, self.shortcut_destroy)
            self.window.add_accel_group(self.my_accelerators)
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
    
        self.window.set_border_width(0)
        self.window.set_size_request(450,100) 
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_title("Ducked")
        self.window.set_decorated(False)

        # input box
        self.entry = gtk.Entry()
        self.entry.set_size_request(450,100)
        
        font_description = pango.FontDescription('Lucida Sans %s' % 36)
        self.entry.modify_font(font_description)

        self.window.add(self.entry)
        self.entry.show()
        
        self.my_accelerators = gtk.AccelGroup()
        self.add_accelerator(self.window, "Escape", signal="destroy")
        self.window.show()
        
    def main(self):
        gtk.main()

if __name__ == "__main__":
    arr= DuckedUI()
    arr.main()
