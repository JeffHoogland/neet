
import neet
import sys
import os

'''#print sys.argv
myEetFile = neet.EETFile()
myEetFile.importFile(sys.argv[1])
#myEetFile.readExtract(sys.argv[1])

myVal = myEetFile.readValue([("value", "theme")])
#myVal = myEetFile.readValue((("list", "modules"), ("item", "E_Config_Module",  "name" , "gadman")))
#myVal = myEetFile.readValue((("list", "themes"), ("item", "E_Config_Theme",  "category" , "theme"), ("value", "file")))

print myVal
print myVal.data

myVal.data = "Derppy.edj"

myEetFile.saveData()'''

eProfileFile = neet.EETFile()
eProfileFile.importFile("%s/.e/e/config/profile.cfg"%os.path.expanduser("~"), "-x")
eProfile = eProfileFile.readValue()

print eProfile

