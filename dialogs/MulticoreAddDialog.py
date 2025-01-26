# GUI imports
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtCore import Qt, QTimer, QUrl, QSize
# OS imports - these should probably be moved somewhere else
import os
import glob
import shutil
import zfbmagic as zfb

"""
import tadpole_functions
import frogtool
"""

from tadpoleConfig import TadpoleConfig
tpConf = TadpoleConfig()

import mcoredata as mcd
from dialogs.DownloadProgressDialog import DownloadProgressDialog


# Subclass Qidget to create a Settings window        
class MulticoreAddDialog(QDialog):
    """
        This window should be called without a parent widget so that it is created in its own window.
    """
    def __init__(self, tpConf):
        super().__init__()
        self.tpConf = tpConf
        self.setWindowIcon(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DesktopIcon)))
        self.setWindowTitle(f"Add Multicore Roms")
        
        self.filenames = []
        # Setup Main Layout
        self.layout_main = QVBoxLayout()
        self.setLayout(self.layout_main)

        #Thumbnail View options
        self.layout_main.addWidget(QLabel("Multicore Core Name"))
        #Viewer

        self.core = QPlainTextEdit()
        self.core.setFixedHeight(25)
        self.layout_main.addWidget(self.core)

        self.layout_main.addWidget(QLabel(" "))


         # Main Buttons Layout (Save/Cancel)
        self.layout_buttons = QHBoxLayout()
        self.layout_main.addLayout(self.layout_buttons)
        
        #Save Existing Cover To File Button
        
        self.button_browse = QPushButton("Browse")
        self.button_browse.clicked.connect(self.selectFiles)
        self.layout_buttons.addWidget(QLabel("Select Roms and Thumbs Files"))
        self.layout_buttons.addWidget(self.button_browse) 
        
        if not tpConf.getThumbnailDownload():
            self.layout_main.addWidget(QLabel("Thumb name has to be the same name as ROM , if no matching\nThumb is found a placeholder selected below will be used."))
        else:
            self.layout_main.addWidget(QLabel("You have Madpole configured to download thumbnails automatically."))
            self.layout_main.addWidget(QLabel("For this to work the name of that rom must match their common released English US localized name."))            
            link_text = "Please refer to <a href='https://thumbnails.libretro.com/'>https://thumbnails.libretro.com/</a> if Madpole isn't finding the thumbnail for you."
            label = QLabel()
            label.setText(link_text)
            label.setOpenExternalLinks(True)
            self.layout_main.addWidget(label)

        self.layout_main.addWidget(QLabel(" "))


        self.layout_main.addWidget(QLabel("Select Placeholder for missing Thumbnails"))
        self.phCombo = QComboBox()
        self.layout_main.addWidget(self.phCombo)

        self.build_pfiles()

         
        self.layout_main.addWidget(QLabel(" "))  # spacer

        # Main Buttons Layout (Save/Cancel)
        self.layout_buttons = QHBoxLayout()
        self.layout_main.addLayout(self.layout_buttons)
        

        self.button_back = QPushButton("Back")
        self.button_back.clicked.connect(self.accept)
        self.layout_buttons.addWidget(self.button_back)
        
        self.status_bar = QStatusBar()
        self.layout_main.addWidget(self.status_bar)

        #Save Existing Cover To File Button
        self.button_addroms = QPushButton("Add Roms")
        self.button_addroms.clicked.connect(self.addroms)
        self.layout_buttons.addWidget(self.button_addroms) 

        #self.statusBar = QStatusBar()
        #self.setStatusBar(self.statusBar)    

        
        #self.setStatusBar(self.status_bar)

    def selectFiles(self):
        #print("Selecting Files")
        self.filenames, _ = QFileDialog.getOpenFileNames(self,"Select ROMs and THUMBs",'',"All Files (*.*)")
        self.status_bar.showMessage(f"{len(self.filenames)} File(s) Selected")

    def addroms(self):
        #print("Adding Roms")

        wdir = self.tpConf.cDir

        bpath = os.path.join(wdir, "bios", "bisrv.asd")
        #print(f"root dir is {wdir} \n Bpath is {bpath}")
        if not os.path.exists(bpath):
            QMessageBox.information(self , "BIOS" , "BIOS not found. Please Select proper root directory.")
            print("BIOS not found", bpath)
            return

        core = self.core.toPlainText().strip()


        if core == "":
            QMessageBox.information(self , "Enter Core" , "CORE is required to add multicore roms.")
            return

        if core not in mcd.cores:
            QMessageBox.information(self , "Unsupported Core" , "The CORE you entered isnt part of multicore.")
            return

        files = self.filenames

        if len(files) < 1:
            QMessageBox.information(self , "No Files" , "No Files Selected. Please Select Roms and Thumbs.")
            return

        

        

        #return

        sdir = self.tpConf.cCon
        #print(f"stock is {sdir}")
        pdir = self.phCombo.currentText().strip()

        doRef = False
        dont = False

        apptxt = ""
        pretxt = ""
        doExt = False

        filenames = self.filenames

        doMove = True
        

        ifexist = "Overwrite"

        prg = DownloadProgressDialog()
        prgT = False

        zfb.create_zfb_files(self ,wdir ,sdir , pdir , core, apptxt , pretxt , doRef , doExt , filenames ,doMove , ifexist , prg , prgT , False)
        self.accept()

    def build_pfiles(self):

        pdir_root = os.path.join(os.getcwd(), "placeholders") #self.pdir_root
        self.phCombo.setFixedHeight(85)
        #pdir = self.phCombo
        if not os.path.isdir(pdir_root):
            os.makedirs(pdir_root)
        #wdir = self.wdir.toPlainText()
        #self.pdir.set("")

        #subdir = "\\ROMS"
        imgtypes = (".jpg" , ".png" , ".bmp")       
        #try:
        #self.pdir.addItems([f.name for f in os.scandir(wdir +"\\placeholders") if not f.is_dir() and f.name.lower().endswith(imgtypes)] )
            #self.pdir.current(0)
        for f in os.scandir(pdir_root):
            self.phCombo.addItem(QIcon(f.path) , f.name)
        self.phCombo.setIconSize(QSize(59, 85))
        if not self.phCombo.count() > 0:
            QMessageBox.information(self,'No Placeholders', 'No Placeholder files found in Placeholder Directory')
            #self.pdir['values'] = []
            #self.pdir.current()

        self.phCombo.insertItem(0,"      Dont Use Placeholder")
        self.phCombo.setCurrentIndex(0)
        #print("pdir selected item is " + self.phCombo.currentText().strip())
        """
        noph = ["Dont Use Placeholder"]

        current_values = list(self.pdir['values'])
        self.pdir['values'] = noph + current_values
        self.pdir.current(0)
        """

