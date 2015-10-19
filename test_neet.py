
import neet
import sys

#print sys.argv
myEetFile = neet.EETFile()
myEetFile.importFile(sys.argv[1])
#myEetFile.readExtract(sys.argv[1])

#myVal = myEetFile.readValue((("list", "modules"), ("item", "E_Config_Module",  "name" , "gadman")))
myVal = myEetFile.readValue((("list", "themes"), ("item", "E_Config_Theme",  "category" , "theme"), ("value", "file")))

print myVal

myVal.data = "Derppy.edj"

myEetFile.saveData()

