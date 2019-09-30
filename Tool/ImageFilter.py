#@title Sort images { form-width: "20%" }
import time
import urllib
from time import sleep
import pandas as pd 
import gc
import socket
from PIL import Image
import math
import os

#define data version
dataVersion = 'data-1.0'
dirName = '/content/drive/My Drive/Projects/BKSeeing/' + dataVersion
curIdData = countImg = countAbort = 0

#number of rows
numRow = 3000000

#get selected classes
dfClass = pd.read_csv(dirName + "/class-des-bkseeing.csv")
numClass = len(dfClass)
print('Classes imported!')

dfBox = pd.read_csv(
    "/content/drive/My Drive/Projects/BKSeeing/Tool/train-annotations-bbox.csv",
    nrows=numRow)
numBox = len(dfBox)

dfBox = dfBox[['ImageID', 'LabelName']]
# print(dfBox)
print('Boxes imported!')
print(numClass, 'Classes')
print(numBox, 'Boxes')

#get dummy selected classes
dfCount = pd.read_csv(dirName + "/class-count-bkseeing.csv")
dfTmp = pd.read_csv(dirName + "/class-count-bkseeing.csv")

dfSort = pd.DataFrame()

curID = 0

folderNum = 1

#get the priority
print('Getting Priority!')
curPos = 0
cntTmp = 0
BoxName = dfBox['ImageID'][0]
for i in range(0, numBox-1):
  if i % 100000 == 0:
    print(i*100/numRow, '%')   
  label = dfBox['LabelName'][i]
  for ii in range (0, numClass):
    if dfClass['LabelName'][ii] == label:
      cntTmp += 1
      break
  if BoxName != dfBox['ImageID'][i + 1]:
    dfSort.loc[curPos, 'ImageID'] = BoxName
    dfSort.loc[curPos, 'Sum'] = cntTmp
    cntTmp = 0
    curPos += 1
    BoxName = dfBox['ImageID'][i+1]
dfSort = dfSort.sort_values(by=['Sum'], ascending = False).reset_index(drop=True)
dfSort = dfSort.reset_index(drop=True)
numSort = len(dfSort)
print(dfSort)
dfSort.to_csv(dirName + "/ImgPriority.csv")
print('Images sorted!')
