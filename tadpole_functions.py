# GUI imports
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
# OS imports
import os
import shutil
import hashlib
import zipfile
from io import BytesIO
#feature imports
import struct
import frogtool
from tadpoleConfig import TadpoleConfig
import requests
from bs4 import BeautifulSoup
import json
import logging
import time

from PIL import Image

tpConf = TadpoleConfig()


try:
    from PIL import Image, ImageDraw, ImageFont
    image_lib_avail = True
except ImportError:
    Image = None
    ImageDraw = None
    image_lib_avail = False

# This dictionary is in the following format:
# "System": []
systems_old_default = {    
    "MENU1":   ["rdbui.tax", "fhcfg.nec", "nethn.bvs",1],
    "MENU2":   ["urefs.tax", "adsnt.nec", "xvb6c.bvs",2],
    "MENU3":   ["scksp.tax", "setxa.nec", "wmiui.bvs",3],
    "MENU4":   ["vdsdc.tax", "umboa.nec", "qdvd6.bvs",4],
    "MENU5":   ["pnpui.tax", "wjere.nec", "mgdel.bvs",5],
    "MENU6":   ["vfnet.tax", "htuiw.nec", "sppnp.bvs",6], 
    "MENU7":   ["mswb7.tax", "msdtc.nec", "mfpmp.bvs",7],
    "MENU8":   ["kjbyr.tax", "djoin.nec", "ke89a.bvs",8]
}

systems_default = {
    "MENU1":   ["m01.ta", "m01.ne", "m01.bv",1],
    "MENU2":   ["m02.ta", "m02.ne", "m02.bv",2],
    "MENU3":   ["m03.ta", "m03.ne", "m03.bv",3],
    "MENU4":   ["m04.ta", "m04.ne", "m04.bv",4],
    "MENU5":   ["m05.ta", "m05.ne", "m05.bv",5],
    "MENU6":   ["m06.ta", "m06.ne", "m06.bv",6],
    "MENU7":   ["m07.ta", "m07.ne", "m07.bv",7],
    "MENU8":   ["m08.ta", "m08.ne", "m08.bv",8],
    "MENU9":   ["m09.ta", "m09.ne", "m09.bv",9],
    "MENU10":  ["m10.ta", "m10.ne", "m10.bv",10],
    "MENU11":  ["m11.ta", "m11.ne", "m11.bv",11],
    "MENU12":  ["m12.ta", "m12.ne", "m12.bv",12]
}

systems = {    
    "MENU1":   ["rdbui.tax", "fhcfg.nec", "nethn.bvs",1],
    "MENU2":   ["urefs.tax", "adsnt.nec", "xvb6c.bvs",2],
    "MENU3":   ["scksp.tax", "setxa.nec", "wmiui.bvs",3],
    "MENU4":   ["vdsdc.tax", "umboa.nec", "qdvd6.bvs",4],
    "MENU5":   ["pnpui.tax", "wjere.nec", "mgdel.bvs",5],
    "MENU6":   ["vfnet.tax", "htuiw.nec", "sppnp.bvs",6], 
    "MENU7":   ["mswb7.tax", "msdtc.nec", "mfpmp.bvs",7],
    "MENU8":   ["kjbyr.tax", "djoin.nec", "ke89a.bvs",8]
}

supported_save_ext = [
    "sav", "sa0", "sa1", "sa2", "sa3"
] 

version_displayString_1_5 = "2023.04.20 (V1.5)"
version_displayString_1_6 = "2023.08.03 (V1.6)"
version_displayString_1_7 = "2023.10.07 (V1.7)"
version_displayString_1_71 ="2023.10.13 (V1.71)"
# hash, versionName
versionDictionary = {
    "151d5eeac148cbede3acba28823c65a34369d31b61c54bdd8ad049767d1c3697": version_displayString_1_5,
    "5335860d13214484eeb1260db8fe322efc87983b425ac5a5f8b0fcdf9588f40a": version_displayString_1_6,
    "b88458bf2c25d3a34ab57ee149f36cfdc6b8a5138d5c6ed147fbea008b4659db": version_displayString_1_7,
    "08bd07ab3313e3f00b922538516a61b5846cde34c74ebc0020cd1a0b557dd54b": version_displayString_1_71,
    "cbe966565b403e9165174ad970d51f21ccd0ebdc6a8faa1a80fba4523dd2b236": version_displayString_1_6,
    "ac22b49617e2b76a09e29efc3879e0258042179002eeee8ec0e6dc82a598a49e": version_displayString_1_6,
    "95f994efb39f44476c2c275a98165afa295ecda31c7baed55300bdd8bacdf449": version_displayString_1_6,
    "9596c44c8c2ac7b21cc8fea5ae05db69d3fff73c6a9fa68ae10115c7aeece509": version_displayString_1_6
}

     #fc155b08d778b74f54e63749fb79c8e2b66bb182efaec2e0b852f0eeff8f1d0f
     #08bd07ab3313e3f00b922538516a61b5846cde34c74ebc0020cd1a0b557dd54b
     # v1.71 SHA256 : fb772d3af075f60cf26a0b923d428bfa35907fff168f55aaa328fd89e21cbb2b

ROMART_baseURL = "https://thumbnails.libretro.com/"

ROMArt_console = {  # Only common rom extensions, along with zxx files
    "zfc":     "Nintendo - Nintendo Entertainment System",      
    "zsf":     "Nintendo - Super Nintendo Entertainment System",
    "zmd":     "Sega - Mega Drive - Genesis",  #TODO: treat zmd as all sega, wrap and read to find out which sega console
    "zgb":     "Nintendo - Game Boy",   #TODO: wrap and read zgb files to find out if its gb/gbc/gba
    "zfb":     "Nintendo - Nintendo Entertainment System", #TODO: wrap and read to see which multicore console and give a warning if its aracde or not found
    "zpc":     "NEC - PC Engine - TurboGrafx 16",
    "nes":     "Nintendo - Nintendo Entertainment System",
    "smc":     "Nintendo - Super Nintendo Entertainment System",
    "sfc":     "Nintendo - Super Nintendo Entertainment System",
    "gb":      "Nintendo - Game Boy",
    "gbc":     "Nintendo - Game Boy Color",
    "gba":     "Nintendo - Game Boy Advance", 
    "sms":     "Sega - Master System - Mark III",
    "md":      "Sega - Mega Drive - Genesis",
    "smd":     "Sega - Mega Drive - Genesis",
    "gen":     "Sega - Mega Drive - Genesis",
    "gg":      "Sega - Game Gear",
    "ws":      "Bandai - WonderSwan", 
    "wsc":     "Bandai - WonderSwan Color", 
    "ngp":     "SNK - Neo Geo Pocket", 
    "ngc":     "SNK - Neo Geo Pocket Color", 
    "pce":     "NEC - PC Engine - TurboGrafx 16"
}

def GetLibretroROMArtUrl(rom_extension):
    url = ROMART_baseURL + ROMArt_console[rom_extension.lower()] + "/Named_" + tpConf.getLibretroThumbnailType() + "/"
    print("libretro ROMArt url is", url)
    return url

def downloadROMArt(rom_path, rom):
    romName = os.path.splitext(rom)[0]
    romExtension = os.path.splitext(rom)[1][1:]
    newThumbnailFile = os.path.join(rom_path, romName + ".png")
    url = GetLibretroROMArtUrl(romExtension) + romName + ".png"       
    response = requests.get(url)
    if response.status_code == 200:
        with open(newThumbnailFile, "wb") as f:
            f.write(response.content)
        print("Downloaded", url)        
        return True    
    else:
        print("Could not downlaod", url)  
        return False  

