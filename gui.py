#!/bin/python
# -*- coding: utf-8 -*-

from gi.repository import Gtk
import subprocess
import os.path

# Change the default admin password here.
STOREPASSWORD = "keystoreadmin"
CSRPATH = "clientCerts/csr/"

CERTPATH = "clientCerts/cert/"


KEYSTOREPATH = "keystore"


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

        self.popup = Gtk.Window()
        self.popup.set_title("CSR File selected")
        self.popup.set_border_width(10)
        self.popup.set_default_size(600,400)
        self.popup.set_modal(False)
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.popup.add(self.grid)

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

        """
        The following lines of code exports vairables with specified name as global variable, as such these exported variables can be accessed by "self.name"
        """
        if name == "Key Pass":
            self.keypass = entry
            self.keypass.set_visibility(False)

        if name == "Store Pass":
            self.storepass = entry
            self.storepass.set_visibility(False)
            self.storepass.set_text(STOREPASSWORD)
        if name == "CA's Path":
            self.capath = entry
            
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

        if not self.info["Alias"]:
            self.info["Alias"] = self.info["Common Name"]

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
        Alias
	key size

        When Alias is not given, use Common Name to search in keystore
        
        """
        label = Gtk.Label("Key Pair", width_chars = 15 )
        keystoreBox.pack_start(label,True,True,0)
        self.packHboxToVbox(keystoreBox, "Alias")
        self.packHboxToVbox(keystoreBox, "Common Name")
        self.packHboxToVbox(keystoreBox, "Org Name")
        self.packHboxToVbox(keystoreBox, "Key Pass")

        label = Gtk.Label("Optional", width_chars = 15 )
        keystoreBox.pack_start(label, True, True, 0)
        self.packHboxToVbox(keystoreBox, "Key Size")
        
        # Create a button for creating key pair
        button = Gtk.Button(" Key Pair")
        button.connect("clicked", self.on_click_keypair_clicked)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox.pack_start(button, True, True, 0)

        button = Gtk.Button("Clear")
        button.connect("clicked", self.on_click_keystore_clear_clicked)
        hbox.pack_start(button, True, True, 0 )
        keystoreBox.pack_start(hbox, True, True, 0)

        button = Gtk.Button("A Request")
        button.connect("clicked", self.on_click_reqbutton_clicked)
        keystoreBox.pack_start(button, True, True, 0)

        button = Gtk.Button("Five Keypairs and Reqs")
        button.connect("clicked", self.on_click_fivereqbutton_clicked)
        keystoreBox.pack_start(button, True, True, 0)     

    def makeSigningBox(self, signingBox):
        """
        This method creates box that contains components of signingBox
        
        Arg:
        signingBox: it's initially an empty box. This methods fills it with components
        """
        # This entry display the path to selected signing ca.
        self.packHboxToVbox(signingBox, "CA's Path")
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        signingBox.pack_start(hbox, True, True, 0)

        button = Gtk.Button("Select Ca")
        button.connect("clicked", self.on_ca_config_clicked)
        hbox.pack_start(button, True, True, 0)

        button = Gtk.Button("Select CSR")
        button.connect("clicked", self.on_csr_file_clicked)
        hbox.pack_start(button, True, True, 0)

        button = Gtk.Button("Sign")
        button.connect("clicked", self.on_sign_clicked)
        signingBox.pack_start(button, True, True, 0)

    def makeShowBox(self, showBox):
        """
        Make a box that contains only a button.
        """
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        showBox.pack_start(hbox, True, True, 0)

        button = Gtk.Button("Display Entries in Keystore")
        button.connect("clicked", self.on_click_show_clicked)
        hbox.pack_start(button, True, True, 0)

    def makeImportBox(self, showBox):
        """
        Refer to make SigningBox
        """
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        showBox.pack_start(hbox, True, True, 0)

        button = Gtk.Button("Import Cert")
        button.connect("clicked", self.on_click_import_clicked)
        hbox.pack_start(button, True, True, 0)

    def makeShowCertBox(self, showBox):
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        showBox.pack_start(hbox, True, True, 0)

        button = Gtk.Button("Cert Content")
        button.connect("clicked", self.on_click_show_cert_clicked)
        hbox.pack_start(button, True, True, 0)

        
    def layout(self):
        """
        The overall layout control func
        The GUI is divieded into 4 parts:

        1: keystoreBox, used to create a keystore and keypairs
        2: signingBox : used to sign cert and concatenate certs as a trust-chain.
        3: clientCertBox, used to make client certificates.
        4: importBox, to import trusted certificate.
        5: showBox, used to show the content of a given keystore/cert by selecting.
        Here is how we pack all the boxes:

        Top level is a vertical box. We pack each of above boxes into the vertical box.
        
        It should look like this in the end:
        ----
        | 1 |
        |---|
        | 2 | 
        |---|
        | 3 |
        |---|
        | 4 |
        |---|
        | 5 |
        -----

        For each box, We also need a label to indicate the purpose.

        """
        # This 2 separators will be used repeatedly
   

        # The top level box
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        """
        The spacing arg controls how far the fieds are from each other.
        
        keystorebox stores all widgets to make a keystore
        """
        
        VerticalBox =  Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)

        keystoreBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        clientCertBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        signingBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        showBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        importBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        # Call functions to construct all those boxes.
        self.makeKeystoreBox(keystoreBox)
        self.makeSigningBox(signingBox)
        self.makeImportBox(importBox)
        self.makeShowBox(showBox)
        self.makeShowCertBox(showBox)

        """
        Start packing Keystore box. 
        First of all, a label is packed to indicate the purpose of the part.
        """
        label = Gtk.Label("Keystore", width_chars = 40 )
        VerticalBox.pack_start(label, True, True, 0)
        hsep4 = Gtk.HSeparator()
        self.packHboxToVbox(VerticalBox, "Store Pass")

        # Following "Store Pass" entry is a visibility checkbutton.
        # check_visible is a check button. We use it to choose the visibility of entry "Store Pass"
        button_box = Gtk.HButtonBox()
        check_visible = Gtk.CheckButton("Visible")

        check_visible.connect("toggled", self.on_storepass_visible_toggled)
        check_visible.set_active(False)
        button_box.add(check_visible)
        VerticalBox.pack_start(button_box, True, True, 0)

        # Pack keystorebox to the vertical box
        VerticalBox.pack_start(hsep4, True, True, 0)
        VerticalBox.pack_start(keystoreBox, True, True, 0)
        hsep = Gtk.HSeparator()
        VerticalBox.pack_start(hsep, True, True, 0)

        # Pack the signing box
        label = Gtk.Label("Signing", width_chars = 40)
        VerticalBox.pack_start(label, True, True, 0)
        VerticalBox.pack_start(signingBox, True, True, 0)
        hsep2 = Gtk.HSeparator()
        VerticalBox.pack_start(hsep2, True, True, 0)
        
        # showBox
        label = Gtk.Label("Miscellaneous", width_chars = 40 )
        VerticalBox.pack_start(label, True, True, 0)
        VerticalBox.pack_start(showBox, True, True, 0)
        hsep3 = Gtk.HSeparator()

        # Import box
        VerticalBox.pack_start(importBox, True, True, 0)
        
        self.box.pack_start(VerticalBox, True, True, 0)


####################  All followings are methods to button click ####################
    def on_storepass_visible_toggled(self, button):
        value = button.get_active()
        self.storepass.set_visibility(value)
        self.keypass.set_visibility(value)
        
    def on_click_keystore_clear_clicked(self, button):
        """
        I understand it's a bad design. All the entries are instaniated in a ording shown on GUI
        From top to down, the order is storepass, alias, CN, keypass, keysize.

        What this method does is clear the content of following 4 entries:
        alias, CN, keypass, keysize
        """
        for i in range(0,4):
            self.entries[i].set_text("")
        
    def on_click_keypair_clicked(self, button):
        # Update the info put in field
        self.updateEntries()

        # @par -alias: specify the alias name of the key pair
        # @par -dname :
        # @par -genkeypari: Generates a key pair (a public key and associated private key).
        # @par -keystore: tell keytool where to place the keystore file:
        #                 in top level of the project folder
        # @par -keysize: the length of the key.

        # By default key size is 2048
        if not self.info["Key Size"]:
            self.info["Key Size"]= 2048

        if self.info["Alias"]:
            if self.info["Common Name"]:
                par = ["/bin/keytool",
                       "-genkeypair",
                       "-alias", str( self.info["Alias"]),
                       "-dname", str("CN=" + self.info["Common Name"]),
                       "-keystore", KEYSTOREPATH,
                       "-keysize", str(self.info["Key Size"]),
                       "-keypass", str(self.info["Key Pass"]),
                       "-storepass", str(self.info["Store Pass"])
                ]
                result = subprocess.call(par)
                if not result:
                    print "Key pair has been generated."
            else:
                print "Common Name is not provided"
        else:
            print "Alias is required"

    def on_click_reqbutton_clicked(self, button):
        self.updateEntries()

        # Make sure folder ./clientCerts exist.
        if not os.path.exists(CSRPATH):
            par = ["mkdir",
                   "-p", CSRPATH
            ]
            subprocess.call(par)

        # @par:
        #  -certreq: make a cert request
        #  -alias: alias name used in key store
        #  -file: output file
        #  -keystore Path to keystore
        #  -storepass , self-explained

        par = ["/bin/keytool",
               "-certreq",
               "-alias", str( self.info["Alias"]),
               "-file", str( CSRPATH+ self.info["Alias"]+".pem"),
               "-keystore", KEYSTOREPATH,
               "-storepass", str(self.info["Store Pass"]),
               "-keypass", self.info["Key Pass"]
        ]
        result = subprocess.call(par)
        if not result:
            print "Req has been successfully made"

    def on_click_fivereqbutton_clicked(self, button):
        self.updateEntries()

        # To make sure the dir exists
        if not os.path.exists(CSRPATH):
            par = ["mkdir",
                   "-p", CSRPATH
            ]
            result = subprocess.Popen(par)
            result.wait()
            
         # To have 5 reqs, we need to have 5 key pairs.
        if not self.info["Key Size"]:
            self.info["Key Size"]= 2048

        for i in range(0, 5):
            par = ["/bin/keytool",
                   "-genkeypair",
                   "-alias", str( self.info["Alias"] + str(i)),
                   "-dname", str("CN=" + self.info["Common Name"]),  # They share common CN
                   "-keystore", KEYSTOREPATH,
                   "-keysize", str(self.info["Key Size"]),
                   "-keypass", str(self.info["Key Pass"]),
                   "-storepass", str(self.info["Store Pass"]),
                ]
            
            result = subprocess.call(par)
            if not result:
                print "Key pair " + self.info["Alias"] + str(i)+ " has been generated." #

       
        # Make 5 certs based on alias
        for j in range(0, 5):
            par = ["/bin/keytool",
                   "-certreq",
                   "-alias", str( self.info["Alias"] + str(j)),
                   "-file", str( CSRPATH + self.info["Alias"]+ str(j) + ".pem"),
                   "-keystore", KEYSTOREPATH,
                   "-storepass", str(self.info["Store Pass"]),
                   "-keypass", self.info["Key Pass"]
            ]
            result = subprocess.call(par)

    def on_click_show_clicked(self,button):
        self.updateEntries()

        # @par -list: argument to list the content of a keystore
        # @par -keystore: where to find target keystore, followed by the path.
        if self.info["Alias"]:
            par = ["/bin/keytool",
                   "-list",
                   "-keystore", KEYSTOREPATH,
                   "-storepass", str(self.info["Store Pass"]),
                   "-alias", self.info["Alias"]
            ]
            subprocess.call(par)
        else:
            par = ["/bin/keytool",
                   "-list",
                   "-keystore", KEYSTOREPATH,
                   "-storepass", str(self.info["Store Pass"]),
            ]
            subprocess.call(par)

    def on_click_import_clicked(self, button):
        self.updateEntries();
        dialog = Gtk.FileChooserDialog("Please choose ca's config file", self,
                                       Gtk.FileChooserAction.OPEN,
                                       ("Cancel", Gtk.ResponseType.CANCEL,
                                        "Open", Gtk.ResponseType.OK))
        self.add_filters(dialog)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            certToBeImported = dialog.get_filename()
            print "CA config selected", certToBeImported
        elif response == Gtk.ResponseType.CANCEL:
            print("Dialog Canceled")
        dialog.destroy()

        # @par -list: argument to list the content of a keystore
        # @par -keystore: where to find target keystore, followed by the path.
        if self.info["Alias"]:
            if self.info["Store Pass"]:
                if certToBeImported:
                    par = ["/bin/keytool",
                           "-import",
                           "-alias", str(self.info["Alias"]),
                           "-keystore", KEYSTOREPATH,
                           "-storepass", str(self.info["Store Pass"]),
                           "-file", certToBeImported
                    ]
                    subprocess.call(par)
                else:
                    print "Please select a file"
            else:
                print "Password to Keystore is not provided"
        else:
            print "Alias not specified"

    def on_ca_config_clicked(self,widge):
        dialog = Gtk.FileChooserDialog("Please choose ca's config file", self,
                                       Gtk.FileChooserAction.OPEN,
                                       ("Cancel", Gtk.ResponseType.CANCEL,
                                        "Open", Gtk.ResponseType.OK))
        self.add_filters(dialog)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.CAConfig = dialog.get_filename()
            print "CA config selected", self.CAConfig
            self.capath.set_text(self.CAConfig)
        elif response == Gtk.ResponseType.CANCEL:
            print("Import Selection Dialog Canceled")
        dialog.destroy()
        
    def on_csr_file_clicked(self, widget):
        """
        By default, Gtk.FileChooser only allows a single file to be selected at a time. 
        To enable multiple files to be selected, use Gtk.FileChooser.set_select_multiple(). 
        Retrieving a list of selected files is possible with either Gtk.FileChooser.get_filenames()or Gtk.FileChooser.get_uris().
        """
        dialog = Gtk.FileChooserDialog("Please choose a certificate request file", self,
                                       Gtk.FileChooserAction.OPEN,
                                       ("Cancel", Gtk.ResponseType.CANCEL,
                                        "Open", Gtk.ResponseType.OK))
        dialog.set_select_multiple(True)
        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.csr = dialog.get_filenames()
            if hasattr(self, "csr"):
                for i in self.csr:
                    print "File selected", i
  
                    csr_liststore = Gtk.ListStore(str)         # creating a list store

                    for i in self.csr:        # Import all the selected csr files into list store.
                         i = [i,]
                         csr_liststore.append(i)

                    treeview = Gtk.TreeView(csr_liststore)            # Creating a treeview
                    renderer = Gtk.CellRendererText()
                    for i, colname in enumerate(["CSR File"]):
                        column = Gtk.TreeViewColumn(colname, renderer, text = i)
                        treeview.append_column(column)
                        column.set_sort_column_id(0)
                    
                    scrollable_treelist = Gtk.ScrolledWindow()             #setting up the layout, putting the treeview in a scrollwindow, and the buttons in a row
                    scrollable_treelist.set_vexpand(True)
                    self.grid.attach(scrollable_treelist, 0, 0, 8, 10)
                    scrollable_treelist.add(treeview)

            self.popup.show_all()

        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel")
        
        dialog.destroy()

        # After the selection of csr files, we pop up a window to display.

    def on_sign_clicked(self,button):
        # To make sure the dir exists
        if not os.path.exists(CERTPATH):
            par = ["mkdir",
                   "-p", CERTPATH
            ]
            subprocess.call(par)
            
        if hasattr(self,"csr"):
            if hasattr(self, "CAConfig"):
                for i in self.csr:
                    par = ["/bin/openssl",
                           "ca",
                           "-config", str( self.CAConfig),
                           "-in", str(i),
                           "-out", CERTPATH + os.path.basename(i)
                        #    "-extensions", "server_ext"
                    ]
                    result = subprocess.call(par)
                    print result
                    if not result:
                        print "All requestions have been signed"
            else:
                print "CAConfig is missing."
        else:
            print "CSR files have not been choosen yet."

    def on_click_show_cert_clicked(self, button):
        self.updateEntries();
        dialog = Gtk.FileChooserDialog("Please choose ca's config file", self,
                                       Gtk.FileChooserAction.OPEN,
                                       ("Cancel", Gtk.ResponseType.CANCEL,
                                        "Open", Gtk.ResponseType.OK))
        self.add_filters(dialog)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            certToShow = dialog.get_filename()
            print "A signed cert selected", certToShow
        elif response == Gtk.ResponseType.CANCEL:
            print("Dialog Canceled")
        dialog.destroy()

        # @par -list: argument to list the content of a keystore
        # @par -keystore: where to find target keystore, followed by the path.
        if certToShow:
            par = ["./utils/showCerts.sh", str(certToShow)]
            subprocess.call(par)
        else:
            print "Select a signed certificate"
            
 ##################### ######################                       
        
    def add_filters(self, dialog):
        filter_conf = Gtk.FileFilter()
        filter_conf.set_name("config files")
        filter_conf.add_pattern("*.conf")
        dialog.add_filter(filter_conf)

        filter_csr = Gtk.FileFilter()
        filter_csr.set_name("csr files")
        filter_csr.add_pattern("*.pem")
        dialog.add_filter(filter_csr)

  
        filter_conf = Gtk.FileFilter()
        filter_conf.set_name("All files")
        filter_conf.add_pattern("*")
        dialog.add_filter(filter_conf)
        
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
        
############################################        
    
if __name__ == "__main__":
    window = ourwindow()
    window.layout()
    window.connect("delete-event", Gtk.main_quit)
    window.show_all()
    Gtk.main()
