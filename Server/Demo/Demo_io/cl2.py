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
	result = []
	while True:
		r = p.stdout.readline()
		if r is None:
			break
		print(int(r.decode("utf-8").rstrip()))
		result.append(int(r))
	p.stdout.flush()
	for r in result:
		print(r*r)