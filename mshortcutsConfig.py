import os
import string
import configparser




def getShortcuts():
    config = configparser.ConfigParser()

    mshortFolder = os.getcwd()
    mshortConfigFile = os.path.join(mshortFolder, 'mshortcuts.ini')
    print(mshortConfigFile)
    if not os.path.exists(mshortConfigFile):
        #Config file not found, create a new one            
        with open(mshortConfigFile, 'w') as newConfigFile:
            config.write(newConfigFile)
      
    # Double check that the config file now exists
    if not os.path.exists(mshortConfigFile):
        #TODO replace this with a proper exception
        raise Exception

    
      
    #open the config  
    config.read(mshortConfigFile)
    data = config.items("arcade")
    print(data)
    print(list(zip(*data) )[1])

    data = config.items("nes")
    print(data)
    print(list(zip(*data) )[1])

    config['arcade']["1"] = "Adventure Island"
    with open(mshortConfigFile, 'w') as newConfigFile:
            config.write(newConfigFile)

getShortcuts()