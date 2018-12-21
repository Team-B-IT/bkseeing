from flask import Flask, request
import os
import socket
import math
import time
import subprocess, threading

cmd = "python yolo_video.py --image"
p = subprocess.Popen(cmd,
	shell=True,
	bufsize=64,
	stdin=subprocess.PIPE,
	stderr=subprocess.PIPE,
	stdout=subprocess.PIPE)

while True:
	print(1)
	line = p.stdout.readline().decode("utf-8").rstrip()
	print(2)
	if line != "":
		print(p.stdout.readline().decode("utf-8").rstrip())
	else:
		break

app = Flask(__name__)

@app.route("/",methods = ['POST', 'GET'])
def hello():
	if request.method == 'POST':
		random = int(round(time.time() * 1000)) % 1000;
		image = "img" + str(random) + ".png"
		f = open(image, "wb")
		f.write(request.data)
		f.close()

		p.stdin.write(bytes(image, "utf-8"))
		p.stdin.flush()
		result = p.stdout.readline().decode("utf-8").rstrip()

		return result.encode("utf-8")
	else:
		return "Yêu cầu không hợp lệ".encode("utf-8")
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80)