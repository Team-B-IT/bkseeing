from flask import Flask, request
import os
import socket
import math

app = Flask(__name__)

@app.route("/",methods = ['POST', 'GET'])
def hello():
	print("hello1")
	if request.method == 'POST':
		# print("hello2")
		print(request.data.decode("utf-8"))
		# print("hello3")
		return "Ok em!"
	else:
		# print("hello4")
		return "D m Cuong ngu"
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80)