def GetLibretroROMArtList(romList):
    ext_to_roms = {}
    png_files = []
    
    # Group ROMs by their extension
    for rom in romList:
        rom_ext = os.path.splitext(rom)[1][1:] 
        if rom_ext not in ext_to_roms:
            ext_to_roms[rom_ext] = []
        ext_to_roms[rom_ext].append(rom)
    
    # Download HTML for each system once and process PNG links
    for ext, roms in ext_to_roms.items():
        url = GetLibretroROMArtUrl(ext)
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                if href.endswith('.png'):
                    href = href.replace('%20', ' ')
                    png_files.append(href)
    
    return png_files

def resize_image(file_path): # Resize a single png
    max_width, max_height = 144, 208
    image = Image.open(file_path)
        
    # Calculate the aspect ratio
    aspect_ratio = image.width / image.height
    if image.width > image.height or image.width == image.height:
        # Landscape or square image
        new_width = max_width
        new_height = int(max_width / aspect_ratio)
    else:
        # Portrait image
        new_height = max_height
        new_width = int(max_height * aspect_ratio)
                    
    # Resize the image to fit within the box while maintaining aspect ratio
    image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
    # Create a new image with a custom background color
    new_image = Image.new("RGBA", (max_width, max_height), tpConf.getRomartBackgroundColor())
            
    # Calculate the position to center the image
    paste_x = (max_width - new_width) // 2
    paste_y = (max_height - new_height) // 2
            
    # Paste the resized image onto the center of the new image
    new_image.paste(image, (paste_x, paste_y))
            
    # Save the modified image
    new_image.save(file_path, quality=100)

def resize_images(directory): # Resize all .png files in a directory
    for filename in os.listdir(directory):
        if filename.endswith('.png'):
            image_path = os.path.join(directory, filename)
            resize_image(image_path)
            

offset_sf2000_logo_presequence = [0x62, 0x61, 0x64, 0x5F, 0x65, 0x78, 0x63, 0x65, 0x70, 0x74, 0x69, 0x6F, 0x6E, 0x00, 0x00, 0x00]
offset_gb300v2_logo_multi_core_presequence = [0x6E, 0x74, 0x61, 0x6C, 0x5F, 0x74, 0x79, 0x70, 0x65, 0x5F, 0x69, 0x6E, 0x66, 0x6F, 0x45, 0x00]
offset_buttonMap_presequence = [0x00, 0x00, 0x00, 0x71, 0xDB, 0x8E, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
offset_buttonMap_postsequence = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00]

class Exception_InvalidPath(Exception):
    pass    

class Exception_StopExecution(Exception):
    pass   
    
class InvalidURLError(Exception):
    pass
   
def changeBootLogo(index_path, newLogoFileName, msgBox, device):
    # Load the new Logo
    msgBox.setText("Uploading new boot logo...")
    msgBox.showProgress(25, True)
    #load bisrv into memory
    file_handle = open(index_path, 'rb')  # rb for read, wb for write
    bisrv_content = bytearray(file_handle.read(os.path.getsize(index_path)))
    file_handle.close()
    #get location of boot logo 
    newLogo = QImage(newLogoFileName)
    if device == 'SF2000':
        logoOffset = findSequence(offset_sf2000_logo_presequence, bisrv_content,
        10000000)
        width = 512
        height = 200
    if device == 'GB300V2':
        logoOffset = findSequence(offset_gb300v2_logo_multi_core_presequence, bisrv_content,
        10000000)
        width = 248
        height = 249
    bootLogoStart = logoOffset + 16
    # Convert to RGB565
    msgBox.setText("Converting boot logo...")
    msgBox.showProgress(40, True)
    rgb565Data = QImageToRGB565Logo(newLogo, width, height)
    # Change the boot logo
    msgBox.setText("Updating boot logo...")
    msgBox.showProgress(60, True)
    
    for i in range(0, width*height):
        data = rgb565Data[i].to_bytes(2, 'little')
        bisrv_content[bootLogoStart+i*2] = data[0]
        bisrv_content[bootLogoStart+i*2+1] = data[1]
    print("Patching CRC")    
    bisrv_content = patchCRC32(bisrv_content)
    msgBox.setText("Uploading BIOS file...")
    msgBox.showProgress(90, True)
    print("Writing bisrv to file")
    file_handle = open(index_path, 'wb')  # rb for read, wb for write
    file_handle.write(bisrv_content)    
    file_handle.close()
    msgBox.showProgress(99, True)
    return True

def patchCRC32(bisrv_content):
    x = crc32mpeg2(bisrv_content[512:len(bisrv_content):1])    
    bisrv_content[0x18c] = x & 255
    bisrv_content[0x18d] = x >> 8 & 255
    bisrv_content[0x18e] = x >> 16 & 255
    bisrv_content[0x18f] = x >> 24
    return bisrv_content

def crc32mpeg2(buf, crc=0xffffffff):
    for val in buf:
        crc ^= val << 24
        for _ in range(8):
            crc = crc << 1 if (crc & 0x80000000) == 0 else (crc << 1) ^ 0x104c11db7
    return crc
     
