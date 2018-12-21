import subprocess
import threading
import time

cmd = "python cd.py"
p = subprocess.Popen(cmd,
	shell=True,
	bufsize=64,
	stdin=subprocess.PIPE,
	stderr=subprocess.PIPE,
	stdout=subprocess.PIPE)

readBuffer = []

def readThread():
	print("readThread start!")
	while True:
		line = p.stdout.readline().decode("utf-8").rstrip()
		if (line != ''):
			print(line)
			readBuffer.append(line)
		else:
			time.sleep(1000)

rT = threading.Thread(target = readThread)
rT.start()

while True:
	try:
		p.stdin.write(bytes(str(5) + '\n', 'utf-8'))
		p.stdin.flush()
		time.sleep(1)
		print(readBuffer)
		readBuffer = []
	except:
		pass