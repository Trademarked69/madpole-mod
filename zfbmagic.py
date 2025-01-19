import sys
import os
import glob
import requests
import struct

import frogtool
import shutil

from PIL import Image

from PyQt5.QtWidgets import QMessageBox

def find_matching_ext(ifold , core,file_name,isRom):
        
    fn = os.path.splitext(os.path.basename(file_name))[0]
    input_path = os.path.join(ifold, fn)

    #fname_noext = os.path.splitext(os.path.basename(input_folder))[0]
    file_ext = os.path.splitext(file_name)[1][1:]
    print("coming filename  is " + file_name)

    files = glob.glob(input_path + ".*" )
    print("path to file is " + input_path)
    print(files)

    for x in glob.glob(input_path + ".*" ):
        fname = os.path.splitext(os.path.basename(x))[0]
        fext = os.path.splitext(x)[1][1:]
        if fext != file_ext:
            if isRom and fext not in ["bmp" , "png" , "gif" , "jpeg" , "jpg" ,"txt" , "pdf" , "sav" , "srm"]:
                print("file except png found , extension is " + fext)
                return fext
            else:
                if fext in ["bmp" , "png" , "gif" , "jpeg" , "jpg"]:
                    print("file for img found , extension is " + fext)
                    return fext
    
    if not isRom:
        print("Image file not found")
    else:
        print("Rom File not found")
    return False


def zfb_from_null(core ,  file_name, output_folder  , apptxt , pretxt , addext , existadd):

    file_path = os.path.join(output_folder , file_name)
    fname_noext = os.path.splitext(os.path.basename(file_path))[0]
    file_ext = os.path.splitext(file_name)[1][1:]

    print(f"File path : {file_path} \n File Name : {file_name}")

    print (f"F no ext before : {fname_noext}")



    fname = fname_noext + "." + file_ext

    fname_noext = os.path.splitext(os.path.basename(file_name))[0]
    print (f"F no ext after : {fname_noext}")
    print(f"extenion is {file_ext}")
    placeholder_data = b'\x00' * 0xEA00 + b'\x00\x00\x00\x00' + f"{core};{fname}.gba".encode('utf-8') + b'\x00\x00'
    zfb_filename = os.path.join(output_folder , pretxt + fname_noext + apptxt + addext + existadd + '.zfb')
    with open(zfb_filename, 'wb') as zfb:
        zfb.write(placeholder_data)

    return True

def zfb_from_image(img , input_folder , core ,  file_name, output_folder , apptxt , pretxt , addext , existadd):
    thumb_size = (144, 208)
    img = img.resize(thumb_size)
    img = img.convert("RGB")

    file_path = os.path.join(output_folder , file_name)
    fname_noext = os.path.splitext(os.path.basename(file_path))[0]
    file_ext = os.path.splitext(file_name)[1][1:]

    raw_data = []

    # Convert image to RGB565
    for y in range(thumb_size[1]):
        for x in range(thumb_size[0]):
            r, g, b = img.getpixel((x, y))
            rgb = ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)
            raw_data.append(struct.pack('H', rgb))

    raw_data_bytes = b''.join(raw_data)


    zfb_filename = os.path.join(output_folder , pretxt + fname_noext + apptxt + addext + existadd + '.zfb')

    fname = fname_noext + "." + file_ext

    # Write the image data to the .zfb file
    try:
        with open(zfb_filename, 'wb') as zfb:
            # Fill with 00 bytes until offset 0xEA00
            zfb.write(raw_data_bytes)
            zfb.write(b'\x00\x00\x00\x00')  # Write four 00 bytes
            #zfb.write(f"{core};{os.path.splitext(file_name)[0]}.{extension}.gba".encode('utf-8'))  # Write the modified filename
            
            zfb.write(f"{core};{fname}.gba".encode('utf-8'))  # Write the modified filename
            print(f"Shortcut is : {core};{fname}.gba")
            zfb.write(b'\x00\x00')  # Write two 00 bytes
    except Exception as e:
        QMessageBox.information(self,"Error" , f"Error is {str(e)}")
    return True

