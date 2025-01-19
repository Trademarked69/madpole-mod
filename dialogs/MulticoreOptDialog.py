# GUI imports
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtCore import Qt, QTimer, QUrl, QSize
# OS imports - these should probably be moved somewhere else
import os
import tadpole_functions
import frogtool
import optdata as opt
from dialogs.DownloadProgressDialog import DownloadProgressDialog
import configparser
import io
from itertools import chain

# Subclass Qidget to create a Settings window        
class MulticoreOptDialog(QDialog):
    """
        This window should be called without a parent widget so that it is created in its own window.
    """
    def __init__(self, tpConf):
        super().__init__()
        self.tpConf = tpConf
        self.setWindowIcon(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DesktopIcon)))
        self.setWindowTitle(f"Edit Multicore OPTs")
        #self.setFixedSize(300, 200)
        self.setMinimumWidth(375)


        self.opt_lc = True;
        self.changed = {}
        self.citems = {}
        self.pitems = {}
        self.ditems= {}
        self.save = False


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
        self.layout_main.addWidget(QLabel("Select OPT Files"))
        self.optfile = QComboBox()

        self.optfile.addItems(list(opt.opts.keys()))
        

        
        self.optfile.insertItem(0,"Select Option File")
        self.optfile.setCurrentIndex(0)
        self.optfile.currentTextChanged.connect(self.loadoptions)

    
        self.layout_main.addWidget(self.optfile)

        #Option ValueS
        self.layout_opt = QGridLayout()#QHBoxLayout()
        self.layout_main.addLayout(self.layout_opt)

        self.layout_opt.addWidget(QLabel("Select Option"), 0 ,0 )

        self.layout_opt.addWidget(QLabel("Select Value") , 0 ,1 )

        self.optcombo = QComboBox()
        self.optcombo.insertItem(0,"Option")
        self.optcombo.currentTextChanged.connect(self.loadoptionvalues)
        #self.optcombo.setCurrentIndex(0)
        
        self.layout_opt.addWidget(self.optcombo , 1,0)
       

        self.valcombo = QComboBox()
        self.valcombo.insertItem(0,"Value")
        self.valcombo.currentTextChanged.connect(self.valuechanged)
        self.layout_opt.addWidget(self.valcombo , 1 , 1)
        
        self.layout_opt.setColumnMinimumWidth(0,225)
        
        #Spacer
        self.layout_main.addWidget(QLabel(" "))

        self.layout_main.addWidget(QLabel("Changed Values"))
        self.sts = QTextEdit()
        self.sts.setFixedHeight(175)
        self.sts.setStyleSheet("background-color: #efefef; font-size:8pt")
        self.layout_main.addWidget(self.sts)  


        """
        self.stubCheckbox = QCheckBox("Create STUBS For All core in ROMS")
        self.stubCheckbox.setChecked(False)
        self.stubCheckbox.stateChanged.connect(self.stubCheckClicked)
        self.layout_main.addWidget(self.stubCheckbox)
        """

        #BUTTONS
        self.layout_buttons = QHBoxLayout()
        self.layout_main.addLayout(self.layout_buttons)

        
        #Cancel Button
        self.button_cancel = QPushButton("Back")
        self.button_cancel.clicked.connect(self.accept)
        self.layout_buttons.addWidget(self.button_cancel)


        #Create STUBS Button
        self.btn_reset = QPushButton("Reset to Default")
        self.layout_buttons.addWidget(self.btn_reset)
        self.btn_reset.clicked.connect(self.resetvalues)

        self.btn_save = QPushButton("Save")
        self.layout_buttons.addWidget(self.btn_save)
        self.btn_save.clicked.connect(self.savevalues)



    def loadoptions(self):

        if not self.opt_lc:
            return
        if self.save:
            qm = QMessageBox
            ret = qm.question(self,'Discard Changes?', "Current OPT has unsaved changes , Leave and Discard Changes ?" , qm.Yes | qm.No)

            if ret == qm.No:
                self.opt_lc = False
                self.optfile.setCurrentText(self.oldoptfile)
                self.opt_lc = True
                return
            else:
                self.save = False
                self.changed = {}
                self.sts.clear()


        optfile = self.optfile.currentText()
        self.oldoptfile = optfile
        conf = configparser.ConfigParser()
        optp = os.path.join(self.tpConf.cDir, "cores", "config", optfile + ".opt")

        with open(optp) as lines:
            lines = chain(("[top]",), lines)  # This line does the trick.
            conf.read_file(lines)

        self.conf = conf
        items = dict(conf.items('top'))
        #items = {k: v.strip("\"") for (k, v) in items.items()}

        itemkeys = items.keys()
        ditems = {}
        pitems = {}
        citems = {}

        for l in opt.opts[optfile]:
            if l[0] in itemkeys:
                ditems[l[0]] = l[1]
                if l[2][0] == "*":
                    r = l[2].strip("*").split("-")
                    #pitems[l[0]] = list(range(str(r[0]), str(int(r[1]) + 1)))
                    pitems[l[0]] = [f"{i}" for i in range(int(r[0]),  int(r[1]) + 1)]
                    #print(" asteric was encountered")
                else:
                    pitems[l[0]] = list(l[2].split("|"))
                citems[l[0]] = items[l[0]].strip("\"")



        self.citems = citems
        self.ditems = ditems
        self.pitems = pitems

        self.opt_lc = False
        self.optcombo.clear()
        self.optcombo.addItems(citems.keys())

        #self.optcombo.insertItem(0,"Option")
        #self.optcombo.setCurrentIndex(0)

        self.valcombo.clear()
        #self.valcombo.insertItem(0,"Value")
        self.valcombo.addItems(pitems[self.optcombo.currentText()])
        self.valcombo.setCurrentText(citems[self.optcombo.currentText()])

        self.opt_lc = True


    def resetvalues(self):
        #print("Resetting Vallues")
        self.sts.clear()

        for k in self.citems.keys():
            self.citems[k] = self.ditems[k]

        self.opt_lc = False
        ck = self.optcombo.currentText()

        self.valcombo.setCurrentText(self.citems[ck])
        self.opt_lc = True

        self.sts.setText("<strong style='color:red'>OPT Values reset to DEFAULT. You will have to Save</strong>")
        QMessageBox.information(self, "Save" , "OPT Values reset to DEFAULT. You will have to Save")
        self.save = True



    def savevalues(self):
        #print("Saving Values")


        buf = io.StringIO()

        for k in self.citems.keys():
            self.conf.set("top", k  , f"\"{self.citems[k]}\"")

        self.conf.write(buf)

        buf.seek(0)
        next(buf)

        optfile = self.optfile.currentText()
        optp = os.path.join(self.tpConf.cDir, "cores", "config", optfile + ".opt")

        try:
            with open(optp, 'w') as fd:
                fd.write(buf.read())
            QMessageBox.information(self ,"Saved" , "OPT file SAVED")
            self.save = False
            self.accept()
        except:
            QMessageBox.error(self ,"Error" , "Error Saving OPT file")
        
    def loadoptionvalues(self):
        if not self.opt_lc:
            return

        citems = self.citems
        ditems = self.ditems
        pitems = self.pitems

        #print("loading options")

        self.opt_lc = False

        self.valcombo.clear()
        #self.valcombo.insertItem(0,"Value")
        self.valcombo.addItems(pitems[self.optcombo.currentText()])
        self.valcombo.setCurrentText(citems[self.optcombo.currentText()])

        self.opt_lc = True

    def valuechanged(self):
        if not self.opt_lc:
            return

        cv = self.valcombo.currentText()
        ck = self.optcombo.currentText()

        if(cv == self.citems[ck]):
            return

        #changed = self.changed

        if ck in self.changed.keys():
            if self.changed[ck] == cv:
                #print("changed has same value")
                return
            else:
                #print("i was here")
                self.changed[ck] = cv

        else:
            self.changed[ck] = cv

            self.citems[ck] = cv
           
        self.citems[ck] = cv
        self.save = True
        self.printChanged()


    def printChanged(self):
        self.sts.clear()
        for k,v in self.changed.items():
             self.sts.append(f"<span background:#ccc;'><strong>{k} : </strong></span><span style='font-weight:bold;color:green'><em>{v}</em></span>")

    
