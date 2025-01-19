# GUI imports
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtCore import Qt, QTimer, QUrl, QSize
# OS imports - these should probably be moved somewhere else
import os
import shutil

import tadpole_functions
import mcoredata as mcd
import frogtool
from dialogs.DownloadProgressDialog import DownloadProgressDialog

# Subclass Qidget to create a Settings window        
class MulticoreChange(QDialog):
    """
        This window should be called without a parent widget so that it is created in its own window.
    """
    def __init__(self, tpConf):
        super().__init__()
        self.tpConf = tpConf
        self.setWindowIcon(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DesktopIcon)))
        self.setWindowTitle(f"Core Changer")

        self.setMinimumWidth(350)
        
        # Setup Main Layout
        self.layout_main = QVBoxLayout()
        self.setLayout(self.layout_main)

        #Thumbnail View options
        self.layout_main.addWidget(QLabel("Enter New Core"))
        #Viewer

        self.wdir2 = QPlainTextEdit()
        self.wdir2.setFixedHeight(25)
        self.layout_main.addWidget(self.wdir2)

        self.movechk = QCheckBox("Dont Move Rom files")
        self.layout_main.addWidget(self.movechk)
        self.movechk.stateChanged.connect(self.mchkstate)


        self.copychk = QCheckBox("Copy Roms (Make Duplicate in new Core Dir)")
        self.layout_main.addWidget(self.copychk)
        self.copychk.stateChanged.connect(self.cchkstate)



        self.syschk = QCheckBox("Enforce System Check")
        self.layout_main.addWidget(self.syschk)
        self.syschk.setChecked(True)

                        
        self.layout_main.addWidget(QLabel("Status"))
        self.sts = QTextEdit()
        self.sts.setFixedHeight(150)
        self.sts.setStyleSheet("background-color: #efefef; font-size:8pt")
        self.layout_main.addWidget(self.sts)

        # Main Buttons Layout (Save/Cancel)
        self.layout_buttons = QHBoxLayout()
        self.layout_main.addLayout(self.layout_buttons)
        
        #Save Existing Cover To File Button
        self.button_cancel = QPushButton("Back")
        self.button_cancel.clicked.connect(self.accept)
        self.layout_buttons.addWidget(self.button_cancel)

        self.button_change = QPushButton("Change Cores")
        self.button_change.clicked.connect(self.changeCores)
        self.layout_buttons.addWidget(self.button_change)

        self.status_bar = QStatusBar()
        self.layout_main.addWidget(self.status_bar)
        fcount = len(self.tpConf.gList)
        self.status_bar.showMessage(f"{fcount} File(s) Selected for CORE Change")


    
    def cchkstate(self):
        if self.copychk.isChecked():
            self.movechk.setEnabled(False)
        else:
            self.movechk.setEnabled(True)

    def mchkstate(self):
        if self.movechk.isChecked():
            self.copychk.setEnabled(False)
        else:
            self.copychk.setEnabled(True)

    def changeCores(self , tpConf):
        #print("Changing Core from Dialog")
        newCore = self.wdir2.toPlainText()
        gList = self.tpConf.gList

        #print("Game lis is ")
        #print(gList)

        if newCore not in mcd.cores:
            QMessageBox.about(self, "Wrong CORE", f"Entered CORE doesnt exist in multicore")
            return

        res = True
        skips = 0
        dones = 0
        totals = 0
        stext = ""
        lbs = ""

        neslist = mcd.neslist
        sneslist = mcd.sneslist
        gbalist = mcd.gbalist
        gblist = mcd.gblist
        segalist = mcd.segalist
        commlist = mcd.commlist

        for zfile in gList:

            """msgBox = DownloadProgressDialog()
            msgBox.setText("Changing Cores")
            msgBox.show()

            msgbox.showProgress(0, True)
            msgbox.showProgress(int(100 * dones+skips / totals), True)
            msgbox.showProgress(100, True)"""
            totals += 1

            fname = os.path.basename(zfile)
            fext = os.path.splitext(zfile)[1][1:].lower()

            if fext != "zfb":
                self.sts.append(lbs + f"<span style='color:red'>{fname} SKIPPED as its not a ZFB</span>")
                lbs = "<br>"
                skips += 1
                continue


            with open(zfile, "rb+") as rom_file:
                #get past the RAW image
                
                rom_file.seek(59908)
                rawfileName = rom_file.read(255).decode().strip('\0')

                if not rawfileName.lower().endswith("gba"):
                    self.sts.append(lbs + f"<span style='color:red'>{fname} <strong>SKIPPED</strong> , Not a Multicore ZFB</span>")
                    lbs = "<br>"
                    skips += 1
                    continue

                rawfileName = rawfileName.split(";")
                oldCore = rawfileName[0].strip('\x00')

                if newCore == oldCore:
                    self.sts.append(lbs + f"<span style='color:blue'>{fname} <strong>SKIPPED</strong> , Core already {newCore}</span>")
                    lbs = "<br>"
                    skips += 1

                romName = rawfileName[1].strip('\x00')
                romName = romName[0:-4]
                #print("Core is : " + oldCore + "||  NewCore " + newCore)
                if self.syschk.isChecked():
                    if (oldCore  in neslist and newCore in neslist ) or (oldCore  in sneslist and newCore in sneslist ) or (oldCore  in gbalist and newCore in gbalist ) or (oldCore  in gblist and newCore in gblist ) or (oldCore  in segalist and newCore in segalist ) or (oldCore  in commlist and newCore in commlist ):
                        res = True
                    else:
                        self.sts.append(lbs + f"<span style='color:red'>{fname} <strong>SKIPPED</strong> , due to core system mismatch</span>")
                        lbs = "<br>"
                        skips += 1
                        continue

                


                #    if not 

                if res:

                    
                    rom_file.truncate(59908)
                    rom_file.seek(59908)
                    newFileName = newCore + ";" + romName + ".gba"
               
                    rom_file.write(newFileName.encode('utf-8') + b'\x00\x00')
                    
                    dones += 1

                    moved = True
                    if not self.movechk.isChecked():
                        rompath = os.path.join(self.tpConf.cDir , "ROMS", oldCore, romName)
                        newpath = os.path.join(self.tpConf.cDir , "ROMS", newCore)
                        if os.path.exists(rompath):
                            #move file
                            if not os.path.isdir(newpath):
                                os.makedirs(newpath)
                            newrompath = os.path.join(newpath , romName)
                            try:
                                if self.copychk.isChecked():
                                    shutil.copy(rompath, newrompath)
                                else:
                                    os.replace(rompath, newrompath)
                                moved = True
                            except:
                                moved = False
                            
                        else:
                            moved = False

                    if res and not moved:
                        self.sts.append(lbs + f"<span style='color:orange'>{fname} core <strong>CHANGED</strong> , Rom file couldnt be moved/copied</span>")
                    else:
                        self.sts.append(lbs + f"<span style='color:green'>{fname} core <strong>CHANGED</strong> to {newCore}</span>")
                    lbs = "<br>"
                else:
                    skips += 1

        #self.sts.setPlainText(stext)
        QMessageBox.about(self, "Result", f"Total : {totals}\n DONE : {dones}\n SKIPPED : {skips}")
        self.status_bar.showMessage(f"RESULT : Total Files - {totals}\n DONE - {dones}\n SKIPPED - {skips}")

        return

    
