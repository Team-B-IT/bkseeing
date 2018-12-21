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
		return "Ơ, Minh béo kìa".encode("utf-8")
	else:
		return "Mày GET cái gì cơ?".encode("utf-8")
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80)