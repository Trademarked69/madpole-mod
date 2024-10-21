# GUI imports
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtCore import Qt, QTimer, QUrl, QSize
# OS imports - these should probably be moved somewhere else
import os
import tadpole_functions
import frogtool
import shutil
from dialogs.DownloadProgressDialog import DownloadProgressDialog

# Subclass Qidget to create a Settings window        
class SectionEdit(QDialog):
    """
        This window should be called without a parent widget so that it is created in its own window.
    """
    def __init__(self, tpConf):
        super().__init__()
        self.tpConf = tpConf
        self.lock = False
        self.fdata = {}
        self.sections = ["ROMS" , "FC" , "SFC" , "MD" ,"GB" , "GBC" , "GBA"  , "ARCADE"]

        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        



        self.setWindowIcon(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DesktopIcon)))
        self.setWindowTitle(f"Edit Stock Sections")
        
        self.setMinimumWidth(350)

        # Setup Main Layout
        self.layout_main = QVBoxLayout()
        self.setLayout(self.layout_main)

        #Thumbnail View options
        self.layout_main.addWidget(QLabel("How Many Sections"))
        self.sects = QComboBox()

        self.sects.addItems(["1" , "2" , "3" , "4" , "5" , "6" , "7" , "8"])
        self.sects.currentTextChanged.connect(self.enableSects)
        self.layout_main.addWidget(self.sects)

        self.layout_main.addWidget(QLabel(" "))  # spacer

        self.layout_main.addWidget(QLabel("Sections Order"))

        self.layout_sections = QGridLayout()
        self.layout_main.addLayout(self.layout_sections)

        self.slot1 = QComboBox()
        #self.slot1.addItems(["ROMS" , "FC" , "SFC" , "GB" , "GBC" , "GBA" , "MD" , "ARCADE"])
        #self.slot1.setCurrentText("ROMS")

        

        self.slot2 = QComboBox()
        #self.slot2.addItems(["ROMS" , "FC" , "SFC" , "GB" , "GBC" , "GBA" , "MD" , "ARCADE"])
        #self.slot2.setCurrentText("FC")

        self.slot3 = QComboBox()
        #self.slot3.addItems(["ROMS" , "FC" , "SFC" , "GB" , "GBC" , "GBA" , "MD" , "ARCADE"])
        #self.slot3.setCurrentText("SFC")

        self.slot4 = QComboBox()
        #self.slot4.addItems(["ROMS" , "FC" , "SFC" , "GB" , "GBC" , "GBA" , "MD" , "ARCADE"])
        #self.slot4.setCurrentText("GB")

        self.slot5 = QComboBox()
        #self.slot5.addItems(["ROMS" , "FC" , "SFC" , "GB" , "GBC" , "GBA" , "MD" , "ARCADE"])
        #self.slot5.setCurrentText("GBC")

        self.slot6 = QComboBox()
        #self.slot6.addItems(["ROMS" , "FC" , "SFC" , "GB" , "GBC" , "GBA" , "MD" , "ARCADE"])
        #self.slot6.setCurrentText("GBA")

        self.slot7 = QComboBox()
        #self.slot7.addItems(["ROMS" , "FC" , "SFC" , "GB" , "GBC" , "GBA" , "MD" , "ARCADE"])
        #self.slot7.setCurrentText("MD")

        self.slot8 = QComboBox()
        #self.slot8.addItems(["ROMS" , "FC" , "SFC" , "GB" , "GBC" , "GBA" , "MD" , "ARCADE"])
        #self.slot8.setCurrentText("ARCADE")



        self.layout_sections.addWidget(QLabel("Slot 1") , 0 , 0)
        self.layout_sections.addWidget(self.slot1 , 1 , 0)
        self.layout_sections.addWidget(QLabel("Slot 2") , 0 , 1)
        self.layout_sections.addWidget(self.slot2 , 1 , 1)
        self.layout_sections.addWidget(QLabel("Slot 3") , 2 , 0)
        self.layout_sections.addWidget(self.slot3 , 3 , 0)
        self.layout_sections.addWidget(QLabel("Slot 4") , 2 , 1)
        self.layout_sections.addWidget(self.slot4 , 3 , 1)

        self.layout_sections.addWidget(QLabel("Slot 5") , 4, 0)
        self.layout_sections.addWidget(self.slot5 , 5 , 0)
        self.layout_sections.addWidget(QLabel("Slot 6") , 4 , 1)
        self.layout_sections.addWidget(self.slot6 , 5 , 1)
        self.layout_sections.addWidget(QLabel("Slot 7") , 6 , 0)
        self.layout_sections.addWidget(self.slot7 , 7 , 0)
        self.layout_sections.addWidget(QLabel("Slot 8") , 6 , 1)
        self.layout_sections.addWidget(self.slot8 , 7 , 1)


        self.combos = [ self.slot1 , self.slot2, self.slot3, self.slot4, self.slot5, self.slot6, self.slot7, self.slot8 ]

        
        self.layout_main.addWidget(QLabel(" "))  # spacer
        
        self.layout_main.addWidget(QLabel("Start at Section"))
        self.first = QComboBox()

        self.first.addItems(self.sections)
        self.layout_main.addWidget(self.first)
        
        


        
        self.layout_main.addWidget(QLabel(" "))  # spacer

        # Main Buttons Layout (Save/Cancel)
        self.layout_buttons = QHBoxLayout()
        self.layout_main.addLayout(self.layout_buttons)
        

        self.button_cancel = QPushButton("Back")
        self.button_cancel.clicked.connect(self.accept)
        self.layout_buttons.addWidget(self.button_cancel)
        
        self.status_bar = QStatusBar()
        self.layout_main.addWidget(self.status_bar)

        #Save Existing Cover To File Button
        self.button_save = QPushButton("Save")
        self.button_save.clicked.connect(self.saveSections)
        self.layout_buttons.addWidget(self.button_save) 

        self.loadValues()

        for x in range(0 , 8):
            self.combos[x].addItem(self.sections[x])
            self.combos[x].setFont(font)

            """
            self.lock = True
            self.combos[x].setCurrentText(self.fdata["sect"+str(x)][0])
            self.lock = False
            """

        self.sects.setFont(font)
        self.first.setFont(font)

        self.sects.setCurrentText(self.fdata["total"])
        self.lock = True
        self.first.setCurrentText(self.sections[int(self.fdata["current"])] )
        self.lock = False
        #self.setHandler()


        #self.statusBar = QStatusBar()
        #self.setStatusBar(self.statusBar)    

        
        #self.setStatusBar(self.status_bar)

    

    def saveSections(self):
        print("Saving Sections")

        fdata = self.fdata
        sdata = fdata['console'] + "\n" + fdata['langs'] + "\n" + fdata['color'] + "\n"

        count = int(self.sects.currentText())

        
        for i in range(0 , 10):
            
            if i < 8:
                citem = self.combos[i].currentText()
            else:
                citem = "ROMS"

            if citem == self.first.currentText():
                sitem = str(i)
            sdata += fdata['sect' + str(i)][1] + " " + citem + "\n"

        sdata += str(count) + " " + sitem + " " + str(self.hasR(True)) + "\n"
        sdata += fdata['lastlines']

        print("\n\nTHE DATA IS \n\n")
        print(sdata)

        opath = self.tpConf.cDir + "\\Resources\\"
        ofile = os.path.join(opath , "Foldername.ini")
        nfile = os.path.join(opath , "Foldername_backup.ini")

        print(f"OLD path is {ofile}")
        print(f"NEW path is {nfile}")

        if os.path.exists(ofile):
            print("copying file now")
            shutil.copy(ofile, nfile)
        else:
            QMessageBox.information(self, "Error" , "Foldername.ini file not found , Make sure the file exists or select proper ROOT or User Directory.")
            return

        try:
            f = open(ofile, "w")
            f.truncate(0)
            f.write(sdata)
            f.close()

            QMessageBox.information(self , "Success" , "Sections Edited. You original file is backed up as Foldername_backup.ini")

        except:
            QMessageBox.information(self , "Error" , "Error Writing File")

        self.accept()


    def loadValues(self):

        fdata = {}

        cDir = self.tpConf.cDir

        cDir += "\\Resources\\Foldername.ini"

        #print(f"Directory is {cDir}")

        fpath = cDir


        print(f"Path is {cDir}")

        if not os.path.exists(fpath):
            QMessageBox.information(self,"Error" , "Foldername.ini Not found")
            return

        f = open(fpath, "r+")
        lines = list(f.readlines())
        f.close()
        #print(f"Lines are \n {lines[0]}")

        fdata['console'] = lines[0].strip("\n")
        fdata['langs'] = lines[1].strip("\n")
        fdata['color'] = lines[2].strip("\n")

        
        secdata = lines[3].strip("\n").split(" ")
        fdata["sect0"] = [secdata[1] , secdata[0] ]

        secdata = lines[4].strip("\n").split(" ")
        fdata["sect1"] = [secdata[1] , secdata[0] ]

        secdata = lines[5].strip("\n").split(" ")
        fdata["sect2"] = [secdata[1] , secdata[0] ]

        secdata = lines[6].strip("\n").split(" ")
        fdata["sect3"] = [secdata[1] , secdata[0] ]

        secdata = lines[7].strip("\n").split(" ")
        fdata["sect4"] = [secdata[1] , secdata[0] ]

        secdata = lines[8].strip("\n").split(" ")
        fdata["sect5"] = [secdata[1] , secdata[0] ]

        secdata = lines[9].strip("\n").split(" ")
        fdata["sect6"] = [secdata[1] , secdata[0] ]

        secdata = lines[10].strip("\n").split(" ")
        fdata["sect7"] = [secdata[1] , secdata[0] ]

        secdata = lines[11].strip("\n").split(" ")
        fdata["sect8"] = [secdata[1] , secdata[0] ]

        secdata = lines[12].strip("\n").split(" ")
        fdata["sect9"] = [secdata[1] , secdata[0] ]


        odata  = lines[13].strip("\n").split(" ")


        fdata["total"] = odata[0]
        fdata["current"] = odata[1]
        fdata["roms"] = odata[2]

        fdata['lastlines'] = lines[14] + lines[15]

        self.fdata = fdata

        #print("Data from file is")

        #print(fdata)


    def setHandler(self):
        for i in range(0 , 8):
            self.combos[i].currentTextChanged.connect(self.slotChanged)

    def slotChanged(self):

        if self.lock:
            return

        self.hasR()
        self.changeStart()
        #sender = self.sender()
        #print(f"Slot {sender.currentText()} changed")
                
    def enableSects(self):

        if self.lock:
            return
        count = int(self.sects.currentText())

        if count < 8:
            for i in range(count , 8):
                self.combos[i].setDisabled(True);
                #print(f"Disabled {self.combos[i].currentText()}")

        if count > 0:
            for j in range(0 , count):
                self.combos[j].setDisabled(False);

        self.changeStart()

    def hasR(self , sMsg = False):
        #hr = False;
        for x in range(0 , int(self.sects.currentText())):
            if self.combos[x].currentText() == "ROMS":
                return x

        

        if not sMsg:
            self.lock = True
            self.combos[0].setCurrentText("ROMS")
            self.lock = False
            QMessageBox.information(self , "ROMS Section" , "ROMS section has to be there , It will be the only Section if you select to have 1 Section.\
                                        \n\nSet ROMS to another slot first before changing this slot")
        
        return -1


    def changeStart(self):

        ti = []
        #self.lock = True

        for x in range(0,int(self.sects.currentText())):
            ti.append(self.combos[x].currentText())
        
        tpi = []
        for y in range(0 , 8):
            
            opi = self.first.model().item(y).text()
            #print(op)
            if opi not in ti:
                self.first.model().item(y).setEnabled(False)
                tpi.append(opi)
            else:
                self.first.model().item(y).setEnabled(True)

        if self.first.currentText() not in ti:
            self.first.setCurrentText(ti[0])
