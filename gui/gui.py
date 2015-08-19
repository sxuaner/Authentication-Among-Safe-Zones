#!/bin/python
# -*- coding: utf-8 -*-

from gi.repository import Gtk
import subprocess
import os.path

class ourwindow(Gtk.Window):

    def __init__(self):
        # Init the window
        Gtk.Window.__init__(self, title="Certificate Generator")
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
        This method creates makes a component for vertical box in format:
        
                   Name     ________

        Left is the label indicates what to fill in the entry on the right.

        Args:
            name: The name used for label to indicate what this entry's content.

        Returns:
           A horizontal box that contains a lable and an entry on the same line
        
        """
        # Init a horizontal box, hbox is short for horizental box.
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

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

    def packHboxToVbox(self, vbox, name):
        """
        This func packs a horizontal box whose name is specified by arg "name" into a vertical box.
        Used when we want to add 2 buttons on the same line.

        Args:
            vbox: the vertical box that we want to contain horizental boxes"
            name: par for hbox
        """
        hbox = self.createFields(name)  # Create all necessary fields
        vbox.pack_start(hbox, True, True, 0)

    def makeKeystoreBox(self, keystoreBox):
        # Create all necessary entries for keystore
        """
        To create a keystore, parameters that must be present:
	1. Alias
	2. Common name
	3. Store pass ( at least 6 characters, A FILE COUBE BE SELECTED, make a icon after  entry)
	4. Key pass ( at least 6 characters)

	Optional:
	key size

        """        
        self.packHboxToVbox(keystoreBox, "Common Name")
        self.packHboxToVbox(keystoreBox, "Store Pass")
        self.packHboxToVbox(keystoreBox, "Key Pass")
        
        # Add the folloing buttons to vbox
        button = Gtk.Button("Create a Key Store")
        button.connect("clicked", self.on_click_keystore_clicked)
        keystoreBox.pack_start(button, True, True, 0)


    def makeSigningBox(self, signingBox):
        # This entry display the path to selected signing ca.
        self.packHboxToVbox(signingBox, "CA's path")
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        signingBox.pack_start(hbox, True, True, 0)

        button = Gtk.Button("Select Ca")
        button.connect("clicked", self.on_file_clicked)
        hbox.pack_start(button, True, True, 0)

        button = Gtk.Button("Sign Req")
        button.connect("clicked", self.on_file_clicked)
        hbox.pack_start(button, True, True, 0)

    def makeClientCertBox(self, clientCertBox):

        self.packHboxToVbox(clientCertBox, "Save To")
        
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        clientCertBox.pack_start(hbox, True, True, 0)

        button = Gtk.Button("A Req")
        button.connect("clicked", self.on_file_clicked)
        hbox.pack_start(button, True, True, 0)

        button = Gtk.Button("Five Requests")
        button.connect("clicked", self.on_click_fivereqbutton_clicked)
        hbox.pack_start(button, True, True, 0)

    def makeShowBox(self, showBox):
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        showBox.pack_start(hbox, True, True, 0)

        button = Gtk.Button("Show Cert")
        button.connect("clicked", self.on_click_show_clicked)
        hbox.pack_start(button, True, True, 0)
        
    def layout(self):
        """
        The overall layout control func
        The GUI is divieded into 4 parts:

        Top-left: keystoreBox, used to create a keystore
        Bottom-left: signingBox : used to sign cert and concatenate certs as a trust-chain.

        Top-right: clientCertBox, used to make client certificates.
        Bottom-right: showBox, used to show the content of a given keystore/cert by selecting.

        Here is how we pack all the boxes:
           The top level is a horizontal box that contains two vertical boxes.
           Each of those 2 vertical boxes has 2 parts with a horizontal separator
        
        It should look like this in the end:
        -------
        |  |  |
        |--|--|
        |  |  |
        -------

        For each box, We also need a label to indicate the purpose.

        For now, we leave the bottom-left block empty
        """
        
        # This 2 separators will be used repeatedly
        hsep = Gtk.HSeparator()
        vsep = Gtk.VSeparator()

        # The top level box
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        """
        The spacing arg controls how far the fieds are from each other.
        
        keystorebox stores all widgets to make a keystore
        """
        
        leftVerticalBox =  Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        rightVerticalBox =  Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        # Components in left vertical box
        keystoreBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        signingBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        # Components in right vertical box
        clientCertBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        showBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        # Pack keystore box, 
        label = Gtk.Label("Keystore", width_chars = 40 )
        leftVerticalBox.pack_start(label, True, True, 0)
        leftVerticalBox.pack_start(keystoreBox, True, True, 0)
        leftVerticalBox.pack_start(hsep, True, True, 0)
        # Pack the signing box
        label = Gtk.Label("Signing", width_chars = 40)
        leftVerticalBox.pack_start(label, True, True, 0)
        leftVerticalBox.pack_start(signingBox, True, True, 0)
        
        # clientCertBox
        label = Gtk.Label("Client Certs", width_chars = 40)
        rightVerticalBox.pack_start(label, True, True, 0)
        rightVerticalBox.pack_start(clientCertBox, True, True, 0)
        # rightVerticalBox.pack_start(hsep, True, True, 0)

        # showBox
        label = Gtk.Label("Display", width_chars = 40 )
        rightVerticalBox.pack_start(label, True, True, 0)
        rightVerticalBox.pack_start(showBox, True, True, 0)
        
        # Pack 2 vertical boxes
        hbox.pack_start(leftVerticalBox, True, True, 0)
        hbox.pack_start(vsep, True, True, 0)
        hbox.pack_start(rightVerticalBox, True, True, 0)
        self.box.pack_start(hbox, True, True, 0)

        # Call functions to construct all those boxes.
        self.makeKeystoreBox(keystoreBox)
        self.makeSigningBox(signingBox)
        self.makeClientCertBox(clientCertBox)
        self.makeShowBox(showBox)
        
   
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
    """
    This is part of the file selection code. Kind of standard. No need to change normally.
    """
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
