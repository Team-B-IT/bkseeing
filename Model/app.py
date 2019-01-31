import pyrealsense2 as rs
import numpy as np
import cv2
from PIL import Image
import os
from time import sleep
import subprocess
import threading

# label = {
#   'Man': 'người',
#   'Woman': 'người',
#   'Chair': 'cái ghế',
#   'Table': 'cái bàn',
#   'Desk': 'cái bàn',
#   'Door': 'cái cửa',
#   'Stairs': 'cầu thang',
#   'Others': 'vật thể'
# }

label = {
  'Man': 'người',
  'Woman': 'người',
  'Chair': 'cái ghế',
  'Table': 'cái bàn',
  'Box': 'cái thùng',
  'Door': 'cái cửa',
  'Stairs': 'cầu thang',
  'Others': 'vật thể'
}

readBuffer = []

cmd = "python yolo_video.py --image"
p = subprocess.Popen(cmd,
    shell=True,
    bufsize=64,
    stdin=subprocess.PIPE,
    stderr=subprocess.PIPE,
    stdout=subprocess.PIPE)

def readThread():
    print("readThread start!")
    while True:
        line = p.stdout.readline().decode("utf-8").rstrip()
        if (line != ''):
            print(line)
            readBuffer.append(line)
        else:
            pass

rT = threading.Thread(target = readThread)
rT.start()

def predict():
    image = 'color.jpeg'

    p.stdin.write(bytes(image + "\n", "utf-8"))
    p.stdin.flush()
    # print(image)

    global readBuffer
    result = tuple(readBuffer)
    readBuffer = []
    counter = {}
    for i in result:
        for k, v in label.items():
            if i.find(k) >= 0:
                if v in counter:
                    counter[v] += 1
                else:
                    counter[v] = 1
    if len(counter) == 0:
        result = "Không có đồ vật nào"
    else:
        result = ''
        for k, v in counter.items():
            result += "có " + str(v) + " " + k + ", "

    print(result)


#CONFIG YOUR PATH
path = ""

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

try:
    while True:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue
        
        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        # print(depth_image)
        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.05), cv2.COLORMAP_BONE)
        
        # Stack both images horizontally
        images = np.hstack((color_image, depth_colormap))

        
        cv2.imwrite( path+'color.jpeg', color_image )
        cv2.imwrite( path+'depth.jpeg', depth_image )
        # cv2.imwrite('01.png',img)
        # Show images
        # cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        # cv2.imshow('RealSense', images)
        # cv2.waitKey(10)
        predict()
        sleep(5)

finally:

    # Stop streaming
    pipeline.stop()