#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

class TreeViewColumnExample:

    # close the window and quit
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def signal_goto(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def make_pb(self, tvcolumn, cell, model, iter):
        stock = model.get_value(iter, 1)
        pb = self.treeview.render_icon(stock, gtk.ICON_SIZE_MENU, None)
        cell.set_property('pixbuf', pb)
        return

    def __init__(self):
        # Create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("arr")

        self.window.connect("delete_event", self.delete_event)

        # list store
        self.liststore = gtk.ListStore(str, str, str, 'gboolean')
        self.treeview = gtk.TreeView(self.liststore)

        # Create column 1
        self.tvcolumn = gtk.TreeViewColumn('')
        self.treeview.append_column(self.tvcolumn)

        # Create column 2
        self.tvcolumn1 = gtk.TreeViewColumn('')
        self.treeview.append_column(self.tvcolumn1)


        # Render Icon
        self.cellpb = gtk.CellRendererPixbuf()
        self.cellpb.set_property('cell-background', '#ffffff')
        self.tvcolumn.pack_start(self.cellpb, False)
        self.tvcolumn.set_attributes(self.cellpb, stock_id=1)

        # Render App name
        self.cell = gtk.CellRendererText()
        self.cell.set_property('cell-background', '#ffffff')
        self.tvcolumn.pack_start(self.cell, True)
        self.tvcolumn.set_attributes(self.cell, text=0)

        # Render shortcut
        self.cell1 = gtk.CellRendererText()
        self.cell1.set_property('cell-background', '#ffffff')
        self.tvcolumn1.pack_start(self.cell1, True)
        self.tvcolumn1.set_attributes(self.cell1, text=2)

        # Dataaaa
        self.liststore.append(['Spotify', gtk.gdk.pixbuf_new_from_file("/home/tim-en-bren/apps/intellij/bin/idea.png"), u"\u23CE", True])
        self.liststore.append(['Ducked', gtk.gdk.pixbuf_new_from_file("/home/tim-en-bren/apps/intellij/bin/idea.png"), "", True])
        self.liststore.append(['Google Chrome', gtk.gdk.pixbuf_new_from_file("/home/tim-en-bren/apps/intellij/bin/idea.png"), "", False])

        print self.treeview.get_selection()

        self.window.add(self.treeview)

        self.window.show_all()

def main():
    gtk.main()

if __name__ == "__main__":
    tvcexample = TreeViewColumnExample()
    main()