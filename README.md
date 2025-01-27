## MADPOLE-MOD
Madpole-mod is a device management tool for the Datafrog SF2000 / GB300 V2. Madpole-mod is a fork of [Madpole](https://github.com/fjdogar/madpole) which was developed by [faanJD](https://github.com/fjdogar) and was also a fork of [Tadpole](https://github.com/EricGoldsteinNz/tadpole) which was developed by [EricGoldstein](https://github.com/EricGoldsteinNz) and was also a fork of [Frogtool](https://github.com/tzlion/frogtool) which was developed by [taizou](https://github.com/tzlion). Madpole-mod wouldn't be possible without any of these people or their amazing projects. Madpole-mod aims to do everything Tadpole and Madpole does but targets SF2000 Multicore, Sf2000 13 menu Multicore, and GB300 V2 Multicore.  
Madpole-mod currently provides the following main features:

* Rebuilding of the console specific rom lists (for both stock and multicore)
* The ability to change the name of console menu entry folders
* Support for the 13 Menus bisrv edit on SF2000 only
* Support for GB300 V2
* Changing the firmware to official releases or multicore
* Merging ROM zips and jpg files with the same name to the relevant Zxx fileformat for each console (stock feature)
* Creating zfb files to load ROMs using Multicore cores
* Downloading cover art for ROMs (including zfb files)
* Editing the Multicore .opt files
* A WIP section editor
* Changing the four in menu game shortcuts for each console
* Changing the boot logo (for Multicore bisrvs also)
* Changing the background music
* Changing the theme
* Applying the bootloader fix
* Applying the battery fix
* Automating the GBA bios fix

Madpole-mod allows you to rebuild the preset game lists on the Datafrog SF2000 / GB300 V2 emulator handhelds, so you can add (or remove) ROMs in the proper system categories instead of only being able to add them in the user folder.  

## Improvements 

## DISCLAIMER
This program is not developed or authorised by any company or individual connected with the SF2000 handheld and is based on public reverse engineering of SF2000 file formats.  
You should make your own backups of the Resources and bios folders and ideally your whole SD card so you can restore the original state of your device if anything goes wrong.  

## IMPORTANT NOTES
+ User directory is set to the path of Madpole.exe by default if you havent set it yet and if theres no SD card.  
+ The madpole.ini (previously tadpole.ini) is now saved in the same folder as the Madpole.exe itself.  
+ It creates an extra file called mshortcuts.ini on the root of SD Card/ User Directory. Do not delete this file from the root of your SD CARD or User Directory.  

## Download/installation
Download the latest release from https://github.com/Trademarked69/madpole-mod/releases/latest  
Download the latest .exe file if you are on windows, or the python source folder if you are on Linux/Mac.  

You should be able to run the source using:  
python3 madpole.py  
Note that you may need to install the required libraries if you do not have them already using:  
python -m pip install -r requirements.txt  

## Basic usage steps

1. Insert the SF2000 or GB300 V2 SD card in a card reader connected to your computer  
2. Drag and drop your desired ROMs into the respective system folders (ARCADE, FC, GB, GBA, GBC, MD, SFC, whatever else you might've renamed them to)   
3. Run Madpole (double-click madpole.exe or run the python from source)  
3. All the standard games lists should be rebuilt as soon as Madpole opens.  
4. Other changes such as updating the OS, changing the boot logo, background music, or theme can be made from the menu.  

## Building a new SD Card

1. Start with Madpole open and the SD card connected to the computer.  
2. Open the OS menu, and select "Build Fresh SD Card".  
3. Follow the instructions on screen to build a new SD  

## Stock Supported files

By default without Multicore the SF2000 OS will load the following file extensions:  

| Type        | Extensions                                                      |
|-------------|-----------------------------------------------------------------|
| Zipped      | bkp, zip                                                        |
| Thumbnailed | zfc, zsf, zmd, zgb, zfb (see "Thumbnails & .zxx files" section) |
| SFC/SNES    | smc, fig, sfc, gd3, gd7, dx2, bsx, swc                          |
| FC/NES      | nes, nfc, fds, unf                                              |
| GB/GBC      | gbc, gb, sgb                                                    |
| GBA         | gba, agb, gbz                                                   |
| MD/GEN/SMS  | bin, md, smd, gen, sms                                          |

It doesn't generally care if you put the wrong system's roms in the wrong folder, it will load them in the correct emulator according to their file extension.  

Master System games are "secretly" supported by the stock Mega Drive emulator, it recognises the .sms extension but will actually run these games with any of the Mega Drive file extensions too. Game Gear games don't work properly.  

Both .bkp and .zip extensions seem to function as normal ZIP files, I think .bkp was used for obfuscated zip files on another system. Any supported ROM inside a ZIP file will be treated the same as an uncompressed ROM, and loaded in the appropriate emulator.  
(Arcade game ZIP files are weird, see the "Arcade games" section below.)  

In the launch firmware version, filenames may contain Chinese and Japanese characters and these will be correctly displayed in the list even when English is selected. In the 2023-04-20 update, supported characters depend on the selected language, as it uses different fonts per language.  

## Arcade games

Arcade ROMs work differently from any others, since they consist of multiple ROM dumps inside a ZIP file, and emulators typically recognise them by their filename and the contained files' checksums. This means they usually can't be renamed.  

For the SF2000 OS's purposes, in order to display the full names of the games in the menu instead of the shortened emulator-standard filenames (eg. "Metal Slug X -Super Vehicle-001" instead of mslugx) their approach is to use .zfb files named with the full name, these files contain a thumbnail image plus the actual filename, which refers in turn to the actual rom zip file which is found in the ARCADE/bin subfolder. 
(See the "Thumbnails & .zxx files" section for more info on this format)  

The OS will still recognise arcade ROM ZIP files placed directly in the ROM folders with their emulator-standard filenames, but I don't know which ROM set it expects; even the manufacturers don't seem to know, they preloaded three Sonic Wings ROMs in the user "ROMS" folder and only one of them loads! Internal strings suggest the emulator is some version of Final Burn Alpha if that helps.   

Many preloaded arcade games also have ".skp" files in the ARCADE/skp folder, these appear to be savestates which are automatically loaded when booting a game, to skip its boot sequence and bring you straight to the title screen with a coin already inserted. However it seems these only function correctly when the ROM is loaded using a .zfb file; if you place an arcade ROM ZIP directly in the ARCADE folder and index it using this tool, and there is a corresponding .skp file in the skp folder, the game will crash after loading the ROM. Personally I prefer to delete these files anyway as I'd rather see the original attract mode instead of jumping straight to the title screen.  

## Thumbnails & .zxx files

The following file formats: zfc, zsf, zmd, zgb, zfb are a custom format created for this and similar devices, containing both a thumbnail image used in the menu and a either a zipped ROM or a pointer to one. Collectively I will refer to them as .zxx files for now.  

They correspond to the following systems:  
* .zfc = FC  
* .zsf = SFC  
* .zmd = MD  
* .zgb = GB, GBC, GBA  
* .zfb = ARCADE  

Madpole-mod supports generating these files, so you can use your own custom thumbnails (including ones for multicore). (Except arcade games.)  

Thumbnails in this system are 144 x 208 pixels, your image will be resized to those dimensions if necessary.  

## Credits  

Madpole-mod is a fork of [Madpole](https://github.com/fjdogar/madpole) which was developed by [faanJD](https://github.com/fjdogar) and was also a fork of [Tadpole](https://github.com/EricGoldsteinNz/tadpole) which was developed by [EricGoldstein](https://github.com/EricGoldsteinNz) and was also a fork of [Frogtool](https://github.com/tzlion/frogtool) which was developed by [taizou](https://github.com/tzlion).  

RGB565 conversion code based on PNG-to-RGB565 (c) 2019 jpfwong  
https://github.com/jimmywong2003/PNG-to-RGB565  

Frog icon from public domain photo by LiquidGhoul  
https://commons.wikimedia.org/wiki/File:Australia_green_tree_frog_(Litoria_caerulea)_crop.jpg  

Special thanks to the firmware devs  
