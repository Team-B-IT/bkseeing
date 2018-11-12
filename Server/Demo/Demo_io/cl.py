import subprocess, os, threading, time

cmd = "python cd.py 1"
p = True
p = subprocess.Popen(cmd,
                     shell=True,
                     bufsize=64,
                     stdin=subprocess.PIPE,
                     stderr=subprocess.PIPE,
                     stdout=subprocess.PIPE)
while True:
	i = input()
	b = bytes(str(i) + '\n', "utf-8")
	p.stdin.write(b)
	p.stdin.flush()
	result = int(p.stdout.readline().decode("utf-8").rstrip())
	p.stdout.flush()
	print(result*result)