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
class SettingsDialog(QDialog):
    """
        This window should be called without a parent widget so that it is created in its own window.
    """
    def __init__(self, tpConf):
        super().__init__()
        self.tpConf = tpConf
        self.setWindowIcon(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DesktopIcon)))
        self.setWindowTitle(f"Madpole Settings")
        
        # Setup Main Layout
        self.layout_main = QVBoxLayout()
        self.setLayout(self.layout_main)

        # Sorting options options
        self.top_games_enabled = self.tpConf.getTopGamesEnabled()  # Get the initial state from configuration
        self.layout_main.addWidget(QLabel("Sorting options"))
        self.top_games_sorting_checkbox = QCheckBox("Enable Top Games List (sdcard/topgames.txt)", self)
        self.top_games_sorting_checkbox.setToolTip("Adds the games specified in topgames.txt to the top of the game listing")
        self.top_games_sorting_checkbox.clicked.connect(self.topGamesToggled)
        self.layout_main.addWidget(self.top_games_sorting_checkbox)
        self.top_games_sorting_checkbox.setChecked(self.top_games_enabled)

        #Thumbnail View options
        self.layout_main.addWidget(QLabel("Thumbnail options"))
        #Viewer
        thubmnailViewCheckBox = QCheckBox("View Thumbnails in ROM list")
        view = tpConf.getViewThumbnailsInTable()
        thubmnailViewCheckBox.setChecked(view)
        thubmnailViewCheckBox.toggled.connect(self.thumbnailViewClicked)
        self.layout_main.addWidget(thubmnailViewCheckBox)
        
        # Border around shortcuts
        self.layout_main.addWidget(QLabel("Shortcuts border (doesn't work with Resizing ROMArt)"))
        shortcutsBorderEnabled = self.tpConf.getShortcutsBorderEnabled()  # Get the initial state from configuration
        shortcutsBorderCheckBox = QCheckBox("Border around shortcuts")
        shortcutsBorderCheckBox.setToolTip("Adds a white border aroung the shortcut image")
        shortcutsBorderCheckBox.clicked.connect(self.shortcutsBorderToggle)
        self.layout_main.addWidget(shortcutsBorderCheckBox)
        shortcutsBorderCheckBox.setChecked(shortcutsBorderEnabled)
        
        # Automatic resize romart
        self.layout_main.addWidget(QLabel("Resizing ROMArt"))
        resizeRomartEnabled = self.tpConf.getResizeRomart()  # Get the initial state from configuration
        resizeRomartCheckBox = QCheckBox("Keep aspect ratio")
        resizeRomartCheckBox.setToolTip("Resizes ROMArt so the aspect ratio is preserved")
        resizeRomartCheckBox.clicked.connect(self.resizeRomartToggle)
        self.layout_main.addWidget(resizeRomartCheckBox)
        resizeRomartCheckBox.setChecked(resizeRomartEnabled)
        
        # Libretro Thumbnail Background Color
        self.layout_main.addWidget(QLabel("ROMArt background color: "))
        romartBackgroundColorTextbox = QLineEdit()
        romartBackgroundColorTextbox.setText(tpConf.getRomartBackgroundColor())
        romartBackgroundColorTextbox.setToolTip("Only used if keeping aspect ratio")
        romartBackgroundColorTextbox.textChanged.connect(self.romartBackgroundColorChanged)
        self.layout_main.addWidget(romartBackgroundColorTextbox)
        
        #Thumbnail upload style
        self.layout_main.addWidget(QLabel("Add thumbnails by: "))
        thubmnailAddCombo = QComboBox()
        thubmnailAddCombo.addItems(["uploading a folder from your PC", "automatically downloading over the internet"])
        thubmnailAddCombo.setCurrentIndex(1 if tpConf.getThumbnailDownload() else 0)
        thubmnailAddCombo.currentTextChanged.connect(self.thumbnailAddChanged)
        self.layout_main.addWidget(thubmnailAddCombo)

        #Thumbnail upload style
        self.layout_main.addWidget(QLabel("When adding thumbnails: "))
        thubmnailOvewriteCombo = QComboBox()
        thubmnailOvewriteCombo.addItems(["always overwrite all thumbnails", "Only add new thumbnails to zip files"])
        thubmnailOvewriteCombo.setCurrentIndex(0 if tpConf.getThumbnailOverwrite() else 1)
        thubmnailOvewriteCombo.currentTextChanged.connect(self.thumbnailOverwriteChanged)
        self.layout_main.addWidget(thubmnailOvewriteCombo)

        #Libretro Thumbnail Type options
        self.layout_main.addWidget(QLabel("Libretro Thumbnail Type"))
        libretroThumbnailTypeCombo = QComboBox()
        libretroThumbnailTypeCombo.addItems(["Boxarts", "Snaps", "Titles"])
        current_type = tpConf.getLibretroThumbnailType()
        libretroThumbnailTypeCombo.setCurrentIndex(["Boxarts", "Snaps", "Titles"].index(current_type))
        libretroThumbnailTypeCombo.currentTextChanged.connect(self.libretroThumbnailTypeChanged)
        self.layout_main.addWidget(libretroThumbnailTypeCombo)

        self.layout_main.addWidget(QLabel(" "))  # spacer

        #File options options
        self.layout_main.addWidget(QLabel("File Options"))
        UserSavedDirectory = tpConf.getLocalUserDirectory()
        self.layout_main.addWidget(QLabel(f"User defined directory:"))
        self.user_directory = QLabel(UserSavedDirectory, self)
        self.layout_main.addWidget(self.user_directory)
        self.btn_change_user_dir = QPushButton("Select your own local directory...")
        self.layout_main.addWidget(self.btn_change_user_dir)
        self.btn_change_user_dir.clicked.connect(self.userSelectedDirectorySettingsButton)
        self.btn_remove_user_dir = QPushButton("Remove your local directory from Madpole")
        self.layout_main.addWidget(self.btn_remove_user_dir)
        self.btn_remove_user_dir.clicked.connect(self.userSelectedDirectoryResetSettingsButton)
                
        self.layout_main.addWidget(QLabel(" "))  # spacer

        # Main Buttons Layout (Save/Cancel)
        self.layout_buttons = QHBoxLayout()
        self.layout_main.addLayout(self.layout_buttons)
        
        #Save Existing Cover To File Button
        self.button_write = QPushButton("Continue")
        self.button_write.clicked.connect(self.accept)
        self.layout_buttons.addWidget(self.button_write)     

    def thumbnailAddChanged(self):
        self.tpConf.setThumbnailDownload(self.sender().currentIndex() == 1)
    
    def thumbnailOverwriteChanged(self):
        self.tpConf.setThumbnailOverwrite(self.sender().currentIndex() == 0)

    def userSelectedDirectorySettingsButton(self):
        qm = QMessageBox
        ret = qm.question(self,'Working location', "Instead of an SD card, you can define your own working location on your drive.\n\
Once you finish working there, you'll need to 'Copy' everything over to your SD card.  Do you want to use this mode?  If so, click Yes and select the folder that has the \
same contents as the SF2000." , qm.Yes | qm.No)
        if ret == qm.No:
            return
        directory = os.path.normpath(QFileDialog.getExistingDirectory()) # getExistingDirectory returns filepath slashes the wrong way around in some OS, lets fix that
        if directory == '': #Check that the user actually selected a directory and didnt just close the window
            return False
        print(f"Trying to set local dir to ({directory})")
        #logging.info(f"Setting local drive to ({directory})")
        # Update the Tadole config file
        self.tpConf.setLocalUserDirectory(directory)
        qm = QMessageBox()

        #See if it has all folders/files we need
        #TODO: Do more than bios?
        if not tadpole_functions.checkDriveLooksFroggy(directory):
            ret = qm.question(self,'Working location', "This folder doesn't contain the bios folder or bisrv.as file, so it doens't look \
like the root of the SD card.  Do you want us to download all the most up to date files to this folder instead?" , qm.Yes | qm.No)
            #Add all these in via the FixSF2000 function
            if ret == qm.Yes:
                msgBox = DownloadProgressDialog()
                msgBox.setText("Downloading Firmware Update.")
                msgBox.show()
                tadpole_functions.DownloadOSFiles(directory, msgBox.progress)
        QMessageBox().about(self, "Working location", "When you want to go back to using an SD card, select it in the dropdown list of drives.\n\n\When you are ready to ovewrite that SD card, press the 'Copy to SD' button")

        #Set the dialog displayed local User Direcotry to the new value
        self.user_directory.setText(self.tpConf.getLocalUserDirectory())


    def userSelectedDirectoryResetSettingsButton(self):
        self.tpConf.setLocalUserDirectory(self.tpConf._static_general_userDirectory_DEFAULT)
        self.user_directory.setText(self.tpConf._static_general_userDirectory_DEFAULT)
        self.user_directory.adjustSize()
        

    def thumbnailViewClicked(self):
        self.tpConf.setViewThumbnailsInTable(self.sender().isChecked())
    
    def topGamesToggled(self):
        self.tpConf.setTopGamesEnabled(self.top_games_sorting_checkbox.isChecked())
    
    def libretroThumbnailTypeChanged(self):
        selected_type = self.sender().currentText()
        self.tpConf.setLibretroThumbnailType(selected_type)
              
    def shortcutsBorderToggle(self):
        self.tpConf.setShortcutsBorderEnabled(self.sender().isChecked())
                
    def resizeRomartToggle(self):
        self.tpConf.setResizeRomart(self.sender().isChecked())
        
    def romartBackgroundColorChanged(self):
        selected_type = self.sender().text()
        self.tpConf.setRomartBackgroundColor(selected_type)

