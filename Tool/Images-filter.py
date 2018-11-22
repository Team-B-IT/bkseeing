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

# socket.setdefaulttimeout(60)
global curIdData
global countImg 
global countAbort

curIdData = countImg = countAbort = 0

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
  ObjectName = 'Others'
  while (dfBox['ImageID'][i] == dfBox['ImageID'][j]) and (j >= 0):
    for ii in range(0, numClass):
        if dfBox['LabelName'][j] == dfClass['LabelName'][ii]:
          ObjectName = dfClass['Name'][ii]
          break
    
    XMin = math.floor(dfBox['XMin'][j] * width)
    XMax = math.ceil(dfBox['XMax'][j] * width)
    YMin = math.floor(dfBox['YMin'][j] * height)
    YMax = math.ceil(dfBox['YMax'][j] * height)
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


def DownloadFile(imageID, imageURL, i):
  global countImg 
  global countAbort
  imageName = imageID+'.jpg'
  imageInfo = imageID+'.xml'
  global startTime
  startTime = time.time()
  r = requests.get(imageURL)
  f = open('/content/drive/My Drive/BKSeeing/data/'+imageName, 'wb')
  for chunk in r.iter_content(chunk_size=512 * 1024):
    if (chunk):
      f.write(chunk)
  f.close()
  countImg += 1
  print(countImg, 'complete')
  imageFolder = '/content/drive/My Drive/BKSeeing/data/'
  imageInfoFolder = '/content/drive/My Drive/BKSeeing/data/'
  writeFile(imageName, imageFolder, imageInfo, imageInfoFolder, i)
  return
  

dfImg = pd.read_csv(
    "/content/drive/My Drive/BKSeeing/Tool/train-images-boxable-with-rotation.csv")
dfImg.fillna(-99999, inplace=True)
dfImg = dfImg.sort_values(by=['ImageID']).reset_index(drop=True)
dfImg = dfImg.reset_index(drop=True)
numImg = len(dfImg)
print('Image URL imported!')

dfClass = pd.read_csv("/content/drive/My Drive/BKSeeing/Tool/class-des-bkseeing.csv")
numClass = len(dfClass)
print('Classes imported!')

dfBox = pd.read_csv(
    "/content/drive/My Drive/BKSeeing/Tool/train-annotations-bbox.csv",
    nrows=20000000)
numBox = len(dfBox)
print('Boxes imported!')
print(numImg, numClass, numBox)

for i in range(0, numBox - 1):
    if dfBox['ImageID'][i] != dfBox['ImageID'][i + 1]:
        flag = 0
        for j in range(0, numClass):
            if dfBox['LabelName'][i] == dfClass['LabelName'][j]:
                flag += 1
                break
        if flag == 1:
            imageID = dfBox["ImageID"][i]
            L = 0
            R = numImg + 1
            while R - L > 1:
                M = (R + L) // 2
                if dfImg['ImageID'][M] > dfBox['ImageID'][i]:
                    R = M
                else:
                    L = M
#             print(dfImg['ImageID'][L], dfBox['ImageID'][i])
            imageURL = dfImg['Thumbnail300KURL'][L]
            # print(imageURL)
            if imageURL != -99999:
              # print(imageURL,'\n')
              my_thread = Thread(target = DownloadFile, args = (imageID, imageURL, i))
              my_thread.start()
                
    if i % 1000 == 0:
        sleep(2)

print("Total:", countImg, "images")
print('Abort:', countAbort, 'images')

