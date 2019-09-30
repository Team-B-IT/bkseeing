#@title Count number of boxes { form-width: "20%" }
import os
import pandas as pd

#define data version
dataVersion = 'data-1.0'
dirName = '/content/drive/My Drive/Projects/BKSeeing/' + dataVersion

dfImg = pd.read_csv(
    "/content/drive/My Drive/Projects/BKSeeing/Tool/train-images-boxable-with-rotation.csv")
dfImg.fillna(-99999, inplace=True)
dfImg = dfImg.sort_values(by=['ImageID']).reset_index(drop=True)
dfImg = dfImg.reset_index(drop=True)
numImg = len(dfImg)
print('Image URL imported!')

dfClass = pd.read_csv(dirName + "/class-des-bkseeing.csv")
numClass = len(dfClass)
print('Classes imported!')

dfBox = pd.read_csv(
    "/content/drive/My Drive/Projects/BKSeeing/Tool/train-annotations-bbox.csv",
    nrows=3000000)
print('Boxes imported!')
numBox = len(dfBox)

dfCount = pd.read_csv(dirName + "/class-count-bkseeing.csv")
dfTmp = pd.read_csv(dirName + "/class-count-bkseeing.csv")

# dfID = pd.read_csv("/content/drive/My Drive/Projects/BKSeeing/Tool/ID.csv")

# curID = 0

# dir = '/content/drive/My Drive/Projects/BKSeeing/data-ver-1.2/'

# list = os.listdir(dir) 
# print('List complete!')
# print(len(list))

parDir = '/content/drive/My Drive/Projects/BKSeeing/' + dataVersion + '/data'

c = 0
for i in range (1, 8):
  dir = "%s/jpg%d/"%(parDir, i)
  print(dir)
  list = os.listdir(dir)
  print("%d jpg files"%(len(list)))
  for fileFullName in list:
    if os.path.exists(dir+fileFullName) and fileFullName.endswith('.jpg') and os.path.getsize(dir+fileFullName) > 5000:
      fileName = os.path.splitext(fileFullName)[0]
      # print(fileName)
      L = 0
      R = numBox + 1
      while R - L > 1:
        M = (R + L) // 2
        if dfBox['ImageID'][M] > fileName:
          R = M
        else:
          L = M
      for i in range (0, numClass):
        dfTmp.loc[i,'Quantity'] = 0
      j = L
      while j >= 0 and dfBox['ImageID'][j] == dfBox['ImageID'][L]:
        for ii in range (0, numClass):
          if dfClass['LabelName'][ii] == dfBox['LabelName'][j]:
            dfTmp.loc[ii, 'Quantity'] += 1
            break
        j -= 1
      flag = 0
#       for i in range (0, numClass):
#         if dfCount.loc[i, 'Quantity'] + dfTmp.loc[i, 'Quantity'] > 2000:
#           flag = 1
#           break
      if flag == 0:
        c += 1
        for i in range (0, numClass):
          dfCount.loc[i, 'Quantity'] += dfTmp.loc[i, 'Quantity']
        # dfID.loc[curID, 'ImageName'] = fileName
#         curID += 1
#       curID += 1
#   if c == 10000:
#     break
# dfID.to_csv('/content/drive/My Drive/Projects/BKSeeing/Tool/ID.csv')
for i in range (1, 8):
  dir = "%s/xml%d/"%(parDir, i)
  print(dir)
  list = os.listdir(dir)
  print("%d xml files"%(len(list)))

print(dfCount)