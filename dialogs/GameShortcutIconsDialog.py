# GUI imports
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtCore import Qt
# OS imports - these should probably be moved somewhere else
import os
# feature imports
from PIL import Image, ImageDraw
import tadpole_functions
from tadpoleConfig import TadpoleConfig
import frogtool
import logging

tpConf = TadpoleConfig()

class GameShortcutIconsDialog(QDialog):
    """
    Dialog used to upload game shortcut with the ability to view existing selection and replacement.

    Args:
        drive (str): Path to root of froggy drive.
    """
    def __init__(self, drive, console, table , mslist):
        super().__init__()
        self.drive = drive
        self.console = console
        self.roms_path = os.path.join(self.drive, self.console)
        #This is the file we will use while modifying the existing resource file
        self.workingPNGPath = 'currentBackground.temp.png'
        #This is the working image we will use while modifying existing resource files
        self.backgroundImage = QLabel(self)
        #Setup a variable to access the current game shortcuts on the system
        self.game_shortcut_list = ["No Game", "No Game", "No Game", "No Game"]
        #Set UI on dialog
        self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.setWindowTitle("Game Shortcut Icon Selection")
        self.setWindowIcon(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DesktopIcon)))
        # Load game shortcuts
        files = frogtool.getROMList(self.roms_path)
        # need a temp list for us to work while iterating
        temp_game_shortcut_list = [''] * 4
        #found = False
        table.setRowCount(len(files))
        files.sort()
        for i, shortcut in enumerate(self.game_shortcut_list): 

            p = mslist[i]
            p = p.strip()
            if(p != ""):
                position = i+1
                if position != 0:
                    temp_game_shortcut_list[position-1] = p.rsplit( ".", 1 )[ 0 ]
                    continue

            for j, game in enumerate(files):
                # set previously saved shortcuts
                
                fe = game.rsplit( ".", 1 )[ 1 ]
                print(f"File is {game} and i is {i} and extension is {fe}")
                #if fe.toLower() == "zfb":
                
                
                    
                
                position = tadpole_functions.getGameShortcutPosition(self.drive, self.console, game)
                # save this list globally beacuse we want to use it in other places
                if position != 0:
                    temp_game_shortcut_list[position-1] = game.rsplit( ".", 1 )[ 0 ]
                    #found = True
                    #break
        #Just scan through and replace  
            for i, shortcut in enumerate(temp_game_shortcut_list):
                if shortcut == '':
                    temp_game_shortcut_list[i] = "No Game Shortcut"
            #if it didn't find a current game, it must be blank
        #save temp to final list
        self.game_shortcut_list = temp_game_shortcut_list.copy()

        # Now load Current Preview image before we do anything else
        self.load_from_Resources()
        
        #ask user if they want to use this list to find files automatically
        qm = QMessageBox()
        ret = qm.question(self, "Find shorcuts?", "Do you want Tadpole to try to find your game shortcut icons automatically \
by matching the name of the game and a folder you select?  You can change the icons it finds before it gets saved.")
        if ret == qm.Yes:
            directory = QFileDialog.getExistingDirectory()
            if len(directory) > 0:  # confirm if user selected a file
                for i, gameName in enumerate(self.game_shortcut_list):
                    gameName = os.path.basename(gameName)
                    for file in os.listdir(directory):
                        file_stripped = frogtool.strip_file_extension(file)
                        if gameName == file_stripped:
                            gameIcon = os.path.join(directory, file)
                            self.ovewrite_background_and_reload(gameIcon, i+1)
                            continue

        # Setup Main Layout
        # TODO...I should have used Grid but here we are
        self.layout_main_vertical = QVBoxLayout()
        self.layout_current_viewer = QVBoxLayout()
        self.setLayout(self.layout_main_vertical)
        self.layout_main_vertical.addLayout(self.layout_current_viewer)
        # set up the main preview
        self.layout_current_viewer.addWidget(self.backgroundImage)
        # Setup Game Shortcut Name Labels
        self.shortcut_game_labels = QHBoxLayout()
        self.layout_main_vertical.addLayout(self.shortcut_game_labels)
        # Setup buttons to change the icons
        self.shortcut_buttons = QHBoxLayout()
        self.layout_main_vertical.addLayout(self.shortcut_buttons)
        #Gameshortcut Icons 1
        self.button_icon1 = QPushButton("Change Icon 1")
        self.button_icon1.setFixedSize(100,100)
        self.button_icon1.clicked.connect(self.addShortcut)
        self.shortcut_buttons.addWidget(self.button_icon1)

        self.label1 = QLabel((self.game_shortcut_list[0]), self)
        self.label1.setWordWrap(True)  
        self.label1.setAlignment(Qt.AlignCenter)
        self.shortcut_game_labels.addWidget(self.label1, Qt.AlignCenter)
        #Gameshortcut Icons 2
        self.button_icon2 = QPushButton("Change Icon 2")
        self.button_icon2.setFixedSize(100,100)
        self.button_icon2.clicked.connect(self.addShortcut)
        self.shortcut_buttons.addWidget(self.button_icon2)

        self.label2 = QLabel((self.game_shortcut_list[1]), self)
        self.label2.setWordWrap(True)  
        self.label2.setAlignment(Qt.AlignCenter)
        self.shortcut_game_labels.addWidget(self.label2, Qt.AlignCenter)
        #Gameshortcut Icons 3
        self.button_icon3 = QPushButton("Change Icon 3")
        self.button_icon3.setFixedSize(100,100)
        self.button_icon3.clicked.connect(self.addShortcut)
        self.shortcut_buttons.addWidget(self.button_icon3)

        self.label3 = QLabel((self.game_shortcut_list[2]), self)
        self.label3.setWordWrap(True)  
        self.label3.setAlignment(Qt.AlignCenter)
        self.shortcut_game_labels.addWidget(self.label3, Qt.AlignCenter)
        
        #Gameshortcut Icons 4
        self.button_icon4 = QPushButton("Change Icon 4")
        self.button_icon4.setFixedSize(100,100)
        self.button_icon4.clicked.connect(self.addShortcut)
        self.shortcut_buttons.addWidget(self.button_icon4)

        self.label4 = QLabel((self.game_shortcut_list[3]), self)
        self.label4.setWordWrap(True)  
        self.label4.setAlignment(Qt.AlignCenter)
        self.shortcut_game_labels.addWidget(self.label4, Qt.AlignCenter)
        # Main Buttons Layout (Save/Cancel)
        self.layout_buttons = QHBoxLayout()
        self.layout_main_vertical.addLayout(self.layout_buttons)
        # Save Button
        self.button_save = QPushButton("Save")
        self.button_save.setDefault(True)
        #self.button_save.setDisabled(True)  # set disabled by default; need to wait for user to select at least new image
        self.button_save.clicked.connect(self.Finish)
        self.layout_buttons.addWidget(self.button_save)
        # Cancel Button
        self.button_cancel = QPushButton("Cancel")
        self.button_cancel.clicked.connect(self.reject)
        self.layout_buttons.addWidget(self.button_cancel)
    
    #thanks to doggyworld from discord Retro Handhelds to imrpove the icon shapes and sizes
    def round_corner(self, radius, fill):
        """Draw a round corner"""
        corner = Image.new('RGBA', (radius, radius), (0, 0, 0, 0))
        draw = ImageDraw.Draw(corner)
        draw.pieslice((0, 0, radius * 2, radius * 2), 180, 270, fill=fill)
        return corner
    
    def round_rectangle(self, size, radius, fill):
        """Draw a rounded rectangle"""
        width, height = size
        rectangle = Image.new('RGBA', size, fill)
        corner = self.round_corner(radius, fill)
        rectangle.paste(corner, (0, 0))
        rectangle.paste(corner.rotate(90), (0, height - radius)) # Rotate the corner and paste it
        rectangle.paste(corner.rotate(180), (width - radius, height - radius))
        rectangle.paste(corner.rotate(270), (width - radius, 0))
        return rectangle
    
    def resize_for_shortcut(self, game):
        max_width, max_height = 124, 124
        if tpConf.getShortcutsBorderEnabled():
            max_width, max_height = 120, 120
            
        if tpConf.getResizeRomart() and not tpConf.getShortcutsBorderEnabled():
            # Calculate the aspect ratio
            aspect_ratio = game.width / game.height
            print(game.width)
            print(aspect_ratio)
            if game.width > game.height or game.width == game.height:
                # Landscape or square image
                new_width = max_width
                new_height = int(max_width / aspect_ratio)
            else:
                # Portrait image
                new_height = max_height
                new_width = int(max_height * aspect_ratio)
                    
            # Resize the image to fit within the box while maintaining aspect ratio
            game = game.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Create a new image with a custom background color
            new_image = Image.new("RGBA", (max_width, max_height))
            
            # Calculate the position to center the image
            paste_x = (max_width - new_width) // 2
            paste_y = (max_height - new_height) // 2
            
            # Paste the resized image onto the center of the new image
            new_image.paste(game, (paste_x, paste_y))
            game = new_image
                    
        # This will resample down to 120x120 or 124x124
        game = game.convert('RGBA')
        game = game.resize((max_width, max_height), Image.Resampling.LANCZOS)
        
        if tpConf.getShortcutsBorderEnabled():
            # Create rectangles for white borders with fillet
            white_rounded_rect = self.round_rectangle((124,124), 8, "white")

            white_rounded_rect.paste(game, (2,2))
            game = white_rounded_rect

            white_rounded_rect2 = self.round_rectangle((124,124), 8, "white")
            black_rounded_rect2 = self.round_rectangle((120,120), 8, "black")
            white_rounded_rect2.paste(black_rounded_rect2, (2,2), black_rounded_rect2)

            datas = white_rounded_rect2.getdata()

            img_data = white_rounded_rect.getdata()

            newData = []
            new_imgData = []
            for idx,item in enumerate(datas):
                if item[3] == 0:
                    new_imgData.append((255, 255, 255, 0))
                else:
                    new_imgData.append(img_data[idx])

                if item[0] == 0 and item[1] == 0 and item[2] == 0:
                    newData.append((255, 255, 255, 0))
                else:
                    newData.append(item)

            white_rounded_rect2.putdata(newData)
            game.putdata(new_imgData)
            game.paste(white_rounded_rect2, (0,0), white_rounded_rect2)
        return game
    
    def ovewrite_background_and_reload(self, path, icon):
        #Following techniques by Zerter at view-source:https://zerter555.github.io/sf2000-collection/mainMenuIcoEditor.html
        #Add this to the temporary PNG
        try:
            game = Image.open(path, 'r')
            game = self.resize_for_shortcut(game)
            workingPNG = Image.open(self.workingPNGPath)
            if icon == 1:
                workingPNG.paste(game, (42,290), game)
            if icon == 2:
                workingPNG.paste(game, (186,290), game)
            if icon == 3:
                workingPNG.paste(game, (330,290), game)
            if icon == 4:
                workingPNG.paste(game, (474,290), game)
        except:
            logging.error("Failed to open {game}")
            return
        #Add to preview and save it
        workingPNG.save(self.workingPNGPath)
        img = QImage(self.workingPNGPath)
        #Update image
        self.backgroundImage.setPixmap(QPixmap().fromImage(img))
        logging.info("Added {game} to the background image")

        return True

    def load_from_Resources(self):
        ResourcePath = tadpole_functions.getBackgroundResourceFileforConsole(self.drive, self.console)
        tadpole_functions.convertRGB565toPNG(ResourcePath)
        self.workingPNGPath
        img = QImage(self.workingPNGPath)
        if (img.width(), img.height()) != (640, 480): 
            img = img.scaled(640, 480, Qt.IgnoreAspectRatio, Qt.SmoothTransformation) #Rescale new boot logo to correct size
        #Update image
        self.backgroundImage.setPixmap(QPixmap().fromImage(img))
        return True
    
    def addShortcut(self):
        sending_button = self.sender()
        #get the icon number
        file_path = QFileDialog.getOpenFileName(self, 'Open file', '',
                                            "Images (*.jpg *.png *.webp);;RAW (RGB565 Little Endian) Images (*.raw)")[0]
        if len(file_path) > 0:  # confirm if user selected a file
            #Add it to be processed
            if sending_button.text() == "Change Icon 1":
                #load into preview image
                self.ovewrite_background_and_reload(file_path, 1)
            elif sending_button.text() == "Change Icon 2":
                #load into preview image
                self.ovewrite_background_and_reload(file_path, 2)
            elif sending_button.text() == "Change Icon 3":
                #load into preview image
                self.ovewrite_background_and_reload(file_path, 3)           
            elif sending_button.text() == "Change Icon 4":
                #load into preview image
                self.ovewrite_background_and_reload(file_path, 4)   
            else:
                print(sending_button.text() + ": icon not found")
            return True #it completed
        return False #User cancelled

    def stripShortcutText(self):
        logging.info(f"GameShortcutIconsDialog~stripShortcutText: Removing shortcut text from {self.drive}")
        tadpole_functions.stripShortcutText(self.drive)

    def Finish(self):
        #Save this working TMP PNG to the right resource file
        resourceFile = frogtool.systems[self.console][3]
        tadpole_functions.convertPNGtoResourceRGB565(self.workingPNGPath, resourceFile, self.drive)
        #Last thing, let's get rid of the text under the icons.
        #The user has confirmed they want these and now they aren't the same
        #TODO: Confirm users are happy removing shortcut labels some beta testing
        #If so, just leave this
        tadpole_functions.stripShortcutText(self.drive)
        #Close dialog as we're all done
        self.accept()
