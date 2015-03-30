#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

class DuckedUI:

    def callback(self, widget, data=None):
        print "arrrrr"

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        print "destroy all the things!"
        gtk.main_quit()

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
    
        self.window.set_border_width(0)
        self.window.set_size_request(450,100) 
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_title("Ducked")

        # input box
        self.entry = gtk.Entry()
        self.window.add(self.entry)
        self.entry.show()
 
        self.window.show()

    def main(self):
        gtk.main()

if __name__ == "__main__":
    arr= DuckedUI()
    arr.main()
