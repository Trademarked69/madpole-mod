# GUI imports
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtCore import Qt, QTimer, QUrl, QSize
# OS imports - these should probably be moved somewhere else
import os
import tadpole_functions
import frogtool
from dialogs.DownloadProgressDialog import DownloadProgressDialog

# Subclass Qidget to create a Settings window        
class MulticoreStubsDialog(QDialog):
    """
        This window should be called without a parent widget so that it is created in its own window.
    """
    def __init__(self, tpConf):
        super().__init__()
        self.tpConf = tpConf
        self.setWindowIcon(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DesktopIcon)))
        self.setWindowTitle(f"Creating Multicore STUBS")
        self.setFixedSize(300, 200)


        # Setup Main Layout
        self.layout_main = QVBoxLayout()
        self.setLayout(self.layout_main)

        #Thumbnail View options
        """
        self.layout_main.addWidget(QLabel("Thumbnail options"))
        #Viewer
        thubmnailViewCheckBox = QCheckBox("View Thumbnails in ROM list")
        view = tpConf.getViewThumbnailsInTable()
        thubmnailViewCheckBox.setChecked(view)
        thubmnailViewCheckBox.toggled.connect(self.thumbnailViewClicked)
        self.layout_main.addWidget(thubmnailViewCheckBox)
        """

        #Multicore Core directories in ROMS
        self.layout_main.addWidget(QLabel("Select Multicore Directory"))
        self.mdirCombo = QComboBox()
        mdir = tpConf.cDir
        try:
            self.mdirCombo.addItems([f.name for f in os.scandir(mdir +"ROMS") if f.is_dir() and f.name != "save" and f.name != "mnt" ])
        except:
            self.mdirCombo.addItems([])

        self.mdirCombo.setCurrentIndex(0)
        self.layout_main.addWidget(self.mdirCombo)

        
        #Spacer
        self.layout_main.addWidget(QLabel(" "))  


        #DIR STUBS or ALL STUBS
        self.stubCheckbox = QCheckBox("Create STUBS For All core in ROMS")
        self.stubCheckbox.setChecked(False)
        self.stubCheckbox.stateChanged.connect(self.stubCheckClicked)
        self.layout_main.addWidget(self.stubCheckbox)


        #BUTTONS
        self.layout_buttons = QHBoxLayout()
        self.layout_main.addLayout(self.layout_buttons)

        
        #Cancel Button
        self.button_cancel = QPushButton("Back")
        self.button_cancel.clicked.connect(self.accept)
        self.layout_buttons.addWidget(self.button_cancel)


        #Create STUBS Button
        self.btn_process = QPushButton("Create STUBS")
        self.layout_buttons.addWidget(self.btn_process)
        self.btn_process.clicked.connect(self.doProcess)


    def stubCheckClicked(self):
        if(self.stubCheckbox.isChecked()):
            self.mdirCombo.setEnabled(False)
        else:
            self.mdirCombo.setEnabled(True)

    def doProcess(self):
        self.create_stub_files()
        self.accept()


    def create_stub_files(self):
        core = self.mdirCombo.currentText()
        wdir = self.tpConf.cDir
        core = core.strip()
        #wdir = self.input_folder_var.get()

        if self.stubCheckbox.isChecked():
            if not wdir:
                QMessageBox.warning(self,'Error', 'Root Directory not selected')
                return

            romfolder = os.path.join(wdir,"ROMS")
            if os.path.exists(romfolder):
                for d in os.listdir(romfolder):                    
                    #romfolder = os.path.join(wdir,"ROMS",d)
                    
                    if os.path.isdir(os.path.join(romfolder , d)) and d not in ["save" , "mnt"]:
                        for rom in os.listdir(os.path.join(romfolder , d)):
                            rext = os.path.splitext(rom)[1][1:]
                            if rext not in ["png" , "gif" , "jpg" , "jpeg" , "gif" , "txt"]:
                                with open(os.path.join(romfolder,f"{d};{rom}.gba"), 'w'): 
                                    pass
            else:
                QMessageBox.warning(self,'Error', 'ROMS folder not found. Check Root Folder')
                return
        else:

            romdir = os.path.join(wdir, "ROMS", core) #self.pdir_root
            if not wdir or not romdir or not core: #or not extension:
                    QMessageBox.warning(self,'Warning', 'Please fill in all the fields and select multicore rom directory')
                    return

            for rom in os.listdir(romdir):
                rext = os.path.splitext(rom)[1][1:]
                if rext not in ["png" , "gif" , "jpg" , "jpeg" , "gif" , "txt"]:
                    with open(os.path.join(wdir,"ROMS",f"{core};{rom}.gba"), 'w'): 
                        pass

        QMessageBox.information(self ,"Processed" , "STUBS created")
