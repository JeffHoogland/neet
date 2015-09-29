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
        
    def importFile(self, eetFile):
        """This method decompiles a binary EET file using the eet system command"""
        self.cfgName = eetFile.split("/")[-1]
        
        nextInt = 0
        
        #ensure we aren't overwriting other CFGs that are open for writing
        while os.path.isfile("%s/%s%s.txt"%(TMPDIR, self.cfgName, nextInt)):
            nextInt += 1
        
        self.cfgName = "%s%s.txt"%(self.cfgName, nextInt)
        
        #print eetFile
        #print "%s/%s"%(TMPDIR, self.cfgName)
        cmd = ecore.Exe("eet -d %s config %s/%s"%(eetFile, TMPDIR, self.cfgName))

        #Wait while the file is extracted
        while not os.path.isfile("%s/%s"%(TMPDIR, self.cfgName)):
            time.sleep(0.5)
        
        extractFile = "%s/%s"%(TMPDIR, self.cfgName)
        
        #Prints the output of the file if we want to see that for debugging
        #print "%s/%s"%(TMPDIR, self.cfgName)
        #for l in tmpFile.readlines():
        #    print l
        
        self.readExtract(extractFile)
        
    def readExtract(self, extractFile):
        """This method reads a decompiled EET file
            and turns it into a python dictonary"""
        
        with open(extractFile) as f:
            extractText = f.read()
        
        extractCfg = ecfg.ECfg(extractText)
        
        if type(extractCfg.root) == Struct:
            self.data = self._structToDict(extractCfg.root)
        
        print self.data
        
    def _structToDict(self, ourStruct):
        """Internal method used for converting EET structures to python dict"""
        tempDict = {}
        
        for li in ourStruct.lists:
            tempDict[li.name] = self._listToList(li)
        
        for val in ourStruct.values:
            tempDict[val.name] = self._valueToValue(val)
        
        return tempDict
    
    def _listToList(self, ourList):
        """Internal method used for converting EET list to python list"""
        tempList = []
        
        for i in ourList.items:
            tmpData = None
            if type(i) == Struct:
                tmpData = self._structToDict(i)
            elif type(i) == List:
                tmpData = self._listToList(i)
            elif type(i) == Value:
                tmpData = self._valueToValue(i)
            else:
                print "Found type %s. Not sure why."%type(i)
            
            tempList.append(tmpData)
        
        return tempList
        
    def _valueToValue(self, ourVal):
        """Internal method used for converting EET value to python value"""
        if ourVal.type in ["uint", "int"]:
            return int(ourVal.data)
        elif ourVal.type in ["float", "double"]:
            return float(ourVal.data)
        else:
            return ourVal.data
