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
  
        # Pack a vertical box into hbox
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=50)
        self.hbox.pack_start(vbox, True, True, 0)

        # Init a horizontal box
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        vbox.pack_start(hbox, True, True, 0)

        # Pack a label and an entry into vbox
        label = Gtk.Label(name, width_chars = 15 )
        self.entry = Gtk.Entry()
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(self.entry, True, True, 0)

        return(self.entry)
    
    def addButton(self):
        button = Gtk.Button("Create")
        button.connect("clicked", self.on_click_button_clicked)
        self.hbox.pack_start(button, True, True, 0)
        
    def on_click_button_clicked(self,button):
       for i in self.info:
           if(i.get_text()):     # Empty check
               print i.get_text()
           else:
               print "Empty value!"

    def collectInfo(self, dn, comn, coun, e, val):
        self.info = [dn, comn, coun, e, val]
        
        
if __name__ == "__main__":
    
    window = ourwindow()

    dn = window.createFields("Domain")
    comn = window.createFields("Common Name")
    coun = window.createFields("Country")
    e = window.createFields("Email")
    val = window.createFields("Validity")

    window.addButton()
    window.collectInfo(dn, comn, coun, e, val)
    
    window.connect("delete-event", Gtk.main_quit)
    window.show_all()
    Gtk.main()
