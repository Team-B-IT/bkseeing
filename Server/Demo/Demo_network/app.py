from flask import Flask, request
import os
import socket
import math

app = Flask(__name__)

@app.route("/",methods = ['POST', 'GET'])
def hello():
	if request.method == 'POST':
		request.data = request.data.decode("utf-8")
		par = list(float(x) for x in request.data.split(" "))
		print(par)
		if par[0] == 0:
			if par[1] == 0:
				if par[2] == 0:
					print("Phuong trinh co vo so nghiem")
					return "Phuong trinh co vo so nghiem"
				else:
					print("Phuong trinh vo nghiem")
					return "Phuong trinh vo nghiem"
			else:
				print("x = " + str(par[2] / par[1]))
				return "x = " + str(par[2] / par[1])
		delta = par[1] * par[1] - 4 * par[0] * par[2]
		if delta < 0:
			print("Phuong trinh vo nghiem")
			return "Phuong trinh vo nghiem"
		elif delta == 0:
			x = -par[1] / (2 * par[0])
			print("x1 = x2 = " + str(x))
			return "x1 = x2 = " + str(x)
		else:
			x1 = -(par[1] - math.sqrt(delta)) / (2 * par[0])
			x2 = -(par[1] + math.sqrt(delta)) / (2 * par[0])
			print("x1 = " + str(x1) + "; x2 = " + str(x2))
			return "x1 = " + str(x1) + "; x2 = " + str(x2)
	else:
		with open('home.html', 'r') as myfile:
			html=myfile.read()
			return html
if __name__ == "__main__":
	app.debug = True
	app.run(host="0.0.0.0", port=9999)