def QImageToRGB565Logo(inputQImage, width, height):
    print("Converting supplied file to boot logo format")
    # Need to increase the size to 512x200
    inputQImage = inputQImage.scaled(width, height, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
    inputQImage = inputQImage.convertToFormat(QImage.Format_RGB16)
    rgb565Data = []
    for y in range(0, height):
        for x in range(0, width):
            pixel = inputQImage.pixelColor(x,y)
            pxValue = ((pixel.red() & 248) << 8) + ((pixel.green() & 252) << 3) + (pixel.blue() >> 3)
            rgb565Data.append(pxValue)
    print("Finished converting image to boot logo format")
    return rgb565Data   

def changeZIPThumbnail(romPath, newImpagePath, romExtension):
    try:
        newLogoPath = os.path.dirname(romPath)
        newLogoName = os.path.basename(newImpagePath)
        romFile = os.path.basename(romPath)
        new_romPath = os.path.dirname(romPath)
        newLogoFile = os.path.join(newLogoPath, newLogoName)
        if newLogoFile != newImpagePath:
            shutil.copyfile(newImpagePath, newLogoFile)
        sys_zxx_ext = frogtool.zxx_ext_romext(romExtension)
        zxx_file_name = f"{frogtool.strip_file_extension(romFile)}.{sys_zxx_ext}"
        zxx_file_name = os.path.splitext(romFile)[0] + "." + sys_zxx_ext 
        zxx_file_path = os.path.join(new_romPath, zxx_file_name)
        converted = frogtool.rgb565_convert(newLogoFile, zxx_file_path, (144, 208))
        if not converted:
            return False
        zxx_file_handle = open(zxx_file_path, "ab")
        zip_file_handle = open(romPath, "rb")
        zxx_file_handle.write(zip_file_handle.read())
        zxx_file_handle.close()
        zip_file_handle.close()
    except Exception as e:
        print(f"! Failed changing zip file")
        logging.error("Could not change thumbnail" + str(e))
        return False

    try:
        os.remove(newLogoFile)
        os.remove(romPath)
    except (OSError, IOError):
        print(f"! Failed deleting source file(s) after creating {zxx_file_name}")
        return False

    return True

def changeZXXThumbnail(romPath, imagePath):
    tempPath = f"{romPath}.tmp"
    converted = frogtool.rgb565_convert(imagePath, tempPath, (144, 208))
    if not converted:
        return False
    # copy the rom data to the temp
    try:
        temp_file_handle = open(tempPath, "ab")
        zxx_file_handle = open(romPath, "rb")
        romData = bytearray(zxx_file_handle.read())
        temp_file_handle.write(romData[59904:])
        temp_file_handle.close()
        zxx_file_handle.close()
    except (OSError, IOError):
        print(f"! Failed appending zip file to ")
        return False
    try:
        shutil.move(tempPath,romPath)
    except (OSError, IOError) as error:
        print(f"! Failed moving temp files. {error}")
        return False
    return True

def getImageData565(src_filename, dest_size=None):
    if not image_lib_avail:
        print("! Pillow module not found, can't do image conversion")
        return False
    try:
        srcimage = Image.open(src_filename)
    except (OSError, IOError):
        print(f"! Failed opening image file {src_filename} for conversion")
        return False

    # convert the image to RGB if it was not already
    image = Image.new('RGB', srcimage.size, (0, 0, 0))
    image.paste(srcimage, None)

    if dest_size and image.size != dest_size:
        #TODO: let user decide to stretch or not
        maxsize = (144, 208)
        image = image.thumbnail(maxsize, Image.ANTIALIAS) 

    image_height = image.size[1]
    image_width = image.size[0]
    pixels = image.load()

    if not pixels:
        print(f"! Failed to load image from {src_filename}")
        return False
    rgb565Data = []
    for h in range(image_height):
        for w in range(image_width):
            pixel = pixels[w, h]
            if not type(pixel) is tuple:
                print(f"! Unexpected pixel type at {w}x{h} from {src_filename}")
                return False
            r = pixel[0] >> 3
            g = pixel[1] >> 2
            b = pixel[2] >> 3
            rgb = (r << 11) | (g << 5) | b
            rgb565Data.append(struct.pack('H', rgb))
    return rgb565Data

def bisrv_getFirmwareVersion(index_path):
    print(f"trying to read {index_path}")
    try:
        file_handle = open(index_path, 'rb')  # rb for read, wb for write
        bisrv_content = bytearray(file_handle.read(os.path.getsize(index_path)))
        file_handle.close()
        print("Finished reading file")        
        print("start finding powercurve")
        prePowerCurve = findSequence([0x11, 0x05, 0x00, 0x02, 0x24], bisrv_content,3000000)
        print(f"found pre-powercurve - ({prePowerCurve})")
        if prePowerCurve > -1:
            powerCurveFirstByteLocation = prePowerCurve + 5
            if powerCurveFirstByteLocation == 0x3564EC:
                # Seems to match August 3rd layout...
                version = version_displayString_1_6

            elif powerCurveFirstByteLocation == 0x356638:
                #Seems to match October 7th/13th layout...
                version = version_displayString_1_71        
            else:
                Version = "UNKNOWN"
        else:
            Version = "UNKNOWN"
            
        return version
    
    except (IOError, OSError):
        print("! Failed reading bisrv.")
        print("  Check the SD card and file are readable, and the file is not open in another program.")
        raise Exception_InvalidPath

class Exception_InvalidConsole(Exception):
    pass

class Exception_InvalidGamePosition(Exception):
    pass


"""
index_path should be the Drive of the Frog card only. It must inlude the semicolon if relevant. ie "E:"
console must be a supported console from the tadpole_functions systems array.
position is a 0-based index of the short. values 0 to 3 are considered valid.
game should be the file name including extension. ie Final Fantasy Tactics Advance (USA).zgb
"""

def changeGameShortcut(drive, console, position, game):
    # Check the passed variables for validity
    if not(0 <= position <= 3):
        raise Exception_InvalidPath
    if not (console in systems.keys()):
        raise Exception_InvalidConsole
        
    try:
        #Read in all the existing shortcuts from file
        xfgle_filepath = os.path.join(drive, "Resources", "xfgle.hgp")
        xfgle_file_handle = open(xfgle_filepath, "r", encoding="utf-8")
        lines = xfgle_file_handle.readlines()
        xfgle_file_handle.close()
        # Check that xfgle had the correct number of lines, if it didnt we will need to fix it.
        if lines == 0:
            raise IOError

        prefix = getPrefixFromConsole(console)
        # Bug fix: Arcade shortcuts point to the ZIP file not the zfb file
        if console == 'ARCADE':
            #Arcade is special as its location is embedded in the ZFB
            #so we need to go get it
            #Regression fix: we must pass in the zfb as that is the path
            #game = game + '.zfb'
            ROM_path = os.path.join(drive, console, game)
            game = extractFileNameFromZFB(ROM_path)
        # Overwrite the one line we want to change
        lines[4*systems[console][3]+position] = f"{prefix} {game}*\n"
        # Save the changes out to file
        xfgle_file_handle = open(xfgle_filepath, "w", encoding="utf-8")
        for line in lines:
            xfgle_file_handle.write(line)
        xfgle_file_handle.close() 


        #WRITE CONSOLE AND POSITION TO THE INI if its a MULTICORE ZFB


    except (OSError, IOError) as e:
        logging.error(f"tadpole_functions~changeGameShortcut: Failed changing the shortcut file. {str(e)}")
        return False
  
    return -1



# NOTE: this doesn't really work as the shortcuts persist visually so removing
# will just mean the links don't go to anything
# def deleteGameShortcut(index_path, console, position, game):
#     # Check the passed variables for validity
#     if not(0 <= position <= 3):
#         raise Exception_InvalidPath
#     if not (console in systems.keys()):
#         raise Exception_InvalidConsole
        
#     try:
#         trimmedGameName = frogtool.strip_file_extension(game)
#         #print(f"Filename trimmed to: {trimmedGameName}")
#         #Read in all the existing shortcuts from file
#         xfgle_filepath = os.path.join(index_path, "Resources", "xfgle.hgp")
#         xfgle_file_handle = open(xfgle_filepath, "r")
#         lines = xfgle_file_handle.readlines()
#         xfgle_file_handle.close()
#         prefix = getPrefixFromConsole(console)
#         # Overwrite the one line we want to change
#         lines[4*systems[console][3]+position] = f"{prefix} {game}*\n"
#         # Save the changes out to file
#         xfgle_file_handle = open(xfgle_filepath, "w")
#         for line in lines:
#             if line.strip("\n") != f"{prefix} {game}*":
#                 xfgle_file_handle.write(line)
#         xfgle_file_handle.close()       
#     except (OSError, IOError):
#         print(f"! Failed changing the shortcut file")
#         return False
  
#     return -1

#returns the position of the game's shortcut on the main screen.  If it isn't a shortcut, it returns 0  
def getGameShortcutPosition(drive, console, game):
    

    # CHECK game in section [drive]
    #if found get the position and return



    try:
        gamePath = os.path.join(drive, console, game)
        #Read in all the existing shortcuts from file
        xfgle_filepath = os.path.join(drive, "Resources", "xfgle.hgp")
        xfgle_file_handle = open(xfgle_filepath, "r")
        lines = xfgle_file_handle.readlines()
        xfgle_file_handle.close()
        prefix = getPrefixFromConsole(console)
        #Arcade is special; the actual game name is embedded in the ZFB
        if(console == "ARCADE" ):
            game = extractFileNameFromZFB(gamePath)             
        savedShortcut = f"{prefix} {game}*\n"
        # see if this game is listed.  If so get its position
        for i, gameShortcutLine in enumerate(lines):
            if gameShortcutLine == savedShortcut:
                #print("Found " + savedShortcut + "as shortcut")
                #now we found the match of the raw location, now we need to return the position from console
                #from xfgle, the positions start with 3 random lines, and then go down in order from FC -> SNES -> ... -> Arcade
                if(console == "FC" ):
                    return (i - 3)
                if(console == "SFC" ):
                    return (i - 7)
                if(console == "MD" ):
                    return (i - 11)
                if(console == "GB" ):
                    return (i - 15)
                if(console == "GBC" ):
                    return (i - 19)
                if(console == "GBA" ):
                    return (i - 23)
                if(console == "ARCADE" ):
                    return (i - 27)
        return 0      
    except (OSError, IOError):
        print(f"! Failed changing the shortcut file")
        return 0

#Although not required, if you don't have seperate prefixes, games with same ROM names/extension
# e.g. Gameboy, gameboy color, and gameboy advance can get confused when loading the shortcuts in other systems.  
def getPrefixFromConsole(console):
    return systems[console][3]

def findSequence(needle, haystack, offset = 0):
    # Loop through the data array starting from the offset
    for i in range(len(haystack) - offset - len(needle) + 1):
        readpoint = offset + i
        # Assume a match until proven otherwise
        match = True
        # Loop through the target sequence and compare each byte
        for j in range(len(needle)):
            if haystack[readpoint + j] != needle[j]:
                # Mismatch found, break the inner loop and continue the outer loop
                match = False
                break
        # If match is still true after the inner loop, we have found a match
        if match:
            # Return the index of the first byte of the match
            return readpoint
    # If we reach this point, no match was found
    return -1
    

    
"""
This function is used to check if the supplied path has relevant folders and files for an SF2000 SD card. 
This should be used to prevent people from accidentally overwriting their other drives.
If the correct files are found it will return True.
If the correct files are not found it will return False.
"""
def checkDriveLooksFroggy(froggypath):
    bisrvpath = os.path.join(froggypath,"bios","bisrv.asd")
    if os.path.exists(bisrvpath):
        return True
    return False


def get_firmware_versions(device):
    OS_options = {} #This approach means that two items must never have the same name or there will be a collision. 
    # Get firmware from tadpole storage
    if device == 'SF2000':
        # TODO fix the repo and switch to that then make a new json
        response = requests.get("https://tadpolestorage.blob.core.windows.net/$web/os.json")
        if response.status_code == 200:
            data = json.loads(response.content)
            # Read official firmware versions
            for item in data["official"]["versions"]:
                title = item["title"]
                link = item["link"]
                OS_options[title] = link
            # Read multicore firmware versions
            for item in data["multicore"]["versions"]:
                title = item["title"]
                link = item["link"]
                OS_options[title] = link  
            return OS_options  
    elif device == 'GB300V2':
        url = 'https://api.github.com/repos/jasongrieves/SF2000_Resources/contents/OS/' + device
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.content)
            for item in data:
                OS_options[item['name'].replace(".zip", "")] = item['download_url']
            return OS_options
    raise ConnectionError("Unable to obtain OS resources. (Status Code: {})".format(response.status_code))


