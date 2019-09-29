#@title Make folder to store images { run: "auto", form-width: "20%" }
import os

#define data version
dataVersion = 'data-1.0'

dirName = '/content/drive/My Drive/Projects/BKSeeing/' + dataVersion + '/data/'

if not os.path.exists(dirName):
  os.mkdir(dirName)
  print("Directory " , dirName ,  " Created ")

for i in range (21, 40):
  dir = "%s/jpg%d"%(dirName, i)
  if not os.path.exists(dir):
      os.mkdir(dir)
      print("Directory " , dir ,  " Created ")
  else:    
      print("Directory " , dir,  " already exists")
  dir = "%s/xml%d"%(dirName, i)
  if not os.path.exists(dir):
      os.mkdir(dir)
      print("Directory " , dir ,  " Created ")
  else:    
      print("Directory " , dir ,  " already exists")
