#!/bin/python
# -*- coding: utf-8 -*-

from gi.repository import Gtk

class ourwindow(Gtk.Window):

    def __init__(self):
        # Init the window
        Gtk.Window.__init__(self, title="Client Certificate Generator")
        self.set_default_size(500,300 )
        self.set_border_width(10)

        # Init a gtk box
        hbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=50)
        self.add(hbox)

        # Init a listbox
        inputbox = Gtk.ListBox()
        inputbox.set_selection_mode(Gtk.SelectionMode.NONE)
        hbox.pack_start(inputbox, True, True, 0)

        # Init a row 
        row = Gtk.ListBoxRow()

        # Init a horizontal box
        hbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        row.add(hbox)
        # Pack a vertical box into hbox
        vbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox.pack_start(vbox, True, True, 0)
        # Pack a label and an entry into vbox
        label = Gtk.Label("Domain Name", width_chars = 15 )
        entry = Gtk.Entry(xalign = 1)
        vbox.pack_start(label, True, True, 0)
        vbox.pack_start(entry, True, True, 0)

        # Add the row to the list box
        inputbox.add(row)

        
        # Init a row 
        row = Gtk.ListBoxRow()

        # Init a horizontal box
        hbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        row.add(hbox)
        # Pack a vertical box into hbox
        vbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox.pack_start(vbox, True, True, 0)
        # Pack a label and an entry into vbox
        label = Gtk.Label("Common Name", width_chars = 15 )
        entry = Gtk.Entry(xalign = 1)
        vbox.pack_start(label, True, True, 0)
        vbox.pack_start(entry, True, True, 0)

        # Add the row to the list box
        inputbox.add(row)



        # Init a row 
        row = Gtk.ListBoxRow()

        # Init a horizontal box
        hbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        row.add(hbox)
        # Pack a vertical box into hbox
        vbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox.pack_start(vbox, True, True, 0)
        # Pack a label and an entry into vbox
        label = Gtk.Label("Country Name", width_chars = 15 )
        entry = Gtk.Entry(xalign = 1)
        vbox.pack_start(label, True, True, 0)
        vbox.pack_start(entry, True, True, 0)

        # Add the row to the list box
        inputbox.add(row)

        
        # Init a row 
        row = Gtk.ListBoxRow()

        # Init a horizontal box
        hbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        row.add(hbox)
        # Pack a vertical box into hbox
        vbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox.pack_start(vbox, True, True, 0)
        # Pack a label and an entry into vbox
        label = Gtk.Label("Email", width_chars = 15 )
        entry = Gtk.Entry()
        vbox.pack_start(label, True, True, 0)
        vbox.pack_start(entry, True, True, 0)

        # Add the row to the list box
        inputbox.add(row)


window = ourwindow()        
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()