def get_background_music():
    """gets index of background music from provided GitHub API URL"""
    music = {}
    # TODO switch to json so we don't keep hosting others work
    url="https://api.github.com/repos/EricGoldsteinNz/SF2000_Resources/contents/BackgroundMusic"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.content)
        for item in data:
            music[item['name'].replace(".bgm", "")] = item['download_url']
        return music
    raise ConnectionError("Unable to obtain music resources. (Status Code: {})".format(response.status_code))

def get_themes(device) -> bool:
    """gets index of theme from provided GitHub API URL"""
    theme = {}
    # TODO switch to json so we don't keep hosting others work
    url = 'https://api.github.com/repos/jasongrieves/SF2000_Resources/contents/Themes/' + device
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.content)

        for item in data:
            theme[item['name'].replace(".zip", "")] = item['download_url']
        return theme
    raise ConnectionError("Unable to obtain theme resources. (Status Code: {})".format(response.status_code))

def get_boot_logos(device) -> bool:
    """gets index of theme from provided GitHub API URL"""
    bootlogos = {}
    # TODO switch to json so we don't keep hosting others work
    url = 'https://api.github.com/repos/jasongrieves/SF2000_Resources/contents/BootLogos/' + device
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.content)
        for item in data:
            bootlogos[item['name'].replace(".zip", "")] = item['download_url']
        return bootlogos
    raise ConnectionError("Unable to obtain boot logo resources. (Status Code: {})".format(response.status_code))


"""
This function downloads a file from the internet and renames it to pagefile.sys to replace the background music.
"""

def changeBackgroundMusic(drive_path: str, url: str = "", file: str = "") -> bool:
    """
    Changes background music to music from the provided URL or file

    Params:
        url (str):  URL to music file to use for replacement.
        file (str):  Full path to a local file to use for replacement.

    Returns:
        bool: True if successful, False if not.

    Raises:
        ValueError: When both url and file params are provided.
    """
    if url and not file:
        return downloadAndReplace(drive_path, os.path.join("Resources","pagefile.sys"), url)
    elif file and not url:
        try:
            shutil.copyfile(file, os.path.join(drive_path, "Resources", "pagefile.sys"))
            return True
        except:
            return False
    else:
        raise ValueError("Provide only url or path, not both")

"""
This function downloads a file from the internet and downloads it to resources.
"""


def changeTheme(drive_path: str, url: str = "", file: str = "", progressBar: QProgressBar = "") -> bool:
    """
    Changes background theme from the provided URL or file

    Params:
        url (str):  URL to theme files to use for replacement.
        file (str):  Full path to a zip file to use for replacement.
        ProgressBar: address of the progressbar to update on screen
    Returns:
        bool: True if successful, False if not.

    Raises:
        ValueError: When both url and file params are provided.
    """
    # TODO do this in memory instead
    if url and not file:
        zip_file = "theme.zip"
        downloadFileFromGithub(zip_file, url)
        try:
            with zipfile.ZipFile(zip_file) as zip:
                progressBar.setMaximum(len(zip.infolist()))
                progress = 6
                #TODO: Hacky but assume any zip folder with more than 55 files is not a theme zip
                #TODO: Seems the GB300 has a bunch of extra files... yikes
                #if len(zip.infolist()) > 55:
                #    return False
                for zip_info in zip.infolist():     
                    #print(zip_info)
                    if zip_info.is_dir():
                        continue
                    zip_info.filename = os.path.basename(zip_info.filename)
                    progress += 1
                    progressBar.setValue(progress)
                    QApplication.processEvents()
                    resourcePath = os.path.join(drive_path, "Resources")
                    zip.extract(zip_info, resourcePath)
                    #Cleanup temp zip file
            if os.path.exists(zip_file):
                    os.remove(zip_file)   
            return True
        except:
            if os.path.exists(zip_file):
                os.remove(zip_file)   
            return False

        return True
    elif file and not url:
        try:
            with zipfile.ZipFile(file) as zip:
                progressBar.setMaximum(len(zip.infolist()))
                progress = 2
                for zip_info in zip.infolist():     
                    #print(zip_info)
                    if zip_info.is_dir():
                        continue
                    zip_info.filename = os.path.basename(zip_info.filename)
                    progress += 1
                    progressBar.setValue(progress)
                    QApplication.processEvents()
                    #TODO validate this is a real theme...maybe just check a set of files?
                    resourcePath =  os.path.join(drive_path, "Resources")
                    zip.extract(zip_info, resourcePath)
            return True
        except:
            return False
    else:
        raise ValueError("Error updating theme")

