from flask import Flask, request
import os
import socket
import math

app = Flask(__name__)

@app.route("/",methods = ['POST', 'GET'])
def hello():
	# print("Request Content", request.data.decode("utf-8"))
	f = open("img.png", "wb")
	f.write(request.data)
	f.close()
	if request.method == 'POST':
		return "Phía trước có một cái cửa".encode("utf-8")
	else:
		return "Mày GET cái gì cơ?".encode("utf-8")
if __name__ == "__main__":
	app.run(host='192.168.69.8', port=80)