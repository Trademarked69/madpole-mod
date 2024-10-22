<h1>MADPOLE</h1>
Madpole is a fork of Tadpole by faanJD. Tadpole was developed by EricGoldstein. Madpole wouldnt be possible without his awesome work.
Madpole does everything Tadpole does , but has some fixes and additions and <a href="https://github.com/fjdogar/multicore_rom_helper">MRH </a> integrated into it for doing multicore things which are listed below. You will find the original Tadpole readme at the end of the following info.

<h2>FIXES</h2>
<h3>1. Shortcuts For Multocore ZFBs</h3>
 + Shorcuts can be set properly<br>
 + Shortcuts can be changed properly<br>
 + Proper name shows in Change Shortcut Icons Dialog<br>

<h3>2. Thumbnails for Multicore ZFBs</h3>
 + Thumbnails now show in roms table<br>
 + Thumbnail can be added/changed from rom table<br>

<h3>3. Deleting Roms</h3>
 + Delete button from Rom table for multicore ZFbs now works<br>
 + Delete Selected now works for multicore ZFBs<br>

<h2>ADDITIONS</h2>
 <h3>1. Add Multicore Roms (MADPOLE Menu)</h3>
 Select roms and thumbs, madpole will create and put zfbs to the Current Section and also copy roms to the multicore core directory<br>
 
 <h3>2. Create ZFBs for existing.. (MADPOLE Menu)</h3>
 Create ZFBs for existing (on SD CARD or User Directoty) multicore roms. Select the existing multicore core (rom) folder and create zfbs<br>

 <h3>3. Create Stubs (MADPOLE Menu)</h3>
 Create for a single or all multicore cores (improved stub creation for all roms)<br>

 <h3>4. CORE Changer (MADPOLE Menu or "Change Selected Core" Button on Top left)</h3>
 + Change core of selected roms (ie from nes to nesq) and rom files are also moved to the new core folder. You can copy instead of moving by checking "Copy roms to new core folder". Sytem Check is enforced by default (it will not let you  change core from nesq to snes because they are different systems<br>

 <h3>6. OPT Editor</h3>
 You can now edit multicore or other common core's opt files using selection based interface ie select an opt, select option and then choose a value from all the possible values. You can also reset an OPT to default values. <br>
 
 <h3>7. Status Bar Info</h3>
  + Fixed deselection bug in rom table on console change. <br>
  + Fixed Rom table Header Click. It now selects all games in the table and show the total number in status bar. <br>
  + Status bar will now show the core of selected rom from rom table if its a multicore zfb. <br>
  + Status bar will also show no. of selected roms<br>

 <h3>8. SECTION Editor</h3>
  + You can edit how many sections you want to be displayed on you sf2000 and which section to start on boot. Unfortunately the order of the sections cant be changed yet.<br>

 <h3>9. New Hashes</h3>
  + Now you can change boot logo for multicore bisrv.asd. Added hashes for multicore 0.10 official, Leonordo' save 3, pr 'n'eo build , Latest changes compiled by me build. It will now enable you to change Boot Logo and Apply battery Fix for these builds.<br>

<h2>IMPORTANT NOTES</h2>
+ User directory is set to the path of Madpole.exe by default if you havent set it yet and if theres no SD card.<br>
+ The madpole.ini (previously tadpole.ini) is now saved in the same folder as the Madpole.exe itself.<br>
+ It creates an extra file called mshortcuts.ini on the root of SD Card/ User Directory. Do not delete this file from the root of your SD CARD or User Directory.<br>


Tadpole
===============

by EricGoldstein  

Tadpole is a device management tool for the SF2000 / Datafrog. It currently provides the following main features:
* Rebuilding of the console specific rom lists
* Changing the firmware to official releases or multicore (including rebuilding multicore gamelists)
* Merging ROM zips and jpg files with the same name to the relevant Zxx fileformat for each console
* Downloading cover art for ROMs
* Changing the four in menu game shortcuts for each console
* Changing the boot logo
* Changing the background music
* Changing the Console logos
* Applying the bootloader fix
* Applying the battery fix
* Automating the GBA bios fix


Tadpole started as a project to provide an easy to use GUI for tzlion's frogtool. However it has since added additional features. 

Tadpole allows you to rebuild the preset game lists on the SF2000 / Datafrog emulator handheld, so you can add (or remove) ROMs
in the proper system categories instead of only being able to add them in the user folder.


DISCLAIMER
----------

This program is not developed or authorised by any company or individual connected with the SF2000 handheld and is based on public reverse engineering of SF2000 file formats.

You should make your own backups of the Resources and bios folders and ideally your
whole SD card so you can restore the original state of your device if anything goes wrong.


Download/installation
---------------------

Download the latest release from https://github.com/EricGoldsteinNz/tadpole/releases

Download the latest .exe file if you are on windows, or the python source folder if you are on Linux/Mac.

You should be able to run the source using:
python tadpole.py
Note that you may need to install the required libraries if you do not have them already using:
python -m pip install -r requirements.txt


Basic usage steps
-----------------

1. Insert the SF2000 SD card in a card reader connected to your computer
2. Drag and drop your desired ROMs into the respective system folders (ARCADE, FC, GB, GBA, GBC, MD, SFC) 
3. Run tadpole (double-click tadpole.exe or run the python from source)
3. All the standard games lists will be rebuilt as soon as tadpole opens.
4. Other changes such as updating the OS, changing the boot logo, background music, or theme can be made from the menu.



Building a new SD Card
-----------------

1. Start with Tadpole open and the SD card connected to the computer.
2. Open the OS menu, and select "Build Fresh SD Card".
3. Follow the instructions on screen to build a new SD

Other Details
===============
Supported files
---------------

The SF2000 OS will load the following file extensions:

| Type        | Extensions                                                      |
|-------------|-----------------------------------------------------------------|
| Zipped      | bkp, zip                                                        |
| Thumbnailed | zfc, zsf, zmd, zgb, zfb (see "Thumbnails & .zxx files" section) |
| SFC/SNES    | smc, fig, sfc, gd3, gd7, dx2, bsx, swc                          |
| FC/NES      | nes, nfc, fds, unf                                              |
| GB/GBC      | gbc, gb, sgb                                                    |
| GBA         | gba, agb, gbz                                                   |
| MD/GEN/SMS  | bin, md, smd, gen, sms                                          |

It doesn't generally care if you put the wrong system's roms in the wrong folder, it will load them in the correct
emulator according to their file extension.

Master System games are "secretly" supported by the Mega Drive emulator, it recognises the .sms extension but will
actually run these games with any of the Mega Drive file extensions too. Game Gear games don't work properly.

Both .bkp and .zip extensions seem to function as normal ZIP files, I think .bkp was used for obfuscated zip files on 
another system. Any supported ROM inside a ZIP file will be treated the same as an uncompressed ROM, and loaded in the
appropriate emulator.  
(Arcade game ZIP files are weird, see the "Arcade games" section below.)

In the launch firmware version, filenames may contain Chinese and Japanese characters and these will be correctly
displayed in the list even when English is selected. In the 2023-04-20 update, supported characters depend on the
selected language, as it uses different fonts per language.


Arcade games
------------

Arcade ROMs work differently from any others, since they consist of multiple ROM dumps inside a ZIP file, and emulators
typically recognise them by their filename and the contained files' checksums. This means they usually can't be renamed.

For the SF2000 OS's purposes, in order to display the full names of the games in the menu instead of the shortened
emulator-standard filenames (eg. "Metal Slug X -Super Vehicle-001" instead of mslugx) their approach is to use .zfb
files named with the full name, these files contain a thumbnail image plus the actual filename, which refers in turn to
the actual rom zip file which is found in the ARCADE/bin subfolder.  
(See the "Thumbnails & .zxx files" section for more info on this format)

The OS will still recognise arcade ROM ZIP files placed directly in the ROM folders with their emulator-standard
filenames, but I don't know which ROM set it expects; even the manufacturers don't seem to know, they preloaded three
Sonic Wings ROMs in the user "ROMS" folder and only one of them loads! Internal strings suggest the emulator is some
version of Final Burn Alpha if that helps.

Many preloaded arcade games also have ".skp" files in the ARCADE/skp folder, these appear to be savestates which are
automatically loaded when booting a game, to skip its boot sequence and bring you straight to the title screen with a
coin already inserted. However it seems these only function correctly when the ROM is loaded using a .zfb file; if you
place an arcade ROM ZIP directly in the ARCADE folder and index it using this tool, and there is a corresponding .skp
file in the skp folder, the game will crash after loading the ROM. Personally I prefer to delete these files anyway as
I'd rather see the original attract mode instead of jumping straight to the title screen.


Thumbnails & .zxx files
-----------------------

The following file formats: zfc, zsf, zmd, zgb, zfb are a custom format created for this and similar devices, containing
both a thumbnail image used in the menu and a either a zipped ROM or a pointer to one. Collectively I will refer to them
as .zxx files for now.

They correspond to the following systems:
* .zfc = FC
* .zsf = SFC
* .zmd = MD
* .zgb = GB, GBC, GBA
* .zfb = ARCADE

Tadpole supports generating these files, so you can use your own custom thumbnails! (Except arcade games for now.)

Just drop a zipped rom and an image (png, jpg, gif) with the same filename in the same folder, run frogtool and it will
automatically combine the two into an appropriate .zxx file. (The source image and zip file will be deleted.)  

Example: "Bubsy.zip" and "Bubsy.jpg" would be combined to "Bubsy.zsf" if placed in the "SFC" folder.

Thumbnails in this system are 144 x 208 pixels, your image will be resized to those dimensions if necessary.


Credits
-------
Frogtool was developed by taizou and Evan Clements

RGB565 conversion code based on PNG-to-RGB565 (c) 2019 jpfwong
https://github.com/jimmywong2003/PNG-to-RGB565

Frog icon from public domain photo by LiquidGhoul
https://commons.wikimedia.org/wiki/File:Australia_green_tree_frog_(Litoria_caerulea)_crop.jpg

Special thanks to the firmware devs