def changeConsoleLogos(drivePath, url=""):
    return downloadAndReplace(drivePath, os.path.join("Resources","sfcdr.cpl"), url)    


def downloadAndReplace(drivePath, fileToReplace, url=""):
    try:
        # retrieve bgm from GitHub resources
        content = ""
        if not url == "":
            print(f"Downloading {fileToReplace} from {url}")
            content = requests.get(url).content

        if not content == "":
            #write the content to file
            bgmPath = os.path.join(drivePath, fileToReplace)
            file_handle = open(bgmPath, 'wb') #rb for read, wb for write
            file_handle.write(content)
            file_handle.close()
        print ("Finished download and replace successfully")
        return True
    except (OSError, IOError) as error:
        print("An error occured while trying to download and replace a file.")
        return False
      
def downloadDirectoryFromGithub(location, url, progressBar):
    response = requests.get(url) 
    if response.status_code == 200:
        data = json.loads(response.content)
        downloadTotal = 0
        progressBar.setMaximum(len(data)+1)
        for item in data:
            if item["type"] == "dir":
                #create folder then recursively download
                foldername = item["name"]
                destination = os.path.join(location,foldername)
                print(f"creating directory if it doesnt exist {destination}")
                os.makedirs(destination, exist_ok=True)
                downloadDirectoryFromGithub(destination, item["url"], progressBar)
            else:# all other cases should be files
                filename = item["name"]
                downloadFileFromGithub(os.path.join(location,filename), item["download_url"])
                downloadTotal += 1
                progressBar.setValue(downloadTotal)
                QApplication.processEvents()
                
        return True
    raise ConnectionError("Unable to V1.5 Update. (Status Code: {})".format(response.status_code))
    return False
    
def downloadFileFromGithub(outFile, url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(outFile, 'wb') as f:
                print(f'downloading {url} to {outFile}')
                f.write(response.content)
            return True
        else:
            print("Error when trying to download a file from Github. Response was not code 200")
            raise InvalidURLError
    except Exception as e:
        print(str(e))
        return False

"""
#This function has been replaced by "downloadAndExtractZIPBar"
def downloadAndExtractZIP(root, url, progress):
    try:
        response = requests.get(url)
        logging.info(f"tadpole_functions~downloadAndExtractZIP: Received {response.status_code} for ({url}) with length {len(response.content)}")
        if response.status_code == 200:
            progress.showProgress(50, True)
            zip = zipfile.ZipFile(BytesIO(response.content))
            zip.extractall(path=root)          
            return True
        else: 
            logging.error("tadpole_functions~downloadAndExtractZIP: Problem when trying to download a file from Github. Response was not code 200")
            raise InvalidURLError
    except Exception as e:
        logging.error(f"tadpole_functions~downloadAndExtractZIP: ERROR {str(e)}")
    return False
"""

def downloadAndExtractZIPBar(root, url, progress):
    try:
        logging.info(f"tadpole_functions~downloadAndExtractZIPBar: Downloading ({url}) to extract to ({root})")
        response = requests.get(url, stream=True)
        total_length = int(response.headers.get('content-length'))
        dl = 0
        zip_in_memory = bytearray()
        for data in response.iter_content(chunk_size=4096):
            if data:
                dl += len(data)
                zip_in_memory.extend(data)  
                progress.showProgress(int(100 * dl / total_length), True)
        logging.info(f"tadpole_functions~downloadAndExtractZIPBar: Received {response.status_code} for ({url})")
        if response.status_code == 200:
            progress.setText("Extracting")
            progress.showProgress(0, True)
            zip = zipfile.ZipFile(BytesIO(zip_in_memory))
            zip.extractall(path=root)   
            progress.showProgress(100, True)       
            return True
        else: 
            logging.error("tadpole_functions~downloadAndExtractZIPBar: Problem when trying to download a file from Github. Response was not code 200")
            raise InvalidURLError
    except Exception as e:
        logging.error(f"tadpole_functions~downloadAndExtractZIPBar: ERROR {str(e)}")
    return False

#Keeping this for now as a failsafe, but should remove it to follow the new design structure
def DownloadOSFiles(correct_drive, progress): 
    downloadDirectoryFromGithub(correct_drive,"https://api.github.com/repos/EricGoldsteinNz/SF2000_Resources/contents/OS/V1.6", progress)
    #Make the ROM directories
    os.mkdir(os.path.join(correct_drive,"ARCADE"))
    os.mkdir(os.path.join(correct_drive,"ARCADE","bin"))
    os.mkdir(os.path.join(correct_drive,"ARCADE","save"))
    os.mkdir(os.path.join(correct_drive,"ARCADE","skp"))
    os.mkdir(os.path.join(correct_drive,"FC"))
    os.mkdir(os.path.join(correct_drive,"FC","save"))
    os.mkdir(os.path.join(correct_drive,"GB"))
    os.mkdir(os.path.join(correct_drive,"GB","save"))
    os.mkdir(os.path.join(correct_drive,"GBC"))
    os.mkdir(os.path.join(correct_drive,"GBC","save"))
    os.mkdir(os.path.join(correct_drive,"GBA"))
    os.mkdir(os.path.join(correct_drive,"GBA","save"))
    os.mkdir(os.path.join(correct_drive,"MD"))
    os.mkdir(os.path.join(correct_drive,"MD","save"))
    os.mkdir(os.path.join(correct_drive,"SFC"))
    os.mkdir(os.path.join(correct_drive,"SFC","save"))
    os.mkdir(os.path.join(correct_drive,"ROMS"))
    os.mkdir(os.path.join(correct_drive,"ROMS","save")) 
    #Need to delete bisrv.asd again to prevent bootloader bug      
    if os.path.exists(os.path.join(correct_drive,"bios","bisrv.asd")):
        os.remove(os.path.join(correct_drive,"bios","bisrv.asd"))
    #Re-add biserv.asd
    #TODO: Review why we are doing this
    #Jason: Per Dteyn, we need to remove and redownlaod bisrv.asd to clear the known bug bootloader crash
    downloadFileFromGithub(os.path.join(correct_drive,"bios","bisrv.asd"), "https://raw.githubusercontent.com/EricGoldsteinNz/SF2000_Resources/main/OS/V1.6/bios/bisrv.asd")        
    return True

def emptyFavourites(drive) -> bool:
    return emptyFile(os.path.join(drive, "Resources", "Favorites.bin"))
    
def emptyFile(path) -> bool:
    print(f"Deleting file {path}")
    try:      
        if os.path.isfile(path):
            os.remove(path)
        else:
            print("File not found, guess thats still a success? @Goldstein to check the spelling if this is a bug")
        return True
    except:
        print("Error while trying to delete a file")
    return False

def emptyHistory(drive) -> bool:
    return emptyFile(os.path.join(drive, "Resources", "History.bin"))

#Thanks Von Millhausen
#The first 59,905 bytes are for the thumbnail image (208px * 144px, stored in RGB565 format which is two bytes per pixel),
# then there's four null bytes, then there's the name of a .zip file with no path (presumably /ARCADE/bin/ is hardcoded), and then finally two null bytes 
def extractFileNameFromZFB(romFilePath):
    try:
        with open(romFilePath, "rb") as rom_file:
            #get past the RAW image
            rom_file.seek(59908)
            #need to now go until we find the null bytes
            rom_file_end = rom_file.read()
            rom_name_content = bytearray()
            i = 0
            while i < len(rom_file_end):
                if rom_file_end[i] == 0x00 and rom_file_end[i+1] == 0x00:
                    break
                rom_name_content.append(rom_file_end[i])
                i += 1
            #rom_content = bytearray(rom_file.read(907))
            fileName = rom_name_content.decode()
            logging.info(f"({fileName}) decoded from ZFB")
            return fileName
    except Exception as e:
        logging.error(f"tadpole_functions~extractFileNameFromZFB: error {str(e)}")
        return ''

#Thanks DTeyn for the code!: https://github.com/Dteyn/ZFBTool/blob/master/ZFBTool.pyw
def createZFBFile(drive, pngPath, romPath):
    """Creates a .ZFB file with input .PNG file and ARCADE ROM .ZIP name"""
    # Define the size of the thumbnail
    thumb_size = (144, 208)
    try:
        #if its blank, just give it 1's as raw data for the first bytes
        if pngPath == '': 
            raw_data_bytes = bytes(b'\x01' * 59904)
        else:
            with Image.open(pngPath) as img:
                img = img.resize(thumb_size)
                img = img.convert("RGB")
                raw_data = []
                # Convert image to RGB565
                for y in range(thumb_size[1]):
                    for x in range(thumb_size[0]):
                        r, g, b = img.getpixel((x, y))
                        rgb = ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)
                        raw_data.append(struct.pack('H', rgb))
                raw_data_bytes = b''.join(raw_data)
        # Create .zfb filename
        ZIPName = os.path.basename(romPath)
        ROMName = os.path.splitext(ZIPName)[0]
        zfb_file = os.path.join(drive, 'ARCADE', ROMName + '.zfb')
        
        # Now we write the entire ZFB file
        with open(zfb_file, 'wb') as zfb:
            # Write the image data to the .zfb file
            zfb.write(raw_data_bytes)
            # Write four 00 bytes
            zfb.write(b'\x00\x00\x00\x00')
            # Write the ROM filename
            zfb.write(ZIPName.encode())
            # Write two 00 bytes
            zfb.write(b'\x00\x00')
        logging.info(f"ZFB file created successfully.")
        return True
    except Exception as e:
        logging.error(f"An error occurred while creating the ZFB file: {str(e)}")
        return False



