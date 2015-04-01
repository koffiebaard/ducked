#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import pango
from src.lib.search import Search

class DuckedUI:

    Search = Search()

    def destroy(self, widget, data=None):
        """Destroy all the things"""
        print "destroy all the things!"
        gtk.main_quit()

    def shortcut_destroy(self, widget, AccelGroup, i, control_mask):
        """Destroy app through shortcut"""
        gtk.main_quit()

    def signal_changed(self,widget):
        """Signal on change for text entry. Searches for apps."""
        self.Search.signal_changed(self, widget)

    def signal_goto(self, widget):
        """App selection through enter key on textview"""
        print "go by textview"
        query = self.entry.get_text()
        self.Search.signal_goto_first_result(query)
        gtk.main_quit()

    def signal_enter_key(self, widget, event):
        """App selection through enter key on listview."""
        if event.keyval == 65293:
            (model, iter) = self.treeview.get_selection().get_selected()
            if iter:
                print "go by window enter"
                app_name = model.get_value(iter, 0)
                self.Search.signal_goto_app_name(app_name)
                gtk.main_quit()
                return True
        return False

    def add_accelerator(self, widget, accelerator, callback):
        """Adds a keyboard shortcut"""
        if accelerator is not None:
            key, mod = gtk.accelerator_parse(accelerator)
            #widget.add_accelerator(signal, self.my_accelerators, key, mod, gtk.ACCEL_VISIBLE)
            self.my_accelerators.connect_group(key, mod, gtk.ACCEL_VISIBLE, callback)
            self.window.add_accel_group(self.my_accelerators)

    def draw_window(self):
        """Draw the main window"""
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        self.window.connect("destroy", self.destroy)

        self.window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#ffffff"))
        self.window.set_border_width(10)
        self.window.set_size_request(650,-1)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_title("Ducked")
        self.window.set_decorated(False)

        # We want the window at the top of the screen
        (x, y) = self.window.get_position()
        self.window.move(x, 150)

    def draw_searchbox(self):
        """Draw the search box on the window"""

        self.entry = gtk.Entry()
        self.entry.set_size_request(650,100)

        self.entry.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#ffffff"))
        self.entry.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#ffffff"))
        self.entry.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse("#22352c"))
        self.entry.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#22352c"))

        font_description = pango.FontDescription('Lucida Sans %s' % 36)
        self.entry.modify_font(font_description)
        self.entry.set_inner_border(None)
        self.entry.set_has_frame(0)

        # Wrap input box for styling
        self.table = gtk.Table(1, 2, True)
        self.table.set_homogeneous(False)
        self.table.attach(self.entry, 0, 1, 0, 1)
        self.window.add(self.table)
        self.window.set_focus(self.entry)

    def draw_listview(self):

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
        font_description = pango.FontDescription('Lucida Sans %s' % 21)
        self.cell.set_property('font-desc', font_description)
        self.cell.set_property('cell-background', '#ffffff')
        self.cell.set_property('foreground', '#525252')
        self.tvcolumn.pack_start(self.cell, True)
        self.tvcolumn.set_attributes(self.cell, text=0)

        # Render shortcut
        self.cell1 = gtk.CellRendererText()
        self.cell1.set_property('cell-background', '#ffffff')
        self.tvcolumn1.pack_start(self.cell1, True)
        self.tvcolumn1.set_attributes(self.cell1, text=2)

        self.treeview.set_headers_visible(False)

        self.tvcolumn.set_resizable(True)
        self.tvcolumn1.set_resizable(True)

        self.treeview.set_cursor(0)
        self.treeview.get_selection().set_mode(gtk.SELECTION_BROWSE)
        self.window.connect('key-press-event', self.signal_enter_key)

        self.table.attach(self.treeview, 0, 1, 1, 2)
        self.window.resize(1,1)

    def remove_listview(self):
        if hasattr(self, "treeview"):
            self.table.remove(self.treeview)
        self.window.resize(1,1)

    def redraw_listview(self):
        self.remove_listview()
        self.draw_listview()

    def clear_listview(self):
        self.liststore.clear()
        self.treeview.hide()
        self.window.resize(1,1)
        self.window.resize(1,1)

    def append_to_listview(self, app_name, image_path, shortcut, command):
        self.treeview.show()
        self.liststore.append([app_name, gtk.gdk.pixbuf_new_from_file(image_path), shortcut, True])

    def set_shortcuts_signals(self):
        """Set shortcuts & signals"""

        self.my_accelerators = gtk.AccelGroup()
        self.add_accelerator(self.window, "Escape", self.shortcut_destroy)

        # on change for text entry
        self.entry.connect("changed", self.signal_changed)

        # on submit for text entry
        self.entry.connect("activate", self.signal_goto)

        self.treeview.get_selection().connect("changed", self.signal_goto)

    def __init__(self):

        self.draw_window()
        self.draw_searchbox()
        self.draw_listview()
        self.clear_listview()

        self.set_shortcuts_signals()

        self.window.show_all()

    def main(self):
        gtk.main()

if __name__ == "__main__":
    arr= DuckedUI()
    arr.main()
