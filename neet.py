"""neet is a Python Library for reading / writing configuration files using EET structure

By: Jeff Hoogland (JeffHoogland@Linux.com)
Started: 7/12/15

Returning data from extracted to .cfg form:

eet -e file.cfg config file.txt 1

"""

from efl import ecore

import os.path
import tempfile
import time
import ecfg

Struct = ecfg.parser.Struct
List = ecfg.parser.List
Value = ecfg.parser.Value

TMPDIR = tempfile.gettempdir()

class EETFile(object):
    def __init__(self):
        self.data = {}
        self.ecfgParse = None
        self.tmpFile = None
        self.cfgName = None
        self.eetFilePath = None
        
    def importFile(self, eetFile, decompArg="-d"):
        """This method decompiles a binary EET file using the eet system command"""
        self.eetFilePath = eetFile
        self.cfgName = eetFile.split("/")[-1]
        self.tmpFile = eetFile.split("/")[-1]
        
        nextInt = 0
        
        #ensure we aren't overwriting other CFGs that are open for writing
        while os.path.isfile("%s/%s%s.txt"%(TMPDIR, self.tmpFile, nextInt)):
            nextInt += 1
        
        self.tmpFile = "%s%s.txt"%(self.tmpFile, nextInt)
        
        #print eetFile
        #print "%s/%s"%(TMPDIR, self.tmpFile)
        cmd = ecore.Exe("eet %s %s config %s/%s"%(decompArg, eetFile, TMPDIR, self.tmpFile))

        #Wait while the file is extracted
        while not os.path.isfile("%s/%s"%(TMPDIR, self.tmpFile)):
            time.sleep(0.5)
        
        extractFile = "%s/%s"%(TMPDIR, self.tmpFile)
        
        #Prints the output of the file if we want to see that for debugging
        #print "%s/%s"%(TMPDIR, self.tmpFile)
        #for l in tmpFile.readlines():
        #    print l
        
        if decompArg == "-d":
            self.readExtract(extractFile)
        else:
            with open(extractFile) as f:
                self.ecfgParse = f.read()
        
    def readExtract(self, extractFile):
        """This method reads a decompiled EET file
            and turns it into a python object"""
        
        with open(extractFile) as f:
            extractText = f.read()
        
        self.ecfgParse = extractCfg = ecfg.ECfg(extractText)
    
    def readValue(self, valuePath=None):
        """example input:
            (("list", "modules"), ("item", "E_Config_Module",  "name" , "gadman"))
            (("list", "themes"), ("item", "E_Config_Theme",  "category" , "theme"), ("value", "file"))"""
        
        '''for li in self.ecfgParse.root.lists:
            if li.name == "themes":
                for i in li.items:
                    if i.name == "E_Config_Theme":
                        for v in i.values:
                            print v.name
                            print v.data'''
        
        if isinstance(self.ecfgParse, basestring):
            return self.ecfgParse
        else:
            currentLevel = self.ecfgParse.root
        
        for x in valuePath:
            if x[0] == "list":
                currentLevel = self._returnList(currentLevel, x[1])
            elif x[0] == "item":
                currentLevel = self._returnItem(currentLevel, x[1], x[2], x[3])
            elif x[0] == "value":
                currentLevel = self._returnValue(currentLevel, x[1])
            
            if not currentLevel:
                break
        
        return currentLevel
    
    def _returnList(self, currentObj, seekName):
        for li in currentObj.lists:
            if li.name == seekName:
                return li
        return False
    
    def _returnItem(self, currentObj, seekName, seekValName, seekVal):
        for it in currentObj.items:
            if it.name == seekName:
                for val in it.values:
                    if val.name == seekValName and val.data == seekVal:
                        return it
        return False
    
    def _returnValue(self, currentObj, seekName):
        for val in currentObj.values:
            if val.name == seekName:
                return val
        return False
    
    def saveData(self, saveAs=False):
        """Writes the data back into an eet file"""
        if saveAs:
            saveLocation = saveAs
            self.eetFilePath = saveAs
        else:
            saveLocation = self.eetFilePath

        # save the new config
        with open("%s/%s"%(TMPDIR, self.tmpFile), 'w') as f:
            f.write(self.ecfgParse.text())
        
        #if save location exists create a backup before writing over it
        if os.path.isfile(saveLocation):
            if os.path.isfile("%s.old"%saveLocation):
                os.remove("%s.old"%saveLocation)
                while os.path.isfile("%s.old"%saveLocation):
                    time.sleep(0.5)
            os.rename(saveLocation, "%s.old"%saveLocation)
            while os.path.isfile(saveLocation):
                time.sleep(0.5)
        
        #print "writing %s from %s/%s"%(saveLocation, TMPDIR, self.tmpFile)
        
        cmd = ecore.Exe("eet -e %s config %s/%s 1"%(saveLocation, TMPDIR, self.tmpFile))
        
        while not os.path.isfile(saveLocation):
            time.sleep(0.5)
        
        os.remove("%s/%s"%(TMPDIR, self.tmpFile))