def deleteROM(ROMfilePath):
    logging.info(f"Tadpole_functions~ Deleting ROM: {ROMfilePath}")
    ext = os.path.splitext(ROMfilePath)[1]
    if(ext.lower() == ".zfb"): #ROM is arcade, need to also delete the zip file in bin
        print("Arcade ROM")
        base = os.path.dirname(ROMfilePath)
        arcadezip = extractFileNameFromZFB(ROMfilePath)
        try:
            os.remove(os.path.join(base,"bin",arcadezip))
        except:
            logging.error(f"ERROR: tadpole_functions~deleteROM: failed to delete arcadezip ({ROMfilePath})")
            # We dont return False here because the main point is to delete the provided ROMfilePath file
    # Delete the zxx file
    try:
        os.remove(ROMfilePath)
    except:
        logging.error(f"ERROR: tadpole_functions~deleteROM: failed to delete provided ROM file ({ROMfilePath})") 
        return False   
    return True          
          

def extractImgFromROM(romFilePath, outfilePath):
    with open(romFilePath, "rb") as rom_file:

        rom_content = bytearray(rom_file.read())
        img = QImage(rom_content[0:((144*208)*2)], 144, 208, QImage.Format_RGB16)
        img.save(outfilePath)

        
def GBABIOSFix(drive: str):
    if drive == "???":
        raise Exception_InvalidPath
    gba_bios_path = os.path.join(drive, "bios", "gba_bios.bin")
    if not os.path.exists(gba_bios_path):
        print(f"! Couldn't find game list file {gba_bios_path}")
        print("  Check the provided path points to an SF2000 SD card!")
        raise Exception_InvalidPath
    try:
        gba_folder_path = os.path.join(drive, "GBA", "mnt", "sda1", "bios")
        roms_folder_path = os.path.join(drive, "ROMS", "mnt", "sda1", "bios")
        os.makedirs(gba_folder_path, exist_ok=True)
        os.makedirs(roms_folder_path, exist_ok=True)
        shutil.copyfile(gba_bios_path, os.path.join(gba_folder_path, "gba_bios.bin"))
        shutil.copyfile(gba_bios_path, os.path.join(roms_folder_path, "gba_bios.bin"))
    except (OSError, IOError) as error:
        print("! Failed to copy GBA BIOS.")
        print(error)
        raise Exception_InvalidPath
    
def stripShortcutText(drive: str):
    if drive == "???" or drive == "":
        raise Exception_InvalidPath
    gakne_path = os.path.join(drive, "Resources", "gakne.ctp")
    try:
        gakne = open(gakne_path, "rb")
        data = bytearray(gakne.read())
        gakne.close()
        # Gakne is made up of 8 rows of 4 items for a total of 32 items.
        # Each image is 144 x 32. Total image size 576 x 256.
        # To only strip the shortcut text we want to leave the settings menu items. So we have to skip the first 18,432 bytes
        
        for i in range (18432, len(data)):
            data[i-1] = 0x00
        gakne = open(gakne_path, "wb")
        gakne.write(data)
        gakne.close()
        return True
    except (OSError, IOError) as e:
        print(f"! Failed striping shortcut labels. {e}")
        return False

_static_shortcut_FC = 0
_static_shortcut_SFC = 1
_static_shortcut_MD = 2
_static_shortcut_GB = 3
_static_shortcut_GBC = 4
_static_shortcut_GBA = 5
_static_shortcut_ARCADE = 6

def updateShortcutTextforConsole(drive: str, console: int, game1:str, game2:str, game3:str, game4:str):
    if drive == "???" or drive == "":
        raise Exception_InvalidPath
    if (console < 0 or console > _static_shortcut_ARCADE):
        raise Exception_InvalidConsole
    gakne_path = os.path.join(drive, "Resources", "gakne.ctp")
    try:
        # Gakne is made up of 8 rows of 4 items for a total of 32 items.
        # Each image is 144 x 32. Total image size 576 x 256.
        # To only strip the shortcut text we want to leave the settings menu items. So we have to skip the first 18,432 bytes
        # Console order: FC, SFC, MD, GB, GBC, GBA, ARCADE
        newText = [game1,game2,game3,game4]
        shortcutText = openBRGAasImage(gakne_path)
        replaceMask = Image.new("RGBA", (144, 32), (255, 255, 255, 255))
        fnt = ImageFont.truetype("arial.ttf", 24)
        for i in range(len(newText)):
            #Game Slot 1
            img_g = Image.new("RGBA", (144, 32), (0, 0, 0, 0)) #In the alpha channel 0 is fully transparent, 255 is fully opaque
            ImageDraw.Draw(img_g).text((72,16), newText[i], (255,255,255),font=fnt, anchor="mm")        
            shortcutText.paste(img_g, (144*i,(console+1)*32), replaceMask)

        shortcutText.save("C:\\Users\\OEM\\Documents\\test.png")
        # TODO XXXXXX
        writeImagetoBGRAfile(shortcutText, gakne_path)
        return True
    except (OSError, IOError) as e:
        print(f"! Failed updating shortcut labels. {e}")
        return False

