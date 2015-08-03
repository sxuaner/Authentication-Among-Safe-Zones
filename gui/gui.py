#!/bin/python
# -*- coding: utf-8 -*-

from gi.repository import Gtk

class ourwindow(Gtk.Window):

    def __init__(self):
        # Init the window
        Gtk.Window.__init__(self, title="Client Certificate Generator")
        self.set_border_width(10)

        # Init a gtk box
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=0)
        self.add(self.hbox)

    def createFields(self, name):
        # Init a listbox
        inputbox = Gtk.ListBox()
        inputbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.hbox.pack_start(inputbox, True, True, 0)

        # Init a row 
        row = Gtk.ListBoxRow()
  
        # Init a horizontal box
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        # Pack a vertical box into hbox
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=50)
        self.hbox.pack_start(vbox, True, True, 0)
        # Pack a label and an entry into vbox
        label = Gtk.Label(name, width_chars = 15 )
        entry = Gtk.Entry()
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(entry, True, True, 0)

        # Add the row to the list box
        inputbox.add(row)
            

if __name__ == "__main__":
    
    window = ourwindow()
    window.createFields("Domain Name")
    window.createFields("Common Name")
    window.createFields("Country Name")
    window.createFields("Email")
    window.connect("delete-event", Gtk.main_quit)
    window.show_all()
    Gtk.main()
