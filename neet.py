"""neet is a Python Library for reading / writing configuration files using EET structure

By: Jeff Hoogland (JeffHoogland@Linux.com)
Started: 7/12/15

"""

from efl import ecore

import os.path
import tempfile
import time

TMPDIR = tempfile.gettempdir()

class EETFile(object):
    def __init__(self, eetFile):
        self.data = {}
        self.cfgName = eetFile.split("/")[-1]
        
        #ensure we aren't overwriting other CFGs that are open for writing
        while os.path.isfile("%s/%s"%(TMPDIR,self.cfgName)):
            self.cfgName = "%sz"%self.cfgName
        
        self.cfgName = "%s.txt"%self.cfgName
        
        self.importFile(eetFile)
        
    def importFile(self, eetFile):
        #print eetFile
        #print "%s/%s"%(TMPDIR, self.cfgName)
        cmd = ecore.Exe("eet -d %s config %s/%s"%(eetFile, TMPDIR, self.cfgName))

        #Wait while the file is extracted
        while not os.path.isfile("%s/%s"%(TMPDIR,self.cfgName)):
            time.sleep(0.5)
        
        tmpFile = open("%s/%s"%(TMPDIR, self.cfgName), "r")
        print "%s/%s"%(TMPDIR, self.cfgName)
        for l in tmpFile.readlines():
            print l
