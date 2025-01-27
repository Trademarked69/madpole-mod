# GUI imports
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
# Tadpole imports
import tadpole_functions
import os

class BootConfirmDialog(QDialog):
    """
    Dialog used to confirm boot logo selection with the ability to view existing selection and replacement.

    Args:
        drive (str): Path to root of froggy drive.
    """
    def __init__(self, drive, basedir, device):
        super().__init__()


        self.basedir = basedir
        self.drive = drive
        self.device = device

        self.setWindowTitle("Boot Image Selection")
        self.setWindowIcon(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DesktopIcon)))

        # Setup Main Layout
        self.layout_main = QVBoxLayout()
        self.setLayout(self.layout_main)

        # set up current image viewer
        self.layout_main.addWidget(QLabel("Current Image"))
        self.current_viewer = BootLogoViewer(self, basedir, device)
        self.layout_main.addWidget(self.current_viewer)

        self.layout_main.addWidget(QLabel(" "))  # spacer

        # set up new image viewer
        self.layout_main.addWidget(QLabel("New Image"))
        self.new_viewer = BootLogoViewer(self, basedir, device, changeable=True)
        self.layout_main.addWidget(self.new_viewer)

        # Main Buttons Layout (Save/Cancel)
        self.layout_buttons = QHBoxLayout()
        self.layout_main.addLayout(self.layout_buttons)

        # Save Button
        self.button_save = QPushButton("Save")
        self.button_save.setDefault(True)
        self.button_save.setDisabled(True)  # set disabled by default; need to wait for user to select new image
        self.button_save.clicked.connect(self.accept)
        self.layout_buttons.addWidget(self.button_save)

        # Cancel Button
        self.button_cancel = QPushButton("Cancel")
        self.button_cancel.clicked.connect(self.reject)
        self.layout_buttons.addWidget(self.button_cancel)

        # Load Initial Image
        self.current_viewer.load_from_bios(self.drive, self.device)


class BootLogoViewer(QLabel):
    """
    Args:
        parent (BootConfirmDialog): Parent widget. Used to enable/disable controls on parent.
        changeable (bool): If True, will allow importing new image. If False, will just allow static display.
    """
    def __init__(self, parent, basedir, device, changeable=False):
        super().__init__(parent)
        
        self.basedir = basedir
        self.changeable = changeable
        self.path = ""  # Used to store path to the currently-displayed file
        self.device = device
        self.setStyleSheet("background-color: white;")

        if device == 'SF2000':
            self.setMinimumSize(512, 200)  # resize to SF2000 boot logo dimensions
        elif device == 'GB300V2':
            self.setMinimumSize(248, 249)  # resize to GB300 V2 boot logo dimensions

        if self.changeable:
            self.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.setText("Click to Select New Image")

    def mousePressEvent(self, ev):
        """
        Overrides built-in function to handle mouse click events. Prompts user for image path and loads same.
        """
        if self.changeable:  # only do something if image is changeable
            file_name = QFileDialog.getOpenFileName(self, 'Open file', '',
                                                    "Images (*.jpg *.png *.webp);;RAW (RGB565 Little Endian) Images (*.raw)")[0]
            if len(file_name) > 0:  # confirm if user selected a file
                if self.device == 'SF2000':
                    self.load_image(file_name, 512, 200)
                elif self.device == 'GB300V2':
                    self.load_image(file_name, 248, 249)


    def load_from_bios(self, drive: str, device: str):
        """
        Extracts image from the bios and passes to load image function.

        Args:
            drive (str):  Path to the root of the Froggy drive.
            device (str): Type of device (e.g. SF2000 or GB300 V2)
        """

        with open(os.path.join(drive, "bios", "bisrv.asd"), "rb") as bios_file:
            bios_content = bytearray(bios_file.read())

        if(device == 'SF2000'):
            width = 512
            height = 200
            offset = tadpole_functions.findSequence(tadpole_functions.offset_sf2000_logo_presequence, bios_content) + 16
        elif(device == 'GB300V2'):
            width = 248
            height = 249
            offset = tadpole_functions.findSequence(tadpole_functions.offset_gb300v2_logo_multi_core_presequence, bios_content) + 16

        # TODO switch this to be in memory
        with open(os.path.join(self.basedir, "bios_image.raw"), "wb") as image_file:
            image_file.write(bios_content[offset:offset+((width*height)*2)])

        self.load_image(os.path.join(self.basedir, "bios_image.raw"), width, height)

    def load_image(self, path: str, width: int, height: int) -> bool:
        """
        Loads an image into the viewer.  If the image is loaded successfully, may enable the parent Save button based
        on the changeable flag.

        Args:
            path (str): Path to the image.  Can be .raw or other format.  If .raw, assumed to be in RGB16 (RGB565 Little
                Endian) format used for Froggy boot logos.  Must be 512x200 pixels or it will not be accepted/displayed.
            width / height (int): the size of the boot logo

        Returns:
            bool: True if image was loaded, False if not.
        """
        if os.path.splitext(path)[1] == ".raw":  # if raw image, assume RGB16 (RGB565 Little Endian)
            with open(path, "rb") as f:
                img = QImage(f.read(), width, height, QImage.Format_RGB16)
        else:  # otherwise let QImage autodetection do its thing
            img = QImage(path)
            if (img.width(), img.height()) != (width, height): 
                img = img.scaled(width, height, Qt.IgnoreAspectRatio, Qt.SmoothTransformation) #Rescale new boot logo to correct size
        self.path = path  # update path
        self.setPixmap(QPixmap().fromImage(img))

        if self.changeable:  # only enable saving for changeable dialogs; prevents enabling with load from bios
            self.parent().button_save.setDisabled(False)
        return True