# progress , progresstype , ifexist
def create_zfb_files(wind ,wdir ,sdir , pdir , core, apptxt , pretxt , doRef , doExt , files , doMove , ifexist, prg , prgT ,justzfb = False):

    

    if len(files) > 0:
        input_fold = os.path.dirname(files[0])
        input_folder = input_fold

    
    else:
        input_fold = wdir.strip()
        input_folder = os.path.join(input_fold, "ROMS", core)
    

    if justzfb:
        input_folder = input_fold
        output_folder = os.path.join(input_fold, "zfbs")
    else:
        #input_folder = os.path.join(input_fold , "ROMS\\" + core)
        output_folder = os.path.join(wdir.strip(), sdir)

    addext = ""
    
    if doExt:
        addext = "." + file_ext

    core = core.strip()
    pdir = pdir.strip()

    rom_ext = False;
    img_ext = False;

    try:
        
        if not os.path.isdir(os.path.join(output_folder)):
            
            if not justzfb:
                tdq = QMessageBox.question(wind,'Stock Directory', 'Selected Stock Folder doesnt Exist , Do you want to Create it?' , QMessageBox.Yes|QMessageBox.No)
                if tdq == QMessageBox.Yes:
                    os.makedirs(output_folder)
                    QMessageBox.information(wind,"Directory" , "Directory Created")
                else:
                    return
            else:
                os.makedirs(output_folder)

        # Check if folders are selected
        if not input_folder or not output_folder or not core: #or not extension:
            
            if not justzfb:
                QMessageBox.warning(wind,'Warning', 'Please fill in all the fields and select multicore rom dir and Stock dir.')
            else:
                QMessageBox.warning(wind,'Warning', 'Please fill in all fields , Select Input Folder and Enter the CORE name')

            return


        thumb_size = (144, 208)

        rom_list = [];

        if not files:
            files = os.listdir(input_folder)
        # Iterate over all files in the input folder

        total_files = len(files)
        print(f"Total files are {total_files}")
        proc_files = 0

        if not prgT:
            prg.progress.reset()
            prg.setText("Creating Rom Zfbs..")
            progress = 0
            prg.showProgress(progress, True)
        else:
            prg.show()
            prg.setValue(0)

        for file_name in files:
            
            if os.path.isdir(os.path.join(input_folder , file_name)):
                proc_files += 1
                continue
            file_path = os.path.join(input_folder, file_name)
            
            fname_noext = os.path.splitext(os.path.basename(file_path))[0]
            file_ext = os.path.splitext(file_name)[1][1:]
            
             

            # Skip if file name has been processed
            if fname_noext in rom_list:
                print("skipping as name already in rom list")
                proc_files += 1
                continue

            # if File is an Image , try to find a matching ROM extension
            if file_ext in ["png" , "bmp" , "jpg" , "jpeg" , "gif"]:
                rom_ext = find_matching_ext(input_folder , core , file_name , True)
                if rom_ext:
                    #file_name = os.path.join(input_folder, fname_noext + "." +rom_ext)
                    file_name = fname_noext + "." +rom_ext
                    img_ext = file_ext
                else:
                    rom_list.append(fname_noext)
                    proc_files += 1
                    continue

            elif file_ext in ["txt" , "pdf" , "sav" , "srm" , "exe"]:
                    rom_list.append(fname_noext)
                    proc_files += 1
                    continue
            else:

                img_ext = find_matching_ext(input_folder , core ,file_name , False)
                if img_ext:
                    file_path = os.path.join(input_folder, fname_noext + "." +img_ext)
                rom_ext = file_ext

            
            crn = fname_noext + "." + rom_ext
            cri = os.path.join(input_folder, crn)
            cro = os.path.join(wdir, "ROMS", core, crn)

            if len(files) > 0 and not justzfb and doMove:
                print("copying file from")
                print(cri)

                print("copying file to")
                print(cro)

                shutil.copyfile(cri , cro)

            efname =  pretxt + fname_noext + apptxt + addext + '.zfb'
            existadd = ""

            if os.path.exists(os.path.join(output_folder , efname)):
                    if ifexist == "Skip":
                        rom_list.append(fname_noext)
                        proc_files += 1
                        continue

                    elif ifexist == "Rename":
                        existadd = "_1"

            if img_ext:

                with Image.open(file_path) as img:

                    #zfb_from_image(img , input_folder , core ,  file_name , output_folder )
                    zfb_from_image(img , input_folder , core ,  file_name, output_folder , apptxt , pretxt , addext , existadd)
                    rom_list.append(fname_noext)
                    proc_files += 1

            else:

                tfp = os.path.join(os.getcwd(), "placeholders", pdir)
                print("the placeholder dir n file is " + tfp)

                try:

                    with Image.open(tfp) as img:

                        print("using the placeholder " + pdir)
                    
                        zfb_from_image(img , input_folder , core ,  file_name, output_folder  , apptxt , pretxt , addext , existadd )
                        print("png created with placeholder")
                        rom_list.append(fname_noext)
                        proc_files += 1

                except:

                    zfb_from_null(core ,  file_name, output_folder  , apptxt , pretxt , addext , existadd)
                    rom_list.append(fname_noext)
                    proc_files += 1

            rom_ext = False
            img_ext = False

            if not prgT:

                progress = (int(proc_files/total_files * 100))
                prg.showProgress(progress, True)
                prg.show()
            else:
                prg.setValue(int(proc_files/total_files * 100))
            

                
        QMessageBox.information(wind,'Success', 'ZFB files created successfully.')
        
        if doRef and not justzfb:
            rebuildAll(wdir)
            QMessageBox.information(wind,'Roms Refresh', 'All Rom lists have been refreshed.')
    
    
    except Exception as e:
        QMessageBox.critical(wind,'Error', f'An error occurred while creating the ZFB files: {str(e)}')
    

    if not prgT:
        prg.close()
    else:
        prg.hide()     

def rebuildAll(wdir):
    #frogtool.run(wdir, "ALL", "-sc")
    #frogtool.process_sys(wdir, "ALL", False)
    for console in frogtool.systems.keys():
        result = frogtool.process_sys(wdir, console, False)
    return
