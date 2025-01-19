# GUI imports
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtCore import Qt, QTimer, QUrl, QSize
# OS imports - these should probably be moved somewhere else
import os
import zfbmagic as zfb
import mcoredata as mcd
import tadpole_functions
import frogtool
from dialogs.DownloadProgressDialog import DownloadProgressDialog

# Subclass Qidget to create a Settings window        
class MulticoreDialog(QDialog):
    """
        This window should be called without a parent widget so that it is created in its own window.
    """
    def __init__(self, tpConf):
        super().__init__()
        self.tpConf = tpConf
        self.setWindowIcon(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DesktopIcon)))
        self.setWindowTitle(f"Creating Multicore ZFBS/STUBS")

        self.setFixedSize(300, 250)
        
        # Setup Main Layout
        self.layout_main = QVBoxLayout()
        self.setLayout(self.layout_main)


        #Multicore Core directory in ROMS
        self.layout_main.addWidget(QLabel("Select Multicore Directory"))
        self.mdirCombo = QComboBox()
        wdir = tpConf.cDir #tpConf.getLocalUserDirectory() #self.combobox_drive.currentText() #self.combobox_console.currentText()
        try:
            self.mdirCombo.addItems([f.name for f in os.scandir(wdir +"ROMS") if f.is_dir() and f.name != "save" and f.name != "mnt" ])
        except:
            self.mdirCombo.addItems([])
        #mdirCombo.addItems(["uploading a folder from your PC", "automatically downloading over the internet"])
        self.mdirCombo.setCurrentIndex(0)
        #mdirCombo.currentTextChanged.connect(self.thumbnailAddChanged)
        self.layout_main.addWidget(self.mdirCombo)

        #Placeholder (if used)to be used if no image found
        self.layout_main.addWidget(QLabel("Select Placeholder"))
        self.phCombo = QComboBox()
        self.layout_main.addWidget(self.phCombo)

        self.build_pfiles()
        self.layout_main.addWidget(QLabel(" "))  # spacer



        


        """
        #File options options
        self.layout_main.addWidget(QLabel("File Options"))
        UserSavedDirectory = tpConf.getLocalUserDirectory()
        self.layout_main.addWidget(QLabel(f"User defined directory:"))
        self.user_directory = QLabel(UserSavedDirectory, self)
        self.layout_main.addWidget(self.user_directory)
        self.btn_change_user_dir = QPushButton("Select your own local directory...")
        self.layout_main.addWidget(self.btn_change_user_dir)
        self.btn_change_user_dir.clicked.connect(self.userSelectedDirectorySettingsButton)
        self.btn_remove_user_dir = QPushButton("Remove your local directory from Tadpole")
        self.layout_main.addWidget(self.btn_remove_user_dir)
        self.btn_remove_user_dir.clicked.connect(self.userSelectedDirectoryResetSettingsButton)
                
        self.layout_main.addWidget(QLabel(" "))  # spacer

        
        """
        # Main Buttons Layout (Cancel/Create ZFBs)
        self.layout_buttons = QHBoxLayout()
        self.layout_main.addLayout(self.layout_buttons)

        

        #Cancel Button
        self.button_back = QPushButton("Back")
        self.button_back.clicked.connect(self.accept)
        self.layout_buttons.addWidget(self.button_back)

        #Create ZFBs button
        self.btn_process = QPushButton("Create ZFBs")
        self.layout_buttons.addWidget(self.btn_process)
        self.btn_process.clicked.connect(self.doProcess)



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

    def doProcess(self):
        wdir = self.tpConf.cDir

        bpath = os.path.join(wdir, "bios", "bisrv.asd")
        #print(f"root dir is {wdir} \n Bpath is {bpath}")
        if not os.path.exists(bpath):
            QMessageBox.information(self , "BIOS" , "BIOS not found. Please Select proper root directory.")
            print("BIOS not found", bpath)
            return

        core = self.mdirCombo.currentText()

        if core not in mcd.cores:
            QMessageBox.information(self , "Unsupported Core" , "The CORE you entered isnt part of multicore.")
            return

        #return

        sdir = self.tpConf.cCon
        #print(f"stock is {sdir}")
        pdir = self.phCombo.currentText().strip()

        doRef = False

        apptxt = ""
        pretxt = ""
        doExt = False


        doMove = False
        

        ifexist = "Overwrite"

        prg = DownloadProgressDialog()
        prgT = False

        zfb.create_zfb_files(self , wdir ,sdir , pdir , core, apptxt , pretxt , doRef , doExt , [] ,doMove , ifexist , prg , prgT  ,  False)
        self.accept()


    