def openBRGAasImage(inputFile):
    # Read the binary data
    with open(inputFile, 'rb') as file:
        data = file.read()
    # Unpack the BGRA8888 data
    pixels = struct.unpack('>' + ('L' * (len(data) // 4)), data)
    # Convert the BGRA8888 values to RGBA888 format
    rgba8888_pixels = [
            ((pixel & 0x0000FF00) >> 8, (pixel & 0x00FF0000) >> 16, (pixel & 0xFF000000) >> 24, (pixel & 0x000000FF))
            for pixel in pixels
    ]
    # Create an image from the pixels
    width = 576  # Specify the width of the image
    height = len(rgba8888_pixels) // width
    image = Image.new('RGBA', (width, height))
    image.putdata(rgba8888_pixels)
    return image

#TODO why is it all coming out yellow???
def writeImagetoBGRAfile(image:Image, outfile:str):
    try:
        dest_file = open(outfile, "wb")
        image_height = image.size[1]
        image_width = image.size[0]
        pixels = image.load()

        if not pixels:
            logging.error(f"tadpole_functions~writeImagetoBGRAfile: Failed to load image")
            return False
        data = []
        for h in range(image_height):
            for w in range(image_width):
                pixel = pixels[w, h]
                if not type(pixel) is tuple:
                    logging.error(f"! Unexpected pixel type at {w}x{h} from {outfile}")
                    return False
                r = pixel[0]
                g = pixel[1]
                b = pixel[2]
                a = pixel[3]
                bgra = (b) | (g << 16) | (r << 8) | (a << 24)
                data.append(struct.pack('>L', bgra))
        dest_file.write(b''.join(data))
        dest_file.close()
        return True
    except (OSError, IOError):
        logging.error(f"tadpole_functions~writeImagetoBGRAfile: Failed opening image file {outfile} for conversion")
        return False


def createSaveBackup(drive: str, zip_file_name):
    if drive == "???" or drive == "":
        raise Exception_InvalidPath 
    try:
        with zipfile.ZipFile(zip_file_name, 'w') as zip_object:
            for root, dirs, files in os.walk(drive):
                for file in files:
                    if check_is_save_file(file):
                        print(f"Found save: {file} in {root}")
                        try:
                            zip_object.write(os.path.join(root, file),
                                os.path.relpath(os.path.join(root, file),
                                                os.path.join(drive, '..')))
                        except Exception as e:
                            print(f"Bad zip file encountered: {os.path.join(root, file)}")
                            continue
        return True
    except Exception as e:
        logging.error({e})
        return False
                     
def check_is_save_file(filename):
    for ext in supported_save_ext:
        if filename.lower().endswith(ext):
            return True
    return False
        
def getHumanReadableFileSize(filesize):
    humanReadableFileSize = "ERROR"          
    if filesize > 1024*1024:  # More than 1 Megabyte
        humanReadableFileSize = f"{round(filesize/(1024*1024),2)} MB"
    elif filesize > 1024:  # More than 1 Kilobyte
        humanReadableFileSize = f"{round(filesize/1024,2)} KB"
    else:  # Less than 1 Kilobyte
        humanReadableFileSize = f"filesize Bytes"
    return humanReadableFileSize

#Credit to OpenAI "Give me sample code to convert little endian RGB565 binary images to PNG's in python"
def convertRGB565toPNG(inputFile):
        # Read the binary data
        with open(inputFile, 'rb') as file:
            data = file.read()
        # Unpack the RGB565 data
        pixels = struct.unpack('<' + ('H' * (len(data) // 2)), data)
        # Convert the RGB565 values to RGB888 format
        rgb888_pixels = [
            ((pixel & 0xF800) >> 8, (pixel & 0x07E0) >> 3, (pixel & 0x001F) << 3)
            for pixel in pixels
        ]
        # Create an image from the pixels
        width = 640  # Specify the width of the image
        height = len(rgb888_pixels) // width
        image = Image.new('RGB', (width, height))
        image.putdata(rgb888_pixels)
        # Save the image as PNG
        image.save('currentBackground.temp.png')
        return image

def convertPNGtoResourceRGB565(srcPNG, resourceFileName, drive):
    tempRawBackground = resourceFileName + ".raw"
    if frogtool.rgb565_convert(srcPNG, tempRawBackground, dest_size=(640, 480)):
        background = os.path.join(drive, 'Resources', resourceFileName)
        shutil.copy(tempRawBackground, background)
        os.remove(srcPNG)
        os.remove(tempRawBackground)
        print(resourceFileName + " updated.")
    else:
        print("Couldn't convert file for gameshortcut")

# Get's the type of device the SD card/directory is configured
def setDeviceType(drive):
    ROMListPath = os.path.join(drive, 'Resources', 'kjbyr.tax') # The PCE rom list for GB300 V2
    FoldernamePath = os.path.join(drive, 'Resources', 'foldername.ini')
    if os.path.exists(FoldernamePath):
        with open(FoldernamePath, 'r') as file:
            first_line = file.readline().strip()
            #print(first_line)
        if first_line == "GB300":
            return 'GB300V1'
        elif os.path.exists(ROMListPath):
            return 'GB300V2'
        else:
            return 'SF2000'
    else: 
        return 'Unknown'


#returns a string to the current resource file for each system
def getBackgroundResourceFileforConsole(drive, system):
    resourceFile = frogtool.systems[system][3]
    resourcePath = os.path.join(drive, 'Resources', resourceFile)
    return (resourcePath)

def copy_files(source, destination, progressBar):
    total_files = 0
    for root, dirs, files in os.walk(source):
        total_files += len(files)
    copied_files = 0
    for root, dirs, files in os.walk(source):
        for file in files:
            source_file = os.path.join(root, file)
            destination_file = os.path.join(destination, os.path.relpath(source_file, source))
            os.makedirs(os.path.dirname(destination_file), exist_ok=True)
            with open(source_file, 'rb') as src, open(destination_file, 'wb') as dst:
                while True:
                    data = src.read(8192)
                    if not data:
                        break

                    dst.write(data)
            copied_files += 1
            progressBar.setValue(int((copied_files / total_files) * 100))
            QApplication.processEvents()

def zip_file(file_path, output_path):
    file_name = os.path.basename(file_path)
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(file_path, arcname=file_name)

#Add a thumbnail to a single rom 
def addThumbnail(rom_path, drive, system, new_thumbnail, ovewrite):
        try:
            #Check if this rom type is supported
            romFullName = os.path.basename(rom_path)
            romName = os.path.splitext(romFullName)[0]
            romExtension = os.path.splitext(romFullName)[1][1:]
            zxx_extensions = {"zfc", "zsf", "zmd", "zgb", "zfb", "zpc"}
            if romExtension in zxx_extensions:
                sys_zxx_ext = romExtension
            else:
                if romExtension == "zfb" and system != "ARCADE":
                    sys_zxx_ext = "zfb"
                else:
                    sys_zxx_ext = frogtool.zxx_ext_romext(romExtension)
            #If its not supported, return
            if romExtension not in frogtool.supported_rom_ext:
                return False
            #If its zip pass to frogtool
            elif romExtension in frogtool.supported_zip_ext:
                if not changeZIPThumbnail(rom_path, new_thumbnail, romExtension):
                    return False
            #If its the supported system .z** pass to frogtool
            elif romExtension == sys_zxx_ext:
                if ovewrite == True:
                    if not changeZXXThumbnail(rom_path, new_thumbnail):
                        return False
            #Finally that means its supported but not zip, let's zip it up
            else:
                new_zipped_rom_path = os.path.join(drive, system, romName + '.zip')
                zip_file(rom_path, new_zipped_rom_path)
                if not changeZIPThumbnail(new_zipped_rom_path, new_thumbnail, romExtension): 
                    return False
                #Frogtool takes care of the zip, we need to remove the base ROM to not confuse the user
                if os.path.exists(rom_path):
                    os.remove(rom_path)
            return True
        except Exception_InvalidPath:
            #QMessageBox.about(window, "Change ROM Cover", "An error occurred.")
            return False

def read_top_games(drive, system):
    topGamesFile = os.path.join(drive, "topgames.txt")
    # Copy the default file
    if not os.path.exists(topGamesFile):
        shutil.copy("topgames.txt", topGamesFile)
    try:
        current_system_name = None
        games = []
        with open(topGamesFile, 'r') as file:
            for line in file:
                line = line.strip()
                if line.endswith(":"):  # Line ending with colon indicates a system name
                    if current_system_name == system:  # Check if the previous system matches the provided system
                        return games
                    current_system_name = line[:-1]  # Remove the colon to get the system name
                    games = []  # Clear the games list
                elif line:  # Non-empty line indicates a game name
                    games.append(line)
            # Check the last system's games if it matches the provided system
            if current_system_name == system:
                return games
        return []  # Return an empty list if the system was not found
    except FileNotFoundError:
        print(f"Error: File" + topGamesFile + "not found. Top Game Sorting will not be enabled.")
        return []
    except Exception as e:
        print(f"Error while reading the" + topGamesFile + "file: {e}")
        return []

#Thanks to Dteyn for putting the python together from here: https://github.com/Dteyn/SF2000_Battery_Level_Patcher/blob/master/main.py
#Thanks to OpenAI for writing the class and converting logging to prints
class BatteryPatcher:
    def __init__(self, firmware_file, fw_version):

        self.fw_version = fw_version
        # Filename of original firmware file to open
        self.firmware_file = firmware_file
        # Filename of patched firmware file to save
        self.patched_file = firmware_file

        # Define voltage values for each battery level (user can modify these)
        self.VOLTAGE_LEVELS = {
            "5 bars": 4.0,  # Full charge
            "4 bars": 3.88,
            "3 bars": 3.80,
            "2 bars": 3.72,
            "1 bar (red)": 3.66  # Near empty
        }

        # Offset addresses for each battery level - firmware 08.03
        self.ADDRESSES_V1_6 = [
            0x3564ec,  # 5 bars (full charge)
            0x3564f4,  # 4 bars
            0x35658c,  # 3 bars
            0x356594,  # 2 bars (yellow)
            0x3565b0  # 1 bar (red)
        ]

        # Offset addresses for each battery level - firmware v1.71
        self.ADDRESSES_V1_71 = [
            0x356638,  # 5 bars (full charge)
            0x356640,  # 4 bars
            0x3566d8,  # 3 bars
            0x3566e0,  # 2 bars (yellow)
            0x3566fc  # 1 bar (red)
        ]

        # Stock values for sanity check
        self.STOCK_VALUES = [
            0xBF,
            0xB7,
            0xAF,
            0xA9,
            0xA1
        ]

        # New values for sanity check
        self.BATTERY_FIX_VALUES = [
             0xC8,
             0xC2,
             0xBE,
             0xBA,
             0xB7
        ]


    def voltage_to_value(self, voltage):
        """Convert voltage to the appropriate firmware value using the 50x multiplier."""
        return int(voltage * 50)

    def calculate_crc32(self, data):
        """
        Calculate the CRC32 value for the given data. 
        Credit to @bnister for the C version of this code (translated to Python by GPT-4)
        """
        tab_crc32 = [(i << 24) & 0xFFFFFFFF for i in range(256)]
        for i in range(256):
            c = tab_crc32[i]
            for _ in range(8):
                c = (c << 1) ^ 0x4c11db7 if (c & (1 << 31)) else c << 1
                c &= 0xFFFFFFFF
            tab_crc32[i] = c

        c = ~0 & 0xFFFFFFFF
        for i in range(512, len(data)):
            c = (c << 8) ^ tab_crc32[((c >> 24) ^ data[i]) & 0xFF]
            c &= 0xFFFFFFFF
        return c

    def check_patch_applied(self):
        with open(self.firmware_file, 'rb') as f:
            bisrv_data = bytearray(f.read())
            logging.info("File '%s' opened successfully." % self.firmware_file)
        # TODO add error checking
        ADDRESSES = self.get_ADRESSES()
        if not ADDRESSES:
            return False
        for addr, expected_value in zip(ADDRESSES, self.BATTERY_FIX_VALUES):
            if bisrv_data[addr] != expected_value:
                logging.info("The firmware does not match the expected battery patched versions at offset %X." %addr)
                return False
        logging.info("The firmware matched the expected battery patched versions at offset %X." %addr)
        return True


    def get_ADRESSES(self):
        if (self.fw_version == version_displayString_1_6):
            return self.ADDRESSES_V1_6
        elif (self.fw_version == version_displayString_1_71):
            return self.ADDRESSES_V1_71  
        else:
            logging.warn("BatteryPatcher~check_latest_firmware: Firmware version mismatch")
            return False 

    def check_latest_firmware(self):
        #TODO: Replace this with a proper check
        """
        Check if the firmware matches the patched values
        """
        with open(self.firmware_file, 'rb') as f:
            bisrv_data = bytearray(f.read())
            logging.info("File '%s' opened successfully." % self.firmware_file)
        ADDRESSES = self.get_ADRESSES()
        if not ADDRESSES:
            return False
        for addr, expected_value in zip(ADDRESSES, self.STOCK_VALUES):
            if bisrv_data[addr] != expected_value:
                print("The firmware does not match the expected '08.03' version at offset %X. "
                              "Please check the offsets." %addr)
                return False
        logging.info("The firmware matched the expected firmware versions at offset %X." %addr)
        return True

    def patch_firmware(self, progressIndicator):
        """
        Patch the firmware file with new battery values and update its CRC32.
        """
        try:
            progressIndicator.setValue(1)
            QApplication.processEvents()
            with open(self.firmware_file, 'rb') as f:
                bisrv_data = bytearray(f.read())
            print("File '%s' opened successfully." % self.firmware_file)

            # Perform sanity check
            if not self.check_latest_firmware():
                return
            ADDRESSES = self.get_ADRESSES()
            if not ADDRESSES:
                return False
            # Convert voltage levels to firmware values
            self.BATTERY_VALUES = {addr: self.voltage_to_value(self.VOLTAGE_LEVELS[bar])
                               for addr, bar in zip(ADDRESSES, self.VOLTAGE_LEVELS)}
            # Patch the battery values
            for addr, value in self.BATTERY_VALUES.items():
                bisrv_data[addr] = value
            print("File patched with new battery values.")
            progressIndicator.setValue(10)
            QApplication.processEvents()

            # Calculate new CRC32
            print("Calculating new CRC32...")
            crc = self.calculate_crc32(bisrv_data)
            print("New CRC32 value: %X" % crc)
            progressIndicator.setValue(80)
            QApplication.processEvents()
            # Update CRC32 in the bisrv_data
            bisrv_data[0x18c] = crc & 0xFF
            bisrv_data[0x18d] = (crc >> 8) & 0xFF
            bisrv_data[0x18e] = (crc >> 16) & 0xFF
            bisrv_data[0x18f] = (crc >> 24) & 0xFF

            # Write the patched data back to the file
            with open(self.patched_file, 'wb') as f:
                f.write(bisrv_data)
            print("Patched data written back to '%s'." % self.patched_file)
            return True
        except FileNotFoundError:
            print("File '%s' not found." % self.firmware_file)
            return False
        except Exception as e:
            print("An error occurred: %s" % str(e))
            return False

    
