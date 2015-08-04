#!/bin/python
# -*- coding: utf-8 -*-

from gi.repository import Gtk
import subprocess

class ourwindow(Gtk.Window):

    def __init__(self):
        # Init the window
        Gtk.Window.__init__(self, title="Client Certificate Generator")
        self.set_border_width(10)

        # Init a gtk box
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=0)
        self.add(self.box)
        # List for storing the entry objects
        self.entries = []
        # dict for storing field names
        self.info = dict()
        # list for storing names
        self.names = []

    def createFields(self, name):

        # Pack a vertical box into hbox
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=50)
        self.box.pack_start(vbox, True, True, 0)

        # Init a horizontal box
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        vbox.pack_start(hbox, True, True, 0)

        # Pack a label and an entry into vbox
        label = Gtk.Label(name, width_chars = 15 )
        entry = Gtk.Entry()
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(entry, True, True, 0)

        # Append the entry to information list. This is used later for refreshing the entries.
        self.entries.append(entry)
        self.names.append(name)
        self.info[name] = entry.get_text()
        
        # button part
    def createButton(self):
        # A warning when some fields are empty should be made.
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing= 1)
        self.box.pack_start(vbox, True, True, 0)

        # Horizontal box for key pair and req buttons
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing= 1)
        vbox.pack_start(hbox, True, True, 0)
        
        button = Gtk.Button("Key Pair")
        button.connect("clicked", self.on_click_keybutton_clicked)
        hbox.pack_start(button, True, True, 0)
   
        button = Gtk.Button("Request")
        button.connect("clicked", self.on_click_reqbutton_clicked)
        hbox.pack_start(button, True, True, 0)

        # Hbox for show cert button
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing= 1)
        vbox.pack_start(hbox, True, True, 0)
        
        button = Gtk.Button("Show Cert")
        button.connect("clicked", self.on_click_reqbutton_clicked)
        hbox.pack_start(button, True, True, 0)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing= 1)
        vbox.pack_start(hbox, True, True, 0)

    def updateEntries(self):
        print "\n\n ------------ "
        for entry, name in zip(self.entries, self.names):
            tmp = entry.get_text()
            if tmp:
                self.info[name] = tmp
                print tmp
            else:
                print name, " Empty value "
        print " ------------ \n\n "

        #  on_click event part
    def on_click_keybutton_clicked(self, button):
        # Update the info put in field
        self.updateEntries()
        par = ["/bin/keytool", "-alias", str( self.info["Alias"]), "-dname",  str("CN=" + self.info["Common Name"]), "-genkeypair", "-keystore", "../keystore"]
        subprocess.Popen(par)
        
    def on_click_reqbutton_clicked(self, button):
        self.updateEntries()
        par = ["/bin/keytool", ""]
                
        
    
if __name__ == "__main__":
    window = ourwindow()

    window.createFields("Alias")
    window.createFields("Common Name")
    window.createFields("Key Size")
    window.createFields("Validity")
    window.createFields("Domain")
    window.createFields("Country")
    window.createFields("Email")
    

    window.createButton()

    window.connect("delete-event", Gtk.main_quit)
    window.show_all()
    Gtk.main()
