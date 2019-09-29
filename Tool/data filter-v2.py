#@title Get images { form-width: "20%" }
import time
import urllib
from time import sleep
import pandas as pd 
import requests
import gc
import socket
from threading import Thread
from PIL import Image
import math
from bs4 import BeautifulSoup
import os

#define data version
dataVersion = 'data-1.0'
dirName = '/content/drive/My Drive/Projects/BKSeeing/' + dataVersion + '/data/'

# socket.setdefaulttimeout(60)
global curIdData
global countImg 
global countAbort
curIdData = countImg = countAbort = 0
countFolder = 1

def printProgressBar(iteration,
                     total,
                     prefix='',
                     suffix='',
                     decimals=1,
                     length=100,
                     fill='█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(
        100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()

class TooSlowException(Exception):
    pass

class CompleteDownload(Exception):
    pass

class AbortImage(Exception):
    pass

def getRow(width, height, i):
  output = ""
  j = i
  while (dfBox['ImageID'][i] == dfBox['ImageID'][j]) and (j > 0):
    ObjectName = 'Others'
    for ii in range(0, numClass):
        if dfBox['LabelName'][j] == dfClass['LabelName'][ii]:
          ObjectName = dfClass['Name'][ii]
          break
    if ObjectName == 'Woman':
      ObjectName = 'Man'
    if ObjectName == 'Desk':
      ObjectName = 'Table'
    XMin = max(0, math.floor(dfBox['XMin'][j] * width))
    XMax = min(width, math.ceil(dfBox['XMax'][j] * width))
    YMin = max(0, math.floor(dfBox['YMin'][j] * height))
    YMax = min(height, math.ceil(dfBox['YMax'][j] * height))
    IsTruncated = dfBox['IsTruncated'][j]
    output = output + (
    """<object>
        <name>%s</name>
        <pose>%s</pose>
        <truncated>%s</truncated>
        <difficult>%d</difficult>
        <bndbox>
            <xmin>%d</xmin>
            <ymin>%d</ymin>
            <xmax>%d</xmax>
            <ymax>%d</ymax>
        </bndbox>
    </object>
    """ % (
      ObjectName, 'Unspecified', IsTruncated, 0, XMin, YMin, XMax, YMax))
    # print(output)
    j -= 1
  return output+'\n'

def writeFile(imageName, imageFolder, imageInfo, imageInfoFolder, i):
  imagePath = imageFolder+imageName
  imageInfoPath = imageInfoFolder+imageInfo
  img = Image.open(imagePath)
  width, height = img.size
  # print(width, height)
  fi = open(imageInfoPath, 'w')
  fi.write(
  """<annotation>
    <folder>%s</folder>
    <filename>%s</filename>
    <path>%s</path>
    <source>
        <database>Unknown</database>
    </source>
    <size>
      <width>%d</width>
      <height>%d</height>
      <depth>3</depth>
    </size>
    <segmented>0</segmented>
    %s</annotation>"""
  %('data', imageName, imagePath, width, height, getRow(width, height, i)))
  fi.close()

def convertBToMb(bytes):
    """converts Bytes to Megabytes"""
    bytes = float(bytes)
    megabytes = bytes / 1048576
    return megabytes

def dlProgress(count, blockSize, totalSize):
    alreadyLoaded = count * blockSize
    timePassed = time.time() - startTime
    transferRate = convertBToMb(
        alreadyLoaded) / timePassed  # mbytes per second
    # transferRate *= 60 # mbytes per minute

    percent = int(alreadyLoaded * 100 / totalSize)
    # print('R:', transferRate)
    # print('T:', timePassed)
    # print('P:', percent)
    if percent >= 100:
        raise CompleteDownload

def DownloadFile(imageID, imageURL, i, dirname):
  global countImg 
  global countAbort
  folderNum = (int)((countImg + 2000) / 2000)
  if(countImg%2000 == 0):
    print(folderNum)
  imageFolder = dirname + '/data/'
  imageInfoFolder = dirname + '/data/'
  imageFolder = "%sjpg%d/"%(imageFolder, folderNum)
  imageInfoFolder = "%sxml%d/"%(imageInfoFolder, folderNum)
  imageName = imageID+'.jpg'
  imageInfo = imageID+'.xml'
  global startTime
  startTime = time.time()
  r = requests.get(imageURL)
  f = open(imageFolder + imageName, 'wb')
  for chunk in r.iter_content(chunk_size = 512 * 1024):
    if (chunk):
      f.write(chunk)
  f.close()
  if os.path.exists(imageFolder+imageName) and os.path.getsize(imageFolder+imageName) < 5000:
    os.remove(imageFolder+imageName)
    countAbort += 1
    return 0
  countImg += 1
  print(countImg, 'complete')
  writeFile(imageName, imageFolder, imageInfo, imageInfoFolder, i)
  return 1
  

dfImg = pd.read_csv(
    "/content/drive/My Drive/Projects/BKSeeing/Tool/train-images-boxable-with-rotation.csv")
dfImg.fillna(-99999, inplace=True)
dfImg = dfImg.sort_values(by=['ImageID']).reset_index(drop=True)
dfImg = dfImg.reset_index(drop=True)
numImg = len(dfImg)
print('Image URL imported!')

#get selected classes
dfClass = pd.read_csv("/content/drive/My Drive/Projects/BKSeeing/" + dataVersion + "/class-des-bkseeing.csv")
numClass = len(dfClass)
print('Classes imported!')

dfBox = pd.read_csv(
    "/content/drive/My Drive/Projects/BKSeeing/Tool/train-annotations-bbox.csv",
    nrows=2000000)
numBox = len(dfBox)
print('Boxes imported!')
print(numImg, numClass, numBox)

#get dummy selected classes
dfCount = pd.read_csv("/content/drive/My Drive/Projects/BKSeeing/" + dataVersion + "/class-count-bkseeing.csv")
dfTmp = pd.read_csv("/content/drive/My Drive/Projects/BKSeeing/" + dataVersion + "/class-count-bkseeing.csv")
dfID = pd.read_csv("/content/drive/My Drive/Projects/BKSeeing/Tool/ID-origin.csv")
dfSort =  pd.read_csv("/content/drive/My Drive/Projects/BKSeeing/Tool/Priority10mil.csv")

curID = 0

printProgressBar(
    0, numBox, prefix='Progress:', suffix='Complete', decimals=3, length=50)

folderNum = 1

#get the priority
# print('Getting Priority!')
# curPos = 0
# cntTmp = 0
# for i in range(0, numBox-1):
#   if i % 1000 == 0:
#     printProgressBar(
#       i, numBox, prefix='Progress:', suffix='Complete', decimals=3, length=50)
#   for ii in range (0, numClass):
#     if dfClass['LabelName'][ii] == dfBox['LabelName'][i]:
#       cntTmp += 1
#       break
#   if dfBox['ImageID'][i] != dfBox['ImageID'][i + 1]:
#     dfSort.loc[curPos, 'ImageID'] = dfBox.loc[i, 'ImageID']
#     dfSort.loc[curPos, 'Sum'] = cntTmp
#     cntTmp = 0
#     curPos += 1
# dfSort = dfSort.sort_values(by=['Sum'], ascending = False).reset_index(drop=True)
# dfSort = dfSort.reset_index(drop=True)
# numSort = len(dfSort)
# print(dfSort)
# dfID.to_csv("/content/drive/My Drive/Projects/BKSeeing/Tool/Priority10mil.csv")
# print('Images sorted!')

print('Downloading Images!')
#get images
for i in range(0, numSort-1):
  if dfSort.loc[i, 'Sum'] == 0:
    break
  #get position of image in boxes file
  fileName = dfSort.loc[i, 'ImageID']
  imageID = fileName
  L = 0
  R = numBox + 1
  while R - L > 1:
    M = (R + L) // 2
    if dfBox['ImageID'][M] > fileName:
      R = M
    else:
      L = M
  for ii in range (0, numClass):
    dfTmp.loc[ii,'Quantity'] = 0
  #count number of each classes
  posImg = L
  j = L
  while j >= 0 and dfBox['ImageID'][j] == dfBox['ImageID'][posImg]:
    for ii in range (0, numClass):
      if dfClass['LabelName'][ii] == dfBox['LabelName'][j]:
        dfTmp.loc[ii, 'Quantity'] += 1
        break
    j -= 1
  #check number of boxes
  flag = 0
  for ii in range (0, numClass):
    if dfTmp.loc[ii, 'Quantity'] > 0:
      if dfCount.loc[ii, 'Quantity'] + dfTmp.loc[ii, 'Quantity'] < 4000:
        flag = 1
        break
  #image satisfied
  if flag == 1:
    #get image URL
    L = 0
    R = numImg + 1
    while R - L > 1:
      M = (R + L) // 2
      if dfImg['ImageID'][M] > dfBox['ImageID'][posImg]:
        R = M
      else:
        L = M
    imageURL = dfImg['Thumbnail300KURL'][L]
    if imageURL != -99999:
      my_thread = Thread(target = DownloadFile, args = (imageID, imageURL, posImg, dirName))
      my_thread.start()
      for ii in range (0, numClass):
        dfCount.loc[ii, 'Quantity'] += dfTmp.loc[ii, 'Quantity']
    #create new folder
    if countFolder * 2000 - countImg < 1000:
      countFolder += 1
      dir = "%s/jpg%d"%(dirName, countFolder)
      if not os.path.exists(dir):
          os.mkdir(dir)
          print("Directory " , dir ,  " Created ")
      else:    
          print("Directory " , dir,  " already exists")
      dir = "%s/xml%d"%(dirName, countFolder)
      if not os.path.exists(dir):
          os.mkdir(dir)
          print("Directory " , dir ,  " Created ")
      else:    
          print("Directory " , dir ,  " already exists")


printProgressBar(
    numBox,
    numBox,
    prefix='Progress:',
    suffix='Complete',
    decimals=3,
    length=50)
print("Total:", countImg, "images")
print('Abort:', countAbort, 'images')
print(dfCount)
