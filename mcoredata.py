neslist = ["nes" , "nesq" , "nest"]
sneslist = ["snes" , "snes02"]
gbalist = ["gba" , "gbav" , "mgba"]
gblist = ["gb" , "gbgb" , "gbb"]
commlist = ["c64f" , "c64fc"]
segalist = ["sega" , "gpgx"]



cores = ["a26", "a5200" , "a78" , "a800" , "amstrad", "arduboy", "c64" , "c64f" , 
         "c64fc" , "c64sc" , "amstradb" , "cavestory" , "cdg" , "chip8" , "col" ,
         "fake08" , "fcf" , "flashback " , "gb" , "gba" , "gbb" ,"gbav" , "gbgb" , "gg" ,
         "gme" , "gong" , "gpgx" , "gw" , "int" , "jnb" , "lnx" , "lnxb" , "lowres-nx " ,
         "m2k" , "mgba", "msx" , "nes" , "nesq" , "nest" , "ngpc" , "o2em" , "outrun",
         "pc8800" , "pce" , "pcesgx" , "pcfx" , "pokem" , "prboom" , "quake" , "retro8" ,
         "sega" , "snes" , "snes02" , "spec" , "testadv" , "testwav" , "thom" , "vapor",
         "vb" , "vec" , "vic20" , "wolf3d" , "wsv" , "wswan" , "xmil" , "xrick"
        ]



def getZfbData(fpath):
    b = False
    with open(fpath , 'rb') as f:
        f.seek(59908)
        b = f.read(255);
        try:
            b = b.decode('UTF-8')
            b = b.strip('\x00')
        except:
            return False;

    if b:

        if not b.lower().endswith("gba"):
            return False
        d = b.split(";")
        if not len(d) == 2:
            return False

        d.append(d[1].strip().lower().endswith("gba"))
        #print(f"endswith result is {d[2]}")
        return d

    return False

def getZfbCore(fpath):
    b =  getZfbData(fpath)

    if b:
        if not b[1].strip().lower().endswith("gba"):
            return False
        return b[0]

    return False

def getZfbFile(fpath):
    b =  getZfbData(fpath)
    if b:
        return b[1][0:-4]

    return False

def isZfbMulticore(fpath):
    b = getZfbFile(fpath)
    b = b.lower()
    if b.endswith("gba"):
        return True

    return False

def buildCoresCombo(wdir , cbox):
    return True
def buildPlaceholdersCombo(wdir , cbox):
    return True

def create_zfb_file(wdir):
    return True

def create_zfb_files(wdir):
    return True