#!/bin/python
# -*- coding: utf-8 -*-

from gi.repository import Gtk
import subprocess
import os.path

class ourwindow(Gtk.Window):

    def __init__(self):
        # Init the window
        Gtk.Window.__init__(self, title="Client Certificate Generator")
        self.set_border_width(10)

        # Init a gtk box, spacing controls how far each components stays from each other
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.add(self.box)
        # List for storing the entry objects
        self.entries = []
        # dict for storing field names
        self.info = dict()
        # list for storing names of users
        self.names = []

    def createFields(self, name):
        """
        This method create an entry for inputing data needed for generating certs.

        Args:
            name: The name used for label to indicate what this entry's content.
        
        """
        # Init a horizontal box, hbox is short for horizental box.
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=80)

        # Pack a label and an entry. The label has char with 15 for aligning lines
        label = Gtk.Label(name, width_chars = 15 )
        entry = Gtk.Entry()
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(entry, True, True, 0)

        # Append the entry to information list. This is used later for refreshing the entries.
        self.entries.append(entry)
        self.names.append(name)
        self.info[name] = entry.get_text()
        return hbox


    def packHboxToVbox(self, vbox, name):
        """
        This func packs a hbox whose name is specified by arg "name" into vbox

        Args:
            vbox: the vertical box that we want to contain horizental boxes"
            name: par for hbox
        """
        hbox = self.createFields(name)  # Create all necessary fields
        vbox.pack_start(hbox, True, True, 0)
        
    def layout(self):
        """
        The overall layout control func
        """
        # The spacing arg controls how far the fieds are from each other.
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        label = Gtk.Label("123", width_chars = 15 )

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox.pack_start(vbox, True, True, 0)
        hbox.pack_start(label, True, True, 0)
        
        self.box.pack_start(hbox, True, True, 0)

        # Create all necessary fields, and pack into a vertical box.
        self.packHboxToVbox(vbox, "Common Name")
        self.packHboxToVbox(vbox, "Store Pass")
        self.packHboxToVbox(vbox, "Key Size")
        self.packHboxToVbox(vbox, "Validity")
        self.packHboxToVbox(vbox, "Domain")
        self.packHboxToVbox(vbox, "Country Code")
        self.packHboxToVbox(vbox, "Email")
        self.packHboxToVbox(vbox, "Key Pass")
        self.packHboxToVbox(vbox, "CA's Path")

        # Add the folloing buttons to vbox
        button = Gtk.Button("Key Store")
        button.connect("clicked", self.on_click_keystore_clicked)
        vbox.pack_start(button, True, True, 0)

        button = Gtk.Button("Show Cert")
        button.connect("clicked", self.on_click_show_clicked)
        vbox.pack_start(button, True, True, 0)

        button = Gtk.Button("Select Ca")
        button.connect("clicked", self.on_file_clicked)
        vbox.pack_start(button, True, True, 0)

        # We want to Put " a request" and " five requests" on the same row, so a hbox is used
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing= 1)
        vbox.pack_start(hbox, True, True, 0)
        
        button = Gtk.Button("A Request")
        button.connect("clicked", self.on_click_reqbutton_clicked)
        hbox.pack_start(button, True, True, 0)

        button = Gtk.Button("Five Requests")
        button.connect("clicked", self.on_click_fivereqbutton_clicked)
        hbox.pack_start(button, True, True, 0)

    # def createButtons(self):
    #     """
    #     Func to create all needed buttons. SHould be optimized.
    #     """
    #     # Create a vertical box
    #     vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing= 1)
    #     self.box.pack_start(vbox, True, True, 0)

    #     # Add the folloing buttons to vbox
    #     button = Gtk.Button("Key Store")
    #     button.connect("clicked", self.on_click_keystore_clicked)
    #     vbox.pack_start(button, True, True, 0)

    #     button = Gtk.Button("Show Cert")
    #     button.connect("clicked", self.on_click_show_clicked)
    #     vbox.pack_start(button, True, True, 0)

    #     button = Gtk.Button("Select Ca")
    #     button.connect("clicked", self.on_file_clicked)
    #     vbox.pack_start(button, True, True, 0)

    #     # We want to Put " a request" and " five requests" on the same row, so a hbox is used
    #     hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing= 1)
    #     vbox.pack_start(hbox, True, True, 0)
        
    #     button = Gtk.Button("A Request")
    #     button.connect("clicked", self.on_click_reqbutton_clicked)
    #     hbox.pack_start(button, True, True, 0)

    #     button = Gtk.Button("Five Requests")
    #     button.connect("clicked", self.on_click_fivereqbutton_clicked)
    #     hbox.pack_start(button, True, True, 0)
        

    def updateEntries(self):
        """
        To update the current content of all entries when it's called
        """
        print "\n\n ------------ "
        for entry, name in zip(self.entries, self.names):

            tmp = entry.get_text()
            self.info[name] = tmp
            if tmp:
                print '{0:20s} {1:20}'.format(name, tmp)
            else:
                print '{0:20} {1:20}'.format(name, "Empty Value")
        print " ------------ \n\n "

    def on_click_keystore_clicked(self, button):
        # Update the info put in field
        self.updateEntries()

        # @par -alias: specify the alias name of the key pair
        # @par -dname :
        # @par -genkeypari: Generates a key pair (a public key and associated private key).
        # @par -keystore: tell keytool where to place the keystore file:
        #                 in top level of the project folder
        # @par -keysize: the length of the key.

        # If key size is not told. Use default 2058
        if not self.info["Key Size"]:
            self.info["Key Size"]= 2048

        if not os.path.exists("../keystore"):
            if self.info["Common Name"]:
                if self.info["Alias"]:
                    par = ["/bin/keytool",
                           "-genkeypair",
                           "-alias", str( self.info["Alias"]),
                           "-dname", str("CN=" + self.info["Common Name"]),
                           "-keystore", "../keystore",
                           "-keysize", str(self.info["Key Size"]),
                           "-keypass", str(self.info["Key Pass"]),
                           "-storepass", str(self.info["Store Pass"])
                    ]
                    subprocess.Popen(par)
                else:
                    print "Alias is not provided"
            else:
                print "Common Name is not provided"
        else:
            print "Your keystore has already been created! You can find it in the top directory."

    def on_click_reqbutton_clicked(self, button):
        self.updateEntries()

        # Make sure folder ./clientCerts exist.
        if not os.path.exists("../clientCerts"):
            par = ["mkdir",
                   "-p", "../clientCerts"
            ]
            subprocess.Popen(par)

        # @par:
        #  -certreq: make a cert request
        #  -alias: alias name used in key store
        #  -file: output file
        #  -keystore Path to keystore
        #  -storepass , self-explained

        par = ["/bin/keytool",
               "-certreq",
               "-alias", str( self.info["Alias"]),
               "-file", str( "../clientCerts/"+ self.info["Common Name"]+".pem"),
               "-keystore", "../keystore",
               "-storepass", str(self.info["Store Pass"])
        ]
        subprocess.Popen(par)

    def on_click_fivereqbutton_clicked(self, button):
        self.updateEntries()

        # To make sure the dir exists
        if not os.path.exists("../clientCerts"):
            par = ["mkdir",
                   "-p", "../clientCerts"
            ]
            subprocess.Popen(par)

        # Make 5 certs based on common name
        for i in range(0,5):
            par = ["/bin/keytool",
                   "-certreq",
                   "-alias", str( self.info["Alias"]),
                   "-file", str( "../clientCerts/" + self.info["Common Name"]+ str(i) + ".pem"),
                   "-keystore", "../keystore",
                   "-storepass", str(self.info["Store Pass"])
            ]
            subprocess.Popen(par)

    

    def on_click_show_clicked(self,button):
        self.updateEntries()

        # @par -list: argument to list the content of a keystore
        # @par -keystore: where to find target keystore, followed by the path.
        par = ["/bin/keytool",
               "-list",
               "-keystore", "../keystore",
               "-storepass", str(self.info["Store Pass"])
        ]
        subprocess.Popen(par)

##################### This part belongs to file selection window ######################
    def on_file_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a file", self,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            print("File selected: " + dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Text files")
        filter_text.add_mime_type("text/plain")
        dialog.add_filter(filter_text)

        filter_py = Gtk.FileFilter()
        filter_py.set_name("Python files")
        filter_py.add_mime_type("text/x-python")
        dialog.add_filter(filter_py)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

    def on_folder_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a folder", self,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             "Select", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Select clicked")
            print("Folder selected: " + dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")
        dialog.destroy()
###################### End of file selection window ######################        
    
if __name__ == "__main__":
    window = ourwindow()
    window.layout()
    window.connect("delete-event", Gtk.main_quit)
    window.show_all()
    Gtk.main()
